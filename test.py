# # test.py
# from database import engine, create_db_and_tables
# from sqlmodel import Session
# from models import UserDB
# from routers.auth import hash_password

# create_db_and_tables()

# with Session(engine) as session:
#     user = UserDB(username="test", hashed_password=hash_password("123"), disabled=False)
#     session.add(user)
#     session.commit()
#     session.refresh(user)
#     print(user)