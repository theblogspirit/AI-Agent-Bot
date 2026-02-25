import yfinance as yf

def check_earnings_strength(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        
        revenue_growth = info.get("revenueGrowth")
        profit_growth = info.get("earningsGrowth")
        margin = info.get("operatingMargins")
        
        if revenue_growth is None or profit_growth is None:
            return None
        
        score = 0
        
        if revenue_growth > 0.15:
            score += 1
        if profit_growth > 0.20:
            score += 1
        if margin and margin > 0.15:
            score += 1
        
        strong = score >= 2
        
        return {
            "symbol": symbol,
            "revenue_growth": revenue_growth,
            "profit_growth": profit_growth,
            "margin": margin,
            "strong": strong
        }
        
    except:
        return None
