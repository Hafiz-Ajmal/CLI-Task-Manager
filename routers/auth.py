
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi.security import OAuth2AuthorizationCodeBearer,OAuth2PasswordRequestForm,OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt
from jose.exceptions import JWTError
#from models import UserInDB,UserOut,User,Token,TokenData

from fastapi import FastAPI,Path,Depends,APIRouter,Query,HTTPException
from typing import Annotated ,Any
from datetime import timedelta,timezone,datetime
from dependencies import session_Dep
from models import TaskDB ,UserDB,UserCreate,UserOut,User,UserUpdate,TaskUpdate,Token,TokenData,TaskCreate,TaskBase,TaskPublic
from sqlmodel import select,Session

router = APIRouter(prefix="/auth", tags=["auth"])

SECRET_KEY="121212121234@3780%^&3082973489y"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
  




pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password:str) ->str:
    return pwd_context.hash(password)

def verifyPassword(plain:str,hashed:str) ->bool:
    return pwd_context.verify(plain,hashed)


auth_2=OAuth2PasswordBearer(tokenUrl="/auth/token")

DUMMY_HASH = hash_password("dummypassword")




def get_user(username:str,db:Session):
    user=db.exec(select(UserDB).where(UserDB.username==username)).first()
    if not user:
        raise HTTPException(status_code=404,detail="User Not Found")
    return user
    
  
def get_current_active_user(current_user:Annotated[UserDB,Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400,detail="Inactive user")
    return current_user


@router.post("/register",response_model=UserOut)
def create_user(user:UserCreate,session:session_Dep):
    hashed_password=hash_password(user.password)
    user=UserDB(username=user.username,hashed_password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

   
    
def get_current_user(token:Annotated[str,Depends(auth_2)],session:session_Dep)->UserDB:
    credentials_exception=HTTPException(
        status_code=401,detail="Credential could not solve",headers={"WWW.Authenticate":"Bearer"},
    )
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username=payload["sub"]
        if username is None:
            raise credentials_exception
        user=get_user(username,session)
    except JWTError:
        raise HTTPException(status_code=401,detail="Invalid/Expired Token")
    if user is None:
        raise credentials_exception
    return user

def authenticate_user(session:Session,username:str,password:str):
    user=get_user(username,session)
    if not user:
        verifyPassword(password,DUMMY_HASH)
        raise HTTPException(status_code=402,detail="authenticate user")
        return False
    if not verifyPassword(password,user.hashed_password):
        raise HTTPException(status_code=401,detail="authenticate user 2")
        return False
    return user
    
        
def create_access_token(data:dict,expires_delta):
    to_encode=data.copy()
    if expires_delta:
        expire=datetime.now(timezone.utc)+expires_delta
    else:
        expire=datetime.now(timezone.utc)+timedelta(minutes=15)    
    try:
        to_encode.update({"exp":expire})
        encoded_JWT=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    except JWTError:
        raise HTTPException(status_code=401,detail="JWT ERROR")
    return encoded_JWT

@router.post("/token")
def login(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],session:session_Dep)->Token:

    username=form_data.username
    password=form_data.password
    user=authenticate_user(session=session,username=username,password=password)
    if not user:
        raise HTTPException(status_code=401,detail="password and username doesnot match")
    access_token_expires=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token=create_access_token(data={"sub":user.username},expires_delta=access_token_expires)
    return Token(access_token=access_token,token_type="Bearer")

@router.get("/me",response_model=UserOut)
def read_me(current_user:Annotated[UserDB,Depends(get_current_active_user)]):
    return current_user





