# main.py

import requests
from flask import Flask, jsonify, request
from city_processor import process_city_data

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
    
    if not city:
        return jsonify({"error": "City parameter is required!"}), 400

    # Step 1: Process the city data using the Langchain agent
    processed_data = process_city_data(city)

    json_str = json.dumps(processed_data, indent=4)

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
