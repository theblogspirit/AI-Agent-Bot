from telegram_utils import send_telegram
from technical_scan import check_stock
from earnings_detector import get_result_stocks

def run_bot():
    stocks = get_result_stocks()
    
    if not stocks:
        send_telegram("No result stocks detected today.")
        return
    
    signals = []
    
    for s in stocks:
        result = check_stock(s)
        if result:
            signals.append(result)
    
    if not signals:
        send_telegram(f"Earnings scan: {len(stocks)} result stocks checked. No bullish setups.")
        return
    
    for sig in signals:
        msg = f"""
📊 Earnings + Bullish Stock

{sig['symbol']}

Price: ₹{sig['price']}
Entry: ₹{sig['entry']}
Stop Loss: ₹{sig['sl']}
Target: ₹{sig['target']}
"""
        send_telegram(msg)

if __name__ == "__main__":
    run_bot()
