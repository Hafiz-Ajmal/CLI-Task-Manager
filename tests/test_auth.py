


def test_create_test(client,session):

    response=client.post("/auth/register",json={ "username":"ajmal","password":"ajmal01"})

    assert response.status_code == 200
    data=response.json()
    assert data["username"]=="ajmal"
    assert "hashed_password" not in data

def test_login(client,session):
     client.post("/auth/register",json={ "username":"ajmal","password":"ajmal01"})

     response=client.post("/auth/token",data={"username":"ajmal","password":"ajmal01"}) #need from_data not json

     assert response.status_code==200
    # data=response.json()
     assert "access_token" in response.json() 


def test_current_user(client,session):
     client.post("/auth/register",json={ "username":"ajmal","password":"ajmal01"})

     login_response=client.post("/auth/token",data={"username":"ajmal","password":"ajmal01"})
     login_data=login_response.json()
     token=login_data["access_token"]
     
     response=client.get("/auth/me",headers={"Authorization":f"Bearer {token}"})


     assert response.status_code == 200
     data=response.json()
     assert data["username"]=="ajmal"
     assert "hashed_password" not in data

