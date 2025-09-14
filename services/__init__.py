from sqlalchemy.orm import Session
from fastapi import Depends
from repositories import get_user_repository,UserRepository
from .user import UserService

def get_user_service(repository:UserRepository = Depends(get_user_repository)):
    service = UserService(repository)
    try:
        yield service
    finally:
        service = None