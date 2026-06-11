
#rom fastapi import 
from sqlmodel import Session,create_engine,SQLModel,select,Field
from datetime import  datetime






engine = create_engine("postgresql://ajmal:ajmal01@localhost/taskmanager")

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)











    
    
    