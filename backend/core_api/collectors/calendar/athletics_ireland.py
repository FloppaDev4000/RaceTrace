from bs4 import BeautifulSoup
import re
from datetime import date

URL = r"https://www.athleticsireland.ie/competitions-events/fixtures-results/"
HEADERS = {"User-Agent": "RaceTrace student project"}

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

MONTHS = {"jan":1,"feb":2,"mar":3,"apr":4,"may":5,"jun":6,
    "jul":7,"aug":8,"sep":9,"oct":10,"nov":11,"dec":12}

def parse_date(text):
    day = int(re.search(r"\d{1,2}", text).group())
    month = MONTHS[re.search(r"[A-Za-z]{3}", text).group().lower()]
    year = 2000 + int(re.search(r"(\d{2})\s*$", text).group(1))
    return date(year, month, day)

def text(card, selector):
    el = card.select_one(selector)
    return el.get_text(strip=True) if el else ""