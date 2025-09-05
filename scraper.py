import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.timeanddate.com"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_weather(country: str, city: str):
    url = f"{BASE_URL}/weather/{country}/{city}"
    print(f"🌍 Fetching weather for {city} from {url}")

    r = requests.get(url, headers=HEADERS)
    print(f"Status code: {r.status_code}")

    soup = BeautifulSoup(r.text, "html.parser")

    # Temperature
    temp_el = soup.select_one(".h2")
    temp = temp_el.get_text(strip=True) if temp_el else "N/A"
    print(f"Temperature: {temp}")

    # Main condition (like Sunny, Cloudy)
    condition_el = soup.select_one("#qlook p")
    condition = condition_el.get_text(strip=True) if condition_el else "N/A"
    print(f"Condition: {condition}")

    # Extra details table (Humidity, Wind, etc.)
    extra = {}
    details_table = soup.select_one("table#qlook")
    if details_table:
        for row in details_table.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) == 2:
                key = cols[0].get_text(strip=True)
                value = cols[1].get_text(strip=True)
                extra[key] = value
                print(f"Detail: {key} = {value}")

    # Forecast section: Sunrise / Sunset
    forecast_table = soup.select_one("table.weatherTable")
    if forecast_table:
        for row in forecast_table.find_all("tr"):
            cols = row.find_all("td")
            if len(cols) == 2:
                key = cols[0].get_text(strip=True)
                value = cols[1].get_text(strip=True)
                extra[key] = value
                print(f"Forecast Detail: {key} = {value}")

    # If no details, add friendly message
    if not extra:
        extra = {"Info": "No additional details available for this city."}
        print("No extra details found.")

    print("✅ Done fetching\n")
    return {
        "temperature": temp,
        "condition": condition,
        "details": extra
    }

# Example test
if __name__ == "__main__":
    get_weather("malaysia", "kuala-lumpur")
