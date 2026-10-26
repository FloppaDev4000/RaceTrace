from pathlib import Path
from datetime import date
from core_api.collectors.calendar.athletics_ireland import get_data, parse_date

FIXTURE = Path(__file__).parent / "fixtures" / "athleticsIrelandPage.html"


def test_parse_date_single_day():
    assert parse_date("10 Jan ‘26") == date(2026, 1, 10)


def test_parse_date_range_uses_first_day():
    assert parse_date("17-18 Jan ‘26") == date(2026, 1, 17)


def test_parser_finds_races():
    html = FIXTURE.read_text(encoding="utf-8")
    races = get_data(html)
    assert len(races) > 0
    assert races[0]["title"]
    assert races[0]["id"]