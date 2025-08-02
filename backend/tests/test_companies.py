def test_user_can_create_company(client,user_token_headers):
    payload={    
        "name": "Stark Industries",
        "description": "software",
        "website": "stark.com"
    }
    response=client.post("/companies",json=payload,headers=user_token_headers)
    assert response.status_code==201
    assert response.json()["name"]=="Start Industries"