from telegram_utils import send_telegram
from technical_scan import check_stock
from earnings_detector import get_result_stocks
from earnings_analysis import check_earnings_strength

def run_bot():
    # 1. Fetch Today's Earnings Stocks
    detected_stocks = get_result_stocks()
    
    # 2. Add Permanent Watchlist
    try:
        with open("stocks.txt", "r") as f:
            watchlist = [line.strip() for line in f if line.strip()]
    except:
        watchlist = []
    
    all_to_scan = list(set(detected_stocks + watchlist))
    
    if not all_to_scan:
        send_telegram("No stocks found to scan today.")
        return

    signals_sent = 0
    for s in all_to_scan:
        e = check_earnings_strength(s)
        # Skip if fundamentals are weak (optional, remove check to scan only technicals)
        if e and (e["strong"] or e["surprise"]):
            t = check_stock(s)
            if t:
                level = "🔥 Rocket Alert" if e["surprise"] else "Strong Trend"
                msg = f"🚀 {level}: {s}\n\n" \
                      f"Rev Growth: {e['revenue_growth']:.1%}\n" \
                      f"RSI: {t['rsi']}\n\n" \
                      f"Price: ₹{t['price']}\n" \
                      f"Entry: ₹{t['entry']}\n" \
                      f"Stop Loss: ₹{t['sl']}\n" \
                      f"Target: ₹{t['target']}"
                send_telegram(msg)
                signals_sent += 1
    
    if signals_sent == 0:
        send_telegram(f"Scanned {len(all_to_scan)} stocks. No 'God-Level' setups found today.")

if __name__ == "__main__":
    run_bot()
