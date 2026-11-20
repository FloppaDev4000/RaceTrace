import pytest
from pathlib import Path
from django.core.management import call_command
from core_api.models import Race

# test to ensure collector is idempotent
@pytest.mark.django_db
def test_athleticsireland_collector_is_idempotent(monkeypatch):
    fixture = Path(__file__).parent / "fixtures" / "athleticsIrelandPage.html"
    html = fixture.read_text(encoding="utf-8")

    class FakeResponse:
        text = html

    monkeypatch.setattr("requests.get", lambda *a, **k: FakeResponse())

    call_command("collect_races")
    first = Race.objects.count()

    call_command("collect_races")
    assert Race.objects.count() == first
    assert first > 0

@pytest.mark.django_db
def test_popupraces_collector_is_idempotent(monkeypatch):
    fixture = Path(__file__).parent / "fixtures" / "athleticsIrelandPage.html"
    html = fixture.read_text(encoding="utf-8")

    class FakeResponse:
        text = html

    monkeypatch.setattr("requests.get", lambda *a, **k: FakeResponse())

    call_command("collect_races")
    first = Race.objects.count()

    call_command("collect_races")
    assert Race.objects.count() == first
    assert first > 0