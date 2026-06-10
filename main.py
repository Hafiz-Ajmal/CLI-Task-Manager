from fastapi import FastAPI ,Query,Path,HTTPException,Depends
from typing import Annotated 
from datetime import datetime ,timedelta
from pydantic import BaseModel ,Field 
from routers import tasks,auth
from contextlib import asynccontextmanager 
from database import create_db_and_tables


@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db_and_tables()
    yield

app=FastAPI(lifespan=lifespan)
app.include_router(tasks.router)

app.include_router(auth.router)  





        
# if __name__=="__main__":
#     import uvicorn 
#     uvicorn.run(app,host="127.0.0.1",port=8000)


# def main():
#     while True:
#         print("Click 1 to create Task")
#         print("Click 2 to read all Tasks")
#         print("Click 3 to read specific Task by ID")
#         print("click 4 to update Task")
#         print("Click 5 to delete Task")


#         choice=input("Kindly Pick Your Choice, It should between (1-4): ").strip()
#         if choice:
#             choice=int(choice)
#         else:
#             continue    

#         if choice==1:

#             title=input("Write title for Task: ").strip()
#             desc=input("Write Description: ").strip()
#             obj = Task(id=global_id+1, title=title, description=desc)
#             print(create_task(obj))
#             global_id+=1

#         elif choice==2:

#             print(get_all_tasks())

#         elif choice==3:

#             id=int(input("Enter ID : ").strip())
#             print(get_by_id(id))

#         elif choice==4:

#             id=int(input("Id of task ,You want to Update :").strip())
#             title=input("Please Write Update title : ").strip()
#             desc=input("Please Write Update description :").strip()
#             completed=bool(input("Is Completed or Not [1/0]: "))
#             obj=Task(id=id,title=title,desc=desc,completed=completed)
#             print(update_task(obj,task_by_ID(id)))

#         elif choice==5:

#             id=int(input("Id of task ,You want to delete : ").strip())
#             print(delete_task_by_id(id))
            
#         else:
#             break








