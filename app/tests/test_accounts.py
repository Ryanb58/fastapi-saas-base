from app.tests import client


def test_read_main():
    response = client.get("/accounts")
    # assert response.status_code == 200
    # assert response.json() == {"message": "Hello World"}
