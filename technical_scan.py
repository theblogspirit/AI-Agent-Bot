import yfinance as yf
import pandas_ta as ta
import time

def check_stock(symbol):
    try:
        # 1. Download data with a retry/delay to avoid being blocked
        df = yf.download(symbol, period="1y", interval="1d", progress=False)
        time.sleep(1) # Small pause to be gentle on Yahoo's servers
        
        # 2. Safety Check: If data is empty or too short for EMA 200, skip it
        if df is None or df.empty or len(df) < 200:
            print(f"Skipping {symbol}: Not enough data (found {len(df) if df is not None else 0} rows)")
            return None
        
        # 3. Calculate Indicators
        df["ema50"] = ta.ema(df["Close"], 50)
        df["ema200"] = ta.ema(df["Close"], 200)
        df["rsi"] = ta.rsi(df["Close"], 14)
        df["vol_sma"] = ta.sma(df["Volume"], 20)

        # 4. Safety Check: Ensure the LATEST row actually has indicator values
        # Sometimes TA returns NaN for the first few rows
        last_row = df.iloc[-1]
        if last_row.isnull().any():
            print(f"Skipping {symbol}: Latest data contains empty indicator values.")
            return None

        # 5. Extract Values Safely (using .item() or direct indexing)
        price = float(last_row["Close"])
        ema50 = float(last_row["ema50"])
        ema200 = float(last_row["ema200"])
        rsi = float(last_row["rsi"])
        current_vol = float(last_row["Volume"])
        avg_vol = float(last_row["vol_sma"])

        # 6. Your Rocket Logic
        is_uptrend = price > ema50 and ema50 > ema200
        is_momentum = rsi > 55
        is_vol_rocket = current_vol > (avg_vol * 1.5)

        if not (is_uptrend and is_momentum and is_vol_rocket):
            return None

        recent_high = float(df["High"].rolling(10).max().iloc[-1])
        recent_low = float(df["Low"].rolling(10).min().iloc[-1])
        
        entry = round(recent_high * 1.005, 2)
        sl = round(recent_low * 0.99, 2)
        target = round(entry + 2 * (entry - sl), 2)

        return {
            "symbol": symbol, "price": round(price, 2),
            "entry": entry, "sl": sl, "target": target, "rsi": round(rsi, 1)
        }
    except Exception as e:
        print(f"Technical error for {symbol}: {e}")
        return None
