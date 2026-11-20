
from bs4 import BeautifulSoup
import requests

from core_api.collectors.collector import Collector

class PopupRacesCollector(Collector):
    url = "https://www.popupraces.ie/race-status/finished/"
    source_name = "popupraces"

    def get_all_pages(self, pages_amount=50):
        pages = []
        base_url = self.url + "page/"

        for page in range(1, pages_amount):
            full_url = base_url.format(page)
            response = requests.get(full_url)
            if response.status_code != 200:
                break
            pages += response.text
        return pages

    def get_results_from_page(self, soup: BeautifulSoup, races, bad):
        for card in soup.select("section#results > article.card"):
            title_el = card.select_one("h1.entry-title")

            row = {
                "id": "", # no id listed in card?
                "rawDate": card.select_one("div.mobile-date-old").getText(separator=" ").split(" ")[0],
                "rawTitle": title_el.getText(strip=True) if title_el else "",
                "source": self.source_name,
                "url": title_el.get("href", "") if title_el else ""
            }

            (races if row["title"] else bad).append(row if row["title"] else card)

    @classmethod
    def fetch_parse_data(self):
        all_pages = self.get_all_pages()
        races, bad = [], []
        for p in all_pages:
            soup = BeautifulSoup(p, "html.parser")
            self.get_results_from_page(soup, races, bad)
            
        raw_data = requests.get(self.url, self.HEADERS)
        soup = BeautifulSoup(raw_data, "html.parser")