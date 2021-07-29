
import unittest
from argparse import Namespace
from unittest.mock import Mock, patch

import mysql.connector as mysql_db
from mysql.connector import ProgrammingError, MySQLConnection

from main import (
    db_connect, get_show_listing, get_actor_filmography, get_show_profile
)
from tables import tables
from helpers import capture_names, check_int_value, format_actor_name
from test_data import table_data


class TestCaptureIntColumn(unittest.TestCase):
    '''Verify that the value to be stored in a numerical
    database column is a rational number.'''

    def test_check_int_value_whole_number(self):
        value = check_int_value('5')
        self.assertIsInstance(value, float)
        self.assertEqual(value, 5.0)

    def test_check_int_value_decimal_number(self):
        value = check_int_value('5.8')
        self.assertIsInstance(value, float)
        self.assertEqual(value, 5.8)


    def test_check_int_value_non_number(self):
        value = check_int_value("$5.0")
        self.assertNotIsInstance(value, float)
        self.assertEqual(value, None)

    def test_check_int_value_large(self):
        value = check_int_value('1834777772')
        self.assertIsInstance(value, float)
        self.assertEqual(value, 1834777772.0)


class TestActorNameFormatter(unittest.TestCase):
    '''Verify that excessive whitespace is trimmed
    in between and around an actor's full name.'''

    def test_format_actor_name1(self):
        name = format_actor_name("    John           Doe ")
        self.assertEqual(name, "John Doe")



class TestShowListing(unittest.TestCase):
    '''Verify that the at most 5 shows are listed
    in descending order'''

    test_db_config = {
        'user': "root",
        'password': "password",
        'database': "test_db"
    }

    @patch.dict('main.credentials', test_db_config)
    def test_db_query_show_listing_no_genre(self):
        shows = get_show_listing()
        self.assertLessEqual(len(shows), 5)

    @patch.dict('main.credentials', test_db_config)
    def test_db_query_show_listing_with_genre(self):
        shows = get_show_listing(genre="genre3")
        self.assertEqual(len(shows), 1)


class TestShowActorDetailListing(unittest.TestCase):

    test_db_config = {
        'user': "root",
        'password': "password",
        'database': "test_db"
    }

    '''Verify that all shows that an actor has played a role in
    are listed in ascending order'''
    @patch.dict('main.credentials', test_db_config)
    def test_all_actor_shows_listed(self):
        actor_shows = get_actor_filmography("actor1_fn actor1_ln")
        self.assertEqual(len(actor_shows), 3)
        for i in range(len(actor_shows) - 1):
            self.assertLess(
                actor_shows[i]['release_year'],
                actor_shows[i + 1]['release_year']
            )

# class TestShowDetailListing(unittest.TestCase):
#     '''Verify that that tags, actors, and show details
#     are listed for a given tvshow profile.'''
#
#     test_db_config = {
#         'user': "root",
#         'password': "password",
#         'database': "test_db"
#     }
#
#     @patch.dict('main.credentials', test_db_config)
#     def test_get_show_profile(self):
#         show = get_show_profile("show3")[0]
#         self.assertEqual(
#             show['release_date'],
#             2015
#         )
#         self.assertEqual(
#             show['title'],
#             'show3'
#         )
#         self.assertEqual(
#             show['view_rating'],
#             'PG'
#         )


class TestRegexFullName(unittest.TestCase):
    '''Verify that names that extend beyond
    first name and last name are captured.'''

    def setUp(self):
        self.names = "John A. Doe, Bob Joesph Dole, Jane Doe, Daniel Day-Lewis"

    def test_regex_name_capture(self):
        result = capture_names(self.names)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], ["John", "A.", "Doe"])
        self.assertEqual(result[1], ['Bob', 'Joesph', 'Dole'])
        self.assertEqual(result[2], ['Jane', None, "Doe"])
        self.assertEqual(result[3], ['Daniel', None, "Day-Lewis"])



if __name__ == "__main__":
    with mysql_db.connect(user="root", password="password") as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA
            WHERE SCHEMA_NAME LIKE 'test_db';
        """)
        cursor.fetchall()
        db_exists = cursor.rowcount
        if not db_exists:
            cursor.execute(
                'CREATE DATABASE IF NOT EXISTS test_db;'
            )
            connection.database = 'test_db'
            print(f"Database: {connection.database}")
            for create_table in tables:
                cursor.execute(create_table)
                connection.commit()
            for insert_data in table_data:
                statement = insert_data[0]
                data = insert_data[1]
                cursor.executemany(statement, data)
                connection.commit()
    unittest.main()
