import sqlalchemy
from pprint import pprint

db = 'postgresql://sergiy:1974@localhost:5432/test_database'
engine = sqlalchemy.create_engine(db)
connection = engine.connect()

# Количество исполнителей в каждом жанре

download_musicians_from_genre = connection.execute(
   """SELECT g.name, COUNT(gm.musician_id ) FROM genres g
JOIN genres_musicians gm ON g.id = gm.genre_id
GROUP BY g.name;""").fetchall()
pprint(download_musicians_from_genre)

print(f'------------------------------------------------------')

# Количество треков, вошедших в альбомы 2019-2020 годов

download_track_in_album = connection.execute(
"""SELECT  COUNT(t.name) FROM albums a
JOIN tracks t ON a.id = t.album_id
WHERE a.year  BETWEEN 2019 AND 2020;""").fetchall()



pprint(download_track_in_album)

print(f'------------------------------------------------------')

#Средняя продолжительность треков по каждому альбому

download_track_vs_album = connection.execute(
   """SELECT a.name, AVG(t.length) FROM albums AS a
   LEFT JOIN tracks AS t ON t.album_id = a.id
   GROUP BY a.id
   ORDER BY AVG(t.length);""").fetchall()

pprint(download_track_vs_album)

print(f'------------------------------------------------------')

# Все исполнители, которые не выпустили альбомы в 2020 году

download_all_musicians_not_in_year = connection.execute(
    """SELECT  DISTINCT m.name  FROM musicians m 
    JOIN albums_musicians am  ON m.id = am.musician_id
    JOIN albums a ON a.id = am.album_id
    WHERE a.year != 2020;""").fetchall()


pprint(download_all_musicians_not_in_year)

print(f'------------------------------------------------------')

# Названия сборников, в которых присутствует конкретный исполнитель (BIXX)

download_bixx_in_collections = connection.execute(
    """SELECT DISTINCT c.name, c.year
    FROM collections AS c
    LEFT JOIN collections_tracks AS ct ON c.id = ct.collection_id
    LEFT JOIN tracks AS t ON t.id = ct.track_id
    LEFT JOIN albums AS a ON a.id = t.album_id
    LEFT JOIN albums_musicians AS am ON am.album_id = a.id
    LEFT JOIN musicians AS m ON m.id = am.musician_id
    WHERE m.name = 'BIXX'
    ORDER BY c.name;""").fetchall()

pprint(download_bixx_in_collections)

print(f'------------------------------------------------------')

# Название альбомов, в которых присутствуют исполнители более 1 жанра

download_albums_in_musicians_no_one_genre = connection.execute(
    """ SELECT a.name
    FROM albums a
    LEFT JOIN albums_musicians am  ON a.id = am.album_id
    LEFT JOIN musicians m   ON m.id = am.musician_id
    LEFT JOIN genres_musicians gm ON m.id = gm.musician_id
    JOIN genres g ON gm.genre_id = g.id
    GROUP BY a.id
    HAVING COUNT(g.id) > 1;""").fetchall()

pprint(download_albums_in_musicians_no_one_genre)

print(f'------------------------------------------------------')

# Наименование треков, которые не входят в сборники

download_track_not_in_genre = connection.execute(
    """SELECT t.name FROM tracks AS t
    LEFT JOIN collections_tracks AS ct ON t.id = ct.track_id
    WHERE ct.track_id IS NULL;""").fetchall()

pprint(download_track_not_in_genre)

print(f'------------------------------------------------------')

#Исполнителя(-ей), написавшего самый короткий по продолжительности трек
#(теоретически таких треков может быть несколько)

download_musicians_bad_work = connection.execute(
    """SELECT t.length,  m.name FROM tracks AS t
    LEFT JOIN albums AS a ON a.id = t.album_id
    LEFT JOIN albums_musicians AS am ON am.album_id = a.id
    LEFT JOIN musicians AS m ON m.id = am.musician_id
    GROUP BY  t.length, m.id HAVING t.length = (SELECT MIN(length) FROM tracks)
    ORDER BY m.name;""").fetchall()

pprint(download_musicians_bad_work)

print(f'------------------------------------------------------')

# Название альбомов, содержащих наименьшее количество треков

download_name_albums_tracks_min = connection.execute(
    """SELECT a.name, count(t.id)
    FROM albums a
    JOIN tracks t  ON a.id = t.album_id
    GROUP BY a.name
    HAVING count(t.id) = (
        SELECT count(t.id)
        FROM albums a
        JOIN tracks t  ON a.id = t.album_id
        GROUP BY a.name
        ORDER BY count(t.id)
        LIMIT 1);""").fetchall()

pprint(download_name_albums_tracks_min)

print(f'------------------------------------------------------')

