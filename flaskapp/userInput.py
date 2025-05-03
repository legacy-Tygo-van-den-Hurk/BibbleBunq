
import pandas as pd
import random
from faker import Faker

def generate_synthetic_tourist_data(
    num_cities: int = 50,
    neighborhoods_per_city: int = 10,
    places_per_neighborhood: int = 5,
    emoji_types: int = 5
) -> pd.DataFrame:
    """
    Generates a table of synthetic tourist data with realistic-looking names using Faker.
    
    - num_cities: number of unique city names to generate
    - neighborhoods_per_city: number of neighborhoods per city
    - places_per_neighborhood: number of famous places per neighborhood
    - emoji_types: number of distinct emoji columns (Emoji 1 … Emoji N)
    """
    faker = Faker()
    Faker.seed(42)
    random.seed(42)

    data = []
    emojis = list(range(1, emoji_types + 1))

    cities = [faker.unique.city() for _ in range(num_cities)]

    for city in cities:
        neighborhoods = [
            f"{faker.unique.street_name()} {random.choice(['District', 'Quarter', 'Neighborhood', 'Zone'])}"
            for _ in range(neighborhoods_per_city)
        ]

        for neighborhood in neighborhoods:
            places = [
                f"{faker.unique.company()} {random.choice(['Museum', 'Park', 'Square', 'Palace', 'Center', 'Gallery'])}"
                for _ in range(places_per_neighborhood)
            ]

            for place in places:
               # --- inside generate_synthetic_tourist_data ---------------------------------
                row = {
                    "city": city,                     # was "City"
                    "neighbourhood": neighborhood,    # was "Neighborhood"
                    "place": place                    # was "Famous Place"
                }
                for emoji in emojis:                  # 1 … 5
                    row[f"emoji_{emoji}"] = random.randint(0, 100)   # was f"Emoji {emoji}"

                data.append(row)

    df = pd.DataFrame(data)
    return df

# if __name__ == "__main__":
#     df = generate_synthetic_tourist_data()
#     print(df.head())
#     print("Total rows:", df.shape[0])



# df['Total Emojis'] = df[['Emoji 1', 'Emoji 2', 'Emoji 3', 'Emoji 4', 'Emoji 5']].sum(axis=1)


# df_sorted = (
#     df
#     .sort_values(by="Emoji 4", ascending=False)
#     .rename(columns={"Emoji 4": "Safety"})
# )
# main.py

