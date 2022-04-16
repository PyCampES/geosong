import models
import schemas
from sqlalchemy.orm import Session
from geojson_pydantic import FeatureCollection
from typing import Iterable


def get_geosongs(
    database: Session, skip: int = 0, limit: int = 100
) -> Iterable[models.GeoSong]:
    """Return a single geosong"""
    result = database.query(models.GeoSong).offset(skip).limit(limit).all()
    return result


def get_geosongs_feature_collection(
    database: Session, skip: int = 0, limit: int = 100
) -> FeatureCollection:
    result = get_geosongs(database, skip, limit)
    feature_collection = FeatureCollection(
        features=[schemas.PointFeature.from_orm(r) for r in result]
    )
    return feature_collection


def create_geosong(database: Session, geosong: schemas.GeoSongCreate):
    """Create a single GeoSong"""
    database_geosong = models.GeoSong(**geosong.to_orm())
    database.add(database_geosong)
    database.commit()
    database.refresh(database_geosong)
