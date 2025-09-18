import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from unittest.mock import AsyncMock,MagicMock
from tests.tools.users_tools import (
    fake_no_admin_user,
    fake_admin_user
)
from settings import TEST_ENVIRONMENT
from repositories import UserRepository
import random

@pytest.fixture(scope='session')
def no_admin_users():
    return list([fake_no_admin_user() for _ in range(TEST_ENVIRONMENT.TOTAL_NON_ADMINS_USERS)])

@pytest.fixture(scope='session')
def admin_users():
    return list([fake_no_admin_user() for _ in range(TEST_ENVIRONMENT.TOTAL_ADMINS_USERS)])

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
    values = list(filter(lambda x:x.id == user.id,users))
    db = AsyncMock(spec_set=AsyncSession)
    execute_mock = MagicMock()
    scalars_mock = MagicMock()
    scalars_mock.first.return_value = values[0]
    execute_mock.scalars.return_value = scalars_mock
    db.execute.return_value = execute_mock
    repository = UserRepository(db)
    db_user = await repository.get_by_id(user.id)
    assert db_user == user
    scalars_mock.first.return_value = None
    db_user = await repository.get_by_id('')
    assert db_user is None
    user_ = list(filter(lambda x:x.id != user.id,users))[0]
    scalars_mock.first.return_value = user_
    db_user = await repository.get_by_id(user_.id)
    assert db_user is not None and db_user != user

@pytest.mark.asyncio
async def test_get_by_email(users):
    user = random.choice(users)
    values = list(filter(lambda x:x.email == user.email,users))
    db = AsyncMock(spec_set=AsyncSession)
    execute_mock = MagicMock()
    scalars_mock = MagicMock()
    scalars_mock.first.return_value = values[0]
    execute_mock.scalars.return_value = scalars_mock
    db.execute.return_value = execute_mock
    repository = UserRepository(db)
    db_user = await repository.get_by_email(user.email)
    assert db_user == user
    scalars_mock.first.return_value = None
    db_user = await repository.get_by_email('')
    assert db_user is None
    user_ = list(filter(lambda x:x.email != user.email,users))[0]
    scalars_mock.first.return_value = user_
    db_user = await repository.get_by_email(user_.email)
    assert db_user is not None and db_user != user