from typing import List, Tuple

import pytest
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from api.ddd.value_object.task_title import TaskTitle
from api.ddd.value_object.exception import ValueObjectError


class TestTaskTitle:

    @pytest.mark.asyncio
    async def test_create_title(self, db: AsyncSession, async_client):
        task_title = TaskTitle(name = "タスクのタイトル")
        assert "タスクのタイトル" == task_title.get_name()

    @pytest.mark.asyncio
    async def test_title_long_error(self, db: AsyncSession, async_client):
        with pytest.raises(ValueObjectError):
            task_title = TaskTitle(name = "a" * 256)
