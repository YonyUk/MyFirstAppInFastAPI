from fastapi import FastAPI
from fastapi.responses import JSONResponse
from database import ENGINE,BaseModel
from api.users import users,admin
from scalar_fastapi.scalar_fastapi import get_scalar_api_reference,Layout
from alembic.config import Config
from alembic import command
import logging
import os
from settings import ENVIRONMENT
import asyncio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_migrations():
    '''
    run the existents migrations
    '''
    path_config = os.path.join(os.getcwd(),ENVIRONMENT.ALEMBIC_CONFIG_FILE_PATH)
    alembic_cfg = Config(path_config)
    command.upgrade(alembic_cfg,'head')

app = FastAPI(
    title='MyApp',
    description='Learning FastAPI',
    version=ENVIRONMENT.API_VERSION,
    # docs_url=None,
    # lifespan=lifespan,
)

@app.on_event('startup')
async def startup():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None,run_migrations)
    async with ENGINE.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

@app.on_event('shutdown')
async def shutdown():
    await ENGINE.dispose()

app.include_router(users.router,prefix=ENVIRONMENT.GLOBAL_API_PREFIX)
app.include_router(admin.router,prefix=f'{ENVIRONMENT.GLOBAL_API_PREFIX}')

@app.exception_handler(404)
async def not_found_exception_handler(request,exc):
    return JSONResponse(
        status_code=404,
        content={'message':'Resource not found'}
    )

@app.exception_handler(505)
async def internal_exception_handler(request,exc):
    return JSONResponse(
        status_code=500,
        content={'message':'An unexpected internal error has ocurred'}
    )

# @app.get("/docs",include_in_schema=False)
# async def scalar_docs():
#     return get_scalar_api_reference(
#         openapi_url=app.openapi_url, # type: ignore
#         title='MyApp',
#         layout=Layout.MODERN,
#         dark_mode=True,
#         show_sidebar=True,
#         default_open_all_tags=True,
#         hide_download_button=False,
#         hide_models=False
#     )