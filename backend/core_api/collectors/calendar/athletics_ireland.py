from bs4 import BeautifulSoup

import parsing

# parse raw html, turn into json race list for athleticsIreland
def get_data(html):
    soup = BeautifulSoup(html, "html.parser")

    # init lists of good and bad results
    races, bad = [], []

    # loop over every fixture card
    for card in soup.select("div.fixture-card"):

        # get title element
        title_el = card.select_one(".font-semibold")

        # get data for race
        row = {
            "id": card.parent.get("data-fixture-id", ""),
            "date_ran": text(card, "div[class*='icon--calendar'] span"),
            "title": title_el.get_text(strip=True) if title_el else "", # only if title element exists
            "source_url": title_el.get("href", "") if title_el else "", # only if title element exists
            "location": text(card, "div[class*='icon--map-pin'] span"),
            "level": text(card, "span.pill")
        }

        # if row has a title, the race is good. append row to "races"
        # if row couldnt get title, the race is bad. append entire card to "bad"
        (races if row["title"] else bad).append(row if row["title"] else card)
    return races