from services.weather_services import get_weather

API_KEY = "91849ce32e7147d4d5a84ee7cf8d8546"

city = input("Enter city : ")
data = get_weather(city, API_KEY)

print("Weather data for" ,city)
print("Temperature : ", data["main"]["temp"], "°C")
print("Humidity : ", data["main"]["humidity"], "%")
print("Decription : ", data["weather"][0]["description"])