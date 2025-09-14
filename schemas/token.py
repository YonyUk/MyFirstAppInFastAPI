from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    '''
    schema for the authorization token
    '''
    access_token:str
    token_type:str

class TokenData(BaseModel):
    '''
    schema for get the authorization token for an user
    '''
    username:Optional[str] = None