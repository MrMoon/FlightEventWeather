class Event:
    def __init__(self, event_id, title, rank, lat, lon, country_code, last_fetched):
        self.event_id = event_id
        self.title = title
        self.rank = rank
        self.lat = lat
        self.lon = lon
        self.country_code = country_code
        self.last_fetched = last_fetched

    def __str__(self):
        return f"{self.event_id}, {self.title}, {self.rank}, {self.lat}, {self.lon}, {self.country_code}, {self.last_fetched}"