from pathlib import Path
from datetime import date
from core_api.collectors.calendar.athletics_ireland import get_data
from core_api.collectors.parsing import parse_date
FIXTURE = Path(__file__).parent / "fixtures" / "athleticsIrelandPage.html"

# date parser works on single day
def test_parse_date_single_day():
    assert parse_date("10 Jan ‘26") == date(2026, 1, 10)

# date parser gets first date from date range
def test_parse_date_range_uses_first_day():
    assert parse_date("17-18 Jan ‘26") == date(2026, 1, 17)

# html parser finds relevant races
def test_parser_finds_races():
    html = FIXTURE.read_text(encoding="utf-8")
    races = get_data(html)
    assert len(races) > 0
    assert races[0]["title"]
    assert races[0]["id"]