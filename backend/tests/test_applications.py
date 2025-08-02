def test_user_create_application(client,user_token_headers):
    payload={  
        "job_id": 2,
        "cover_letter": "something for now"
    }
    response=client.post("/applications/",json=payload,headers=user_token_headers)
    assert response.status_code==201
    assert response.json()["cover_letter"]=="something for now"



def test_user_can_not_post_application(client,user_token_headers):#job_id is null
    payload={  
        "cover_letter": "something for now"
    }
    response=client.post("/applications/",json=payload,headers=user_token_headers)
    assert response.status_code==422
    assert response.json()["detail"][0]["msg"]=="Field required"



def test_user_can_get_all_application(client,user_token_headers):
    response=client.get("/applications/",headers=user_token_headers)
    assert response.status_code==200
    assert isinstance(response.json(),list)



def test_user_can_not_get_his_applications(client,admin_token_headers):#no applications
    response=client.get("/applications/me",headers=admin_token_headers)
    assert response.status_code==404
    assert response.json()["detail"]== "User does not have any job applications"



def test_user_can_get_his_applications(client,user_token_headers):   
    response=client.get("/applications/me",headers=user_token_headers)
    assert response.status_code==200
    assert response.json()[0]["cover_letter"]== "something for now"



def test_user_can_update_application(client,user_token_headers):
    udpated_payload={
        "cover_letter":"the latest announce"
    }
    response=client.put("/applications/1",json=udpated_payload,headers=user_token_headers)
    assert response.status_code==200
    assert response.json()["cover_letter"]=="the latest announce"

def test_user_can_not_update_application(client,admin_token_headers,user_token_headers):#restriction for other users
    payload={  
        "job_id": 2,
        "cover_letter": "one more time"
    }

    response=client.post("/applications/",json=payload,headers=admin_token_headers)
    assert response.status_code==201
    assert response.json()["cover_letter"]=="one more time"
    application_id=response.json()["id"]
    print("App created:", response.json()) 
    updated_payload={
        "cover_letter":"the latest announce"
    }
    response=client.put(f"/applications/{application_id}",json=updated_payload,headers=user_token_headers)
    assert response.status_code==403
    assert response.json()["detail"]=="Not authenticated to update this application"



def test_admin_can_update_application(client,admin_token_headers):
    updated_payload={
        "cover_letter":"the latest announce updated by admin"
    }
    response=client.put("/applications/1",json=updated_payload,headers=admin_token_headers)
    assert response.status_code==200
    assert response.json()["cover_letter"]=="the latest announce updated by admin"
