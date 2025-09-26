import pytest
import random
from uuid import uuid4
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient
from services import UserService
from schemas import (
    UserCreate,
    UserCreateAdmin
)
from models import User
from main import app
from settings import ENVIRONMENT,TEST_ENVIRONMENT
from tests.tools.users_tools import (
    fake_create_no_admin_user,
    fake_admin_create_admin_user,
    fake_admin_create_no_admin_user
)
from services import get_user_service
from utils.lists import first

@pytest.fixture(scope='session')
def database():
    return []

@pytest.fixture(scope='session')
def users():
    return []

def mock_get_user_service(database,users):
    
    def mock_add_user(user:UserCreateAdmin | UserCreate) -> User | None:
        admin = False if isinstance(user,UserCreate) else user.admin
        _user = User(
            id=str(uuid4()),
            username=user.username,
            email=user.email,
            hashed_password=ENVIRONMENT.CRYPT_CONTEXT.hash(user.password),
            admin=admin
        )
        users.append(user)
        database.append(_user)
        return _user
    
    def mock_get_by_name(username:str) -> User | None:
        return first(database,lambda u:u.username==username) # type: ignore
    
    def mock_get_user_by_email(email:str) -> User:
        return first(database,lambda u:u.email==email) # type: ignore
    
    def mock_authenticate_user(username:str,password:str) -> User | None:
        user:User = first(database,lambda u:u.username==username) # type: ignore
        return user if ENVIRONMENT.CRYPT_CONTEXT.verify(password,user.hashed_password) else None
    
    service_mock = AsyncMock(spec_set=UserService)
    service_mock.add_user.side_effect=mock_add_user
    service_mock.get_by_name.side_effect=mock_get_by_name
    service_mock.get_user_by_email.side_effect=mock_get_user_by_email
    service_mock.authenticate_user.side_effect=mock_authenticate_user
    return service_mock

@pytest.fixture(scope='session')
def client(database,users):
    app.dependency_overrides[get_user_service] = lambda:mock_get_user_service(database,users)
    with TestClient(app) as client_:
        yield client_
    app.dependency_overrides.clear()

def test_register_endpoint(client):
    data = fake_create_no_admin_user().model_dump()
    response = client.post(
        '/api/v1/users/register',
        json=data
    )
    assert response.status_code == 201
    json_data = response.json()
    assert json_data['username'] == data['username']
    assert json_data['email'] == data['email']

def test_authenticate_user_endpoint(client,users):
    assert len(users) > 0
    data = random.choice(users)
    data_ = {
        'grant_type':'password',
        'username':data.username,
        'password':data.password
    }
    headers={
        'Content-Type':'application/x-www-form-urlencoded'
    }
    response = client.post(
        '/api/v1/users/token',
        data = data_,
        headers=headers
    )
    # assert response.json() == {}
    assert response.status_code == 200