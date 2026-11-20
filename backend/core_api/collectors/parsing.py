from datetime import date
import re

# const dict of indexed months
MONTHS = {"jan":1,"feb":2,"mar":3,"apr":4,"may":5,"jun":6,
    "jul":7,"aug":8,"sep":9,"oct":10,"nov":11,"dec":12}

# parse date from date string
def parse_date(text):
    day = int(re.search(r"\d{1,2}", text).group())
    month = MONTHS[re.search(r"[A-Za-z]{3}", text).group().lower()]
    year = 2000 + int(re.search(r"(\d{2})\s*$", text).group(1))
    return date(year, month, day)

# get text from card using specified selector
def text(card, selector):
    el = card.select_one(selector)
    return el.get_text(strip=True) if el else ""