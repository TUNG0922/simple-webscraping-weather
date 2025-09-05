import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from scraper import get_weather

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load Malaysia cities
with open("locations.json", "r", encoding="utf-8") as f:
    LOCATIONS = json.load(f)

COUNTRY = "malaysia"

# Map basic weather keywords to icons
WEATHER_ICONS = {
    "sun": "☀️",
    "clear": "☀️",
    "cloud": "⛅",
    "overcast": "☁️",
    "rain": "🌧️",
    "drizzle": "🌦️",
    "thunder": "⛈️",
    "storm": "⛈️",
    "snow": "❄️",
    "fog": "🌫️",
}

def get_icon(condition: str):
    cond = condition.lower()
    for keyword, icon in WEATHER_ICONS.items():
        if keyword in cond:
            return icon
    return "🌤️"


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    cities = LOCATIONS[COUNTRY]
    all_weather = []

    # Fetch weather for each city
    for city in cities:
        data = get_weather(COUNTRY, city)
        icon = get_icon(data["condition"])
        all_weather.append({
            "city": city.replace("-", " ").title(),
            "temperature": data["temperature"],
            "condition": data["condition"],
            "details": data["details"],
            "icon": icon
        })

    return templates.TemplateResponse("index.html", {
        "request": request,
        "all_weather": all_weather
    })
