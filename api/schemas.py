import datetime
from typing import Optional
from shapely.geometry import box

from geoalchemy2.shape import to_shape
from geojson_pydantic import Feature, Point, FeatureCollection
from pydantic import BaseModel, conlist


class SongMetadata(BaseModel):
    title: Optional[str]
    artist: Optional[str]
    year: Optional[int]
    genre: Optional[str]


class Props(BaseModel):
    song_metadata: SongMetadata
    username: str
    date: datetime.datetime
    from_source: bool


class GeoSongBase(BaseModel):
    date: datetime.datetime
    song_metadata: SongMetadata
    point: Optional[Point]
    bbox: conlist(float, min_items=4,max_items=4)
    username: str

    def to_orm(self):
        tmp = self.dict()
        from_source = True
        if not self.point:
            from_source = False
            centroid = box(*self.bbox).centroid
            calculated_x, calculated_y = centroid.xy[0][0], centroid.xy[1][0]
            self.point = Point(coordinates=[calculated_x, calculated_y])
        point = (
            f"SRID=4326;POINT({self.point.coordinates[0]} {self.point.coordinates[1]})"
        )
        tmp["point"] = point
        tmp["bbox"] = ";".join([str(i) for i in self.bbox])
        tmp["from_source"] = from_source
        return tmp

    @classmethod
    def from_orm(cls, obj):
        if obj.point:
            geom = to_shape(obj.point)
            obj.point = Point(coordinates=(geom.x, geom.y))
        obj.bbox = [float(i) for i in obj.bbox.split(";")]
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
        bbox = [float(i) for i in obj.bbox.split(";")]
        return PointFeature(
            geometry=Point(coordinates=[geom.x, geom.y]),
            properties=Props(
                song_metadata=obj.song_metadata,
                username=obj.username,
                date=obj.date,
                from_source=obj.from_source or False,
            ),
            id=obj.id,
            bbox=bbox
        )
