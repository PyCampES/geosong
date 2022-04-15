from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_create_item():
    response = client.post(
        "/geosong/",
        json={
            "date": "2022-04-15T19:07:38.272349",
            "song_metadata": {"foo": "bar"},
            "username": "gilgamezh",
        },
    )
    assert response.status_code == 201
