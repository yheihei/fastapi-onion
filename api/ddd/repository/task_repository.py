from sqlalchemy import select
from sqlalchemy.engine import Result

import api.models.task as task_model
from api.ddd.entity import Task
from api.ddd.repository.i_task_repository import ITaskRepository
from api.ddd.value_object import TaskId, TaskTitle


class TaskRepository(ITaskRepository):

    async def create(self, task_entity: Task) -> Task:
        task_data_model = self.__transfer(task_entity)
        self.db.add(task_data_model)
        await self.db.commit()
        await self.db.refresh(task_data_model)
        return self.__to_model(task_data_model, False)
    
    async def get_tasks_with_done(self) -> list[Task]:
        result: Result = await (
            self.db.execute(
                select(
                    task_model.Task,
                    task_model.Done.id.isnot(None).label("done"),
                ).outerjoin(task_model.Done)
            )
        )
        tasks: list[Task] = []
        task_data_model: task_model.Task
        done: bool
        for task_data_model, done in result.all():
            tasks.append(self.__to_model(task_data_model, done))
        return tasks
    
    def __transfer(self, task_entity: Task) -> task_model.Task:
        return task_model.Task(id=task_entity.id.value(), title=task_entity.title.value())
    
    def __to_model(self, task_data_model: task_model.Task, done: bool) -> Task:
        task_id = TaskId(task_data_model.id)
        task_title = TaskTitle(task_data_model.title)
        return Task(id=task_id, title=task_title, done=done)
