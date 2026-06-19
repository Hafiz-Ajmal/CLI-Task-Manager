from fastapi import FastAPI ,Query,Path,HTTPException,Depends
from typing import Annotated 
from datetime import datetime ,timedelta
from pydantic import BaseModel ,Field 
from routers import tasks,auth ,ai_tasks
from contextlib import asynccontextmanager 
from database import create_db_and_tables



@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db_and_tables()
    yield

app=FastAPI(lifespan=lifespan)
app.include_router(tasks.router)

app.include_router(auth.router) 
app.include_router(ai_tasks.router) 












