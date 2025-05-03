# main.py

import requests
from flask import Flask, jsonify, request
from city_processor import process_city_data
from userInput import generate_synthetic_tourist_data
from something import generate_neighbourhood_safety_json

app = Flask(__name__)

# External API URL where we'll send the processed data
EXTERNAL_API_URL = "https://httpbin.org/post"   # echoes your JSON back


import json
from pathlib import Path
from typing import List, Any, Optional


@app.route('/process_city', methods=['POST'])
def process_city():
    # Get the city from the incoming request
    city = request.json.get('city')
    print(f"Received city: {city}")
    
    if not city:
        return jsonify({"error": "City parameter is required!"}), 400

    # Step 1: Process the city data using the Langchain agent
    city = city.lower()
    processed_data = process_city_data(city)

    json_str = json.dumps(processed_data, indent=4)
    df = generate_synthetic_tourist_data()
    df_str = df.to_string(index=False)

    articles       = []          # List[dict]
    emoji_table    = df       # pandas DataFrame
    vibe_keywords  = processed_data        # Dict[str, List[str]]

    final_json = generate_neighbourhood_safety_json(
          vibe_keywords, emoji_table
    )

    print(f"Processed data: {final_json}")


    # Step 2: Send the processed data to an external API via POST request
    external_response = send_to_external_api(processed_data)

    return jsonify({"status": "success", "external_response": external_response.json()}), 200


# Function to send data to an external source via a POST request
def send_to_external_api(data):
    payload = {"city_info": data}
    headers = {"Content-Type": "application/json"}
    
    # Make the POST request to the external API
    response = requests.post(EXTERNAL_API_URL, json=payload, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to send data to external API: {response.status_code}")
    
    return response


if __name__ == '__main__':
    app.run(debug=True)
