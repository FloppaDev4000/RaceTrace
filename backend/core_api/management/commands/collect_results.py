#popupraces version

from django.core.management.base import BaseCommand
from core_api.collectors.result.popup_races import PopupRacesCollector
from core_api.models import Race
from core_api.collectors import parsing

class Command(BaseCommand):
    collectors = [PopupRacesCollector]

    help = "Collect results from Popup Races and store to DB" # HARD CODED

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
                    "rawTitle": r["rawTitle"],
                    "rawDate": parsing.parse_date(r["rawDate"]),
                    "url": r["url"],
                    "source": r["source"]
                },
            )

        # output success result
        self.stdout.write(f"saved {len(races)} races")