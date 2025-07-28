def test_register_user(client):
    payload={
        "email":"testuser@example.com",
        "password":"testpassword"
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "testuser@example.com"
    assert "id" in data

def test_login_user(client):
    response=client.post("/auth/login",
        data={
            "username":"testuser@example.com",
            "password":"testpassword"
        })
    assert response.status_code==200
    assert "access_token" in response.json()
    assert response.json()["token_type"]=="bearer"

def test_incorrect_login_user(client):
    response=client.post("/auth/login",
        data={
            "username":"testuser@example.com",
            "password":"testpassword1"
        })
    assert response.status_code==401
    assert "access_token" not in response.json()

def test_incorrect_register_user(client):
    payload={
        "email":"test1@user.com"
    }
    response=client.post("/auth/register",json=payload)
    assert response.status_code==422

def test_admin_can_create_user(client):
  
    login_data = {
        "username": "admin@example.com",
        "password": "adminpass"
    }
    login_response = client.post("/auth/login", data=login_data)
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "email": "testuser2@example.com",
        "password": "testpass123",
        "role": "user"
    }
    response = client.post("/users/", json=payload, headers=headers)
    assert response.status_code == 201
    assert response.json()["email"] == payload["email"]

def test_admin_can_create_user(client):
    login_data={
        "username": "admin@example.com",
        "password": "adminpass"
    }
    login_response=client.post("/auth/login",data=login_data)
    assert login_response.status_code==200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "email": "testuser2@example.com",
        "password": "testpass123",
        "role": "user"
    }
    response = client.post("/users/", json=payload, headers=headers)
    assert response.status_code ==  400 
    assert response.json()["detail"] =="Email already exists"