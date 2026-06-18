from pydantic  import BaseModel 
from datetime import datetime
from sqlmodel import SQLModel , Field ,Relationship


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
   

class TaskPublic(TaskBase):
    id:int
    created_at:datetime
    updated_at:datetime
    owner_id: int

class TaskDB(TaskBase,table=True):
    id:int | None=Field(default=None,primary_key=True)
    created_at:datetime=Field(default_factory=datetime.now)
    updated_at:datetime=Field(default_factory=datetime.now)
    owner_id: int=Field(foreign_key="userdb.id")
    owner:"UserDB"=Relationship(back_populates="tasks")

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
    tasks:list["TaskDB"]=Relationship(back_populates="owner")
