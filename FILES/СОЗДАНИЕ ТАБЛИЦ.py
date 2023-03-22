
from pprint import pprint
import sqlalchemy

db = 'postgresql://sergiy:1974@localhost:5432/test_database'
engine = sqlalchemy.create_engine(db)
connection = engine.connect()

connection.execute('''CREATE TABLE if not exists genres(
id serial primary key, 
name varchar(50) unique not null);''')

connection.execute('''CREATE TABLE if not exists musicians(
id serial primary key, 
name varchar(50) unique not null);''')

connection.execute('''CREATE TABLE if not exists genres_musicians(
genre_id integer references genres(id) not null, 
musician_id integer references musicians(id) not null, 
constraint genres_musicians_genre_id_artists_id_pk1 primary key (genre_id, musician_id)
);''')


connection.execute('''CREATE TABLE if not exists albums(
id serial primary key, 
name  varchar(50) not null, 
year integer not null check(year > 0)
);''')

connection.execute('''CREATE TABLE if not exists albums_musicians(
album_id integer references albums(id) not null, 
musician_id integer references musicians(id) not null, 
constraint albums_musicians_album_id_musician_id_pk2 primary key (album_id, musician_id)
);''')

connection.execute('''CREATE TABLE if not exists tracks(
id serial primary key, name varchar(70) not null, 
length time not null, 
album_id integer references albums(id)
);''')

connection.execute('''CREATE TABLE if not exists collections(
id serial primary key, name varchar(30) not null, 
year integer not null check(year > 0)
);''')

connection.execute('''CREATE TABLE if not exists collections_tracks(
collection_id integer references collections(id) not null, 
track_id integer references tracks(id) not null, 
constraint collections_tracks_collection_id_track_id_pk3 primary key (collection_id, track_id)
);''')

pprint("Tables created successfully")
connection.close()
