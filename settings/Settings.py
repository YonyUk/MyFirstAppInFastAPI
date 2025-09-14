import dotenv
import os
from passlib.context import CryptContext

dotenv.load_dotenv()

class EnvironmentSettings:
    '''
    container class for the environment variables
    '''
    def __init__(self):
        self._db_engine:str = os.getenv('DB_ENGINE','database engine')
        self._db_user:str = os.getenv('DB_USER','database user')
        self._db_host:str = os.getenv('DB_HOST','database host')
        self._db_port:int = int(os.getenv('DB_PORT','listener port for the database'))
        self._db_password:str = os.getenv('DB_PASSWORD','database password')
        self._db_name:str = os.getenv('DB_NAME','database name')
        self._global_api_prefix:str = os.getenv('API_GLOBAL_PREFIX','global api prefix for endpoints')
        self._api_version:str = os.getenv('VERSION','api version')
        self._secret_key:str = os.getenv('SECRET_KEY','your secret key')
        self._algorithm:str = os.getenv('ALGORITHM','algorithm to use')
        self._token_life_time:int = int(os.getenv('ACCESS_TOKEN_EXPIRES_MINUTES','access token life time'))
        self._alembic_config_file_path:str = os.getenv('ALEMBIC_CONFIG_FILE','alembic config file path')
        self._crypt_context:CryptContext = CryptContext(schemes=['bcrypt'],deprecated='auto')

    @property
    def CRYPT_CONTEXT(self) -> CryptContext:
        '''
        return the global cryptography context
        '''
        return self._crypt_context

    @property
    def DB_ENGINE(self) -> str:
        '''
        database engine currently used
        '''
        return self._db_engine
    
    @property
    def DB_USER(self) -> str:
        '''
        current database host user
        '''
        return self._db_user
    
    @property
    def DB_HOST(self) -> str:
        '''
        database host url
        '''
        return self._db_host
    
    @property
    def DB_PORT(self) -> int:
        '''
        database host listener port 
        '''
        return self._db_port
    
    @property
    def DB_PASSWORD(self) -> str:
        '''
        current user's password in for the database host
        '''
        return self._db_password

    @property
    def DB_NAME(self) -> str:
        '''
        database name
        '''
        return self._db_name

    @property
    def DB_URL(self) -> str:
        '''
        database url
        '''
        return f'{self._db_user}:{self._db_password}@{self._db_host}:{self._db_port}/{self._db_name}'
    
    @property
    def GLOBAL_API_PREFIX(self) -> str:
        '''
        global api prefix for endpoints
        '''
        return self._global_api_prefix
    
    @property
    def API_VERSION(self) -> str:
        '''
        API Version
        '''
        return self._api_version
    
    @property
    def SECRET_KEY(self) -> str:
        '''
        Secret key
        '''
        return self._secret_key
    
    @property
    def ALGORITHM(self) -> str:
        '''
        Algorithm for the OAuth section
        '''
        return self._algorithm
    
    @property
    def TOKEN_LIFE_TIME(self) -> int:
        '''
        authorization token life time
        '''
        return self._token_life_time
    
    @property
    def ALEMBIC_CONFIG_FILE_PATH(self) -> str:
        '''
        config file path for alembic
        '''
        return self._alembic_config_file_path