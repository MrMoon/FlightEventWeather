class Weather:
    def __init__(self, event_id, temperature, humidity, last_fetched):
        self.event_id = event_id
        self.temperature = temperature
        self.humidity = humidity
        self.last_fetched = last_fetched

    def __str__(self):
        return f"{self.event_id}, {self.temperature}, {self.humidity}, {self.last_fetched}"
