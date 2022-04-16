import models
from database import SessionLocal, engine
from fastapi.testclient import TestClient
from main import app, get_db
from sqlalchemy.orm import Session
from schemas import GeoSong

client = TestClient(app)


def test_create_item():
    database = SessionLocal()
    response = client.post(
        "/geosong/",
        json={
            "date": "2022-04-15T19:07:38.272349",
            "song_metadata": {"title": "Verdura"},
            "username": "gilgamezh",
            "point": {
                "type": "Point",
                "coordinates": [-3.71337890625, 39.825413103424786],
            },
        },
    )
    assert response.status_code == 201
    geosong = database.query(models.GeoSong).first()
    pydantic_geosong = GeoSong.from_orm(geosong)
    assert pydantic_geosong.username == "gilgamezh"
    assert pydantic_geosong.song_metadata.title == "Verdura"
    assert pydantic_geosong.point.coordinates == (-3.71337890625, 39.825413103424786)


def test_get_geosongs():
    client.post(
        "/geosong/",
        json={
            "date": "2022-04-15T19:07:38.272349",
            "song_metadata": {"title": "Verdura"},
            "username": "gilgamezh",
            "point": {
                "type": "Point",
                "coordinates": [-3.71337890625, 39.825413103424786],
            },
        },
    )
    response = client.get("/geosongs/")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response
