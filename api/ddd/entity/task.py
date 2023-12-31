from typing import Optional, Type

from api.ddd.entity.i_equatable import IEquatable
from api.ddd.value_object.task_id import TaskId
from api.ddd.value_object.task_title import TaskTitle


class Task(IEquatable[Type["Task"]]):

    def __init__(self, title: TaskTitle, id: Optional[TaskId] = None) -> None:
        if type(title) is not TaskTitle:
            raise ValueError("titleは必須です")
        if id is None:
            id = TaskId(None)
        self.__id: TaskId = id
        self.__title: TaskTitle = title

    @property
    def id(self):
        return self.__id
    
    @property
    def title(self):
        return self.__title

    def equals(self, other: Type["Task"]) -> bool:
        return self.id.value() == other.id.value()
