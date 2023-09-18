from typing import Type

from api.ddd.entity.i_equatable import IEquatable
from api.ddd.value_object.task_id import TaskId
from api.ddd.value_object.task_title import TaskTitle


class Task(IEquatable[Type["Task"]]):

    def __init__(self, id: TaskId, title: TaskTitle) -> None:
        if type(id) is not TaskId:
            raise ValueError("idは必須です")
        if type(title) is not TaskTitle:
            raise ValueError("titleは必須です")
        self.__id: TaskId = id
        self.__title: TaskTitle = title

    @property
    def id(self):
        return self.__id

    def equals(self, other: Type["Task"]) -> bool:
        return self.id == other.id
