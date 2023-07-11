import logging
import time
from datetime import datetime

from database.weather_db_api import clean_weather, get_weather_by_event_id, insert_weather
from integerations.events_api import get_event
from middleware.api_call import get_call
from models.weather import Weather

TABLE_NAME = 'weather'


def request_weather_from_event_id(event_id):
    event = get_event(event_id=event_id)
    if event is None:
        return 'Event not found'
    lat, lon = event.lat, event.lon
    response = get_call(
        url=f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=76bb4f85a8a16691dd9cd391e9114e68',
        headers={},
        params={}
    )
    if response['main'] is None:
        return None
    response = response['main']
    return Weather(event_id=event_id, temperature=f"{response['temp'] - 273.15:.2f} Celsius",
                   humidity=f"{response['humidity']}%", last_fetched=int(time.time()))


def weather_at_event(event_id):
    clean_weather()
    weather = request_weather_from_event_id(event_id)
    if weather is None:
        return 'Weather not found'
    logging.info(weather.__str__())
    if get_weather_by_event_id(event_id=weather.event_id) is None:
        insert_weather(weather)

    weather.last_fetched = datetime.utcfromtimestamp(weather.last_fetched).strftime('%Y-%m-%d %H:%M:%S.%f+00:00 (UTC)')
    return weather
