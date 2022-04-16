import models
import schemas
from sqlalchemy.orm import Session

def get_geosongs(database: Session, skip: int = 0, limit: int = 100):
    """Return a single geosong"""
    return database.query(models.GeoSong).offset(skip).limit(limit).all()

def create_geosong(database: Session, geosong: schemas.GeoSongCreate):
    """Create a single GeoSong"""
    database_geosong = models.GeoSong(**geosong.to_orm())
    database.add(database_geosong)
    database.commit()
    database.refresh(database_geosong)
