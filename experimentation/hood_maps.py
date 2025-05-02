#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

def fetch_header_and_list(url: str) -> None:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/112.0.0.0 Safari/537.36"
        )
    }
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # Print the main header
    h1 = soup.find("h1")
    if h1:
        print(h1.get_text(strip=True))
        print()  # blank line

    # Find the first <ul> and print its items
    ul = soup.find("ul")
    if not ul:
        print("No list found.")
        return

    for li in ul.find_all("li"):
        # prints the text of each list item
        print(f"• {li.get_text(strip=True)}")

if __name__ == "__main__":
    fetch_header_and_list("https://hoodmaps.com/paris-neighborhood-map")
