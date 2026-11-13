from bs4 import BeautifulSoup
import re
from datetime import date

# parse raw html, turn into json race list for athleticsIreland
def get_data(html):
    soup = BeautifulSoup(html, "html.parser")

    # init lists of good and bad results
    races, bad = [], []

    # loop over every fixture card
    for card in soup.select("div.fixture-card"):

        # get title element
        title_el = card.select_one(".font-semibold")

        # get data for race
        row = {
            "id": card.parent.get("data-fixture-id", ""),
            "date_ran": text(card, "div[class*='icon--calendar'] span"),
            "title": title_el.get_text(strip=True) if title_el else "", # only if title element exists
            "source_url": title_el.get("href", "") if title_el else "", # only if title element exists
            "location": text(card, "div[class*='icon--map-pin'] span"),
            "level": text(card, "span.pill")
        }

        # if row has a title, the race is good. append row to "races"
        # if row couldnt get title, the race is bad. append entire card to "bad"
        (races if row["title"] else bad).append(row if row["title"] else card)
    return races

# const dict of indexed months
MONTHS = {"jan":1,"feb":2,"mar":3,"apr":4,"may":5,"jun":6,
    "jul":7,"aug":8,"sep":9,"oct":10,"nov":11,"dec":12}

# parse date from date string
def parse_date(text):
    day = int(re.search(r"\d{1,2}", text).group())
    month = MONTHS[re.search(r"[A-Za-z]{3}", text).group().lower()]
    year = 2000 + int(re.search(r"(\d{2})\s*$", text).group(1))
    return date(year, month, day)

# get text from card using specified selector
def text(card, selector):
    el = card.select_one(selector)
    return el.get_text(strip=True) if el else ""