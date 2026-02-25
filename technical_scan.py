import yfinance as yf
import pandas_ta as ta

def check_stock(symbol):
    try:
        df = yf.download(symbol, period="1y", interval="1d", progress=False)
        if df.empty or len(df) < 200:
            return None
        
        # Technical Calculations
        df["ema50"] = ta.ema(df["Close"], 50)
        df["ema200"] = ta.ema(df["Close"], 200)
        df["rsi"] = ta.rsi(df["Close"], 14)
        df["vol_sma"] = ta.sma(df["Volume"], 20) # 20-day Average Volume

        price = df["Close"].iloc[-1]
        ema50 = df["ema50"].iloc[-1]
        ema200 = df["ema200"].iloc[-1]
        rsi = df["rsi"].iloc[-1]
        current_vol = df["Volume"].iloc[-1]
        avg_vol = df["vol_sma"].iloc[-1]

        # God-Level Conditions: Trend + Momentum + Volume Rocket
        is_uptrend = price > ema50 and ema50 > ema200
        is_momentum = rsi > 55
        is_vol_rocket = current_vol > (avg_vol * 1.5) # Volume is 50% above average

        if not (is_uptrend and is_momentum and is_vol_rocket):
            return None

        # Calculate Levels
        recent_high = df["High"].rolling(10).max().iloc[-1]
        recent_low = df["Low"].rolling(10).min().iloc[-1]
        
        entry = round(recent_high * 1.005, 2)
        sl = round(recent_low * 0.99, 2) # 1% below recent low
        target = round(entry + 2 * (entry - sl), 2) # 1:2 Risk-Reward

        return {
            "symbol": symbol, "price": round(price, 2),
            "entry": entry, "sl": sl, "target": target, "rsi": round(rsi, 1)
        }
    except Exception as e:
        print(f"Technical error for {symbol}: {e}")
        return None
