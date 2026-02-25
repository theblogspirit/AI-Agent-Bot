import requests
import time

BASE_URL = "https://www.nseindia.com/api/corporate-announcements?index=equities"
HOME_URL = "https://www.nseindia.com/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/companies-listing/corporate-filings-announcements"
}

RESULT_KEYWORDS = ["results", "financial results", "quarterly results"]

def get_result_stocks():
    try:
        session = requests.Session()
        # Initialize session by visiting home page to get cookies
        session.get(HOME_URL, headers=HEADERS, timeout=15)
        time.sleep(2) # Natural delay
        
        r = session.get(BASE_URL, headers=HEADERS, timeout=15)
        if r.status_code != 200:
            print(f"NSE API Error: {r.status_code}")
            return []
            
        data = r.json()
        stocks = set()

        for item in data:
            desc = str(item.get("desc", "")).lower()
            symbol = item.get("symbol")
            if any(k in desc for k in RESULT_KEYWORDS) and symbol:
                stocks.add(symbol + ".NS")

        return list(stocks)
    except Exception as e:
        print(f"Detector error: {e}")
        return []
