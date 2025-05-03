import requests
import feedparser
from urllib.parse import quote_plus
from datetime import datetime, timedelta

def get_google_news_rss(neighborhood, city, keywords, start_date=None, end_date=None):
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

    # Display the results
    for entry in feed.entries:
        # Convert published date to datetime
        published_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z")

        # Filter by date range
        if start_date and published_date < start_date:
            continue
        if end_date and published_date > end_date:
            continue

        # Extract title, link, published date, and text
        print(f"Title: {entry.title}")
        print(f"Link: {entry.link}")
        print(f"Published: {published_date.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Extract summary or content (the text of the article)
        text = entry.summary if 'summary' in entry else "No summary available"
        print(f"Text: {text}")
        print()

# Example usage
neighborhood = "Halsoor"
city = "Bengaluru"
keywords = ["crime"]
start_date = "2023-09-01"  # Optional, format YYYY-MM-DD

get_google_news_rss(neighborhood, city, keywords, start_date, end_date = None)
