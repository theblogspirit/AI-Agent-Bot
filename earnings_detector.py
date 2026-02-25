import requests
from bs4 import BeautifulSoup

URL = "https://www.screener.in/company/"

def get_result_stocks():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    
    try:
        r = requests.get(URL, headers=headers, timeout=20)
        soup = BeautifulSoup(r.text, "lxml")
        
        # Find "Recently announced results"
        section = soup.find("section", {"id": "recently-announced-results"})
        if not section:
            return []
        
        stocks = []
        
        for a in section.find_all("a"):
            name = a.text.strip()
            if not name:
                continue
            
            symbol = name.upper().replace(" ", "") + ".NS"
            stocks.append(symbol)
        
        return stocks
    
    except:
        return []
