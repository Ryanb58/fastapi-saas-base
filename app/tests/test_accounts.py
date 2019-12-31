from app.tests.base import TestBase


class AccountsTestCase(TestBase):

    def test_unauth_list(self):
        response = self.client.get("/accounts")
        assert response.status_code == 401

    def test_list(self):
        self.create_system_admin()
        response = self.client.get("/accounts", headers=self.auth_headers())
        assert response.status_code == 200
