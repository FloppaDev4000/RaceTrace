from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
from core_api.collectors.calendar.athleticsIreland import AthleticsIrelandCollector
from core_api.models import Race
from core_api.collectors import parsing

# hard coded (FOR NOW!!)
# URL = r"https://www.athleticsireland.ie/competitions-events/fixtures-results/"

# # set up headers for scraping
# HEADERS = {"User-Agent": "RaceTrace student project"}

class Command(BaseCommand):
    collectors = [AthleticsIrelandCollector]

    help = "Collect races from Athletics Ireland and store to DB" # HARD CODED

    def handle(self, *args, **options):

        # get raw html from page
        # html = requests.get(URL, headers=HEADERS).text

        # # convert html data to json using specific collector
        # races = athletics_ireland.get_data(html)
        races = []
        for c in self.collectors:
            races += c.fetch_parse_data()

        # convert json to model objects
        for r in races:
            Race.objects.update_or_create(
                source="athleticsireland", # HARD CODED
                sourceId=r["id"],
                defaults={
                    "title": r["title"],
                    "dateRan": parsing.parse_date(r["date_ran"]),
                    "location": r["location"],
                    "sourceUrl": r["source_url"]
                },
            )

        # output success result
        self.stdout.write(f"saved {len(races)} races")