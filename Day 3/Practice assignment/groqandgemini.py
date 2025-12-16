import os
import requests
from dotenv import load_dotenv
import time
import json

load_dotenv()

google_api = os.getenv("GOOGLE_API_KEY")

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={google_api}"

headers = {
    "Content-Type": "application/json"
}

user_prompt = input("Enter your prompt : ")

data = {
    "contents": [
        {
            "parts": [
                {"text": user_prompt}
            ]
        }
    ]
}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200:
    print(response.json()["candidates"][0]["content"]["parts"][0]["text"])
else:
    print("Error:", response.json())

# -----------------------#



groq_api = os.getenv("GROQ_API_KEY")

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {"Authorization": f"Bearer {groq_api}", "Content-Type": "application/json"}



data = {
    "model" : "llama-3.3-70b-versatile", 
    "messages": [{"role": "user",
                  "content": user_prompt
                  }]
}

start = time.time()
response = requests.post(url, headers=headers, data=json.dumps(data))
end = time.time()

print(f"Status: {response.status_code}, Time: {end - start:.2f}s")
print(response.json()["choices"][0]["message"]["content"])