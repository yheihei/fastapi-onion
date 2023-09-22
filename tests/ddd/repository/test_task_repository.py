
import pytest

import api.models.task as task_model
from api.ddd.entity import Task
from api.ddd.repository import TaskRepository


class TestTaskRepository:

    @pytest.mark.asyncio
    async def test_get_tasks_with_done(self, db, async_client):
        # タスク生成
        expected_tasks: list[task_model.Task] = []
        for i in range(0, 2):
            task = task_model.Task(title=f"{i+1}")
            db.add(task)
            await db.commit()
            await db.refresh(task)
            expected_tasks.append(task)

        tasks = await TaskRepository(db).get_tasks_with_done()
        for index, task in enumerate(tasks):
            assert expected_tasks[index].id == task.id.value()
            assert False == task.done

    @pytest.mark.asyncio
    async def test_get_task(self, db, async_client):
        # タスク生成
        created_task = task_model.Task(title=f"1")
        db.add(created_task)
        await db.commit()
        await db.refresh(created_task)

        task: Task = await TaskRepository(db).get_task(created_task.id)
        assert 1 == task.id.value()
        assert "1" == task.title.value()
        assert False == task.done
