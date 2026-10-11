from playwright.sync_api import sync_playwright
import requests
import pandas as pd
import time
import json

START_URL = "https://www.zomato.com/mumbai/drinks-and-nightlife"
API_URL = "https://www.zomato.com/webroutes/search/home"

# ✅ YOUR FUNCTION
def extract_restaurants(api_response):
    restaurants = []

    sections = api_response.get("sections", {})
    results = sections.get("SECTION_SEARCH_RESULT", [])

    for item in results:
        info = item.get("info", {})
        rating_data = info.get("rating", {})
        locality = info.get("locality", {})

        restaurant = {
            "name": info.get("name"),
            "rating": rating_data.get("aggregate_rating"),
            "votes": rating_data.get("votes"),
            "cost": info.get("costText", {}).get("text"),
            "cuisines": ", ".join(
                [c.get("name") for c in info.get("cuisine", [])]
            ),
            "address": locality.get("address"),
        }

        restaurants.append(restaurant)

    return restaurants


# STEP 1 — Get cookies from real browser
print("Launching browser to get session...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto(START_URL)

    print("Wait 10 seconds for page to fully load...")
    time.sleep(10)

    cookies = context.cookies()
    browser.close()

print("Session acquired ✅")

# Convert cookies for requests
session = requests.Session()
for cookie in cookies:
    session.cookies.set(cookie["name"], cookie["value"])

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36",
    "Content-Type": "application/json",
    "Referer": START_URL,
    "Origin": "https://www.zomato.com"
}

payload = {
    "context": "drinks-and-nightlife",
    "page_url": "/mumbai/drinks-and-nightlife",
    "locationId": 3,
    "isMobile": 0,
    "pageType": "nightlife",
    "entity_type": "city",
    "entity_id": 3,
    "page": 1
}

# STEP 2 — Paginate using API
all_data = []
page_no = 1

while True:
    print(f"Fetching page {page_no}")

    payload["page"] = page_no
    response = session.post(API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        print("Stopped. Status:", response.status_code)
        break

    data = response.json()
    restaurants = extract_restaurants(data)

    if not restaurants:
        break

    all_data.extend(restaurants)
    page_no += 1
    time.sleep(1)

df = pd.DataFrame(all_data)
df.drop_duplicates(subset=["name", "address"], inplace=True)
df.to_csv("zomato_mumbai_nightlife.csv", index=False)

print("\nDone ✅")
print("Total restaurants:", len(df))
print("Saved as zomato_mumbai_nightlife.csv")