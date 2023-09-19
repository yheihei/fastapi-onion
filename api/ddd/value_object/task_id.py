from typing import Optional


class TaskId:
    def __init__(self, id: Optional[int]) -> None:
        self.id: int = id

    def value(self) -> Optional[int]:
        return self.id
