#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import re
import requests
import feedparser
from urllib.parse import quote_plus
from datetime import datetime, timedelta
from bs4 import BeautifulSoup  # Import BeautifulSoup for HTML cleaning



def process_city_data(city_lower: str):
    city_title = city_lower.capitalize()  # Title-case for matching
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

    list_of_crimes = ["crime"]

    news_list= []

    # split on commas
    entries = [e.strip() for e in payload.split(",") if e.strip()]
    for entry in entries:
        if ":" in entry:
            name, desc = entry.split(":", 1)

            neighbour_info = {
                "neighbourhood": name.strip(),
                "description": desc.strip(),
                "news": news_per_neighborhood(name.strip(), city_title, list_of_crimes)
            }
            news_list.append(neighbour_info)
        
    return news_list

def news_per_neighborhood(neighborhood, city, keywords):
    start_date = None  # Optional, format YYYY-MM-DD
    end_date = None  # Optional, format YYYY-MM-DD
    # Combine neighborhood, city, and keywords into a single query
    query = f"{neighborhood} {city} " + " ".join(keywords)

    # URL encode the query to ensure spaces are properly handled
    encoded_query = quote_plus(query)  # Converts spaces to '+', etc.
    url = f"https://news.google.com/rss/search?q={encoded_query}+near+me&hl=en-US&gl=US&ceid=US:en"

    # Parse the RSS feed
    feed = feedparser.parse(url)

    # Parse the date range (if any)
    if start_date:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
    if end_date:
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

    # List to collect summaries
    summaries = []

    i = 0

    # Process each entry in the feed
    for entry in feed.entries:
        i += 1
        if i > 15:
            break
        # Convert published date to datetime
        published_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z")

        # Filter by date range
        if start_date and published_date < start_date:
            continue
        if end_date and published_date > end_date:
            continue

        # Extract summary or content (the text of the article)
        text = entry.summary if 'summary' in entry else "No summary available"
        
        # Clean HTML from the summary text
        clean_text = BeautifulSoup(text, "html.parser").get_text()

        # Add the cleaned summary to the list
        summaries.append(clean_text)

    return summaries  # Return the list of summaries



    






   