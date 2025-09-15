from string import ascii_letters,ascii_lowercase
import random
from schemas import UserCreate,UserCreateAdmin

def _fake_username() -> str:
    '''
    create a fake username
    '''
    length = random.randint(5,15)
    return ''.join([ascii_letters[random.randint(0,len(ascii_letters) - 1)] for _ in range(length)])

def _fake_valid_email() -> str:
    '''
    create a fake valid email
    '''
    name_length = random.randint(5,15)
    domain_length = random.randint(5,10)
    name = ''.join([ascii_letters[random.randint(0,len(ascii_letters) - 1)] for _ in range(name_length)])
    domain = ''.join([ascii_lowercase[random.randint(0,len(ascii_lowercase) - 1)] for _ in range(domain_length)])
    return f'{name}@{domain}.com'

def fake_valid_user() -> dict:
    '''
    create a fake valid User
    '''
    return {
        'username':_fake_username(),
        'email':_fake_valid_email(),
        'password':_fake_username()
    }

def fake_invalid_user() -> dict:
    '''
    create an invalid User
    '''
    return {
        'username':_fake_username(),
        'email':_fake_username(),
        'password':_fake_username()
    }

def fake_admin_user() -> dict:
    '''
    create a fake admin user
    '''
    return {
        'username':_fake_username(),
        'email':_fake_valid_email(),
        'password':_fake_username(),
        'admin':True
    }