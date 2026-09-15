import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY ="b260e53620f14ff3b1dee87fff6b2806"

url = "https://api.geoapify.com/v2/places"

url = "https://api.geoapify.com/v1/geocode/search"

params = {
    "text": "Cairo Tower",
    "apiKey": API_KEY,
    "limit": 5
}

response = requests.get(url, params=params)

print(response.status_code)

data = response.json()

for place in data["features"]:
    p = place["properties"]

    print("Name:", p.get("name"))
    print("Address:", p.get("formatted"))
    print("Location:", p.get("lat"), p.get("lon"))
    print("-" * 40)