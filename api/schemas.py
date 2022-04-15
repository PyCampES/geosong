import datetime

from geojson_pydantic import Point
from pydantic import BaseModel


class GeoSongBase(BaseModel):
    date = datetime.datetime
    song_metadata = dict
    # point = Point
    username = str


class GeoSongCreate(GeoSongBase):
    pass


class GeoSong(GeoSongBase):
    id: int

    class Config:
        orm_mode = True
