import datetime
from typing import Optional

from geoalchemy2.shape import to_shape
from geojson_pydantic import Feature, Point, FeatureCollection
from pydantic import BaseModel


class SongMetadata(BaseModel):
    title: Optional[str]
    artist: Optional[str]
    year: Optional[int]
    genre: Optional[str]


class Props(BaseModel):
    song_metadata: SongMetadata
    username: str
    date: datetime.datetime


class GeoSongBase(BaseModel):
    date: datetime.datetime
    song_metadata: SongMetadata
    point: Point
    username: str

    def to_orm(self):
        tmp = self.dict()
        point = (
            f"SRID=4326;POINT({self.point.coordinates[0]} {self.point.coordinates[1]})"
        )
        tmp["point"] = point
        return tmp

    @classmethod
    def from_orm(cls, obj):
        geom = to_shape(obj.point)
        obj.point = Point(coordinates=(geom.x, geom.y))
        geosong = super().from_orm(obj)
        return geosong


class GeoSongCreate(GeoSongBase):
    pass


class GeoSong(GeoSongBase):
    id: int

    class Config:
        orm_mode = True


class PointFeature(Feature[Point, Props]):
    class Config:
        orm_mode = True

    @classmethod
    def from_orm(cls, obj):
        geom = to_shape(obj.point)
        return PointFeature(
            geometry=Point(coordinates=[geom.x, geom.y]),
            properties=Props(
                song_metadata=obj.song_metadata,
                username=obj.username,
                date=obj.date,
            ),
            id=obj.id,
        )
