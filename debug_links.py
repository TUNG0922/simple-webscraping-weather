import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.timeanddate.com/weather/"
HEADERS = {"User-Agent": "Mozilla/5.0"}

r = requests.get(BASE_URL, headers=HEADERS)
print("Status:", r.status_code)

soup = BeautifulSoup(r.text, "html.parser")

print("\n--- First 30 <a> links ---")
for link in soup.select("a")[:30]:
    print(link.get("href"), "-", link.text.strip())
