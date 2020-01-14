from unittest.mock import patch

from app.tests.conftests import TestBase
from app.models.account import Account
from app.models.account import EmailAddress
from app.controllers.account import create_email_address
from app.controllers.account import create_token_from_id

class EmailAddressTestCase(TestBase):
    @patch("app.controllers.account.send_email")
    def test_create(self, mock_send_email):
        self.create_system_admin()
        assert self.db_session.query(EmailAddress).count() == 1
        payload = {"email": "another@example.com"}
        response = self.client.post(
            "/email_addresses", json=payload, headers=self.auth_headers()
        )
        assert response.status_code == 201
        assert self.db_session.query(EmailAddress).count() == 2
        # Adding a new email address should send a verification email.
        mock_send_email.assert_called_once()

    def test_get(self):
        self.create_system_admin()
        payload = {"email": "another@example.com"}
        response = self.client.get(
            "/email_addresses", json=payload, headers=self.auth_headers()
        )
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_verify(self):
        admin_obj = self.create_system_admin()

        # Add new unverified email address to user.
        email_obj = create_email_address(
            self.db_session, 
            "michael.scott@gmail.com", 
            admin_obj.id, 
            send_verification_email=False)

        token = create_token_from_id(email_obj.id)
        response = self.client.post(
            "/email_addresses/verify?token={}".format(token)
        )
        assert response.status_code == 200
