from datetime import datetime, timezone
import time
import requests

def get_daily_history(days=30):
    """
    Fetch daily BTC/USDT price history from Binance public API.
    Returns a list of dicts: [{date, open, close, pct_change, volume}, ...]
    """
    url = f"https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1d&limit={days}"
    headers = {"User-Agent": "Mozilla/5.0"}

    max_attempts = 3
    response = None

    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()
            break
        except Exception as e:
            if attempt < max_attempts:
                print(f"Connection failed, retrying (attempt {attempt + 1}/{max_attempts})...")
                time.sleep(2)
            else:
                print(f"An error occurred while fetching data after {max_attempts} attempts: {e}")
                return []

    if response is None:
        return []

    try:
        klines = response.json()
        history = []
        for kline in klines:
            open_time_ms = kline[0]
            open_price = float(kline[1])
            close_price = float(kline[4])
            volume = float(kline[5])
            date_str = datetime.fromtimestamp(open_time_ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d")
            pct_change = ((close_price - open_price) / open_price) * 100
            history.append({
                "date": date_str,
                "open": open_price,
                "close": close_price,
                "pct_change": pct_change,
                "volume": volume
            })
        return history
    except Exception as e:
        print(f"An error occurred while parsing data: {e}")
        return []

def main():
    history = get_daily_history(days=30)
    if not history:
        return

    print(f"{'Date':<12} | {'Open Price':<12} | {'Close Price':<12} | {'% Change':<10} | {'Volume':<15}")
    print("-" * 75)
    for day in history:
        formatted_open = f"${day['open']:,.2f}"
        formatted_close = f"${day['close']:,.2f}"
        formatted_pct = f"{day['pct_change']:+.2f}%"
        formatted_volume = f"{day['volume']:,.2f}"
        print(f"{day['date']:<12} | {formatted_open:<12} | {formatted_close:<12} | {formatted_pct:<10} | {formatted_volume:<15}")

if __name__ == "__main__":
    main()