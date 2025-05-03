# city_processor.py
import pandas as pd
from my_llm_function import generate_neighbourhood_safety_json
from external_sources import fetch_articles, fetch_emoji_data, fetch_vibe_tags

def process_city_data(city: str):
    """
    1. Pull live data for <city> from your own APIs or DB
    2. Pass it to generate_neighbourhood_safety_json()
    3. Return the structured JSON
    """

    # Replace these with your real API calls
    articles       = fetch_articles(city)          # List[dict]
    emoji_table    = fetch_emoji_data(city)        # pandas DataFrame
    vibe_keywords  = fetch_vibe_tags(city)         # Dict[str, List[str]]

    return generate_neighbourhood_safety_json(
        articles, emoji_table, vibe_keywords
    )
