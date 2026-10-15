import requests
from bs4 import BeautifulSoup

URL = r"https://www.athleticsireland.ie/competitions-events/fixtures-results/"

res = requests.get(URL, headers={"User-Agent": "RaceTrace student project"})
soup = BeautifulSoup(res.text, "html.parser")

for tag in soup(["script", "style", "svg", "noscript", "header", "footer", "nav"]):
    tag.decompose()

text = soup.get_text("\n", strip=True)
open("fixtures_text.txt", "w", encoding="utf-8").write(text)
print(len(text))