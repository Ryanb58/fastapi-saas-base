from unittest.mock import patch

from app.tests.base import TestBase
from app.models.account import Account
from app.models.account import EmailAddress


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
