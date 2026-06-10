from pydantic  import BaseModel 
from datetime import datetime
from sqlmodel import SQLModel , Field


class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    username:str |None=None




class TaskBase(SQLModel):
    title:str
    description:str |None=None
    completed:bool=Field(default=False)

class TaskCreate(TaskBase):
    pass
   

class TaskUpdate(SQLModel):
    title:str |None=None
    description:str |None=None
    completed:bool=Field(default=False)
    # updated_at:datetime=Field(default_factory=datetime.now) #now() wrong...this will call immediately nor passing the func

class TaskPublic(TaskBase):
    id:int
    created_at:datetime
    updated_at:datetime

class TaskDB(TaskBase,table=True):
    id:int | None=Field(default=None,primary_key=True)
    created_at:datetime=Field(default_factory=datetime.now)
    updated_at:datetime=Field(default_factory=datetime.now)

class User(SQLModel):
    username:str

class UserCreate(User):
    password:str

class UserUpdate(SQLModel):
    username:str |None=None
    password:str |None=None

class UserOut(User):
    id:int
   

class UserDB(User,table=True):
    id:int |None=Field(default=None,primary_key=True)
    hashed_password:str 
    disabled:bool =False
