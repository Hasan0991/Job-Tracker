class TestJob:

    def test_user_post_job(self, client, user_token_headers):
        payload = {
            "title": "Frontend Engineer",
            "url": "something1.com"
        }
        response = client.post("/jobs/", json=payload, headers=user_token_headers)
        assert response.status_code == 201
        assert response.json()["title"] == "Frontend Engineer"

    def test_create_job_without_title(self, client, user_token_headers):
        payload = {"url": "example.com"}
        response = client.post("/jobs/", json=payload, headers=user_token_headers)
        assert response.status_code == 422
        assert response.json()["detail"][0]["msg"] == "Field required"

    def test_user_can_not_post_job(self, client, user_token_headers):
        payload = {
            "company_id": 2,
            "title": "Backend Engineer",
            "url": "something.com"
        }
        response = client.post("/jobs/", json=payload, headers=user_token_headers)
        assert response.status_code == 404
        assert response.json()["detail"] == "No such company"

    def test_user_can_not_post_same_job(self, client, user_token_headers):
        payload = {
            "title": "Backend Engineer",
            "url": "something.com"
        }
        response = client.post("/jobs/", json=payload, headers=user_token_headers)
        assert response.status_code == 403
        assert response.json()["detail"] == "You can not create same post"

    def test_user_can_get_all_jobs(self, client, user_token_headers):
        response = client.get("/jobs/", headers=user_token_headers)
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_user_can_not_get_job_by_id(self, client, user_token_headers):
        response = client.get("/jobs/12", headers=user_token_headers)
        assert response.status_code == 404
        assert response.json()["detail"] == "Job not found"

    def test_user_can_get_job_by_id(self, client, user_token_headers):
        response = client.get("/jobs/1", headers=user_token_headers)
        assert response.status_code == 200
        assert response.json()["title"] == "Backend Engineer"

    def test_user_can_not_update_job(self, client, user_token_headers):
        payload = {
            "url": "someurl.com"
        }
        response = client.put("/jobs/2", json=payload, headers=user_token_headers)
        assert response.status_code == 403
        assert response.json()["detail"] == "Not authorized to update this job"

    def test_user_can_update_his_job(self, client, user_token_headers):
        payload = {
            "url": "someurl.com"
        }
        response = client.put("/jobs/1", json=payload, headers=user_token_headers)
        assert response.status_code == 200
        assert response.json()["url"] == "someurl.com"

    def test_admin_can_update_job(self, client, admin_token_headers):
        payload = {
            "url": "someurl.com"
        }
        response = client.put("/jobs/2", json=payload, headers=admin_token_headers)
        assert response.status_code == 200
        assert response.json()["url"] == "someurl.com"

    def test_admin_can_delete_job(self, client, admin_token_headers):
        response = client.delete("/jobs/1", headers=admin_token_headers)
        assert response.status_code == 200
        assert response.json()["details"] == "Job deleted"

    def test_user_can_delete_job(self, client, user_token_headers):
        response = client.delete("/jobs/1", headers=user_token_headers)
        assert response.status_code == 200
        assert response.json()["details"] == "Job deleted"

    def test_user_can_not_delete_job(self, client, user_token_headers):
        response = client.delete("/jobs/2", headers=user_token_headers)
        assert response.status_code == 403
        assert response.json()["detail"] == "Not authorized to delete this job"
