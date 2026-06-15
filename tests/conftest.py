
import pytest 
from sqlmodel import select,create_engine,SQLModel,Session
from fastapi.testclient import TestClient
from main import app
from dependencies import get_session
from sqlalchemy.pool import StaticPool


TEST_DB_URL="sqlite://"
engine=create_engine(TEST_DB_URL,connect_args={"check_same_thread":False},poolclass=StaticPool)

def get_session_override():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session]=get_session_override

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)    

@pytest.fixture(name="client")
def client_fixture():
    client=TestClient(app)
    yield client

