from datetime import datetime

from bs4 import BeautifulSoup
import requests
from core_api.collectors.collector import Collector

class JustRunEventsCollector(Collector):
    url = "https://justrunsevents.ie/event-results"

    def get_all_pages(self): # all until 2021 (earliest year stored)
        current_year = datetime.now().year
        pages = []
        base_url = self.url + "?year="

        while(current_year >= 2021):
            full_url = base_url + str(current_year)
            current_year -= 1

            response = requests.get(full_url)
            if response.status_code != 200:
                break
            pages += response.text
        return pages

    def get_results_from_page(self, soup: BeautifulSoup, races, bad):
        for card in soup.select("div.styles_eventContainer__YEQVz"):
            title_el = card.select_one("div.styles_eventName__6PXOq")

            row = {
                "id": "",
                "rawDate": card.select_one("div.styles_eventDateContainer__cfVp0").getText(strip=True),
                "rawTitle": title_el.getText(strip=True) if title_el else "",
                "source": self.source_name,
                "url": card.select_one("div.styles_resultsLinl__lvq3k > a").get("href", "")
            }

            (races if row["title"] else bad).append(row if row["title"] else card)

    def fetch_parse_data(self):
        all_pages = self.get_all_pages()
        races, bad = [], []
        for p in all_pages:
            soup = BeautifulSoup(p, "html.parser")
            self.get_results_from_page(soup, races, bad)
            
        return races