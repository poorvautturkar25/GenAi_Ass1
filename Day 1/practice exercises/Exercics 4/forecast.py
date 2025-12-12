import requests

api_key = "91849ce32e7147d4d5a84ee7cf8d8546"

city = input("Enter city name: ")

url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

response = requests.get(url)
print("Status:", response.status_code)

data = response.json()

if response.status_code == 200:
    print(f"\n5-Day Weather Forecast for {city}:\n")

    for item in data["list"][:10]:   # show first 10 forecasts
        dt = item["dt_txt"]
        temp = item["main"]["temp"]
        desc = item["weather"][0]["description"]
        wind = item["wind"]["speed"]

        print(f"{dt}  |  Temp: {temp}°C  |  {desc}  |  Wind: {wind} m/s")

else:
    print("\nError:", data.get("message"))
