from typing import AsyncGenerator, List, Tuple

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import api.models.task as task_model
from api.db import Base, get_db
from api.main import app

ASYNC_DB_URL = "sqlite+aiosqlite:///:memory:"

@pytest_asyncio.fixture
async def db():
    # Async用のengineとsessionを作成
    async_engine = create_async_engine(ASYNC_DB_URL, echo=False)
    async_session = sessionmaker(
        autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
    )

    # テスト用にオンメモリのSQLiteテーブルを初期化（関数ごとにリセット）
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # DIを使ってFastAPIのDBの向き先をテスト用DBに変更
    async def get_test_db():
        async with async_session() as session:
            yield session

    app.dependency_overrides[get_db] = get_test_db
    async with async_session() as session:
        yield session

@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="https://test") as c:
        yield c

@pytest.mark.asyncio
async def test_create_task(db: AsyncSession, async_client):
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
async def test_get_task(db, async_client):
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
