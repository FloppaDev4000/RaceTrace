#popupraces version

from django.core.management.base import BaseCommand
from core_api.collectors.result.just_run_events import JustRunEventsCollector
from core_api.collectors.result.popup_races import PopupRacesCollector
from core_api.models import Result
from core_api.collectors import parsing

class Command(BaseCommand):
    p = PopupRacesCollector()
    j = JustRunEventsCollector()
    collectors = [p, j]

    help = "Collect results from all results sources and store to DB"

    def handle(self, *args, **options):
        results = []
        for c in self.collectors:
            results += c.fetch_parse_data()

        # convert json to model objects
        for r in results:
            Result.objects.update_or_create(
                source=r["source"],
                sourceId=r["id"],
                defaults={
                    "rawTitle": r["rawTitle"],
                    "rawDate": parsing.parse_date(r["rawDate"]),
                    "url": r["url"]
                },
            )

        # output success result
        self.stdout.write(f"saved {len(results)} results")