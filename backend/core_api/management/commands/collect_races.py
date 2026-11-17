from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup
from core_api.collectors.calendar import athletics_ireland
from core_api.models import Race

# hard coded (FOR NOW!!)
URL = r"https://www.athleticsireland.ie/competitions-events/fixtures-results/"

# set up headers for scraping
HEADERS = {"User-Agent": "RaceTrace student project"}

class Command(BaseCommand):
    help = "Collect races from Athletics Ireland and store to DB" # HARD CODED

    def handle(self, *args, **options):

        # get raw html from page
        html = requests.get(URL, headers=HEADERS).text

        # convert html data to json using specific collector
        races = athletics_ireland.get_data(html)

        # convert json to model objects
        for r in races:
            Race.objects.update_or_create(
                source="athleticsireland", # HARD CODED
                sourceId=r["id"],
                defaults={
                    "title": r["title"],
                    "dateRan": athletics_ireland.parse_date(r["date_ran"]),
                    "location": r["location"],
                    "sourceUrl": r["source_url"]
                },
            )

        # output success result
        self.stdout.write(f"saved {len(races)} races")