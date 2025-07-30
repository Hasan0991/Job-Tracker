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
            "username":"testuser1@example.com",
            "password":"testpassword1"
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

def test_admin_can_create_user(client,admin_token_headers):

    payload = {
        "email": "testuser2@example.com",
        "password": "testpass123",
        "role": "user"
    }
    response = client.post("/users/", json=payload, headers=admin_token_headers)
    assert response.status_code == 201
    assert response.json()["email"] == payload["email"]

def test_admin_can_create_same_user(client,admin_token_headers):
    payload = {
        "email": "testuser1@example.com",
        "password": "testpass123",
        "role": "user"
    }
    response = client.post("/users/", json=payload, headers=admin_token_headers)
    assert response.status_code ==  400 
    assert response.json()["detail"] =="Email already exists"

def test_create_user_empty_password(client, admin_token_headers):
    payload = {
        "email": "empty@example.com",
        "password": "",  
        "role": "user"
    }
    response = client.post("/users/", json=payload, headers=admin_token_headers)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "String should have at least 8 characters"


def test_user_auth_wrong_email(client,admin_token_headers):
  

    payload = {
        "email": "testuser2@example",# without .com
        "password": "testpass123", 
        "role": "user"
    }
    response = client.post("/users/", json=payload, headers=admin_token_headers)
    assert response.status_code ==  422 
    assert response.json()["detail"][0]["msg"] =="value is not a valid email address: The part after the @-sign is not valid. It should have a period."

def test_user_post_user(client,user_token_headers):
    payload = {
        "email": "testuser3@example.com",
        "password": "testpass123", 
        "role": "user"
    }
    response = client.post("/users/", json=payload, headers=user_token_headers)
    assert response.status_code ==  403
    assert response.json()["detail"]=="Not authorized to create this user"

def test_create_user_short_password(client,admin_token_headers):
    payload = {
            "email": "testuser4@example.com",
            "password": "123", 
            "role": "user"
        }
    response=client.post("/auth/register",json=payload,headers=admin_token_headers)
    assert response.status_code==422
    assert "String should have at least 8 characters" in response.json()["detail"][0]["msg"]

def test_admin_get_users(client,admin_token_headers):

    response = client.get("/users/",headers=admin_token_headers)
    assert response.status_code==200
    assert isinstance(response.json(),list)

def test_admin_get_user_by_id(client,admin_token_headers):
    response=client.get("/users/1",headers=admin_token_headers)
    assert response.status_code==200
    assert response.json()["email"]=="testuser1@example.com"

def test_user_get_user_by_id(client,user_token_headers):
    response=client.get("/users/2",headers=user_token_headers)
    assert response.status_code==403
    assert response.json()["detail"]=="Not authorized to view this user"

def test_user_get_own_info(client,user_token_headers):
    response=client.get("/users/users/me",headers=user_token_headers)
    assert response.status_code==200
    assert response.json()["email"]=="testuser1@example.com"

def test_user_get_own_info_without_auth(client,user_token_headers):
    response=client.get("/users/users/me")
    assert response.status_code==401
    assert response.json()["detail"]=="Not authenticated"

def test_admin_can_update_user(client, admin_token_headers):
    payload = {
        "first_name": "Updated",
        "last_name": "User"
    }
    response = client.put("/users/1", json=payload, headers=admin_token_headers)
    assert response.status_code == 200
    assert response.json()["first_name"] == "Updated"

def test_user_cannot_update_user(client, user_token_headers):
    payload = {
        "first_name": "Not Updated",
        "last_name": "User"
    }
    response = client.put("/users/2", json=payload, headers=user_token_headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized to update this user"

def test_admin_can_delete_user(client,admin_token_headers):
    response = client.delete("/users/1", headers=admin_token_headers)
    assert response.status_code == 200
    assert response.json()["details"] == "user deleted"

def test_user_cannot_delete_user(client,user_token_headers):
    response = client.delete("/users/2", headers=user_token_headers)
    assert response.status_code == 403
    assert response.json()["detail"] == "Not authorized to delete this user"


def test_user_can_delete_himself(client,user_token_headers):
    response = client.delete("/users/1", headers=user_token_headers)
    assert response.status_code == 200
    assert response.json()["details"] == "user deleted"
