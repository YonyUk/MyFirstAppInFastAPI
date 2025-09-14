from typing import List
from repositories import UserRepository
from models import User
from schemas import UserAdminUpdate
from settings import ENVIRONMENT

class UserService:

    def __init__(self,user_repository:UserRepository):
        '''
        service manager for the users
        '''
        self._repository = user_repository
        self._crypt_context = ENVIRONMENT.CRYPT_CONTEXT

    def _get_password_hash(self,password:str) -> str:
        return self._crypt_context.hash(password)

    def _verify_password_hash(self,password:str,hashed_password:str) -> bool:
        return self._crypt_context.verify(password,hashed_password)
    
    async def authenticate_user(self,username:str,password:str) -> User | None:
        '''
        authenticates an user
        '''
        user = await self._repository.get_by_username(username)
        if not user:
            return None
        if not self._verify_password_hash(password,user.hashed_password):
            return None
        return user

    async def add_user(self,user:User) -> User | None:
        '''
        adds a new user
        '''
        return await self._repository.create(user)

    async def update_user(self,user_id:str,user_update:UserAdminUpdate) -> User | None:
        '''
        updates an user
        '''
        return await self._repository.update(user_id,user_update)
    
    async def delete_user(self,user_id:str) -> bool:
        '''
        deletes an user
        '''
        return await self._repository.delete(user_id)

    async def get_by_name(self,username:str) -> User | None:
        '''
        gets the user by his username
        '''
        return await self._repository.get_by_username(username)
    
    async def get_user_by_email(self,email:str) -> User | None:
        '''
        gets the user by his email
        '''
        return await self._repository.get_by_email(email)

    async def get_user_by_id(self,id:str) -> User | None:
        '''
        gets an user by his id
        '''
        return await self._repository.get_by_id(id)

    async def get_users(self,limit:int=100,skip:int=0) -> List[User]:
        '''
        gets the users

        params:
            limit: int -> limit of users in the result
            skip: int -> number of registes to skip
        '''
        return await self._repository.get_all(limit,skip)