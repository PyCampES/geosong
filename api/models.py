from geoalchemy2 import Geometry
from sqlalchemy import JSON, Column, DateTime, Integer, String

from database import Base


class GeoSong(Base):
    """A geolocated song

    {
         "type": "Feature",
         "properties": {
           "date": "2022-04-15T09:10:35Z",
           "username": "@juanluisback",
           "geosong": {
             "title": "U Can't Touch This",
             "artist": "MC Hammer",
             "year": 1990,
             "genre": "hip hop"
           }
         },
    """

    __tablename__ = "geosongs"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    song_metadata = Column(JSON)
    point = Column(Geometry("POINT", srid=4326, management=True))
    username = Column(String)
