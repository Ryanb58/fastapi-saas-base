import responses
from unittest.mock import patch

from app.tests.conftests import TestBase
from app.models.account import Account, EmailAddress
from app.models.tenant import Tenant
from app.controllers.account import (
    create_token_from_id,
    verify_email_address,
)


class RegisterTestCase(TestBase):
    @patch("app.controllers.account.send_email")
    @responses.activate
    def test_success(self, mock_send_email):
        # Mock out request to stripe.
        responses.add(
            responses.POST,
            "https://api.stripe.com/v1/customers",
            json={"id": 1},
            status=200,
        )

        # Make sure no emails have been sent.
        mock_send_email.assert_not_called()

        payload = {
            "first_name": "Andy",
            "last_name": "Benard",
            "email": "andy.bernard@example.com",
            "password": "password123",
            "name": "Dunder Mifflin Scranton",
            "slug": "dunder-mifflin-scranton",
        }
        response = self.client.post("/auth/register", json=payload)

        # Validate that the registration email was sent.
        mock_send_email.assert_called_once()

        assert response.status_code == 201
        assert self.db_session.query(Account).count() == 1
        assert self.db_session.query(Tenant).count() == 1
        assert self.db_session.query(Tenant).first().accounts.count() == 1

        # Should not be able to login until after they have verified their email.
        payload = {"username": "andy.bernard@example.com", "password": "password123"}
        response = self.client.post("/auth/token", data=payload)
        assert response.status_code == 409

        # Get the signed jwt and try to validate the account.
        email_obj = (
            self.db_session.query(EmailAddress)
            .filter(EmailAddress.email == "andy.bernard@example.com")
            .first()
        )
        token = create_token_from_id(email_obj.id)
        response = self.client.post(
            "/auth/verify?token={}".format(token)
        )
        assert response.status_code == 200

        payload = {"username": "andy.bernard@example.com", "password": "password123"}
        response = self.client.post("/auth/token", data=payload)
        assert response.status_code == 200
