from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,update
from models import User
from schemas import UserCreateAdmin,UserCreate
from settings import ENVIRONMENT

class UserRepository:
    
    def __init__(self,db:AsyncSession):
        '''
        database repository for 'User' entity
        '''
        self._db = db
        self._crypt_context = ENVIRONMENT.CRYPT_CONTEXT
    
    def _get_password_hash(self,password:str) -> str:
        return self._crypt_context.hash(password)

    def _user_to_dict(self,user:User) -> dict:
        return {
            'id':user.id,
            'username':user.username,
            'email':user.email,
            'hashed_password':user.hashed_password,
            'admin':user.admin
        }

    async def create(self,user:User) -> User | None:
        '''
        adds a new user to database
        '''
        self._db.add(user)
        await self._db.commit()
        await self._db.refresh(user)
        return user
    
    async def update(self,user_id:str,user_update:User) -> User | None:
        '''
        updates the data of the given user
        '''
        user = await self.get_by_id(user_id)
        if user is None:
            return None

        update_data = self._user_to_dict(user_update)
        if not update_data is None:
            await self._db.execute(
                update(User).where(User.id==user_id).values(**update_data)
            )
            await self._db.commit()
            await self._db.refresh(user)
        
        return user

    async def delete(self,user_id:str) -> bool:
        '''
        deletes an user
        '''
        user = await self.get_by_id(user_id)
        if user is None:
            return False
        
        await self._db.delete(user)
        await self._db.commit()
        return True
    
    async def get_by_username(self,username:str) -> User | None:
        '''
        gets an user by his username
        '''
        result = await self._db.execute(
            select(User).where(User.username==username)
        )
        return result.scalars().first()
    
    async def get_by_email(self,email:str) -> User | None:
        '''
        gets an user by his email
        '''
        result = await self._db.execute(
            select(User).where(User.email==email)
        )
        return result.scalars().first()
    
    async def get_by_id(self,user_id:str) -> User | None:
        '''
        gets an user by his id
        '''
        result = await self._db.execute(
            select(User).where(User.id==user_id)
        )
        return result.scalars().first()
    
    async def get_all(self,limit:int=100,skip:int=0,admin:bool | None = None) -> List[User]:
        '''
        gets the users

        params:
            limit: int -> limit of users in the result
            skip: int -> number of registes to skip
        '''
        # build the query
        query = select(User).offset(skip).limit(limit)
        result = await self._db.execute(
            # if not admin param is passed, execute tha query as it, else an 'where' sentence is applied
            query if admin is None else query.where(User.admin==admin)
        )
        return list(result.scalars().all())