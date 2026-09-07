import gspread
import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def scrape_lotus_placeholder():
    """
    Placeholder scraping engine. 
    Replace this function with your actual beautifulsoup/requests selectors 
    when you are ready to parse live retail websites.
    """
    print("Executing Lotus's Malaysia scrape routine...")
    # Simulated scraped payload conforming to schema
    return [
        ["Milo Chocolate Malt Powder 1kg", "Lotus's Malaysia", 18.90],
        ["Farm Fresh Pure Fresh Milk 1L", "Lotus's Malaysia", 8.20],
        ["Goodday Full Cream Milk 1L", "Lotus's Malaysia", 7.40],
        ["Anlene Gold 5X High Calcium 1kg", "Lotus's Malaysia", 34.50]
    ]

def scrape_mydin_placeholder():
    """Placeholder for Mydin bulk pricing channel."""
    print("Executing Mydin Hypermarket scrape routine...")
    return [
        ["Milo Chocolate Malt Powder 1kg", "Mydin Hypermarket", 17.50],
        ["Farm Fresh Pure Fresh Milk 1L", "Mydin Hypermarket", 7.90],
        ["Goodday Full Cream Milk 1L", "Mydin Hypermarket", 6.90],
        ["Anlene Gold 5X High Calcium 1kg", "Mydin Hypermarket", 32.90]
    ]

def scrape_seven_eleven_placeholder():
    """Placeholder for convenience store baseline pricing."""
    print("Executing 7-Eleven Malaysia convenience baseline scrape routine...")
    return [
        ["Milo Chocolate Malt Powder 1kg", "7-Eleven / GrabMart", 22.50],
        ["Farm Fresh Pure Fresh Milk 1L", "7-Eleven / GrabMart", 9.90],
        ["Goodday Full Cream Milk 1L", "7-Eleven / GrabMart", 8.90],
        ["Anlene Gold 5X High Calcium 1kg", "7-Eleven / GrabMart", 39.90]
    ]

def update_google_sheet(all_data):
    print("Initializing Google Sheets connection...")
    
    # Authenticate using the secret key we stored in GitHub
    service_account_info = json.loads(os.environ['GCP_SA_KEY'])
    gc = gspread.service_account_from_dict(service_account_info)
    
    # Open sheet and target worksheet
    spreadsheet = gc.open("SmartGrocer_Database")
    worksheet = spreadsheet.worksheet("Scraped_Cache")
    
    # Prepare batch rows with timestamps
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows_to_upload = [[item[0], item[1], float(item[2]), timestamp] for item in all_data]
    
    # Clear old data and batch insert new data to prevent API rate limits
    print("Clearing Scraped_Cache worksheet...")
    worksheet.clear()
    worksheet.append_row(['item_name', 'retailer', 'price_rm', 'last_updated'])
    worksheet.append_rows(rows_to_upload)
    print(f"🎉 Successfully pushed {len(rows_to_upload)} live pricing records to Google Sheets!")

if __name__ == "__main__":
    # Gather data from all placeholder scrapers
    combined_data = (
        scrape_lotus_placeholder() + 
        scrape_mydin_placeholder() + 
        scrape_seven_eleven_placeholder()
    )
    update_google_sheet(combined_data)
