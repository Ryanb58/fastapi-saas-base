from unittest import TestCase

from starlette.testclient import TestClient

from app.main import app
from app.database import engine, Base, DBSession


class TestBase(TestCase):
    def setUp(self):
        self.db_session = DBSession()
        self.connection = engine.connect()

        # # Configure Search DDL triggers.
        Base.metadata.drop_all(self.connection)
        Base.metadata.create_all(self.connection)

        # TODO: Create admin.
        self.client = TestClient(app)

    def tearDown(self):
        self.db_session.rollback()
        self.db_session.close()

    def create_system_admin(self, *args, **kwargs):
        from app.controllers.account import create_account
        from app.schemas.account import AccountCreate

        return create_account(
            self.db_session,
            first_name="Admin",
            last_name="Istrator",
            email="admin@example.com",
            password="password123",
            is_system_admin=True,
            is_active=True,
            send_registration_email=False
        )

    def auth_headers(self, email="admin@example.com", password="password123"):
        payload = {"username": email, "password": password}
        resp = self.client.post("/auth/token", data=payload)
        return {"Authorization": "Bearer " + resp.json().get("access_token")}
