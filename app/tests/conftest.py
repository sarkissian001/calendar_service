from typing import AsyncIterable

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)

from app.models.event_models import Base
from app.database.connection import get_db

from app.main import app


@pytest.fixture(scope="session", autouse=True)
async def engine() -> AsyncIterable[AsyncEngine]:
    from sqlalchemy.pool import StaticPool

    _engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    async with _engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield _engine
    await _engine.dispose()


@pytest.fixture(scope="function")
async def session(engine: AsyncEngine) -> AsyncIterable[AsyncSession]:
    """Create a new database session with a rollback at the end of the test.

    Inspired by https://dev.to/jbrocher/fastapi-testing-a-database-5ao5
    """
    connection: AsyncConnection = await engine.connect()
    transaction = await connection.begin()
    session = AsyncSession(bind=connection)
    yield session
    await transaction.rollback()
    await connection.close()


@pytest.fixture(scope="function")
async def client(session: AsyncSession) -> AsyncIterable[AsyncClient]:
    """Create a test client that uses the override_get_db fixture to return
    a session.
    """
    app.dependency_overrides[get_db] = lambda: session
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
