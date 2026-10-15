import requests, json

URL = r"https://www.athleticsireland.ie/wp-json/wp/v2/fixture"
HEADERS = {"User-Agent": "RaceTrace student project"}
PARAMS = {"per_page": 3}

res = requests.get(URL, params=PARAMS, headers=HEADERS)
print("Total:", res.headers.get("X-WP-Total"), "Pages:", res.headers.get("X-WP-TotalPages"))
print(json.dumps(res.json()[0], indent=2))