import logging
from sqlite3 import Error

from database import database_api

dbname = "events.db"

SQL_CREATE_TOP_EVENTS_TABLE = """
        CREATE TABLE IF NOT EXISTS top_events (
            event_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            rank INTEGER NOT NULL,
            lat TEXT NOT NULL,
            lon TEXT NOT NULL,
            country_code TEXT NOT NULL,
            last_fetched INTEGER NOT_NULL
        );"""

SQL_CREATE_EVENTS_WEATHER_TABLE = """
    CREATE TABLE IF NOT EXISTS weather (
            event_id TEXT PRIMARY KEY,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            last_fetched INTEGER NOT_NULL
        );"""

SQL_CREATE_EVENTS_FLIGHT_TABLE = """
     CREATE TABLE IF NOT EXISTS flight (
            event_id TEXT NOT NULL,
            dep_iata TEXT NOT NULL, 
            arr_iata TEXT NOT NULL,
            flight_number TEXT PRIMARY KEY, 
            last_fetched INTEGER NOT_NULL
        );"""


def create_table(connection, sql_create_query):
    try:
        c = connection.cursor()
        c.execute(sql_create_query)
    except Error as e:
        logging.error(f'SQLite Create table from statement ${sql_create_query}, more info: {e}')


def database_init():
    connection = database_api.connection_to_db_file(dbname)

    if connection is not None:
        create_table(connection, SQL_CREATE_TOP_EVENTS_TABLE)
        create_table(connection, SQL_CREATE_EVENTS_WEATHER_TABLE)
        create_table(connection, SQL_CREATE_EVENTS_FLIGHT_TABLE)
        logging.info('Tables created')
    else:
        logging.error(f'SQLite in connection')
