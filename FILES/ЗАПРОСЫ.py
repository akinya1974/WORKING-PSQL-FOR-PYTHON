
import sqlalchemy
from pprint import pprint

db = 'postgresql://sergiy:1974@localhost:5432/test_database'
engine = sqlalchemy.create_engine(db)
connection = engine.connect()

# СЕЛЕКТ ЗАПРОСЫ

download_album = connection.execute(
    """SELECT name, year 
    FROM  albums 
    WHERE year = 2018;"""
).fetchall()
pprint(download_album)

pprint(f"-----------------------------------------------")

download_max_length = connection.execute(
    """SELECT name, length 
    FROM  tracks 
    ORDER BY length 
    DESC limit 1;"""
).fetchall()
pprint(download_max_length)

pprint(f"-----------------------------------------------")

download_track_name = connection.execute(
    """SELECT name 
    FROM  tracks 
    WHERE length >= '00:03:30' 
    ORDER BY length DESC;"""
).fetchall()
pprint(download_track_name)

pprint(f"-----------------------------------------------")

download_collections = connection.execute(
    """SELECT name 
    FROM  collections 
    WHERE year 
    BETWEEN 2018 and  2020;"""
).fetchall()
pprint(download_collections)

pprint(f"-----------------------------------------------")

download_artists_name = connection.execute(
    """SELECT name 
    FROM musicians 
    WHERE NOT name like ('%% %%');"""
).fetchall()
pprint(download_artists_name)

pprint(f"-----------------------------------------------")

download_tracks_name_my = connection.execute(
    """SELECT name 
    FROM tracks 
    WHERE name 
    LIKE '%%My%%' OR name LIKE '%%мой%%';"""
).fetchall()
pprint(download_tracks_name_my)