
from tests.conftest import get_authenticated_token
from sqlmodel import select
from models import TaskDB

def test_user_cannot_access_others_task(client,session):

    alice=get_authenticated_token(client,"alice","pw1")
    bob=get_authenticated_token(client,"bob","pw2")

    response_1=client.post("/tasks", json={"title":"Game"},headers={"Authorization":f"Bearer {alice}"})

    

    assert response_1.status_code == 200
    task_dict=response_1.json()
    id=task_dict["id"]

    
    response_2=client.get(f"/tasks/{id}",headers={"Authorization":f"Bearer {bob}"})
    
    
    assert response_2.status_code == 404
    assert response_2.json()["detail"] == "Task not found"

    
def test_user_cannot_update_others_task(client,session):

    alice=get_authenticated_token(client,"alice","pw1")
    bob=get_authenticated_token(client,"bob","pw2")
    
    response_1=client.post("/tasks", json={"title":"Game"},headers={"Authorization":f"Bearer {alice}"})

    assert response_1.status_code==200

    task_dict=response_1.json()
    id=task_dict["id"]

    response=client.put(f"/tasks/{id}",json={"title":"Work"},headers={"Authorization":f"Bearer {bob}"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_user_cannot_delete_others_task(client,session):
    alice=get_authenticated_token(client,"alice","pw1")
    bob=get_authenticated_token(client,"bob","pw2")
    
    response_1=client.post("/tasks", json={"title":"Game"},headers={"Authorization":f"Bearer {alice}"})

    assert response_1.status_code==200

    task_dict=response_1.json()
    id=task_dict["id"]

    response=client.delete(f"/tasks/{id}",headers={"Authorization":f"Bearer {bob}"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"

def test_user_only_sees_own_tasks_in_list(client,session):
    alice=get_authenticated_token(client,"alice","pw1")
    bob=get_authenticated_token(client,"bob","pw2")
    
    alice_task=client.post("/tasks", json={"title":"Game"},headers={"Authorization":f"Bearer {alice}"})
    bob_task=client.post("/tasks", json={"title":"Game Over"},headers={"Authorization":f"Bearer {bob}"})

    alice_response=client.get(f"/tasks",headers={"Authorization":f"Bearer {alice}"})
    bob_response=client.get(f"/tasks",headers={"Authorization":f"Bearer {bob}"})

    assert alice_response.status_code==200
    alice_dict=alice_response.json()
    assert len(alice_dict) ==1
    assert alice_dict[0]["id"]==alice_task.json()["id"]
    assert alice_dict[0]["owner_id"]==alice_task.json()["owner_id"]

    assert bob_response.status_code==200
    bob_dict=bob_response.json()
    assert len(bob_dict) ==1
    assert bob_dict[0]["id"]==bob_task.json()["id"]

   
    




