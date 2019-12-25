from unittest import TestCase

from starlette.testclient import TestClient

from app.main import app
from app.database import engine, Base, SessionLocal


class TestBase(TestCase):
    def setUp(self):
        self.db_session = SessionLocal()
        # Configure Search DDL triggers.
        Base.metadata.create_all(bind=engine)
        # TODO: Create admin.
        self.client = TestClient(app)

    def tearDown(self):
        self.db_session.remove()
        Base.metadata.create_all(bind=engine)

    def create_system_admin(self, *args, **kwargs):
        from app.controllers.account import create_account
        from app.schemas.account import AccountCreate

        return create_account(self.db_session, AccountCreate(
            first_name = "Admin",
            last_name = "Istrator",
            is_system_admin = True,
            email = "admin@example.com",
            password = "password123"
        ))

    def auth_headers(self, email="admin@example.com", password="password123"):
        resp = self.client.post(
            "/auth/token", json={"email": email, "password": password}
        )
        return {"Authorization": "Bearer " + resp.json.get("access_token")}
