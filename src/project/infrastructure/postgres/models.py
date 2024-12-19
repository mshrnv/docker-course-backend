from sqlalchemy import Column, Integer, String, Text, ForeignKey, Time, Date, false
from sqlalchemy.orm import Mapped, mapped_column


from project.infrastructure.postgres.database import Base



class Hosts(Base):
    __tablename__ = "hosts"

    id = Column(Integer, primary_key=True)
    host_name = Column(String(255), nullable=False)
    experience = Column(Integer, nullable=False)
    age = Column(Integer, nullable=False)


class Programs(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True)
    program_name = Column(String(255), nullable=False)
    duration = Column(Time, nullable=False)
    program_ratings = Column(Integer, nullable=False)


class HostProgramPair(Base):
    __tablename__ = "host_program_pair"

    id = Column(Integer, primary_key=True)
    program_id = Column(Integer, ForeignKey('programs.id'), nullable=False)
    host_id = Column(Integer, ForeignKey('hosts.id'), nullable=False)


class Genres(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True)
    genre_name = Column(String(255), nullable=False)
    genre_desc = Column(String(255))


class Artists(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True)
    artist_name = Column(String(255), nullable=False)
    country_name = Column(String(100), nullable=False)
    birthdate = Column(Date, nullable=False)
    genre_id = Column(Integer, ForeignKey('genres.id'), nullable=False)


class Tracks(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True)
    track_name = Column(String(255), nullable=False)
    release_date = Column(Date, nullable=False)
    duration = Column(Time, nullable=False)
    artist_id = Column(Integer, ForeignKey('artists.id'))
    genre_id = Column(Integer, ForeignKey('genres.id'))


class Album(Base):
    __tablename__ = "album"

    id = Column(Integer, primary_key=True)
    album_name = Column(String(255), nullable=False)
    artist_id = Column(Integer, ForeignKey('artists.id'), nullable=False)
    track_id = Column(Integer, ForeignKey('tracks.id'), nullable=False)
    year_of_release = Column(Integer, nullable=False)


class SongRequests(Base):
    __tablename__ = "song_requests"

    id = Column(Integer, primary_key=True)
    program_id = Column(Integer, ForeignKey('programs.id'), nullable=False)
    track_id = Column(Integer, ForeignKey('tracks.id'), nullable=False)
    request_time = Column(Time, nullable=False)
    request_date = Column(Date, nullable=False)


class Playlists(Base):
    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True)
    program_id = Column(Integer, ForeignKey('programs.id'), nullable=False)
    airtime = Column(Time, nullable=False)
    playlist_date = Column(Date, nullable=False)


class PlaylistAndTrackPair(Base):
    __tablename__ = "playlist_and_track_pair"

    id = Column(Integer, primary_key=True)
    playlist_id = Column(Integer, ForeignKey('playlists.id'), nullable=False)
    track_id = Column(Integer, ForeignKey('tracks.id'), nullable=False)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=True)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=false())

