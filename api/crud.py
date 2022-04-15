from sqlalchemy.orm import Session

import models, schemas


def get_geosongs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.GeoSong).offset(skip).limit(limit).all()


def create_geosong(db: Session, geosong: schemas.GeoSongCreate):
    db_geosong = models.GeoSong(**geosong.dict())
    db.add(db_geosong)
    db.commit()
    db.refresh(db_geosong)

