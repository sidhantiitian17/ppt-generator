from __future__ import annotations

from collections import deque
from typing import Callable, Deque, Generator


class TaskQueue:
    _instance: "TaskQueue" | None = None

    def __init__(self) -> None:
        self._tasks: Deque[Callable[[], None]] = deque()

    @classmethod
    def default_instance(cls) -> "TaskQueue":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def enqueue(self, task: Callable[[], None]) -> None:
        self._tasks.append(task)

    def run_once(self) -> None:
        if self._tasks:
            task = self._tasks.popleft()
            task()

    def stream_progress(self) -> Generator[str, None, None]:
        yield "queued"
        yield "completed"
