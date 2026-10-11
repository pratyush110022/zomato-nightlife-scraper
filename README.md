# Zomato Nightlife & Restaurant Listing Scraper

A Python scraper that reads restaurant listings from the configured Zomato nightlife search page and saves structured results as CSV.

## How it works

1. Opens the configured start page in a visible Chromium browser through Playwright.
2. Waits for the page to load, captures browser cookies, and closes the browser.
3. Sends paginated requests to Zomato's web search endpoint using the captured session cookies.
4. Extracts restaurant information from each response until the endpoint returns an error or no further results.
5. Removes duplicate records using restaurant name and address, then writes the final CSV.

## Data fields

The extractor collects the following fields when present in the response:

- Restaurant name
- Aggregate rating and vote count
- Displayed cost text
- Cuisine names
- Locality/address text

## Files

- Zomato_Scraper.py — scraper entry point
- requirements.txt — Python package list
- README.md — project documentation

## Requirements

- Python 3.10 or a compatible version
- Packages in requirements.txt
- Playwright Chromium browser

## Setup

    python -m venv .venv
    .venv/Scripts/Activate.ps1
    pip install -r requirements.txt
    playwright install chromium

## Configuration and run

Review the values at the top of Zomato_Scraper.py before running:

- START_URL — browser page used to establish a session
- API_URL — search endpoint
- Request payload fields, including page_url, context, pageType, locationId, and entity_id

When changing the search target or category, keep the start URL and payload values consistent.

Run:

    python Zomato_Scraper.py

The script currently writes `zomato_mumbai_nightlife.csv` to the current working directory. Change the filename in the final `to_csv()` call if you want a different output name.

## Operational notes

- The browser is launched with headless=False, so a visible browser window is expected.
- The script waits for the page session and adds a short delay between paginated requests; actual results depend on the site's current response behavior.
- Review the target site's terms, access policies, and applicable laws before collecting or redistributing data.

## Synthetic sample data

[`sample_synthetic_12_records.csv`](sample_synthetic_12_records.csv) contains **12 synthetic test records** using the scraper's output schema. These records were generated for schema inspection and portfolio/demo purposes; they were not collected from the source website or API. Names and addresses are fictional, contact details and example.com links are placeholders, coordinates are illustrative, and ratings/prices are not real or current. Do not use them for real-world navigation or pricing decisions.
