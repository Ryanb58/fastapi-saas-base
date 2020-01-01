import responses

from app.tests.base import TestBase
from app.models.account import Account
from app.models.tenant import Tenant


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
