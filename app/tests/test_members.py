import responses
from unittest.mock import patch

from app.tests.base import TestBase
from app.models.account import Account
from app.models.account import EmailAddress
from app.controllers.tenant import create_tenant_and_account

class MembersTestCase(TestBase):

    @patch('app.controllers.account.send_email')
    @responses.activate
    def test_get(self, mock_send_email):
        # Mock out request to stripe.
        responses.add(
            responses.POST,
            "https://api.stripe.com/v1/customers",
            json={"id": 1},
            status=200,
        )

        payload = {
            "first_name": "Andy",
            "last_name": "Benard",
            "email": "andy.bernard@example.com",
            "password": "password123",
            "name": "Dunder Mifflin Scranton",
            "slug": "dunder-mifflin-scranton",
        }
        tenant_obj = create_tenant_and_account(
            self.db_session,
            **payload
        )
        account_obj = tenant_obj.accounts.first().account
        account_obj.is_active = True
        email_obj = account_obj.email_addresses.first()
        email_obj.verified = True
        self.db_session.add(account_obj)
        self.db_session.add(email_obj)
        self.db_session.commit()
        headers = self.auth_headers(email="andy.bernard@example.com")
        response = self.client.get(
            "/members?tenant_id={}".format(tenant_obj.id),
            headers=headers
        )

        assert response.status_code == 200
        assert len(response.json()) == 1

