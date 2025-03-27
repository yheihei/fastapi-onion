from typing import List, Tuple

import pytest
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.testclient import TestClient


class TestCreateActivity:

    @pytest.mark.asyncio
    async def test_create(self, db: AsyncSession, async_client):
        response = await async_client.post(
            "/users/1/activities"
        )
        print(response.json())
