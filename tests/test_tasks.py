from typing import List, Tuple

import pytest
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

import api.models.task as task_model


class TestTask:
    """
    tasks関連のエンドポイントのテスト
    """

    @pytest.mark.asyncio
    async def test_create_task(self, db: AsyncSession, async_client):
        response = await async_client.post(
            "/tasks", json={"title": "foo",}
        )
        result: Result = await db.execute(
            select(
                task_model.Task.id,
                task_model.Task.title,
                task_model.Done.id.isnot(None).label("done"),
            ).outerjoin(task_model.Done).filter(task_model.Task.title == "foo")
        )
        tasks: List[Tuple] = result.all()
        assert 1 == len(tasks)
        assert (1, "foo", False) == tasks[0]

    @pytest.mark.asyncio
    async def test_get_task(self, db, async_client):
        # タスク生成
        for i in range(0, 2):
            task = task_model.Task(title=f"{i+1}")
            db.add(task)
            await db.commit()
            await db.refresh(task)

        response = await async_client.get(
            "/tasks",
        )
        assert [
            {"title": "1", "id": 1, "done": False},
            {"title": "2", "id": 2, "done": False}
        ] == response.json()
