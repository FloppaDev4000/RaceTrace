from django.core.management.base import BaseCommand
from core_api.collectors.calendar.athleticsIreland import AthleticsIrelandCollector
from core_api.models import Race
from core_api.collectors import parsing

class Command(BaseCommand):
    collectors = [AthleticsIrelandCollector]

    help = "Collect races from Athletics Ireland and store to DB" # HARD CODED

    def handle(self, *args, **options):

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
                    "sourceUrl": r["source_url"],
                    "source": r["source"]
                },
            )

        # output success result
        self.stdout.write(f"saved {len(races)} races")