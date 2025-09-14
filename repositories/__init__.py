from .user import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from database import get_database_session

def get_user_repository(db:AsyncSession = Depends(get_database_session)):
    repository = UserRepository(db)
    try:
        yield repository
    finally:
        repository = None