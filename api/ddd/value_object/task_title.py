from api.ddd.value_object.exception import ValueObjectError


class TaskTitle:
    def __init__(self, name: str) -> None:
        # 255文字以上はエラー
        if len(name) > 255:
            raise ValueObjectError("タスク名は255文字以下にしてください")
        self.name: str = name

    def get_name(self) -> str:
        return self.name
