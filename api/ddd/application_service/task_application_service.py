from api.ddd.domain_service.task_service import TaskService
from api.ddd.entity.task import Task
from api.ddd.repository.i_task_repository import ITaskRepository
from api.ddd.value_object.task_title import TaskTitle


class TaskApplicationService:

    def __init__(self, repository: ITaskRepository, service: TaskService) -> None:
        self.repository: ITaskRepository = repository
        self.service: TaskService = service

    async def register(self, title: str) -> Task:
        task = Task(title=TaskTitle(title))
        return await self.repository.create(task)