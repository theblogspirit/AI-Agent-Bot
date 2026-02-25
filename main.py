from telegram_utils import send_telegram
from technical_scan import check_stock

def load_stocks():
    with open("stocks.txt") as f:
        return [line.strip() for line in f if line.strip()]

def run_bot():
    stocks = load_stocks()
    signals = []
    
    for s in stocks:
        result = check_stock(s)
        if result:
            signals.append(result)
    
    if not signals:
        send_telegram("No bullish stocks found today.")
        return
    
    for sig in signals:
        msg = f"""
📈 Bullish Stock Detected

{sig['symbol']}

Price: ₹{sig['price']}
Entry: ₹{sig['entry']}
Stop Loss: ₹{sig['sl']}
Target: ₹{sig['target']}
"""
        send_telegram(msg)

if __name__ == "__main__":
    run_bot()
