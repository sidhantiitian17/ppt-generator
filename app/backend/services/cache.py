from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Callable, Dict, Optional, TypedDict, cast


class CacheEntry(TypedDict):
    path: str
    size: int
    last_access: float


class DiskLRUCache:
    """Simple disk-backed cache with size and TTL guards."""

    def __init__(self, root: Path, max_bytes: int, ttl_seconds: int) -> None:
        self.root = root
        self.max_bytes = max_bytes
        self.ttl_seconds = ttl_seconds
        self.root.mkdir(parents=True, exist_ok=True)
        self._index_path = self.root / "index.json"
        self._entries: Dict[str, CacheEntry] = self._load_index()

    def get(self, key: str) -> Optional[Path]:
        entry = self._entries.get(key)
        if not entry:
            return None
        path = Path(entry["path"])
        if not path.exists():
            self._entries.pop(key, None)
            self._persist()
            return None
        if self.ttl_seconds and (time.time() - entry["last_access"]) > self.ttl_seconds:
            self._remove_entry(key, path)
            return None
        entry["last_access"] = time.time()
        self._persist()
        return path

    def store(self, key: str, writer: Callable[[Path], None]) -> Path:
        path = self.root / key
        writer(path)
        size = path.stat().st_size if path.exists() else 0
        self._entries[key] = {
            "path": str(path),
            "size": size,
            "last_access": time.time(),
        }
        self._persist()
        self._enforce_limits()
        return path

    def _enforce_limits(self) -> None:
        total = sum(entry["size"] for entry in self._entries.values())
        if total <= self.max_bytes:
            return
        for key, entry in sorted(
            self._entries.items(), key=lambda item: item[1]["last_access"]
        ):
            path = Path(entry["path"])
            self._remove_entry(key, path)
            total -= entry["size"]
            if total <= self.max_bytes:
                break

    def _remove_entry(self, key: str, path: Path) -> None:
        if path.exists():
            path.unlink()
        self._entries.pop(key, None)
        self._persist()

    def _load_index(self) -> Dict[str, CacheEntry]:
        if not self._index_path.exists():
            return {}
        try:
            raw = json.loads(self._index_path.read_text())
        except json.JSONDecodeError:
            return {}
        return cast(Dict[str, CacheEntry], raw)

    def _persist(self) -> None:
        self._index_path.write_text(json.dumps(self._entries))
