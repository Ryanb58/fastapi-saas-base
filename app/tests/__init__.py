from starlette.testclient import TestClient
from app.main import app

client = TestClient(app)