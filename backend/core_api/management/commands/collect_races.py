from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from core_api.collectors.calendar import athletics_ireland
from core_api.models import Race
import re
from datetime import date

MONTHS = {"jan":1,"feb":2,"mar":3,"apr":4,"may":5,"jun":6,
          "jul":7,"aug":8,"sep":9,"oct":10,"nov":11,"dec":12}

URL = r"https://www.athleticsireland.ie/competitions-events/fixtures-results/"
HEADERS = {"User-Agent": "RaceTrace student project"}

class Command(BaseCommand):
    help = "Collect races from Athletics Ireland and store to DB"

    def handle(self, *args, **options):
        html = requests.get(URL, headers=HEADERS).text
        races = athletics_ireland.get_data(html)

        for r in races:
            Race.objects.update_or_create(
                source="athleticsireland",
                sourceId=r["id"],
                defaults={
                    "title": r["title"],
                    "dateRan": parse_date(r["date_ran"]),
                    "location": r["location"],
                    "sourceUrl": r["source_url"]
                },
            )
        self.stdout.write(f"saved {len(races)} races")


def text(card, selector):
    el = card.select_one(selector)
    return el.get_text(strip=True) if el else ""

def parse_date(text):
    day = int(re.search(r"\d{1,2}", text).group())
    month = MONTHS[re.search(r"[A-Za-z]{3}", text).group().lower()]
    year = 2000 + int(re.search(r"(\d{2})\s*$", text).group(1))
    return date(year, month, day)