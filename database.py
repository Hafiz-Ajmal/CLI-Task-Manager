
#rom fastapi import 
from sqlmodel import Session,create_engine,SQLModel,select,Field
from datetime import  datetime
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL=os.getenv("DATABASE_URL","sqlite:///./test.db") #for Github

engine = create_engine(DB_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)











    
    
    