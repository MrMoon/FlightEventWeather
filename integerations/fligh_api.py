import time

from database.flight_db_api import get_flights, insert_flight, clean_flight, get_flights_from_event_id
from integerations.events_api import get_event
from middleware.api_call import get_call
from models.flight import Flight

API_KEY = "02fb1dae-93a0-449d-b205-ee59f5d99b60"
DISTANCE = 200
TABLE_NAME = "flight"


def request_flight_to_event(lan, lon, airport_code):
    airport_code_icao_code = get_call(
        url=f"https://airlabs.co/api/v9/airports?iata_code={airport_code}&api_key={API_KEY}",
        headers={},
        params={},
    )
    airport_code_icao_code = airport_code_icao_code['response'][0]['icao_code']

    event_airports_nearby_response = get_call(
        url=f"https://airlabs.co/api/v9/nearby?lat={lan}&lng={lon}&distance={DISTANCE}&api_key={API_KEY}",
        params={},
        headers={}
    )
    airports = event_airports_nearby_response['response']['airports']
    if airports is None:
        return None

    flights = []
    options = []
    if len(airports) > 5:
        airports = airports[:5]
    for airport in airports:
        # https://airlabs.co/api/v9/routes?api_key=02fb1dae-93a0-449d-b205-ee59f5d99b60&dep_iata=CMB&arr_iata=AUH
        if 'iata_code' in airport:
            options = get_call(
                url=f"https://airlabs.co/api/v9/routes?api_key={API_KEY}&dep_iata={airport_code}&arr_iata={airport['iata_code']}",
                headers={},
                params={},
            )
        else:
            options = get_call(
                url=f"https://airlabs.co/api/v9/routes?api_key={API_KEY}&dep_icao={airport_code_icao_code}&arr_icao={airport['icao_code']}",
                headers={},
                params={},
            )
        options = options['response']
        if len(options) == 0:
            continue
        flights.append(options)
    return flights


def flight_to_event(event_id, airport_code):
    clean_flight()

    flights = get_flights_from_event_id(event_id)
    if len(flights) != 0:
        return flights

    event = get_event(event_id)
    if event is None:
        return "Event not found"
    flights = request_flight_to_event(event.lat, event.lon, airport_code)
    flights = [flight for sub in flights for flight in sub]
    for flight in flights:
        if get_flights(flight_number=flight['flight_number']) is None:
            insert_flight(Flight(event_id=event_id, dep_iata=flight['dep_iata'], arr_iata=flight['arr_iata'], flight_number=flight['flight_number'], last_fetched=int(time.time())))
    return flights

