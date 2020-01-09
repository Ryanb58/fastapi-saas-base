import responses

from app.tests.base import TestBase
from app.models.account import Account, EmailAddress
from app.models.tenant import Tenant
from app.controllers.account import create_email_verification_token, verify_email_address

class RegisterTestCase(TestBase):
    @responses.activate
    def test_success(self):
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
        response = self.client.post("/auth/register", json=payload)

        assert response.status_code == 201
        assert self.db_session.query(Account).count() == 1
        assert self.db_session.query(Tenant).count() == 1
        assert self.db_session.query(Tenant).first().accounts.count() == 1

        # Should not be able to login until after they have verified their email.
        payload = {"username": "andy.bernard@example.com", "password": "password123"}
        response = self.client.post("/auth/token", data=payload)
        assert response.status_code == 409

        #TODO: Get the signed jwt and try to validate the account.
        email_obj = self.db_session.query(EmailAddress).filter(
            EmailAddress.email == "andy.bernard@example.com"
        ).first()
        token = create_email_verification_token(email_obj)
        response = self.client.post("/email_addresses/verify?token={}".format(token), data=payload)
        assert response.status_code == 200

        payload = {"username": "andy.bernard@example.com", "password": "password123"}
        response = self.client.post("/auth/token", data=payload)
        assert response.status_code == 200


    # def test_duplicate(self):
    #     payload = {
    #         'first_name': 'Andy',
    #         'last_name': 'Benard',
    #         'username': 'andy.bernard@example.com',
    #         'password': 'password123',
    #         'tenant_name': 'Dunder Mifflin Scranton'
    #     }
    #     response = self.client.post("/auth/register", data=payload)
    #     assert response.status_code == 401
