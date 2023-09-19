from typing import List, Tuple

import pytest
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from api.ddd.repository import TaskRepository

import api.models.task as task_model


class TestTaskRepository:

    @pytest.mark.asyncio
    async def test_get_task(self, db, async_client):
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
