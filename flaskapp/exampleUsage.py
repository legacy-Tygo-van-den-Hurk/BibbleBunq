from my_llm_function import generate_neighbourhood_safety_json

result = generate_neighbourhood_safety_json(articles, emoji_table)
print(result)

#in flask pipeline

def process_city_data(city):
    articles      = fetch_articles(city)      # list of dicts
    emoji_table   = fetch_emoji_data(city)    # DataFrame
    return generate_neighbourhood_safety_json(articles, emoji_table)
