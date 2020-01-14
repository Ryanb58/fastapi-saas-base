# From @euri10 -- https://gitter.im/tiangolo/fastapi?at=5cd915ed56271260f95275ac

import asyncio
from unittest import TestCase

import pytest
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists, drop_database

from starlette.config import environ
from starlette.testclient import TestClient

# This sets `os.environ`, but provides some additional protection.
# If we placed it below the application import, it would raise an error
# informing us that 'TESTING' had already been read from the environment.

environ["TESTING"] = "True"
environ["EMAILS_ENABLED"] = "False"

from app.main import app  # isort:skip
from app.database import engine, Base, DBSession


class TestBase(TestCase):
    def setUp(self):
        self.db_session = DBSession()
        self.connection = engine.connect()

        # # Configure Search DDL triggers.
        Base.metadata.drop_all(self.connection)
        Base.metadata.create_all(self.connection)

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
            send_registration_email=False,
        )

    def auth_headers(self, email="admin@example.com", password="password123"):
        payload = {"username": email, "password": password}
        resp = self.client.post("/auth/token", data=payload)
        return {"Authorization": "Bearer " + resp.json().get("access_token")}
