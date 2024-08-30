from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from .database_config import settings

DATABASE_URL = settings.DATABASE_URL

# Create an AsyncEngine
engine = create_async_engine(DATABASE_URL, future=True, echo=True)

# Use async_sessionmaker for creating async sessions
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

Base = declarative_base()


# Dependency to get the async session
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
