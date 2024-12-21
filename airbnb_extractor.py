from pyairbnb import search_all
import pandas as pd
import json

def extract_to_json_file(city_name, ne_lat, ne_long, sw_lat, sw_long, check_in, check_out):
    # Define search parameters
    currency = "EUR"  # Currency for the search
    zoom_value = 2  # Zoom level for the map

    # Search listings within specified coordinates and date range
    search_results = search_all(check_in, check_out, ne_lat, ne_long, sw_lat, sw_long, zoom_value, currency, "")

    # Save the search results as a JSON file
    with open(f'data/bnb/{city_name}.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(search_results))  # Convert results to JSON and write to file