import requests
import re
import json

# URL of the page
url = "https://www.pumangol.co.ao/pt/institucional/mapa-de-postos-de-abastecimento"  # Replace with actual URL

# Fetch the page content
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Find the JavaScript block containing 'stores' data
    match = re.search(r'const stores = ({.*?});', response.text, re.DOTALL)
    
    if match:
        # Extract the stores object from the JavaScript code
        stores_data_str = match.group(1)

        # Dynamically sanitize the data:
        # 1. Remove trailing commas
        stores_data_str = re.sub(r',\s*}', '}', stores_data_str)  # Remove trailing commas before closing curly brace
        stores_data_str = re.sub(r',\s*]', ']', stores_data_str)  # Remove trailing commas before closing square bracket

        # 2. Replace single quotes with double quotes
        stores_data_str = stores_data_str.replace("'", '"')

        # Debug: Print the updated string after replacement
        print("Updated stores data string (after sanitization):")
        print(stores_data_str)

        # Parse the JSON string into a Python dictionary
        try:
            stores_data = json.loads(stores_data_str)
            # Process the stores data
            gas_station_data = []
            for feature in stores_data['features']:
                coordinates = feature['geometry']['coordinates']
                properties = feature['properties']
                gas_station_data.append({
                    'name': properties['title'],
                    'address': properties['address'],
                    'city': properties['city'],
                    'state': properties['state'],
                    'country': properties['country'],
                    'latitude': coordinates[1],
                    'longitude': coordinates[0]
                })

            # Save extracted gas station data into a JSON file
            with open('gas_stations.json', 'w', encoding='utf-8') as f:
                json.dump(gas_station_data, f, ensure_ascii=False, indent=4)

            print("Data saved to gas_stations.json")

        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
    else:
        print("Stores data not found in the page.")
else:
    print(f"Failed to fetch data: {response.status_code}")
