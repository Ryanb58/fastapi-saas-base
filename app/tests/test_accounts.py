from app.tests.base import TestBase


class AccountsTestCase(TestBase):
    def test_unauth_list(self):
        resp = self.client.get("/accounts")
        assert resp.status_code == 401

    def test_list(self):
        self.create_system_admin()
        resp = self.client.get("/accounts", headers=self.auth_headers())
        assert resp.status_code == 200


class AccountEmailAddressTestCase(TestBase):
    def test_list_email_addresses(self):
        self.create_system_admin()
        resp = self.client.get("/email_addresses", headers=self.auth_headers())
        assert resp.status_code == 200
        assert len(resp.json()) == 1

    def test_add_email(self):
        admin = self.create_system_admin()
        resp = self.client.post(
            "/email_addresses",
            json={"email": "admin2@gmail.com", "account_id": admin.id},
            headers=self.auth_headers(),
        )
        assert resp.status_code == 201

        resp = self.client.get("/email_addresses", headers=self.auth_headers())
        assert resp.status_code == 200
        assert len(resp.json()) == 2
