import pytest
import random
from unittest.mock import AsyncMock
from uuid import uuid4
from tests.tools.users_tools import (
    fake_create_no_admin_user,
    fake_admin_create_no_admin_user,
    fake_admin_create_admin_user
)

from settings import TEST_ENVIRONMENT,ENVIRONMENT
from repositories import UserRepository
from services import UserService
from models import User
from schemas import UserCreateAdmin,UserAdminUpdate
from utils.lists import first,remove

@pytest.fixture(scope='session')
def no_admin_users_created():
    return list([fake_create_no_admin_user() for _ in range(TEST_ENVIRONMENT.TOTAL_NON_ADMINS_USERS // 2)])

@pytest.fixture(scope='session')
def admin_users_created_by_admin():
    return list([fake_admin_create_admin_user() for _ in range(TEST_ENVIRONMENT.TOTAL_ADMINS_USERS)])

@pytest.fixture(scope='session')
def no_admin_users_created_by_admin():
    return list([fake_admin_create_no_admin_user() for _ in range(TEST_ENVIRONMENT.TOTAL_NON_ADMINS_USERS // 2)])

@pytest.fixture(scope='session')
def users(no_admin_users_created,admin_users_created_by_admin,no_admin_users_created_by_admin):
    return no_admin_users_created_by_admin + admin_users_created_by_admin + no_admin_users_created

@pytest.fixture(scope='session')
def db_users(users):
    result = []
    for user in users:
        admin=False
        if isinstance(user,UserCreateAdmin):
            admin = user.admin
        _user = User(
                id=str(uuid4()),
                username=user.username,
                email=user.email,
                hashed_password=ENVIRONMENT.CRYPT_CONTEXT.hash(user.password),
                admin=admin
            )
        result.append(_user)
    return result

@pytest.mark.asyncio
async def test_add_user(users,db_users,admin_users_created_by_admin):
    no_admins = list(filter(lambda x:not x in admin_users_created_by_admin,users))
    admins = list(filter(lambda u:u in admin_users_created_by_admin,users))
    user = random.choice(no_admins)
    r_user = first(db_users,lambda u: u.username==user.username)
    repository = AsyncMock(spec_set=UserRepository)
    repository.create.return_value = r_user
    service = UserService(repository)
    repository_user = await service.add_user(user)
    assert repository_user == r_user
    user = random.choice(admins)
    r_user = first(db_users,lambda u: u.username==user.username)
    repository.create.return_value = r_user
    repository_user = await service.add_user(user)
    assert repository_user == r_user

@pytest.mark.asyncio
async def test_authenticate_user(users,db_users):
    user = random.choice(users)
    username = user.username
    password = user.password
    r_user = first(db_users,lambda u: u.username == username)
    repository = AsyncMock(spec_set=UserRepository)
    repository.get_by_username.return_value = r_user
    service = UserService(repository)
    respository_user = await service.authenticate_user(username,password)
    assert respository_user == r_user

@pytest.mark.asyncio
async def test_update_user(users,db_users):
    user = random.choice(users)
    username = user.username + '_test'
    email = 'test_' + user.email
    password = 'test_' + user.password
    admin = not user.admin if isinstance(user,UserCreateAdmin) else True
    update_data = UserAdminUpdate(
        username=username,
        email=email,
        password=password,
        admin=admin
    )
    r_user:User = first(db_users,lambda u:u.username == user.username) # type: ignore
    r_user:User = User(
        id=r_user.id,
        username=username,
        email=email,
        hashed_password=ENVIRONMENT.CRYPT_CONTEXT.hash(password),
        admin=admin
    )
    repository = AsyncMock(spec_set=UserRepository)
    repository.update.return_value = r_user
    service = UserService(repository)
    repository_user = await service.update_user(r_user.id,update_data)
    assert repository_user == r_user

@pytest.mark.asyncio
async def test_delete_user(db_users):
    user = random.choice(db_users)
    db_users = remove(db_users,lambda u: u.id == user.id)
    repository = AsyncMock(spec_set=UserRepository)
    repository.delete.return_value = True
    service = UserService(repository)
    result = await service.delete_user(user.id)
    assert result

@pytest.mark.asyncio
async def test_get_user_by_name(db_users):
    user = random.choice(db_users)
    repository = AsyncMock(spec_set=UserRepository)
    repository.get_by_username.return_value = user
    service = UserService(repository)
    r_user = await service.get_by_name(user.username)
    assert r_user == user

@pytest.mark.asyncio
async def test_get_user_by_email(db_users):
    user = random.choice(db_users)
    repository = AsyncMock(spec_set=UserRepository)
    repository.get_by_email.return_value = user
    service = UserService(repository)
    r_user = await service.get_user_by_email(user.email)
    assert r_user == user

@pytest.mark.asyncio
async def test_get_user_by_id(db_users):
    user = random.choice(db_users)
    repository = AsyncMock(spec_set=UserRepository)
    repository.get_by_id.return_value = user
    service = UserService(repository)
    r_user = await service.get_user_by_id(user.id)
    assert r_user == user

@pytest.mark.asyncio
async def test_get_all_users(db_users):
    limit:int = random.randint(1,len(db_users))
    skip:int = random.randint(0,len(db_users))
    result = db_users[skip:skip + limit]
    repository = AsyncMock(spec_set=UserRepository)
    repository.get_all.return_value = result
    service = UserService(repository)
    r = await service.get_users(limit,skip)
    assert r == result
    result = list(filter(lambda u:u.admin,db_users))[skip:skip+limit]
    repository.get_all.return_value = result
    r = await service.get_users(limit,skip,True)
    assert r == result
    result = list(filter(lambda u:not u.admin,db_users))[skip:skip+limit]
    repository.get_all.return_value = result
    r = await service.get_users(limit,skip,False)
    assert r == result