import requests

URL = "https://www.nseindia.com/api/corporate-announcements?index=equities"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/"
}

def get_result_stocks():
    try:
        session = requests.Session()
        session.get("https://www.nseindia.com", headers=HEADERS, timeout=10)
        
        r = session.get(URL, headers=HEADERS, timeout=10)
        data = r.json()
        
        stocks = []
        
        for item in data.get("data", []):
            subject = item.get("subject", "").lower()
            symbol = item.get("symbol")
            
            if "financial results" in subject and symbol:
                stocks.append(symbol + ".NS")
        
        return list(set(stocks))
    
    except:
        return []
