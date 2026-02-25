import requests

BASE_URL = "https://www.nseindia.com/api/corporate-announcements"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.nseindia.com/"
}

RESULT_KEYWORDS = [
    "financial results",
    "quarterly results",
    "audited results",
    "unaudited results",
    "results"
]

def get_result_stocks():
    try:
        session = requests.Session()
        session.get("https://www.nseindia.com", headers=HEADERS, timeout=10)

        stocks = set()

        # scan multiple pages (recent announcements)
        for start in [0, 100, 200, 300]:
            url = f"{BASE_URL}?index=equities&from={start}"
            r = session.get(url, headers=HEADERS, timeout=10)
            data = r.json()

            for item in data:
                desc = str(item.get("desc", "")).lower()
                symbol = item.get("symbol")

                if any(k in desc for k in RESULT_KEYWORDS) and symbol:
                    stocks.add(symbol + ".NS")

        return list(stocks)

    except Exception as e:
        print("Detector error:", e)
        return []
