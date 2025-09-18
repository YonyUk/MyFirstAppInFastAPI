import dotenv
import os

dotenv.load_dotenv()

class TestEnvironmentSettings:

    def __init__(self):
        self._test_async_client_base_url:str=os.getenv(
            'TEST_ASYNC_CLIENT_BASE_URL',
            'base url for the async client during the test phase'
        )
        self._concurrent_requests:int=int(os.getenv(
            'CONCURRENT_REQUESTS',
            'number of concurrent requests to the app'
        ))
        self._total_get_requests:int=int(os.getenv(
            'TOTAL_GET_REQUESTS',
            'total get requests for tests'
        ))
        self._total_admins_users:int=int(os.getenv(
            'TOTAL_ADMINS_USERS',
            'admins users to create in tests'
        ))
        self._total_non_admins_users:int=int(os.getenv(
            'TOTAL_NON_ADMINS_USERS',
            'non admins users to create in tests'
        ))
        self._main_admin_user_id:str=os.getenv(
            'MAIN_ADMIN_USER_ID',
            'main admin user id'
        )
        self._main_admin_username:str=os.getenv(
            'MAIN_ADMIN_USERNAME',
            'main admin user username'
        )
        self._main_admin_password:str=os.getenv(
            'MAIN_ADMIN_PASSWORD',
            'main admin user password'
        )
        self._defaults_users_in_database:int=int(os.getenv(
            'DEFAULT_USERS_IN_DATABASE',
            'count of users in database by default'
        ))

    @property
    def DEFAULT_USERS_IN_DATABASE(self) -> int:
        '''
        count of users in database by default
        '''
        return self._defaults_users_in_database

    @property
    def MAIN_ADMIN_USERNAME(self) -> str:
        '''
        main admin user username
        '''
        return self._main_admin_username

    @property
    def MAIN_ADMIN_PASSWORD(self) -> str:
        '''
        main admin user password
        '''
        return self._main_admin_password

    @property
    def MAIN_ADMIN_USER_ID(self) -> str:
        '''
        main admin user id
        '''
        return self._main_admin_user_id

    @property
    def TOTAL_ADMINS_USERS(self) -> int:
        '''
        non admins users to create in tests
        '''
        return self._total_admins_users
    
    @property
    def TOTAL_NON_ADMINS_USERS(self) -> int:
        '''
        non admins users to create in tests
        '''
        return self._total_non_admins_users

    @property
    def TOTAL_GET_REQUESTS(self) -> int:
        '''
        total get requests for tests
        '''
        return self._total_get_requests

    @property
    def TEST_ASYNC_CLIENT_BASE_URL(self) -> str:
        '''
        base url for the async client during the test phase
        '''
        return self._test_async_client_base_url

    @property
    def CONCURRENT_REQUESTS(self) -> int:
        '''
        number of concurrent requests to the app
        '''
        return self._concurrent_requests