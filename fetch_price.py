import requests

def main():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        price = float(data["price"])
        print(f"BTC/USDT: ${price:,.2f}")
    except Exception as e:
        print(f"Error fetching price: {e}")

if __name__ == "__main__":
    main()
