from abc import abstractclassmethod

from sqlalchemy.ext.asyncio import AsyncSession

from api.ddd.entity.task import Task
from api.ddd.value_object import TaskId, TaskTitle


class ITaskRepository:

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    @abstractclassmethod
    async def create(self, task: Task) -> Task:
        return task

    @abstractclassmethod
    async def get_tasks_with_done(self) -> list[Task]:
        return [Task(TaskTitle("title1"), TaskId(1), False), Task(TaskTitle("title2"), TaskId(2), False)]

    @abstractclassmethod
    async def get_task(self, id: int) -> Task:
        return Task(TaskTitle("title1"), TaskId(1), False)

    @abstractclassmethod
    async def save(self, task: Task) -> Task:
        return task
