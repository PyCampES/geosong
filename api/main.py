"""Main module"""
import crud
import models
import schemas
from database import SessionLocal, engine
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from geojson_pydantic import Feature, Point, FeatureCollection

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    """Return the DB connection"""
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


@app.post("/geosong/", response_model=schemas.GeoSong, status_code=201)
def create_geosong(geosong: schemas.GeoSongCreate, database: Session = Depends(get_db)):
    """Endpoint to create a geosong"""
    return crud.create_geosong(database=database, geosong=geosong)


@app.get("/geosongs/", response_model=FeatureCollection)
def read_geosongs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_geosongs_feature_collection(db, skip=skip, limit=limit)
