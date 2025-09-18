import random
from string import ascii_letters,ascii_lowercase
from uuid import uuid4
from models import User
from settings import ENVIRONMENT

def fake_no_admin_user() -> User:
    username = ''.join(random.choices(ascii_letters,k=random.randint(5,15)))
    e1 = ''.join(random.choices(ascii_letters,k=random.randint(5,15)))
    e2 = ''.join(random.choices(ascii_lowercase,k=random.randint(5,15)))
    email = f'{e1}@{e2}.com'
    id = str(uuid4())
    password = ''.join(random.choices(ascii_letters,k=random.randint(5,15)))
    hashed_password = ENVIRONMENT.CRYPT_CONTEXT.hash(password)
    return User(
        id=id,
        username=username,
        email=email,
        hashed_password=hashed_password,
        admin=False
    )

def fake_admin_user() -> User:
    user = fake_no_admin_user()
    return User(
        id=user.id,
        username=user.username,
        email=user.email,
        hashed_password=user.hashed_password,
        admin=True
    )