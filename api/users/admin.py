from typing import List
from fastapi import APIRouter,HTTPException, Query,status,Depends
from models import User
from schemas import UserCreateAdmin,UserAdmin as UserSchema,UserAdminUpdate
from security import get_current_user
from .users_http_exceptions import UNAUTHORIZED_EXCEPTION,USER_ALREADY_EXISTS_ECXCEPTION,EMAIL_ALREADY_REGISTERED_EXCEPTION
from services import UserService,get_user_service
from settings import ENVIRONMENT

router = APIRouter(prefix='/admin',tags=['admin'])

@router.post(
    '/users/register',
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user:UserCreateAdmin,
    status_code=status.HTTP_201_CREATED,
    service:UserService=Depends(get_user_service),
    current_user:User=Depends(get_current_user)
):
    if not bool(current_user.admin):
        raise UNAUTHORIZED_EXCEPTION
    db_user = await service.get_by_name(user.username)
    if db_user:
        raise USER_ALREADY_EXISTS_ECXCEPTION
    db_email = await service.get_user_by_email(user.email)
    if db_email:
        raise EMAIL_ALREADY_REGISTERED_EXCEPTION
    hashed_password = ENVIRONMENT.CRYPT_CONTEXT.hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        admin=user.admin
    )
    await service.add_user(db_user)
    return db_user

@router.get(
        '/users',
        response_model=List[UserSchema],
)
async def get_users(
    service:UserService=Depends(get_user_service),
    current_user:User=Depends(get_current_user),
    skip: int = Query(0,ge=0,description='Number of registers to skip'),
    limit:int = Query(100,ge=1,le=1000,description='Limit of registers pre response')
):
    if bool(current_user.admin):
        return await service.get_users(limit,skip)
    raise UNAUTHORIZED_EXCEPTION

@router.get(
        '/users/id/{user_id}',
        response_model=UserSchema,
)
async def get_user_by_id(
    user_id:str,
    service:UserService=Depends(get_user_service),
    current_user:User=Depends(get_current_user)
):
    if not bool(current_user.admin):
        raise UNAUTHORIZED_EXCEPTION
    user = await service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found'
        )
    return user

@router.get(
        '/users/name/{user_name}',
        response_model=UserSchema,
)
async def get_user_by_name(
    user_name:str,
    service:UserService=Depends(get_user_service),
    current_user:User=Depends(get_current_user)
):
    if not bool(current_user.admin):
        raise UNAUTHORIZED_EXCEPTION
    user = await service.get_by_name(user_name)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found'
        )
    return user

@router.put(
        '/users/id/{user_id}',
        response_model=UserSchema
)
async def update_user_by_id(
    user_id:str,
    user_update:UserAdminUpdate,
    service:UserService=Depends(get_user_service),
    current_user:UserSchema=Depends(get_current_user)
):
    if not bool(current_user.admin):
        raise UNAUTHORIZED_EXCEPTION
    user = await service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found'
        )
    await service.update_user(user_id,user_update)
    return user

@router.put(
        '/users/name/{user_name}',
        response_model=UserSchema
)
async def update_user_by_name(
    user_name:str,
    user_update:UserAdminUpdate,
    service:UserService=Depends(get_user_service),
    current_user:UserSchema=Depends(get_current_user)
):
    if not bool(current_user.admin):
        raise UNAUTHORIZED_EXCEPTION
    user = await service.get_by_name(user_name)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found'
        )
    await service.update_user(user,user_update)
    return user

@router.delete(
    '/users/id/{user_id}',
    status_code=status.HTTP_200_OK
)
async def delete_user_by_id(
    user_id:str,
    service:UserService=Depends(get_user_service),
    current_user:User=Depends(get_current_user)
):
    if not current_user.admin:
        raise UNAUTHORIZED_EXCEPTION
    user = service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found'
        )
    await service.delete_user(user_id)
    return {'message':'user deleted'}

@router.delete(
    '/users/name/{user_name}',
    status_code=status.HTTP_200_OK
)
async def delete_user_by_name(
    user_name:str,
    service:UserService=Depends(get_user_service),
    current_user:User=Depends(get_current_user)
):
    if not current_user.admin:
        raise UNAUTHORIZED_EXCEPTION
    user = await service.get_by_name(user_name)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='user not found'
        )
    await service.delete_user(user.id)
    return {'message':'user deleted'}