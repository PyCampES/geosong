from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/geosong/", response_model=schemas.GeoSong, status_code=201)
def create_geosong(geosong: schemas.GeoSongCreate, db: Session = Depends(get_db)):
    import ipdb; ipdb.set_trace()
    return crud.create_geosong(db=db, geosong=geosong)


@app.get("/geosongs/", response_model=list[schemas.GeoSong])
def read_geosongs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    geosongs = crud.get_geosongs(db, skip=skip, limit=limit)
    return geosongs
