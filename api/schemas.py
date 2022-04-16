import datetime
from typing import Optional

from geoalchemy2.shape import to_shape
from geojson_pydantic import Point
from pydantic import BaseModel


class SongMetadata(BaseModel):
    title: Optional[str]
    artist: Optional[str]
    year: Optional[int]
    genre: Optional[str]



class GeoSongBase(BaseModel):
    date: datetime.datetime
    song_metadata: SongMetadata
    point: Feature[Point]
    username: str

    def to_orm(self):
        tmp = self.dict()
        tmp['point'] = f'SRID=4326;POINT({self.point.coordinates[0]} {self.point.coordinates[1]})'
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

