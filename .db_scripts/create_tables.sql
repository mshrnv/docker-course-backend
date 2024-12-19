\connect postgres;

CREATE TABLE IF NOT EXISTS hosts (
  host_id serial PRIMARY KEY NOT NULL,
  host_name varchar(255) NOT NULL,
  experience int NOT NULL,
  age int NOT NULL
);

CREATE TABLE IF NOT EXISTS programs (
  program_id serial PRIMARY KEY NOT NULL,
  program_name varchar(255) NOT NULL,
  duration time NOT NULL,
  program_ratings int NOT NULL
);

CREATE TABLE IF NOT EXISTS host_program_pair (
  pair_id serial PRIMARY KEY NOT NULL,
  program_id int NOT NULL,
  host_id int NOT NULL,
  FOREIGN KEY (program_id) REFERENCES programs(program_id),
  FOREIGN KEY (host_id) REFERENCES hosts(host_id)
);

CREATE TABLE IF NOT EXISTS genres (
  genre_id serial PRIMARY KEY NOT NULL,
  genre_name varchar(255) NOT NULL,
  genre_desc varchar(255)
);


CREATE TABLE IF NOT EXISTS artists (
  artist_id serial PRIMARY KEY NOT NULL,
  artist_name varchar(255) NOT NULL,
  country varchar(100) NOT NULL,
  birthdate date NOT NULL,
  genre_id int,
  FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
);


CREATE TABLE IF NOT EXISTS tracks (
  track_id serial PRIMARY KEY NOT NULL,
  track_name varchar(255) NOT NULL,
  release_date date NOT NULL,
  duration time NOT NULL,
  artist_id int NOT NULL,
  genre_id int,
  FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
  FOREIGN KEY (genre_id) REFERENCES genres(genre_id)
);


CREATE TABLE IF NOT EXISTS album (
  album_id serial PRIMARY KEY NOT NULL,
  album_name varchar(255) NOT NULL,
  artist_id int NOT NULL,
  track_id int NOT NULL,
  year_of_release int NOT NULL,
  FOREIGN KEY (artist_id) REFERENCES artists(artist_id),
  FOREIGN KEY (track_id) REFERENCES tracks(track_id)
);


CREATE TABLE IF NOT EXISTS song_requests (
  request_id serial PRIMARY KEY NOT NULL,
  track_id int NOT NULL,
  program_id int NOT NULL,
  request_time time NOT NULL,
  request_date date NOT NULL,
  FOREIGN KEY (track_id) REFERENCES tracks(track_id),
  FOREIGN KEY (program_id) REFERENCES programs(program_id)
);


CREATE TABLE IF NOT EXISTS playlists (
  playlist_id serial PRIMARY KEY NOT NULL,
  program_id int NOT NULL,
  airtime time NOT NULL,
  playlist_date date NOT NULL,
  FOREIGN KEY (program_id) REFERENCES programs(program_id)
);


CREATE TABLE IF NOT EXISTS playlist_and_track_pair (
  pair_id serial PRIMARY KEY NOT NULL,
  playlist_id int NOT NULL,
  track_id int NOT NULL,
  FOREIGN KEY (playlist_id) REFERENCES playlists(playlist_id),
  FOREIGN KEY (track_id) REFERENCES tracks(track_id)
);