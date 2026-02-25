import yfinance as yf
import pandas_ta as ta

def check_stock(symbol):
    try:
        # Fetching 1 year of data to ensure EMA 200 is accurate
        df = yf.download(symbol, period="1y", interval="1d", progress=False)
        
        # Security check: Ensure we have enough data
        if df.empty or len(df) < 200:
            return None
        
        # Step 1: Calculate Indicators
        df["ema50"] = ta.ema(df["Close"], 50)
        df["ema200"] = ta.ema(df["Close"], 200)
        df["rsi"] = ta.rsi(df["Close"], 14)
        df["vol_sma"] = ta.sma(df["Volume"], 20)

        # Step 2: Extract LATEST values as single numbers (Scalars)
        # Using .iloc[-1].item() fixes the "Ambiguous Series" error
        price = float(df["Close"].iloc[-1].item())
        ema50 = float(df["ema50"].iloc[-1].item())
        ema200 = float(df["ema200"].iloc[-1].item())
        rsi = float(df["rsi"].iloc[-1].item())
        current_vol = float(df["Volume"].iloc[-1].item())
        avg_vol = float(df["vol_sma"].iloc[-1].item())

        # Step 3: Rocket Conditions
        is_uptrend = price > ema50 and ema50 > ema200
        is_momentum = rsi > 55
        is_vol_rocket = current_vol > (avg_vol * 1.5)

        if not (is_uptrend and is_momentum and is_vol_rocket):
            return None

        # Step 4: Calculate Entry/Exit Levels
        # We use .max() and .min() which return scalars automatically
        recent_high = float(df["High"].rolling(10).max().iloc[-1])
        recent_low = float(df["Low"].rolling(10).min().iloc[-1])
        
        entry = round(recent_high * 1.005, 2)
        sl = round(recent_low * 0.99, 2)
        target = round(entry + 2 * (entry - sl), 2)

        return {
            "symbol": symbol, 
            "price": round(price, 2),
            "entry": entry, 
            "sl": sl, 
            "target": target, 
            "rsi": round(rsi, 1)
        }
    except Exception as e:
        print(f"Technical error for {symbol}: {e}")
        return None
