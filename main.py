from fastapi import FastAPI

from database.create_table import database_init
from integerations.events_api import top_10_events
from integerations.fligh_api import flight_to_event
from integerations.weather_api import weather_at_event

app = FastAPI()

database_init()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    if name is None:
        name = "World"
    return {"message": f"Hello {name}"}


@app.get("/list/{country_code}")
async def list_top_10_events(country_code: str):
    return top_10_events(country_code=country_code)


@app.get("/weather/{event_id}")
async def weather(event_id):
    return weather_at_event(event_id=event_id)


@app.get("/flighs/{event_id}/{airport_code}")
async def flight(event_id, airport_code):
    return flight_to_event(event_id=event_id, airport_code=airport_code)
