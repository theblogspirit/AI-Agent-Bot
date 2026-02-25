import yfinance as yf

def check_earnings_strength(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info
        
        revenue_growth = info.get("revenueGrowth")
        profit_growth = info.get("earningsGrowth")
        margin = info.get("operatingMargins")
        roe = info.get("returnOnEquity")
        
        if revenue_growth is None or profit_growth is None:
            return None
        
        score = 0
        
        # Growth strength
        if revenue_growth > 0.15:
            score += 1
        if profit_growth > 0.20:
            score += 1
        
        # Profit quality
        if margin and margin > 0.15:
            score += 1
        if roe and roe > 0.18:
            score += 1
        
        strong = score >= 2
        surprise = score >= 3   # higher threshold
        
        return {
            "symbol": symbol,
            "revenue_growth": revenue_growth,
            "profit_growth": profit_growth,
            "margin": margin,
            "roe": roe,
            "strong": strong,
            "surprise": surprise,
            "score": score
        }
        
    except:
        return None
