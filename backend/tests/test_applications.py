class TestApplication:

    def test_user_create_application(self, client, user_token_headers):
        payload = {
            "job_id": 2,
            "cover_letter": "something for now"
        }
        response = client.post("/applications/", json=payload, headers=user_token_headers)
        assert response.status_code == 201
        assert response.json()["cover_letter"] == "something for now"

    def test_user_can_not_post_application(self, client, user_token_headers):
        payload = {
            "cover_letter": "something for now"
        }
        response = client.post("/applications/", json=payload, headers=user_token_headers)
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "Field required"

    def test_user_can_get_all_application(self, client, user_token_headers):
        response = client.get("/applications/", headers=user_token_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_user_can_not_get_his_applications(self, client, admin_token_headers):
        response = client.get("/applications/me", headers=admin_token_headers)
        assert response.status_code == 404
        assert response.json()["detail"] == "User does not have any job applications"

    def test_user_can_get_his_applications(self, client, user_token_headers):
        response = client.get("/applications/me", headers=user_token_headers)
        assert response.status_code == 200
        assert response.json()[0]["cover_letter"] == "something for now"

    def test_user_can_update_application(self, client, user_token_headers):
        updated_payload = {
            "cover_letter": "the latest announce"
        }
        response = client.put("/applications/1", json=updated_payload, headers=user_token_headers)
        assert response.status_code == 200
        assert response.json()["cover_letter"] == "the latest announce"

    def test_user_can_not_update_application(self, client, admin_token_headers, user_token_headers):
        payload = {
            "job_id": 2,
            "cover_letter": "one more time"
        }
        response = client.post("/applications/", json=payload, headers=admin_token_headers)
        assert response.status_code == 201
        application_id = response.json()["id"]

        updated_payload = {
            "cover_letter": "the latest announce"
        }
        response = client.put(f"/applications/{application_id}", json=updated_payload, headers=user_token_headers)
        assert response.status_code == 403
        assert response.json()["detail"] == "Not authenticated to update this application"

    def test_admin_can_update_application(self, client, admin_token_headers):
        updated_payload = {
            "cover_letter": "the latest announce updated by admin"
        }
        response = client.put("/applications/1", json=updated_payload, headers=admin_token_headers)
        assert response.status_code == 200
        assert response.json()["cover_letter"] == "the latest announce updated by admin"

    def test_admin_can_delete_application(self, client, admin_token_headers):
        response = client.delete("/applications/1", headers=admin_token_headers)
        assert response.status_code == 200
        assert response.json()["details"] == "application deleted"

    def test_user_can_not_delete_application(self, client, user_token_headers, admin_token_headers):
        payload = {
            "job_id": 2,
            "cover_letter": "one more time"
        }
        response = client.post("/applications/", json=payload, headers=admin_token_headers)
        assert response.status_code == 201
        application_id = response.json()["id"]

        response = client.delete(f"/applications/{application_id}", headers=user_token_headers)
        assert response.status_code == 403
        assert response.json()["detail"] == "Not authenticated to delete this application"

    def test_user_can_delete_application(self, client, user_token_headers):
        response = client.delete("/applications/1", headers=user_token_headers)
        assert response.status_code == 200
        assert response.json()["details"] == "application deleted"
