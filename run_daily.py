import requests
from bs4 import BeautifulSoup

print("Housing split agent started")

URL = "https://www.funda.nl/zoeken/koop?selected_area=%5B%22utrecht%22,%22amersfoort%22%5D"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

links = soup.find_all("a", href=True)

results = []

for link in links:
    href = link["href"]

    if "/koop/" in href:
        full_url = "https://www.funda.nl" + href

        text = link.get_text(strip=True)

        if "m²" in text:
            results.append((text, full_url))

print("\n=== GEVONDEN WONINGEN ===\n")

for i, (text, url) in enumerate(results[:10], 1):
    print(f"{i}. {text}")
    print(f"Link: {url}\n")

print("Script finished WITHOUT crashing")
