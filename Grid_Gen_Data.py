import os
import requests

def fetch_grid_generation_mix():
    api_key = os.getenv("EIA_API_KEY", "YOUR_EIA_KEY")
    # EIA v2 API Endpoint for Hourly Generation by Fuel Type
    endpoint = "https://api.eia.gov/v2/electricity/rto/fuel-type-data/data/"
    
    params = {
        "api_key": api_key,
        "frequency": "hourly",
        "data[0]": "value",
        "sort[0][column]": "period",
        "sort[0][direction]": "desc",
        "length": 5
    }
    
    response = requests.get(endpoint, params=params)
    
    if response.status_code == 200:
        payload = response.json()
        records = payload.get("response", {}).get("data", [])
        
        print("--- Telemetry: Recent Grid Fuel Generation ---")
        for entry in records:
            fuel = entry.get("fueltype")
            mw_val = entry.get("value")
            timestamp = entry.get("period")
            print(f"[{timestamp}] Fuel Type: {fuel} | Generation: {mw_val} MW")
    else:
        print(f"Failed to query grid data: HTTP {response.status_code}")

# Example Run
fetch_grid_generation_mix()