
import os
import time
import pandas as pd
import yfinance as yf
from datetime import datetime

def get_top_200():
    url = "https://www.marketwatch.com/tools/screener/mostactive"
    tables = pd.read_html(url)
    df = tables[0]
    df = df[df['Symbol'].str.len() <= 5]
    return df['Symbol'].tolist()[:200]

def scan(tickers):
    results = []
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            price = info.get("regularMarketPrice", 0)
            volume = info.get("volume", 0)
            avg_volume = info.get("averageVolume", 1)
            vol_spike = round(volume / avg_volume, 2) if avg_volume else 0
            if vol_spike > 1.5:
                results.append({
                    "Ticker": ticker,
                    "Price": price,
                    "Volume": volume,
                    "Avg Volume": avg_volume,
                    "Vol Spike": vol_spike
                })
        except:
            continue
    return results

def save_results(data):
    if not os.path.exists("scans"):
        os.makedirs("scans")
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    df = pd.DataFrame(data)
    df.to_csv(f"scans/breakout_scan_{ts}.csv", index=False)
    print(f"[✅] Saved: scans/breakout_scan_{ts}.csv")

def run_loop():
    while True:
        print("[🔁] Running scan...")
        tickers = get_top_200()
        results = scan(tickers)
        if results:
            save_results(results)
        else:
            print("[⚠️] No results.")
        time.sleep(120)  # wait 2 minutes

if __name__ == "__main__":
    run_loop()
