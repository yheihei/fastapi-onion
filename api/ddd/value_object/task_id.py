class TaskId:
    def __init__(self, id: int) -> None:
        self.id: int = id

    def get_id(self) -> int:
        return self.id