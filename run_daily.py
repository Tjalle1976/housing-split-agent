import re
import math
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

print("Housing split agent started")

BASE_URL = "https://www.funda.nl"
SEARCH_URLS = [
    "https://www.funda.nl/zoeken/koop?selected_area=%5B%22utrecht%22%5D",
    "https://www.funda.nl/zoeken/koop?selected_area=%5B%22amersfoort%22%5D",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "nl-NL,nl;q=0.9,en;q=0.8",
}

MAX_DETAIL_PAGES = 20


def to_int(text):
    if not text:
        return None
    digits = re.sub(r"[^\d]", "", text)
    return int(digits) if digits else None


def estimate_units(living_area):
    if not living_area:
        return None
    if living_area >= 240:
        return 4
    if living_area >= 180:
        return 3
    if living_area >= 140:
        return 2
    return 1


def estimate_profit(price, living_area, units):
    if not price or not living_area or not units or units < 2:
        return None

    renovation = living_area * 1200
    extra_costs = price * 0.10
    total_cost = price + renovation + extra_costs

    unit_size = living_area / units

    if unit_size >= 75:
        resale_per_m2 = 6000
    elif unit_size >= 60:
        resale_per_m2 = 6200
    else:
        resale_per_m2 = 5800

    exit_value = living_area * resale_per_m2
    return round(exit_value - total_cost)


def score_listing(price_per_m2, text):
    score = 0.0

    if price_per_m2:
        score += max(0, 7000 - price_per_m2) / 1000

    text_l = text.lower()

    keywords = [
        "dubbele entree",
        "eigen toegang",
        "beleggingspand",
        "kamerverhuur",
        "praktijkruimte",
        "winkel",
        "bovenwoning",
        "dubbel bovenhuis",
        "gastenverblijf",
        "inwoning",
        "zelfstandig appartement",
        "meerdere badkamers",
        "meerdere keukens",
    ]

    for kw in keywords:
        if kw in text_l:
            score += 2

    return round(score, 2)


def collect_listing_links(search_url):
    print(f"Scanning search page: {search_url}")
    response = requests.get(search_url, headers=HEADERS, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    links = []

    for a in soup.find_all("a", href=True):
        href = a["href"]

        # pak koop-detailpagina's
        if "/koop/" in href:
            full_url = urljoin(BASE_URL, href.split("?")[0])
            if full_url not in links:
                links.append(full_url)

    return links


def parse_detail_page(url):
    response = requests.get(url, headers=HEADERS, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    text = soup.get_text(" ", strip=True)

    # titel/adres
    title = None
    if soup.title:
        title = soup.title.get_text(" ", strip=True)

    h1 = soup.find("h1")
    if h1:
        address = h1.get_text(" ", strip=True)
    elif title:
        address = title
    else:
        address = "Onbekend adres"

    # prijs
    price_match = re.search(r"€\s?[\d\.\,]+", text)
    price = to_int(price_match.group(0)) if price_match else None

    # alle m² waarden vinden, dan een plausibele woonoppervlakte kiezen
    m2_matches = re.findall(r"(\d+)\s?m²", text)
    m2_values = [int(x) for x in m2_matches if 40 <= int(x) <= 1000]
    living_area = m2_values[0] if m2_values else None

    price_per_m2 = round(price / living_area) if price and living_area else None
    units = estimate_units(living_area)
    profit = estimate_profit(price, living_area, units)
    score = score_listing(price_per_m2, text)

    return {
        "address": address,
        "price": price,
        "living_area": living_area,
        "price_per_m2": price_per_m2,
        "units": units,
        "profit": profit,
        "score": score,
        "url": url,
    }


def main():
    try:
        all_links = []

        for search_url in SEARCH_URLS:
            try:
                links = collect_listing_links(search_url)
                all_links.extend(links)
                time.sleep(2)
            except Exception as e:
                print(f"ERROR search page {search_url}: {e}")

        # dedupe
        all_links = list(dict.fromkeys(all_links))
        print(f"Found {len(all_links)} listing links")

        if not all_links:
            print("No links found")
            print("Script finished WITHOUT crashing")
            return

        results = []
        for url in all_links[:MAX_DETAIL_PAGES]:
            try:
                item = parse_detail_page(url)
                if item["living_area"] and item["price"]:
                    results.append(item)
                time.sleep(1)
            except Exception as e:
                print(f"ERROR detail page {url}: {e}")

        if not results:
            print("No parsable detail pages found")
            print("Script finished WITHOUT crashing")
            return

        # eerst beste score, daarna laagste €/m²
        results.sort(key=lambda x: (-(x["score"] or 0), x["price_per_m2"] or math.inf))

        print("\n=== TOP KANDIDATEN ===\n")
        for i, item in enumerate(results[:10], 1):
            print(f"{i}. {item['address']}")
            print(f"Vraagprijs: € {item['price']:,}".replace(",", ".") if item["price"] else "Vraagprijs: onbekend")
            print(f"Woonoppervlak: {item['living_area']} m²" if item["living_area"] else "Woonoppervlak: onbekend")
            print(f"€/m²: € {item['price_per_m2']:,}".replace(",", ".") if item["price_per_m2"] else "€/m²: onbekend")
            print(f"Verwachte units: {item['units']}" if item["units"] else "Verwachte units: onbekend")
            print(f"Geschatte winst: € {item['profit']:,}".replace(",", ".") if item["profit"] is not None else "Geschatte winst: onbekend")
            print(f"Score: {item['score']}")
            print(f"Link: {item['url']}\n")

    except Exception as e:
        print(f"FATAL ERROR: {e}")

    print("Script finished WITHOUT crashing")


if __name__ == "__main__":
    main()
