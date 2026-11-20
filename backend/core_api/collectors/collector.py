class Collector:
    url = ""
    source_name = ""
    HEADERS = {"User-Agent": "RaceTrace student project"}

    @classmethod
    def fetch_parse_data(self): ...