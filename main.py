
import csv
import re
import mysql.connector
from datetime import datetime
from time import sleep


from tables import tables
from helpers import capture_names, check_int_value, cls

credentials = {
    'user': "root",
    'password': "password",
    'database': "main_database"
}

def db_connect(func):
    def wrapper_db_connect(*args, **kwargs):
        with mysql.connector.connect(**credentials) as db_connection:
            return func(db_connection, *args, **kwargs)
    return wrapper_db_connect

@db_connect
def populate_tables(connection, row):
    cursor = connection.cursor(dictionary=True)
    _row = {
        'tvshow': {},
        'genres': [],
        'actors': []
    }
    for column, value in row.items():
        column = column.replace(" ", "_")
        if column == "":
            pass
        elif column == "release_date":
            try:
                value = (datetime.strptime(value, "%d %b %Y")
                                    .strftime("%Y-%m-%d"))
            except ValueError:
                value = None
            finally:
                _row['tvshow']['release_date'] = value
        elif column == "votes" or column == "score":
            value = check_int_value(value)
            _row['tvshow'][f'{column}'] = value
        elif column != 'genre' and column != 'actors':
            if not value:
                value = None
            else:
                value = value.strip()
            _row['tvshow'][column] = value
        elif column == 'genre':
            genres = value.split(",")
            if not genres:
                _row['genres'] = None
            else:
                genres = [genre.strip() for genre in genres]
                _row['genres'].extend(genres)
        else:
            actors = capture_names(value)
            _row['actors'].extend(actors)
    try:
        cursor.execute('''
            INSERT INTO tvshow VALUES (
                 %(title)s, %(view_rating)s, %(release_date)s,
                 %(summary)s, %(score)s, %(votes)s
            );
        ''', _row['tvshow'])
    except mysql.connector.IntegrityError:
        pass
    else:
        connection.commit()
    for genre in _row['genres']:
        try:
            cursor.execute(
                "INSERT INTO genre VALUES (%(genre)s);", {'genre': genre}
            )
            print(f"Create genre: {genre}")
        except mysql.connector.IntegrityError:
            print(f"Genre {genre} already created.")
            cursor.execute("""INSERT INTO show_genre VALUES (
                NULL, %(genre)s, %(title)s
            );""", {'genre': genre, 'title': _row['tvshow']['title']})
            print(f"Create show_genre: {_row['tvshow']['title']}:{genre})")
        finally:
            connection.commit()
    for actor in _row['actors']:
        fn, mn, ln = actor
        try:
            cursor.execute("""
                INSERT INTO actor VALUES (%(fn)s, %(mn)s, %(ln)s);
            """, {'fn': fn, 'mn': mn, 'ln': ln})
        except mysql.connector.IntegrityError:
            cursor.execute("""
                INSERT INTO show_actor VALUES (
                    NULL, %(actor_fn)s, %(actor_ln)s, %(title)s
                )
            """, {
                'actor_fn': fn, 'actor_ln': ln,
                'title': _row['tvshow']['title']}
            )
        finally:
            connection.commit()

@db_connect
def get_show_listing(connection, genre=None):
    cursor = connection.cursor(dictionary=True)
    if not genre:
        cursor.execute("""
            SELECT DISTINCT title, view_rating,
            YEAR(release_date) as release_date, score, votes
            FROM tvshow AS t LEFT JOIN show_genre as s
            ON t.title = s.tvshow_title RIGHT JOIN genre as g
            ON s.genre_name = g.name WHERE votes IS NOT NULL
            ORDER BY votes DESC LIMIT 10;
        """)
    else:
        cursor.execute("""
            SELECT DISTINCT title, view_rating,
            YEAR(release_date) as release_date, score, votes
            FROM tvshow AS t LEFT JOIN show_genre as s
            ON t.title = s.tvshow_title RIGHT JOIN genre as g
            ON s.genre_name = g.name
            WHERE g.name = %(genre)s AND votes IS NOT NULL
            ORDER BY votes DESC LIMIT 10;
        """, {'genre': genre})
    return cursor.fetchall()

@db_connect
def get_actor_filmography(connection, actor):
    cursor = connection.cursor(dictionary=True)
    fn, ln = actor.split(" ")
    cursor.execute("""
        SELECT YEAR(release_date) as release_year, title FROM tvshow
        INNER JOIN show_actor ON tvshow.title = show_actor.tvshow_title
        INNER JOIN actor ON show_actor.actor_fn = actor.first_name
        AND show_actor.actor_ln = actor.last_name
        WHERE first_name = %(fn)s AND last_name = %(ln)s
        ORDER BY release_date;
    """, {'fn': fn, 'ln': ln})
    return cursor.fetchall()

