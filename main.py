
import csv
import re
import mysql.connector
from datetime import datetime

from tables import tables
from patterns import capture_names

credentials = {
    'user': "root",
    'password': "password",
    'database': "main_database"
}

def db_connect(func):
    def wrapper_db_connect(*args, **kwargs):
        with mysql.connector.connect(**credentials) as db_connection:
            cursor = db_connection.cursor(dictionary=True)
            return func(cursor, *args, **kwargs)
    return wrapper_db_connect


@db_connect
def get_show_listing(cursor, genre=None):
    if not genre:
        cursor.execute("""
            SELECT title, view_rating, YEAR(release_date), score, votes
            FROM tvshow AS t LEFT JOIN show_genre as s
            ON t.title = s.tvshow_title RIGHT JOIN genre as g
            ON s.genre_name = g.name WHERE votes is NOT NULL
            ORDER BY votes DESC LIMIT 5;
        """)
    else:
        cursor.execute("""
            SELECT title, view_rating, YEAR(release_date), score, votes
            FROM tvshow AS t LEFT JOIN show_genre as s
            ON t.title = s.tvshow_title RIGHT JOIN genre as g
            ON s.genre_name = g.name
            WHERE g.name = %(genre)s AND votes IS NOT NULL
            ORDER BY votes DESC LIMIT 5;
        """, {'genre': genre})
    return cursor.fetchall()

@db_connect
def get_actor_filmography(cursor, actor):
    fn, ln = actor.split(" ")
    cursor.execute("""
        SELECT release_date, title FROM tvshow
        INNER JOIN show_actor ON tvshow.title = show_actor.tvshow_title
        INNER JOIN actor ON show_actor.actor_fn = actor.first_name
        AND show_actor.actor_ln = actor.last_name
        WHERE first_name = %(fn)s AND last_name = %(ln)s
        ORDER BY release_date;
    """, {'fn': fn, 'ln': ln})
    return cursor.fetchall()

@db_connect
def get_show_profile(cursor, show):
    cursor.execute("""
        SELECT t.title, t.view_rating, YEAR(t.release_date) as release_date,
        t.summary, t.score, t.votes, (
            SELECT GROUP_CONCAT(sa.actor_fn, " ", sa.actor_ln SEPARATOR ', ')
            FROM show_actor AS sa WHERE tvshow_title = %(show)s
            ORDER BY sa.actor_ln
        ) AS actors FROM tvshow as t WHERE t.title = %(show)s;
    """, {'show': show})
    return cursor.fetchall()

def display_shows(genre=None):
    shows = get_show_listing(genre)
    if not shows:
        print("No shows in this genre have been voted on.")
    else:
        s = ''
        for show in shows:
            s += f"""
                {show['title']} - {show['release_date']} - {show['view_rating']}
                {show['score']} - {show['votes']}
            """
        print(s)
