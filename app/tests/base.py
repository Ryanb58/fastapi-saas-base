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
