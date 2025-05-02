#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import re

# ——— Configure city here ———
city_lower = "bengaluru"               # lowercase for URL
city_title = city_lower.capitalize()   # Title-case for matching

def fetch_neighborhood_list(city_lower: str, city_title: str):
    url = f"https://hoodmaps.com/{city_lower}-neighborhood-map"
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/112.0.0.0 Safari/537.36"
        )
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    resp.encoding = "utf-8"
    html = resp.text

    prefix = f"{city_title} Neighborhood Map:"
    # capture everything between the tag that contains the prefix and its closing tag
    pattern = rf"<em[^>]*>\s*{re.escape(prefix)}\s*(.+?)</em>"
    match = re.search(pattern, html, flags=re.DOTALL | re.IGNORECASE)
    if not match:
        print(f"❌ Could not find the “{prefix}” block.")
        return

    # full comma-separated payload
    payload = match.group(1).strip()

    # split on commas
    entries = [e.strip() for e in payload.split(",") if e.strip()]

    for entry in entries:
        if ":" in entry:
            name, desc = entry.split(":", 1)
            print(f"{name.strip()}: {desc.strip()}")
        else:
            print(entry)

if __name__ == "__main__":
    fetch_neighborhood_list(city_lower, city_title)
