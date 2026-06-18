
from tests.conftest import get_authenticated_token
from routers.tasks import create_task,TaskCreate

def test_get_category(client,session):
    token=get_authenticated_token(client,"ajmal","123")
    task_create=TaskCreate(title="Tax Payment",description="for Business")


    task=client.post(f"/tasks",json={"title":"Tax Payment","description":"for Business"},headers={"Authorization":f"Bearer {token}"})
    task_id=task.json()["id"]
    response=client.post(f"/categorize/{task.id}",headers={"Authorization":f"Bearer {token}"})
    
    assert response.status_code ==200
    data=response.json()
    assert data["category"] == "Finance"
    