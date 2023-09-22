from abc import abstractclassmethod

from sqlalchemy.ext.asyncio import AsyncSession

from api.ddd.entity.task import Task


class ITaskRepository:

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    @abstractclassmethod
    async def create(self, task: Task) -> Task:
        pass

    @abstractclassmethod
    async def get_tasks_with_done(self) -> list[Task]:
        pass

    @abstractclassmethod
    async def get_task(self, id: int) -> Task:
        pass

    @abstractclassmethod
    async def save(self, task: Task) -> Task:
        pass