@db_connect
def get_show_profile(connection, show):
    show_param = '%' + show + '%'
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT title FROM tvshow WHERE title LIKE %(show)s",
        {'show': show_param}
    )
    shows = cursor.fetchall()
    while True:
        cls()
        if len(shows) > 0:
            print(f"Titles that contain: {show}. Select your show...\n")
            for i, s in enumerate(shows):
                print(f"{i + 1} - {s['title']}")
            _show = input(">>> ")
            cursor.execute("""
                SELECT * FROM tvshow WHERE title = %(show)s
            """, {'show': _show})
            try:
                selected_show = cursor.fetchall()[0]
            except IndexError:
                print("\nNo show found. Check the title you searched by.")
                sleep(2)
                continue
            show = selected_show
            break
    cursor.execute("""
        SELECT t.title, t.view_rating, YEAR(t.release_date) AS release_date,
        t.summary, t.score, t.votes, (
            SELECT GROUP_CONCAT(sa.actor_fn, " ", sa.actor_ln SEPARATOR ', ')
            FROM show_actor AS sa WHERE tvshow_title LIKE %(show)s
        ) AS actors, (
            SELECT GROUP_CONCAT(sg.genre_name SEPARATOR ', ')
            FROM show_genre AS sg WHERE tvshow_title = %(show)s
        ) AS genres FROM tvshow as t WHERE t.title = %(show)s;
    """, {'show': show['title']})
    return cursor.fetchall()

def display_shows(genre=None):
    cls()
    shows = get_show_listing(genre)
    if not shows:
        return "No shows in this genre have been voted on."
    else:
        if genre:
            print(f"Top {len(shows)} movies/shows found in {genre.title()}:")
        else:
            print(f"Top {len(shows)} overall shows: (No genre searched)")
        s = ''
        for show in shows:
            s += f"""
                Title: {show['title']} - Year: {show['release_date']}
                Rating: {show['view_rating']} - Score: {show['score']} - Votes: {show['votes']}
            """
        return s

def display_show(show):
    cls()
    try:
        show = get_show_profile(show)[0]
    except IndexError:
        return "No show exists under that title..."
    else:
        return f"""
            Title: {show['title']} - Genres: {show['genres']}
            Year: {show['release_date']} - Rating: {show['view_rating']}
            Score: {show['score']} - Votes: {show['votes']}
            Summary: {show['summary']}
            Actors: {show['actors']}
        """

def display_actor_filmography(actor):
    cls()
    shows = get_actor_filmography(actor)
    if not shows:
        return f"There are no shows the given actor...({actor})"
    else:
        print(f"{actor.title()} Filmography (by Year): \n")
        s = ''
        for show in shows:
            s += f"{show['title']} - {show['release_year']}\n"
        return s

def main():
    while True:
        print("""
            Pick from one of the following options:
            1) View an actor's filmography
            2) Get an overview of a given show
            3) See the top shows for a given genre
        """)
        user_option = input("\n>>> ")
        if user_option not in ["1", "2", "3"]:
            print("That option is not avialable.")
            continue
        break
    if user_option == "1":
        while True:
            actor = input(
                "What actor filmography would you like to see?\n>>> "
            ).strip()
            try:
                actor_fn, actor_ln = actor.split(" ")
            except ValueError:
                print("\nError: Actor's full name wasn't provided")
            else:
                sleep(1)
                print(display_actor_filmography(actor))
                return
    elif user_option == "2":
        while True:
            print(
                "Name the show/movie you'd like to see more information about..."
            )
            show = input("\n>>> ").title().strip()
            if not show:
                print("No show provided...")
            else:
                print(display_show(show))
                return
    else:
        while True:
            print(
                "Enter the genre that you want to filter shows by..."
            )
            genre = input("\n>>> ").strip()
            print(display_shows(genre))
            return

def store_database():
    with mysql.connector.connect(user="root", password="password") as connection:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS main_database;")
        cursor.execute("USE main_database;")
        cursor.execute("""
            SELECT table_name FROM INFORMATION_SCHEMA.tables
            WHERE TABLE_SCHEMA =  %(db)s;
        """, {'db': 'main_database'})
        tables_exist = cursor.fetchall()
        if not tables_exist:
            for table in tables:
                cursor.execute(table)
            with open("netflix_data_v_1.csv", encoding="utf8") as data:
                netflix_data = csv.DictReader(data)
                for row in netflix_data:
                    populate_tables(row)
    main()

if __name__ == "__main__":
    store_database()
