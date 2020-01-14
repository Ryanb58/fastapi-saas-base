from app.tests.conftests import TestBase


class AccountsTestCase(TestBase):
    def test_unauth_list(self):
        resp = self.client.get("/accounts")
        assert resp.status_code == 401

    def test_list(self):
        self.create_system_admin()
        resp = self.client.get("/accounts", headers=self.auth_headers())
        assert resp.status_code == 200
