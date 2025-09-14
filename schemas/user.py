from pydantic import EmailStr,BaseModel

class UserBase(BaseModel):
    '''
    User base schema
    '''
    username:str
    email:EmailStr

class UserAdminBase(UserBase):
    '''
    schema for admin users
    '''
    admin:bool

class UserCreate(UserBase):
    '''
    schema for create a new user
    '''
    password:str

class UserCreateAdmin(UserCreate):
    '''
    schema for create a new user from the admin section
    '''
    admin:bool

class UserUpdate(UserCreate):
    '''
    schema to update the data of one user
    '''

class UserAdminUpdate(UserCreateAdmin):
    '''
    schema to update the data of one user for an admin
    '''

class User(UserBase):
    '''
    schema for an user
    '''
    id:str

    class Config:
        orm_mode = True

class UserAdmin(UserAdminBase):
    '''
    schema for an admin user
    '''
    id:str

    class Config:
        orm_mode =True