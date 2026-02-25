import requests
from bs4 import BeautifulSoup

SCREENER_URL = "https://www.screener.in/screens/1776430/quarterly-results/"

def get_result_stocks():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    r = requests.get(SCREENER_URL, headers=headers, timeout=20)
    soup = BeautifulSoup(r.text, "lxml")
    
    table = soup.find("table")
    if not table:
        return []
    
    stocks = []
    
    for row in table.find_all("tr")[1:]:
        cols = row.find_all("td")
        if not cols:
            continue
        
        name = cols[0].text.strip()
        
        # Convert Screener name → Yahoo symbol guess
        symbol = name.upper().replace(" ", "") + ".NS"
        stocks.append(symbol)
    
    return stocks
