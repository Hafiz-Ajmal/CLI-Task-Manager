import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fastapi import FastAPI,Path,Depends,APIRouter,Query,HTTPException
from typing import Annotated
from datetime import datetime ,timedelta , timezone

from fastapi.security import OAuth2AuthorizationCodeBearer,OAuth2PasswordRequestForm,OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt
from jose.exceptions import JWTError


from routers.auth import get_current_user
from routers.auth import SECRET_KEY,ALGORITHM,ACCESS_TOKEN_EXPIRE_MINUTES
from database import engine

from dependencies import session_Dep
#from database import TaskPublic,TaskDB,TaskCreate,TaskUpdate
from sqlmodel import Session ,select
from models import TaskBase,TaskCreate,TaskDB,TaskPublic,TaskUpdate,Token,TokenData
from models import User,UserUpdate,UserCreate,UserDB,UserOut






router=APIRouter(prefix="/tasks",tags=["tasks"])

global_id:int =1


@router.get("",response_model=list[TaskPublic])  #tasks is just list but of which
def get_all_tasks(current_user: Annotated[str, Depends(get_current_user)],session:session_Dep):
    tasks = session.exec(select(TaskDB)).all()
    if len(tasks)<1:
        return []
    return tasks

@router.get("/{task_id}")
def get_by_id(task_id:int,current_user: Annotated[str, Depends(get_current_user)],session:session_Dep):
    task=session.get(TaskDB,task_id)
    return task
    

@router.post("",response_model=TaskPublic)
def create_task(task:TaskCreate,session:session_Dep,current_user: Annotated[str, Depends(get_current_user)]):
    new_task=TaskDB.model_validate(task)
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task

@router.put("/{task_id}",response_model=TaskPublic)
def update_task(task_id:int,newTask:TaskUpdate,session:session_Dep,current_user: Annotated[str, Depends(get_current_user)]):
        task=session.get(TaskDB,task_id)
        if not task:
            raise HTTPException(status_code=404,detail="Task Not Found")
        input_task=newTask.model_dump(exclude_unset=True)
        input_task["updated_at"] = datetime.now()
        task.sqlmodel_update(input_task)   
        session.add(task)
        session.commit()
        session.refresh(task)
        return task


#task.id and tasks[id] can be differ
@router.delete("/{task_id}")
def delete_task_by_id(task_id:Annotated[int,Path(ge=1)],session:session_Dep ,current_user: Annotated[str, Depends(get_current_user)]):
    task=session.get(TaskDB,task_id)
    if not task:
        raise HTTPException(status_code=404,detail="Task Not Found")   
    session.delete(task)
    session.commit()
    return {"Deleted":task}

   


#Security
