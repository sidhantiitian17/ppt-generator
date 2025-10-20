from __future__ import annotations

from pathlib import Path
from typing import Tuple


class AssetStore:
    """Persist uploaded font and image assets on disk."""

    def __init__(self, base_dir: Path, max_bytes: int) -> None:
        self.base_dir = base_dir
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.max_bytes = max_bytes

    def save(self, filename: str, data: bytes) -> Path:
        if len(data) > self.max_bytes:
            raise ValueError("asset exceeds maximum configured size")
        destination = self.base_dir / filename
        destination.write_bytes(data)
        return destination

    def delete(self, filename: str) -> None:
        target = self.base_dir / filename
        if target.exists():
            target.unlink()

    def stat(self, filename: str) -> Tuple[int, float]:
        target = self.base_dir / filename
        stat = target.stat()
        return stat.st_size, stat.st_mtime
