from fastapi import HTTPException,Depends
#from models import Task
from database import engine,Session
from typing import Annotated







def get_session():
    with Session(engine) as session:
        yield session

session_Dep=Annotated[Session,Depends(get_session)]
