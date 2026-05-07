import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_weather_and_aqi(city):
    # Sabse pehle API Key check karein
    # Agar .env mein nahi mili toh manual wali use karein
    api_key = os.getenv("OPENWEATHER_API_KEY") or "10fe390e1f6a4188f594b4e8ae574392"

    # 1. Geocoding API: City ke Lat/Lon nikalne ke liye
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={api_key}"
    
    try:
        geo_response = requests.get(geo_url)
        geo_data = geo_response.json()
        
        # Agar city nahi mili
        if not geo_data:
            print(f"❌ Error: City '{city}' nahi mili.")
            return None
            
        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']

        # 2. Weather API
        weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        weather_res = requests.get(weather_url).json()

        # 3. Air Pollution API
        aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
        aqi_res = requests.get(aqi_url).json()

        # Check karein ki API ne koi error message toh nahi bheja (jaise 401 Unauthorized)
        if 'cod' in weather_res and weather_res['cod'] != 200:
            print(f"❌ API Error: {weather_res.get('message', 'Unknown error')}")
            return None

        return weather_res, aqi_res

    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return None
