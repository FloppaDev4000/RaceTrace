from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from core_api.collectors.calendar import athletics_ireland
from core_api.models import Race


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
                    "dateRan": athletics_ireland.parse_date(r["date_ran"]),
                    "location": r["location"],
                    "sourceUrl": r["source_url"]
                },
            )
        self.stdout.write(f"saved {len(races)} races")