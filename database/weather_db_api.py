from database.database_api import insert, select, clean_unfresh_data
from models.weather import Weather

TABLE_NAME = "weather"


def insert_weather(weather_data: Weather):
    SQL_INSERT_QUERY = f"""
    INSERT INTO {TABLE_NAME}
    (event_id, temperature, humidity, last_fetched) 
    VALUES(?, ?, ?, ?)
    """
    return insert(insert_query=SQL_INSERT_QUERY, data=(weather_data.event_id, weather_data.temperature, weather_data.humidity, weather_data.last_fetched))


def clean_weather():
    clean_unfresh_data(table_name=TABLE_NAME)

def get_weather_by_event_id(event_id):
    SQL_SELECT_QUERY = f"""
            SELECT * FROM {TABLE_NAME} WHERE event_id = ?
        """
    result = select(select_query=SQL_SELECT_QUERY, params=(event_id,))
    if len(result) == 0:
        return None
    return Weather(*result[0])

