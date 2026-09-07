import gspread
import os
import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import re

def clean_price(price_str):
    match = re.search(r"RM\s*(\d+\.\d{2})|(\d+\.\d{2})", str(price_str), re.IGNORECASE)
    return float(match.group(1) or match.group(2)) if match else 0.0

def scrape_lotus():
    # Replace with the actual URL for a Lotus's category page
    URL = "https://www.lotuss.com.my/en/category/fresh-produce"
    HEADERS = {"User-Agent": "Mozilla/5.0"}
    print(f"Scraping Lotus's from {URL}...")
    # --- Add your scraping logic here from the blueprint ---
    # This is a placeholder for the output of that logic:
    return [['Lotus Brand Milk 1L', "Lotus's", 7.20], ['Farm Fresh Milk 1L', "Lotus's", 8.50]]

def update_google_sheet(all_data):
    print("Connecting to Google Sheets...")
    service_account_info = json.loads(os.environ['GCP_SA_KEY'])
    gc = gspread.service_account_from_dict(service_account_info)
    spreadsheet = gc.open("SmartGrocer_Database") # Make sure your sheet is named this
    worksheet = spreadsheet.worksheet("Scraped_Cache")

    # Prepare data with timestamps
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows_to_upload = [[item[0], item[1], item[2], timestamp] for item in all_data]

    worksheet.clear()
    worksheet.append_row(['item_name', 'retailer', 'price_rm', 'last_updated'])
    worksheet.append_rows(rows_to_upload)
    print(f"✅ Google Sheet updated with {len(rows_to_upload)} records.")

if __name__ == "__main__":
    lotus_data = scrape_lotus()
    # You could add more scraper functions here:
    # mydin_data = scrape_mydin()
    # all_scraped_data = lotus_data + mydin_data
    update_google_sheet(lotus_data)

