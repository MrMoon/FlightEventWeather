from database.database_api import insert, select, clean_unfresh_data
from models.event import Event

TABLE_NAME = "top_events"


def insert_event(event_data):
    SQL_INSERT_QUERY = f"""
    INSERT INTO {TABLE_NAME}
    (event_id, title, rank, lat, lon, country_code, last_fetched) 
    VALUES(?, ?, ?, ?, ?, ?, ?)
    """
    return insert(insert_query=SQL_INSERT_QUERY, data=(
    event_data.event_id, event_data.title, event_data.rank, event_data.lat, event_data.lon, event_data.country_code,
    event_data.last_fetched))


def select_top_10_events(country):
    SQL_SELECT_QUERY = f"""
        SELECT * FROM {TABLE_NAME} WHERE country_code = ?  ORDER BY rank DESC LIMIT 10
    """
    return select(select_query=SQL_SELECT_QUERY, params=(country,))


def clean_events():
    clean_unfresh_data(table_name=TABLE_NAME)

def get_event_by_id(event_id):
    SQL_SELECT_QUERY = f"""
            SELECT * FROM {TABLE_NAME} WHERE event_id = ?
        """
    result = select(select_query=SQL_SELECT_QUERY, params=(event_id,))
    if len(result) == 0:
        return None
    return Event(*result[0])

