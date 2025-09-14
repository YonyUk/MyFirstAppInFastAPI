from fastapi import APIRouter,HTTPException,status,Depends
from models import User
from schemas import UserCreate,User as UserSchema,Token
from security import create_access_token
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from .users_http_exceptions import USER_ALREADY_EXISTS_ECXCEPTION,EMAIL_ALREADY_REGISTERED_EXCEPTION
from settings import ENVIRONMENT
from services import UserService,get_user_service

router = APIRouter(prefix='/users',tags=['users'])

@router.post(
    '/register',
    response_model=UserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user:UserCreate,
    status_code=status.HTTP_201_CREATED,
    service:UserService=Depends(get_user_service)
):
    db_user = await service.get_by_name(user.username)
    if db_user:
        raise USER_ALREADY_EXISTS_ECXCEPTION
    db_email = await service.get_user_by_email(user.email)
    if db_email:
        raise EMAIL_ALREADY_REGISTERED_EXCEPTION
    hashed_password = ENVIRONMENT.CRYPT_CONTEXT.hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    await service.add_user(db_user)
    return db_user

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    service:UserService=Depends(get_user_service)
):
    # look for the user
    user = await service.authenticate_user(form_data.username, form_data.password)
    if not user:
        # if no exists raise 401 error
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # create the auth token
    access_token_expires = timedelta(minutes=float(ENVIRONMENT.TOKEN_LIFE_TIME))
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}