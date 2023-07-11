class Flight:
    def __init__(self, event_id, dep_iata, arr_iata, flight_number, last_fetched):
        self.event_id = event_id
        self.dep_iata = dep_iata
        self.arr_iata = arr_iata
        self.flight_number = flight_number
        self.last_fetched = last_fetched

    def __str__(self):
        return f"{self.event_id}, {self.dep_iata}, {self.arr_iata}, {self.flight_number}, {self.last_fetched}"