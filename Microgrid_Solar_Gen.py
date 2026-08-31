import os
import requests

def get_regional_solar_conditions(city_name="Douala"):
    # Always pull keys from environment variables for security
    api_key = os.getenv("OPENWEATHER_API_KEY", "YOUR_OPENWEATHER_KEY")
    endpoint = "https://api.openweathermap.org/data/2.5/weather"
    
    params = {
        "q": city_name,
        "appid": api_key,
        "units": "metric"
    }
    
    response = requests.get(endpoint, params=params)
    
    if response.status_code == 200:
        data = response.json()
        cloudiness = data["clouds"]["all"] # % cloud cover
        temp = data["main"]["temp"]
        
        # Simple microgrid solar generation estimate logic
        solar_capacity_factor = max(0, (100 - cloudiness) / 100.0)
        
        print(f"--- Weather Telemetry for {city_name} ---")
        print(f"Temperature: {temp}°C")
        print(f"Cloud Cover: {cloudiness}%")
        print(f"Estimated Solar Output Factor: {solar_capacity_factor * 100:.1f}%\n")
    else:
        print(f"Error fetching data: HTTP {response.status_code}")

# Example Run
get_regional_solar_conditions("Douala")