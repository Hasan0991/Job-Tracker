class TestCompany:
    def test_user_can_create_company(self, client, user_token_headers):
        payload = {
            "name": "Hasan Industries",
            "description": "software",
            "website": "stark.com"
        }
        response = client.post("/companies", json=payload, headers=user_token_headers)
        assert response.status_code == 201
        assert response.json()["name"] == "Hasan Industries"

    def test_user_can_not_create_same_company(self, client, user_token_headers):
        payload = {
            "name": "Stark Industries",
            "description": "software",
            "website": "stark.com"
        }
        response = client.post("/companies", json=payload, headers=user_token_headers)
        assert response.status_code == 400
        assert response.json()["detail"] == "Company already exists"

    def test_admin_can_not_create_same_company(self, client, admin_token_headers):
        payload = {
            "name": "Stark Industries",
            "description": "software",
            "website": "stark.com"
        }
        response = client.post("/companies", json=payload, headers=admin_token_headers)
        assert response.status_code == 400
        assert response.json()["detail"] == "Company already exists"

    def test_user_can_get_company_by_id(self, client, user_token_headers):
        response = client.get("/companies/1", headers=user_token_headers)
        assert response.status_code == 200
        assert response.json()["name"] == "Stark Industries"

    def test_user_can_not_get_nonexistent_company(self, client, user_token_headers):
        response = client.get("/companies/2", headers=user_token_headers)
        assert response.status_code == 404
        assert response.json()["detail"] == "No such a company"

    def test_user_can_get_all_companies(self, client, user_token_headers):
        response = client.get("/companies/", headers=user_token_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_user_can_update_company_data(self, client, user_token_headers):
        payload = {
            "description": "software",
            "website": "stark.com"
        }
        response = client.put("/companies/1", json=payload, headers=user_token_headers)
        assert response.status_code == 200
        assert response.json()["website"] == "stark.com"

    def test_user_can_not_update_other_company(self, client, user_token_headers, admin_token_headers):
        payload = {
            "name": "Hasan Industries",
            "description": "software",
            "website": "stark.com"
        }
        create_response = client.post("/companies", json=payload, headers=admin_token_headers)
        assert create_response.status_code == 201
        company_id = create_response.json()["id"]

        updated_payload = {
            "description": "robot",
            "website": "stark.com"
        }
        response = client.put(f"/companies/{company_id}", json=updated_payload, headers=user_token_headers)
        assert response.status_code == 403
        assert response.json()["detail"] == "Not authenticated to update this Company"

    def test_admin_can_update_company(self, client, admin_token_headers):
        updated_payload = {
            "description": "robot",
            "website": "stark.com"
        }
        response = client.put("/companies/1", json=updated_payload, headers=admin_token_headers)
        assert response.status_code == 200
        assert response.json()["description"] == "robot"

    def test_admin_can_delete_company(self, client, admin_token_headers):
        response = client.delete("/companies/1", headers=admin_token_headers)
        assert response.status_code == 200
        assert response.json()["details"] == "company deleted"

    def test_user_can_not_delete_company(self, client, user_token_headers, admin_token_headers):
        payload = {
            "name": "Hasan Industries",
            "description": "software",
            "website": "stark.com"
        }
        create_response = client.post("/companies", json=payload, headers=admin_token_headers)
        assert create_response.status_code == 201
        company_id = create_response.json()["id"]

        response = client.delete(f"/companies/{company_id}", headers=user_token_headers)
        assert response.status_code == 403
        assert response.json()["detail"] == "Not authenticated to delete this Company"

    def test_check_company_requires_name(self, client, user_token_headers):
        payload = {
            "description": "software",
            "website": "stark.com"
        }
        response = client.post("/companies", json=payload, headers=user_token_headers)
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "Field required"
