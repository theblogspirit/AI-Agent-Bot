import yfinance as yf
import pandas_ta as ta

def check_stock(symbol):
    try:
        df = yf.download(symbol, period="6mo", progress=False)
        
        if df.empty:
            return None
        
        df["ema50"] = ta.ema(df["Close"], 50)
        df["ema200"] = ta.ema(df["Close"], 200)
        df["rsi"] = ta.rsi(df["Close"], 14)
        
        price = df["Close"].iloc[-1]
        ema50 = df["ema50"].iloc[-1]
        ema200 = df["ema200"].iloc[-1]
        rsi = df["rsi"].iloc[-1]
        
        bullish = price > ema50 and ema50 > ema200 and rsi > 55
        
        if not bullish:
            return None
        
        recent_high = df["High"].rolling(20).max().iloc[-1]
        recent_low = df["Low"].rolling(20).min().iloc[-1]
        
        entry = round(recent_high * 1.01, 2)
        sl = round(recent_low, 2)
        target = round(entry + 2 * (entry - sl), 2)
        
        return {
            "symbol": symbol,
            "price": round(price, 2),
            "entry": entry,
            "sl": sl,
            "target": target
        }
        
    except:
        return None
