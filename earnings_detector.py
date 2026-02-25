def get_result_stocks():
    try:
        session = requests.Session()
        # You must visit the home page first to get cookies
        session.get("https://www.nseindia.com", headers=HEADERS, timeout=10)
        
        stocks = set()
        # Focus on the 'all' equity announcements endpoint
        url = "https://www.nseindia.com/api/corporate-announcements?index=equities"
        
        r = session.get(url, headers=HEADERS, timeout=10)
        if r.status_code != 200:
            print(f"Error: API returned status {r.status_code}")
            return []
            
        data = r.json()
        for item in data:
            desc = str(item.get("desc", "")).lower()
            symbol = item.get("symbol")
            
            # Key improvement: NSE uses specific subject codes for results
            is_result = any(k in desc for k in RESULT_KEYWORDS)
            if is_result and symbol:
                stocks.add(symbol + ".NS")
        
        return list(stocks)
