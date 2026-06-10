
#rom fastapi import 
from sqlmodel import Session,create_engine,SQLModel,select,Field
from datetime import  datetime


sqlite_file_name="database.db"
sqlite_file_url=f"sqlite:///{sqlite_file_name}"

connect_args={"check_same_thread":False}
engine=create_engine(sqlite_file_url,connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)










    
    
    