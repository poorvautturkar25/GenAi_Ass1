#Q2:
#Create a Streamlit application that takes a city name as input from the user.
# Fetch the current weather using a Weather API 
# and use an LLM to explain the weather conditions in simple English.

import streamlit as st
import requests
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()

st.set_page_config(page_title="Weather App", page_icon="🌦️")
st.title("🌦️ Weather Information App")

weather_api_key = os.getenv("OPENWEATHER_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

llm = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="openai",
    base_url="https://api.groq.com/openai/v1",
    api_key=groq_api_key
)

city = st.text_input("Enter City Name")

if st.button("Get Weather"):
    if not city:
        st.warning("Please enter a city name")
    elif not weather_api_key:
        st.error("Weather API key not found")
    else:
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather?appid={weather_api_key}&units=metric&q={city}"
            response = requests.get(url, timeout=5)
            data = response.json()

            temp = data["main"]["temp"]
            condition = data["weather"][0]["description"]
            wind = data["wind"]["speed"]
            humidity = data["main"]["humidity"]

            st.subheader(f"Weather in {city}")
            st.write(f"🌡️ Temperature: {temp} °C")
            st.write(f"☁️ Condition: {condition.title()}")
            st.write(f"💨 Wind Speed: {wind} km/h")
            st.write(f"💧 Humidity: {humidity} %")

            prompt = f"""
            The current weather details are:
            Temperature: {temp} °C
            Condition: {condition}
            Wind Speed: {wind} km/h
            Humidity: {humidity} %

            Explain this weather in simple English for a normal person.
            """

            explanation = llm.invoke(prompt)

            st.subheader("🤖 Weather Explanation")
            st.write(explanation.content)

        except Exception as e:
            st.error("❌ Unable to fetch weather. Please check city name or internet.")
            