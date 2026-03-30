from playwright.sync_api import sync_playwright
import re
import math
import time

print("Housing split agent started")

SEARCH_URLS = [
    "https://www.funda.nl/zoeken/koop?selected_area=%5B%22utrecht%22%5D",
    "https://www.funda.nl/zoeken/koop?selected_area=%5B%22amersfoort%22%5D",
]

def to_int(text):
    if not text:
        return None
    digits = re.sub(r"[^\d]", "", text)
    return int(digits) if digits else None
