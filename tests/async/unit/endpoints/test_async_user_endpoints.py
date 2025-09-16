import pytest
import pytest_asyncio
import asyncio
import datetime
from httpx import AsyncClient,ASGITransport
from tests.tools import fake_valid_user
from settings import ENVIRONMENT
from main import app
from api.users.users import router as user_router

TOTAL_USERS = 10

async def create_user_async(async_client:AsyncClient,url:str,headers:dict | None = None):
    user = fake_valid_user()
    response = await async_client.post(
        url,
        json=user,
        headers=headers if not headers is None else {} 
    )
    return response

@pytest.mark.asyncio
async def test_massive_create_user():
    async_client = AsyncClient(
        base_url='http://localhost:8000',
        transport=ASGITransport(app=app)
    )
    url = f'{ENVIRONMENT.GLOBAL_API_PREFIX}{user_router.prefix}/register'
    successfull_responses_count = 0
    t = datetime.datetime.now()
    tasks = set()
    for _ in range(TOTAL_USERS):
        task = asyncio.create_task(create_user_async(async_client,url))
        tasks.add(task)
        task.add_done_callback(tasks.discard)
    responses = await asyncio.gather(*tasks)
    for resp in responses:
        if resp.status_code == 201:
            successfull_responses_count += 1
    t = datetime.datetime.now() - t
    msg = f'OK {successfull_responses_count}, WRONG {TOTAL_USERS - successfull_responses_count}'
    msg += f' time transcurred {t}'
    assert successfull_responses_count == TOTAL_USERS,msg