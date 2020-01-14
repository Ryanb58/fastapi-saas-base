from app.tests.conftests import TestBase
from app.models.account import Account


class LoginTestCase(TestBase):
    def test_success(self):
        self.create_system_admin()
        payload = {"username": "admin@example.com", "password": "password123"}
        response = self.client.post("/auth/token", data=payload)
        assert response.status_code == 200
        assert response.json().get("access_token", False)
        assert response.json().get("token_type", False) == "bearer"

    def test_invalid(self):
        self.create_system_admin()
        payload = {"username": "admin@example.com", "password": "password"}
        response = self.client.post("/auth/token", data=payload)
        assert response.status_code == 401
