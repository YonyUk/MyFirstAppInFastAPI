from fastapi.testclient import TestClient
from settings import ENVIRONMENT
from api.users.users import router as user_router

def test_create_user(client:TestClient):
    data = {
        'username':'test-user',
        'email':'test@example.com',
        'password':'test-password'
    }
    response = client.post(
        f'{ENVIRONMENT.GLOBAL_API_PREFIX}{user_router.prefix}/register',
        json=data
    )
    assert response.status_code == 201
    assert response.json()['email'] == data['email']
    assert response.json()['username'] == data['username']
        