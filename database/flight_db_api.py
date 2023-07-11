from database.database_api import insert, select, clean_unfresh_data
from models.flight import Flight

TABLE_NAME = "flight"

def insert_flight(flight_data: Flight):
    print(flight_data)
    SQL_INSERT_QUERY = f"""
    INSERT INTO {TABLE_NAME}
    (event_id, dep_iata, arr_iata, flight_number, last_fetched) 
    VALUES(?, ?, ?, ?, ?)
    """
    return insert(insert_query=SQL_INSERT_QUERY, data=(flight_data.event_id, flight_data.dep_iata, flight_data.arr_iata, flight_data.flight_number, flight_data.last_fetched))


def clean_flight():
    clean_unfresh_data(table_name=TABLE_NAME)

def get_flights_from_event_id(event_id):
    SQL_SELECT_QUERY = f"""
                SELECT * FROM {TABLE_NAME} WHERE event_id = ?
            """
    results = select(select_query=SQL_SELECT_QUERY, params=(event_id,))
    return results

def get_flights(flight_number):
    SQL_SELECT_QUERY = f"""
            SELECT * FROM {TABLE_NAME} WHERE flight_number = ?
        """
    results = select(select_query=SQL_SELECT_QUERY, params=(flight_number,))
    if len(results) == 0:
        return None
    return results[0]


