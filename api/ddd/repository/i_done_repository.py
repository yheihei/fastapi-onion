from abc import abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession


class IDoneRepository:

    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    @abstractmethod
    async def mark_as_done(self, task_id: int) -> None:
        pass
