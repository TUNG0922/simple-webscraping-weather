import requests, json
from bs4 import BeautifulSoup

BASE_URL = "https://www.timeanddate.com"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_cities(country: str):
    url = f"{BASE_URL}/weather/{country}"
    r = requests.get(url, headers=HEADERS)
    print(f"🌎 Fetching cities for {country} from {url}")

    soup = BeautifulSoup(r.text, "html.parser")
    cities = set()  # use a set to avoid duplicates

    # Scrape links like /weather/malaysia/kuala-lumpur
    for link in soup.select("a[href^='/weather/']"):
        href = link.get("href", "")
        parts = href.strip("/").split("/")
        if len(parts) == 3 and parts[0] == "weather" and parts[1] == country:
            cities.add(parts[2])  # add to set (no duplicates)

    city_list = sorted(cities)  # sort alphabetically for consistency
    print(f"✅ Found {len(city_list)} unique cities for {country}")
    return city_list

if __name__ == "__main__":
    country = "malaysia"
    locations = {country: get_cities(country)}

    with open("locations.json", "w", encoding="utf-8") as f:
        json.dump(locations, f, indent=2)

    print("🎉 Saved Malaysia locations to locations.json")
