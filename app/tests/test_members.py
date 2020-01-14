import responses
from unittest.mock import patch

from app.tests.conftests import TestBase
from app.models.account import Account
from app.models.account import EmailAddress
from app.controllers.tenant import create_tenant_and_account
from app.controllers.account import create_account


class MembersTestCase(TestBase):
    @patch("app.controllers.account.send_email")
    @responses.activate
    def test_get(self, mock_send_email):
        # Mock out request to stripe.
        responses.add(
            responses.POST,
            "https://api.stripe.com/v1/customers",
            json={"id": 1},
            status=200,
        )

        tenant_account = {
            "first_name": "Andy",
            "last_name": "Benard",
            "email": "andy.bernard@example.com",
            "password": "password123",
            "name": "Dunder Mifflin Scranton",
            "slug": "dunder-mifflin-scranton",
            "is_active": True,
            "is_verified": True,
        }
        tenant_obj = create_tenant_and_account(self.db_session, **tenant_account)

        headers = self.auth_headers(email=tenant_account.get("email"))
        response = self.client.get(
            "/members?tenant_id={}".format(tenant_obj.id), headers=headers
        )

        assert response.status_code == 200
        assert len(response.json()) == 1

    @responses.activate
    def test_add_existing_account_as_member(self):
        # Mock out request to stripe.
        responses.add(
            responses.POST,
            "https://api.stripe.com/v1/customers",
            json={"id": 1},
            status=200,
        )

        # Create the account that will join the tenant.
        account_obj = create_account(
            self.db_session,
            first_name="Jim",
            last_name="Halpert",
            email="jim.halpert@example.com",
            password="password123",
            is_active=True,
            is_verified=True,
            send_registration_email=False,
        )

        # Setup tenant and admin account.
        tenant_account = {
            "first_name": "Andy",
            "last_name": "Benard",
            "email": "andy.bernard@example.com",
            "password": "password123",
            "name": "Dunder Mifflin Scranton",
            "slug": "dunder-mifflin-scranton",
            "is_active": True,
            "is_verified": True,
            "do_send_emails": False
        }
        tenant_obj = create_tenant_and_account(self.db_session, **tenant_account)

        # Add member
        payload = {
            "tenant_id": tenant_obj.id,
            "email": "jim.halpert@example.com",
        }
        headers = self.auth_headers(email=tenant_account.get("email"))
        response = self.client.post("/members", json=payload, headers=headers)
        assert response.status_code == 201

        headers = self.auth_headers(email=tenant_account.get("email"))
        response = self.client.get(
            "/members?tenant_id={}".format(tenant_obj.id), headers=headers
        )
        assert response.status_code == 200
        assert len(response.json()) == 2

    # @patch("app.controllers.account.send_email")
    # @responses.activate
    # def test_add_new_account_as_member(self, mock_send_email):
    #     # Mock out request to stripe.
    #     responses.add(
    #         responses.POST,
    #         "https://api.stripe.com/v1/customers",
    #         json={"id": 1},
    #         status=200,
    #     )

    #     # Setup tenant and admin account.
    #     tenant_account = {
    #         "first_name": "Andy",
    #         "last_name": "Benard",
    #         "email": "andy.bernard@example.com",
    #         "password": "password123",
    #         "name": "Dunder Mifflin Scranton",
    #         "slug": "dunder-mifflin-scranton",
    #         "is_active": True,
    #         "is_verified": True,
    #     }
    #     tenant_obj = create_tenant_and_account(self.db_session, **tenant_account)

    #     # Add member
    #     payload = {
    #         "tenant_id": tenant_obj.id,
    #         "email": "jim.halpert@example.com",
    #     }
    #     headers = self.auth_headers(email=tenant_account.get("email"))
    #     response = self.client.post("/members", json=payload, headers=headers)
    #     assert response.status_code == 201

    #     headers = self.auth_headers(email=tenant_account.get("email"))
    #     response = self.client.get(
    #         "/members?tenant_id={}".format(tenant_obj.id), headers=headers
    #     )
    #     assert response.status_code == 200
    #     assert len(response.json()) == 2
