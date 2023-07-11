import logging
import time

from database.events_db_api import get_event_by_id, insert_event, select_top_10_events, clean_events
from middleware.api_call import get_call
from models.event import Event


def request_event_for_country(country_code):
    response = get_call(
        url=f"https://api.predicthq.com/v1/events/?country={country_code}&sort=rank&limit=10",
        params={},
        headers={
            "Authorization": "Bearer EqpJf87ypBIW6cbbhkXRj_HOyxkNezMRw66NdI86",
            "Accept": "application/json"
        }
    )
    if "results" not in response:
        return None
    response = response['results']
    events = []
    for data in response:
        events.append(
            Event(data['id'], data['title'], data['rank'], data['location'][1], data['location'][0], country_code,
                  int(time.time())))
    return events


def get_event(event_id):
    return get_event_by_id(event_id=event_id)


def top_10_events(country_code):
    clean_events()
    events = request_event_for_country(country_code)
    if events is None:
        return f"No events in {country_code}"
    for vent in events:
        logging.info(vent.__str__())
        if get_event(event_id=vent.event_id) is None:
            insert_event(vent)
    events = select_top_10_events(country_code)
    if len(events) == 0:
        return f"No events where found in {country_code}"
    return events
