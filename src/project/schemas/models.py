from pydantic import BaseModel, Field, ConfigDict
from datetime import time, date


class ProgramCreateUpdateSchema(BaseModel):
    program_name: str
    duration: time
    program_ratings: int


class ProgramSchema(ProgramCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int

class HostCreateUpdateSchema(BaseModel):
    host_name: str
    experience: int
    age: int


# Схема для отображения данных хоста (при получении из базы данных)
class HostSchema(HostCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int


class HostProgramPairCreateUpdateSchema(BaseModel):
    program_id: int
    host_id: int


class HostProgramPairSchema(HostProgramPairCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int


class GenreCreateUpdateSchema(BaseModel):
    genre_name: str
    genre_desc: str | None = None


class GenreSchema(GenreCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ArtistCreateUpdateSchema(BaseModel):
    artist_name: str
    country_name: str
    birthdate: date
    genre_id: int


class ArtistSchema(ArtistCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int


class TrackCreateUpdateSchema(BaseModel):
    track_name: str
    release_date: date
    duration: time
    artist_id: int | None = None
    genre_id: int | None = None


class TrackSchema(TrackCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int


class AlbumCreateUpdateSchema(BaseModel):
    album_name: str
    artist_id: int
    track_id: int
    year_of_release: int


class AlbumSchema(AlbumCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int


class SongRequestCreateUpdateSchema(BaseModel):
    program_id: int
    track_id: int
    request_time: time
    request_date: date


class SongRequestSchema(SongRequestCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int


class PlaylistCreateUpdateSchema(BaseModel):
    program_id: int
    airtime: time
    playlist_date: date

class PlaylistSchema(PlaylistCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int


class PlaylistAndTrackPairCreateUpdateSchema(BaseModel):
    playlist_id: int
    track_id: int


class PlaylistAndTrackPairSchema(PlaylistAndTrackPairCreateUpdateSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int