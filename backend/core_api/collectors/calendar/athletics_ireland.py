import requests
from bs4 import BeautifulSoup

URL = r"https://www.athleticsireland.ie/competitions-events/fixtures-results/"
HEADERS = {"User-Agent": "RaceTrace student project"}

def text(card, selector):
    el = card.select_one(selector)
    return el.get_text(strip=True) if el else ""

def get_data(html):
    soup = BeautifulSoup(html, "html.parser")

    card = soup.select_one("div.fixture-card")
    print(card.parent.attrs)

    races, bad = [], []
    for card in soup.select("div.fixture-card"):
        title_el = card.select_one(".font-semibold")
        row = {
            "id": card.parent.get("data-fixture-id", ""),
            "date_ran": text(card, "div[class*='icon--calendar'] span"),
            "title": title_el.get_text(strip=True) if title_el else "",
            "source_url": title_el.get("href", "") if title_el else "",
            "location": text(card, "div[class*='icon--map-pin'] span"),
            "level": text(card, "span.pill")
        }
        (races if row["title"] else bad).append(row if row["title"] else card)

    return races