import requests

api_key = "91849ce32e7147d4d5a84ee7cf8d8546"
city = input("Enter city : ")
url =  f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
response = requests.get(url)
print("status :", response.status_code)
weather = response.json()
#print(weather)
print("Temperature  :" , weather["main"]["temp"])
print("Humidity :", weather["main"]["humidity"])
print("Wind Speed :" , weather["wind"]["speed"])