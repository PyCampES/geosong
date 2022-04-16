import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.event import listen
from sqlalchemy.orm import sessionmaker
import pytest
import models
from database import Base
from main import app, get_db
from schemas import GeoSong

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"


def load_spatialite(dbapi_conn, connection_record):
    dbapi_conn.enable_load_extension(True)
    dbapi_conn.load_extension("/usr/lib/mod_spatialite.so")


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=False
)
listen(engine, "connect", load_spatialite)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    os.remove("test.db")


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)



def test_create(test_db):
    database = TestingSessionLocal()
    assert database.query(models.GeoSong).count() == 0
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
    database.close()


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
