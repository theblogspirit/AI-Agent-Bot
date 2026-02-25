from telegram_utils import send_telegram
from technical_scan import check_stock
from earnings_detector import get_result_stocks
from earnings_analysis import check_earnings_strength

def run_bot():
    stocks = get_result_stocks()
    
    if not stocks:
        send_telegram("No result stocks detected today.")
        return
    
    strong_results = []
    surprise_results = []
    
    for s in stocks:
        e = check_earnings_strength(s)
        if not e:
            continue
        
        if e["surprise"]:
            surprise_results.append(e)
        elif e["strong"]:
            strong_results.append(e)
    
    # Prefer surprise stocks
    candidates = surprise_results if surprise_results else strong_results
    
    if not candidates:
        send_telegram(f"Earnings scan: {len(stocks)} results checked. No strong earnings.")
        return
    
    signals = []
    
    for e in candidates:
        t = check_stock(e["symbol"])
        if t:
            signals.append((e, t))
    
    if not signals:
        send_telegram(f"{len(candidates)} strong/surprise earnings stocks, but no bullish charts.")
        return
    
    for e, t in signals:
        level = "🔥 Earnings Surprise" if e["surprise"] else "Strong Earnings"
        
        msg = f"""
🚀 {level} + Bullish Trend

{e['symbol']}

Revenue Growth: {e['revenue_growth']:.1%}
Profit Growth: {e['profit_growth']:.1%}
Margin: {e['margin']:.1%}
ROE: {e['roe']:.1%}

Price: ₹{t['price']}
Entry: ₹{t['entry']}
Stop Loss: ₹{t['sl']}
Target: ₹{t['target']}
"""
        send_telegram(msg)

if __name__ == "__main__":
    run_bot()
