



# from fastapi import APIRouter ,Depends,HTTPException
# import google.generativeai as genai
# import os
# from dependencies import  get_session , Session 
# from routers.auth import get_current_user
# from models import UserDB ,TaskDB

# router= APIRouter(prefix="/ai",tags=["AI Features"])
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# model=genai.GenerativeModel("gemini-2.5-flash")


from google import genai
import os
from dotenv import load_dotenv
from fastapi import APIRouter , HTTPException ,Depends
from models import UserDB ,TaskDB
from dependencies import session_Dep 
from routers.auth import get_current_user
from sqlmodel import Session,select


router=APIRouter(prefix="/ai",tags=["AI Feature"])

load_dotenv()




CATEGORY_PROMPT= """
You are a smart task organizer.

Categorize this task into EXACTLY ONE category.

Task Title: {title}
Task Description: {description}

Available categories:
- Work: Job, office, business, meetings, projects, clients, coding, development.
- Personal: Family, friends, home, hobbies, personal errands.
- Urgent: Tasks requiring immediate attention, deadlines, emergencies.
- Learning: Studying, courses, tutorials, reading educational material, practice.
- Health: Exercise, gym, doctor appointments, medicine, diet, fitness.
- Finance: Bills, banking, taxes, payments, budgeting, investments.
- Other: Anything that does not clearly fit the above categories.

Rules:
1. Return exactly one category.
2. Choose the best matching category.
3. Return only the category name.
4. Do not explain your answer.


Category:
"""


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY","dummy-key-for-testing")) #for github



@router.post("/categorize/{task_id}")
def categorize(task_id:int,session:session_Dep,user:UserDB=Depends(get_current_user)):
    task=session.get(TaskDB,task_id)
    if not task:
        raise HTTPException(status_code=404,detail="Task Not Found")
    if task.owner_id != user.id:
        raise HTTPException(status_code=404,detail="Task Not Found")
    category=get_category(task.title,task.description) # what id pass session_DEp instead of session-d --
    return {"category":category}


def get_category(title:str,description:str)->str:

    prompt=CATEGORY_PROMPT.format(title=title,description=description)
    response=client.models.generate_content(model="gemini-2.5-flash",contents=prompt)
    return response.text #why not return response























# @router.post("/Ctegorize/{task_id}")
# def categorize_task(task_id:int,session:Session=Depends(get_session),current_user:UserDB=Depends(get_current_user)):

#     task=session.get(TaskDB,task_id)

#     if not task:
#         raise HTTPException(status_code=401,detail="Task Not Found")
    
#     if (task.owner!=current_user.id): 
#         raise HTTPException(status_code=401,detail="Task Owner is not you")
    
#     category_types=["Urgent","Learning","Personal","Work","Health","Finanace"]

#     prompt=format(title={"title"},description={"description"},user_id={current_user.id})

#     response=model.generate_content(prompt)
#     category=response.text.strip().upper()

#     if category in category_types:
#         return category
#     else :
#         return "other"





