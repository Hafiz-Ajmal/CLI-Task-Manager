
#rom fastapi import 
from sqlmodel import Session,create_engine,SQLModel,select,Field
from datetime import  datetime
import os

DB_URL=os.getenv("DATABASE_URL")

engine = create_engine(DB_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)











    
    
    