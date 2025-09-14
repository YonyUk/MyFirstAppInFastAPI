from fastapi.testclient import TestClient
from .unit.endpoints.test_user_endpoints import test_create_user
from main import app

client = TestClient(app)

def test_users_endpoints():
    test_create_user(client)