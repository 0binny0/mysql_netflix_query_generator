
import unittest

import mysql.connector as mysql_db
from mysql.connector import ProgrammingError

from main import populate_db
from sql_data import tables
from patterns import capture_names
from test_data import table_data


class DBTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_connect = mysql_db.connect(
            username="root",
            password="password"
        )
        cls.db_cursor = cls.db_connect.cursor()
        # cls.db_cursor.execute(create_tables())

        # cls.db_connect.commit()


    @classmethod
    def tearDownClass(cls):
        cls.db_connect.close()


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


class TestDBCreateTables(DBTestCase):
    '''Verify that the tables for the database are created.'''

    def setUp(self):
        super().setUp()

    def test_database_tables_created(self):
        pass





if __name__ == "__main__":
    with mysql_db.connect(user="root", password="password") as connection:
        cursor = connection.cursor()
        cursor.execute("""SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME LIKE 'test_db';""")
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
            import pdb; pdb.set_trace()
            for insert_data in table_data:
                statement = insert_data[0]
                data = insert_data[1]
                cursor.executemany(statement, data)
                connection.commit()
    unittest.main()
