from tests.conftest import get_authenticated_token
from routers.tasks import create_task,TaskCreate



def test_get_category(client,session):
    token=get_authenticated_token(client,"ajmal","123")
    
    
  

    task=client.post(f"/tasks",json={"title":"Tax Payment","description":"for Business"},headers={"Authorization":f"Bearer {token}"})
    task_id=task.json()["id"]
    print(task.json())
    

    assert task.status_code ==200
   
    response=client.post(f"/ai/categorize/{task_id}",headers={"Authorization":f"Bearer {token}"})

    
    data=response.json()
    VALID_CATEGORIES = {"Work", "Personal", "Urgent", "Learning", "Health", "Finance", "Other"}
    assert data["category"]  in VALID_CATEGORIES
    

def test_user_cannot_access_others_task(client,session):

    alice=get_authenticated_token(client,"alice","123")
    bob=get_authenticated_token(client,"bob","123")

    task=client.post(f"/tasks",json={"title":"Tax Payment","description":"for Business"},headers={"Authorization":f"Bearer {alice}"})
    task_dict=task.json()
    task_id=task_dict["id"]
    
    assert task.status_code ==200
   
    response=client.post(f"/ai/categorize/{task_id}",headers={"Authorization":f"Bearer {bob}"})
    data=response.json()
    assert response.status_code == 404
    assert data["detail"] == "Task Not Found"





