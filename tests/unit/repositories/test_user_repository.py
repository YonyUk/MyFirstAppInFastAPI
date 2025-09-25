import pytest
import random
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock,MagicMock
from tests.tools.users_tools import (
    fake_no_admin_user,
    fake_admin_user
)
from settings import TEST_ENVIRONMENT
from repositories import UserRepository
from models import User

@pytest.fixture(scope='session')
def no_admin_users():
    return list([fake_no_admin_user() for _ in range(TEST_ENVIRONMENT.TOTAL_NON_ADMINS_USERS)])

@pytest.fixture(scope='session')
def admin_users():
    return list([fake_admin_user() for _ in range(TEST_ENVIRONMENT.TOTAL_ADMINS_USERS)])

@pytest.fixture(scope='session')
def users(admin_users,no_admin_users):
    return admin_users + no_admin_users

@pytest.mark.asyncio
async def test_create_user():
    db = AsyncMock(spec_set=AsyncSession)
    repository = UserRepository(db)
    user = fake_no_admin_user()
    db_user = await repository.create(user)
    assert db_user == user

@pytest.mark.asyncio
async def test_get_by_id(users):
    user = random.choice(users)
    db = AsyncMock(spec_set=AsyncSession)
    execute_mock = MagicMock()
    db.execute.return_value = execute_mock
    execute_mock.scalars.return_value.first.return_value = user
    repository = UserRepository(db)
    db_user = await repository.get_by_id(user.id)
    assert db_user == user
    execute_mock.scalars.return_value.first.return_value = None
    db_user = await repository.get_by_id('')
    assert db_user is None
    user_ = list(filter(lambda x:x.id != user.id,users))[0]
    execute_mock.scalars.return_value.first.return_value = user_
    db_user = await repository.get_by_id(user_.id)
    assert db_user is not None and db_user != user

@pytest.mark.asyncio
async def test_get_by_email(users):
    user = random.choice(users)
    db = AsyncMock(spec_set=AsyncSession)
    execute_mock = MagicMock()
    db.execute.return_value = execute_mock
    execute_mock.scalars.return_value.first.return_value = user
    repository = UserRepository(db)
    db_user = await repository.get_by_email(user.email)
    assert db_user == user
    execute_mock.scalars.return_value.first.return_value = None
    db_user = await repository.get_by_email('')
    assert db_user is None
    user_ = list(filter(lambda x:x.email != user.email,users))[0]
    execute_mock.scalars.return_value.first.return_value = user_
    db_user = await repository.get_by_email(user_.email)
    assert db_user is not None and db_user != user

@pytest.mark.asyncio
async def test_get_by_username(users):
    user = random.choice(users)
    db = AsyncMock(spec_set=AsyncSession)
    execute_mock = MagicMock()
    db.execute.return_value = execute_mock
    execute_mock.scalars.return_value.first.return_value = user
    repository = UserRepository(db)
    db_user = await repository.get_by_username(user.username)
    assert db_user == user
    execute_mock.scalars.return_value.first.return_value = None
    db_user = await repository.get_by_username('')
    assert db_user is None
    user_ = list(filter(lambda x:x.username != user.username,users))[0]
    execute_mock.scalars.return_value.first.return_value = user_
    db_user = await repository.get_by_username(user_.username)
    assert db_user is not None and db_user != user

@pytest.mark.asyncio
async def test_get_all(users):
    limit:int = random.randint(1,len(users) - 1)
    offset:int = random.randint(0,len(users) - 1)
    admin:bool | None = None
    db = AsyncMock(spec_set=AsyncSession)
    execute_mock = MagicMock()
    db.execute.return_value = execute_mock
    result = users[offset:offset + limit]
    execute_mock.scalars.return_value.all.return_value = result
    repository = UserRepository(db)
    db_users = await repository.get_all(limit,offset,admin)
    assert db_users == result
    admin = True
    limit = random.randint(1,len(users) - 1)
    offset = random.randint(0,len(users) - 1)
    result = list(filter(lambda x:x.admin == admin,users))[offset:offset+limit]
    execute_mock.scalars.return_value.all.return_value = result
    db_users = await repository.get_all(limit,offset,admin)
    assert db_users == result
    admin = False
    limit = random.randint(1,len(users) - 1)
    offset = random.randint(0,len(users) - 1)
    result = list(filter(lambda x:x.admin == admin,users))[offset:offset+limit]
    execute_mock.scalars.return_value.all.return_value = result
    db_users = await repository.get_all(limit,offset,admin)
    assert db_users == result

@pytest.mark.asyncio
async def test_update(users):
    user = random.choice(users)
    update_data = fake_no_admin_user()
    db = AsyncMock(spec_set=AsyncSession)
    execute_mock = MagicMock()
    db.execute.return_value = execute_mock
    execute_mock.scalars.return_value.first.return_value = update_data
    repository = UserRepository(db)
    db_user:User | None = await repository.update(user.id,update_data)
    assert db_user is not None
    assert db_user.email == update_data.email
    assert db_user.hashed_password == update_data.hashed_password
    assert db_user.username == update_data.username
    assert db_user.admin == update_data.admin

@pytest.mark.asyncio
async def test_delete(users):
    user = random.choice(users)
    db = AsyncMock(spec_set=AsyncSession)
    execute_mock = MagicMock()
    db.execute.return_value = execute_mock
    repository = UserRepository(db)
    execute_mock.scalars.return_value.first.return_value = user
    result = await repository.delete(user.id)
    assert result
    user = fake_no_admin_user()
    execute_mock.scalars.return_value.first.return_value = None
    result = await repository.delete(user.id)
    assert not result