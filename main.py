from service import get_weather_and_aqi

def main():
    city = input("Enter city: ")
    data = get_weather_and_aqi(city)
    
    if data:
        weather, aqi = data
        temp = weather['main']['temp']
        desc = weather['weather'][0]['description']
        pm25 = aqi['list'][0]['components']['pm2_5']

        if pm25 > 150: 
            status = "Unhealthy"
        elif pm25 > 50: 
            status = "Moderate"
        else: 
            status = "Good"

        print(f"City: {city}")
        print(f"Temperature: {temp}°C")
        print(f"Condition: {desc}")
        print(f"Overall Status: {status}")
    else:
        print("City not found!")

if __name__ == "__main__":
    main()
