from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker

ASYNC_DB_URL = "mysql+aiomysql://root@db:3306/demo?charset=utf8"

async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()


async def get_db():
    async with async_session() as session:
        yield session
