from fastapi.testclient import TestClient
from settings import ENVIRONMENT
from api.users.users import router as user_router
from api.users.admin import router as admin_router
from main import app
from tests.tools import fake_invalid_user,fake_valid_user,fake_admin_user
from security import get_current_user
import pytest
from models import User

valid_user = fake_valid_user()
invalid_user = fake_invalid_user()
admin_user = fake_admin_user()

@pytest.fixture
def client():
    def mock_get_current_user():
        return User(
            username='admin',
            id='8340b3f6-a6f1-41b5-8c51-217288ef7e62',
            email='admin@example.com',
            hashed_password=ENVIRONMENT.CRYPT_CONTEXT.hash('admin'),
            admin=True
        )
    app.dependency_overrides[get_current_user] = mock_get_current_user
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def auth_token(client):
    response = client.post(
        f'{ENVIRONMENT.GLOBAL_API_PREFIX}{user_router.prefix}/token',
        data={
            'username':'admin',
            'password':'admin',
            'grant_type':'password'
        },
        headers={
            'Content-Type':'application/x-www-form-urlencoded',
        }
    )
    return response.json()['access_token']

def test_create_valid_user(client):
    response = client.post(
        f'{ENVIRONMENT.GLOBAL_API_PREFIX}{user_router.prefix}/register',
        json=valid_user
    )
    assert response.status_code == 201
    assert response.json()['email'] == valid_user['email']
    assert response.json()['username'] == valid_user['username']

def test_create_invalid_user(client):
    response = client.post(
        f'{ENVIRONMENT.GLOBAL_API_PREFIX}{user_router.prefix}/register',
        json=invalid_user
    )
    assert response.status_code == 422
    assert response.json()['detail'][0]['type'] == 'value_error'

def test_create_admin_user(client):
    response = client.post(
        f'{ENVIRONMENT.GLOBAL_API_PREFIX}{user_router.prefix}/token',
        data={
            'username':'admin',
            'password':'admin',
            'grant_type':'password'
        },
        headers={
            'Content-Type':'application/x-www-form-urlencoded',
        }
    )
    token = response.json()['access_token']
    response = client.post(
        f'{ENVIRONMENT.GLOBAL_API_PREFIX}{admin_router.prefix}/users/register',
        json=admin_user,
        headers={
            'Authorization':f'Bearer {token}'
        },
    )
    assert response.status_code == 201
    assert response.json()['email'] == admin_user['email']
    assert response.json()['username'] == admin_user['username']
    assert response.json()['admin'] == admin_user['admin']

def test_valid_login(client):
    response = client.post(
        f'{ENVIRONMENT.GLOBAL_API_PREFIX}{user_router.prefix}/token',
        data={
            'username':valid_user['username'],
            'password':valid_user['password'],
            'grant_type':'password'
        },
        headers={
            'Content-Type':'application/x-www-form-urlencoded'
        }
    )
    assert response.status_code == 200
    assert response.json()['token_type'] == 'bearer'

def test_invalid_login(client):
    response = client.post(
        f'{ENVIRONMENT.GLOBAL_API_PREFIX}{user_router.prefix}/token',
        data={
            'username':invalid_user['username'],
            'password':invalid_user['password'],
            'grant_type':'password'
        },
        headers={
            'Content-Type':'application/x-www-form-urlencoded'
        }
    )
    assert response.status_code == 401
    assert response.json()['detail'] == 'Incorrect username or password'

def test_admin_login(client):
    response = client.post(
        f'{ENVIRONMENT.GLOBAL_API_PREFIX}{user_router.prefix}/token',
        data={
            'username':admin_user['username'],
            'password':admin_user['password'],
            'grant_type':'password'
        }
    )
    assert response.status_code == 200
    assert response.json()['token_type'] == 'bearer'
    
def test_valid_get_users(client,auth_token):
    response = client.get(
        f'{ENVIRONMENT.GLOBAL_API_PREFIX}{admin_router.prefix}/users?skip=0&limit=100',
        headers={
            'Authorization':f'Bearer {auth_token}'
        }
    )
    assert response.status_code == 200
    assert len(response.json()) <= 100