from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession,async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings import ENVIRONMENT

DB_ENGINE = ENVIRONMENT.DB_ENGINE

# create the engine to use in the database
ENGINE = create_async_engine(url=f'{DB_ENGINE}+asyncpg://{ENVIRONMENT.DB_URL}',echo=True)

# create the database session manager
AsyncSessionLocal = async_sessionmaker(
    ENGINE,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False
)

# create the base model for the models of database
BaseModel = declarative_base()

# dependency to get the database session
async def get_database_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()