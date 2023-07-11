import logging
import sqlite3
import time
from sqlite3 import Error

from database import create_table

connection = None
db_name = create_table.dbname
FRESHNESS_DURATION = 21600



def connection_to_db_file(file):
    global connection
    if connection is not None:
        return connection
    try:
        connection = sqlite3.connect(file)
        logging.debug(sqlite3.version)
    except Error as e:
        logging.error(f'SQLite Connection Error with code {e.sqlite_errorcode}, more info: {e}')

    return connection


def check_data_freshness(table_name, event_id, freshness_duration):
    cursor = connection.cursor(f"SELECT last_fetched from {table_name} WHERE event_id={event_id}")
    rows = cursor.fetchall()
    last_fetch = rows[0]
    if last_fetch is None:
        logging.error(f'Error finding event id {event_id}')
    last_fetch = int(last_fetch)
    return freshness_duration - (time.time() - last_fetch) > 0


def clean_unfresh_data(table_name):
    before_six_hours = time.time() - FRESHNESS_DURATION
    SQL_DELETE_QUERY = f"""
     DELETE FROM {table_name} WHERE last_fetched < ?
    """
    delete(delete_query=SQL_DELETE_QUERY, params=(before_six_hours,))


def insert(insert_query, data):
    if connection is None:
        connection_to_db_file(db_name)
    cursor = connection.cursor()
    cursor.execute(insert_query, data)
    connection.commit()
    return cursor.lastrowid


def select(select_query, params):
    if connection is None:
        connection_to_db_file(db_name)
    cursor = connection.cursor()
    cursor.execute(select_query, params)
    rows = cursor.fetchall()
    return rows


def delete(delete_query, params):
    if connection is None:
        connection_to_db_file(db_name)
    curses = connection.cursor()
    curses.execute(delete_query, params)
    connection.commit()
