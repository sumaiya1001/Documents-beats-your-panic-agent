from datetime import datetime, timezone
import time
import requests

def main():
    # Binance public API endpoint for klines (candlestick data)
    # symbol=BTCUSDT: Trading pair BTC to USDT
    # interval=1h: 1-hour interval per candle
    # limit=24: Retrieve the last 24 candles
    url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=24"
    headers = {"User-Agent": "Mozilla/5.0"}

    # Automatic retry configuration
    max_attempts = 3
    response = None

    for attempt in range(1, max_attempts + 1):
        try:
            # Step 1: Send HTTP GET request to Binance
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()  # Check if request was successful
            break  # If successful, exit retry loop
        except Exception as e:
            if attempt < max_attempts:
                print(f"Connection failed, retrying (attempt {attempt + 1}/{max_attempts})...")
                time.sleep(2)
            else:
                print(f"An error occurred while fetching data after {max_attempts} attempts: {e}")
                return

    if response is None:
        return

    try:
        # Step 2: Parse the response JSON into a Python list
        # Binance returns a list of candles, where each candle is an array of values:
        # [0] Open time (ms timestamp)
        # [1] Open price
        # [2] High price
        # [3] Low price
        # [4] Close price
        # ...
        klines = response.json()

        # Step 3: Print table headers
        print(f"{'Time (UTC)':<17} | {'Open Price':<12} | {'Close Price':<12} | {'% Change':<10}")
        print("-" * 60)

        # Step 4: Loop through each 1-hour candle and print formatted data
        for kline in klines:
            open_time_ms = kline[0]
            open_price = float(kline[1])
            close_price = float(kline[4])

            # Convert open time timestamp (ms) to human-readable UTC date and time string
            time_str = datetime.fromtimestamp(open_time_ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")

            # Calculate percent change: ((Close - Open) / Open) * 100
            pct_change = ((close_price - open_price) / open_price) * 100

            # Format prices as currency and percent change with explicit + / - sign
            formatted_open = f"${open_price:,.2f}"
            formatted_close = f"${close_price:,.2f}"
            formatted_pct = f"{pct_change:+.2f}%"

            # Print row in neat tabular columns
            print(f"{time_str:<17} | {formatted_open:<12} | {formatted_close:<12} | {formatted_pct:<10}")

        # Step 5: Panic detection logic (24-hour overall change)
        if klines:
            # Oldest candle open price (first item in klines list)
            oldest_open = float(klines[0][1])
            # Newest candle close price (last item in klines list)
            newest_close = float(klines[-1][4])

            # Calculate overall % change over the last 24 hours
            overall_change = ((newest_close - oldest_open) / oldest_open) * 100

            print("-" * 60)
            # Check panic thresholds
            if overall_change < -3.0:
                print(f"⚠️ PANIC ZONE: BTC dropped {abs(overall_change):.2f}% in 24h")
            elif overall_change <= 0.0:
                print(f"🟡 Mild dip: {overall_change:.2f}%")
            else:
                print(f"🟢 BTC is up +{overall_change:.2f}% - no panic")

    except Exception as e:
        print(f"An error occurred while parsing data: {e}")

if __name__ == "__main__":
    main()
