from datetime import datetime, timezone
import time
import requests

def fetch_btc_klines():
    """Fetches the last 24 hourly candles for BTC/USDT from Binance with retry logic."""
    url = "https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=24"
    headers = {"User-Agent": "Mozilla/5.0"}
    max_attempts = 3

    for attempt in range(1, max_attempts + 1):
        try:
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            if attempt < max_attempts:
                print(f"Connection failed, retrying (attempt {attempt + 1}/{max_attempts})...")
                time.sleep(2)
            else:
                print(f"An error occurred while fetching data after {max_attempts} attempts: {e}")
                return None

def panicked_human_decision(pct_change):
    """Simulates an emotional human trader."""
    if pct_change <= -2.0:
        return "SELL EVERYTHING", "Sharp drop triggered fear, sold in panic"
    else:
        return "HOLD", "No red, no reaction"

def disciplined_agent_decision(pct_change):
    """Simulates a rational trading agent."""
    if pct_change <= -2.99:
        return "REDUCE POSITION 25%", "Real panic zone, trim risk but don't fully exit"
    elif pct_change <= 0.0:
        return "HOLD", "Normal volatility, no action needed"
    else:
        return "HOLD", "Uptrend, stay invested"

def test_decisions():
    """Tests both decision functions with three fake scenarios and prints results."""
    scenarios = [-5.0, -1.5, 2.0]
    
    print("=" * 65)
    print("RUNNING DECISION FUNCTION TESTS (Fake Scenarios)")
    print("=" * 65)
    
    for pct in scenarios:
        human_action, human_reason = panicked_human_decision(pct)
        agent_action, agent_reason = disciplined_agent_decision(pct)
        
        print(f"\nScenario: 24h % Change = {pct:+.1f}%")
        print("-" * 65)
        print(f"😱 Panicked Human:")
        print(f"   Decision : {human_action}")
        print(f"   Reason   : {human_reason}")
        print(f"🤖 Disciplined Agent:")
        print(f"   Decision : {agent_action}")
        print(f"   Reason   : {agent_reason}")
    print("=" * 65)

def main():
    # Fetch historical klines data
    klines = fetch_btc_klines()
    if not klines:
        return

    # Calculate overall 24-hour % change (Oldest Open to Newest Close)
    oldest_open = float(klines[0][1])
    newest_close = float(klines[-1][4])
    overall_change = ((newest_close - oldest_open) / oldest_open) * 100

    # Get decisions from both traders
    human_action, human_reason = panicked_human_decision(overall_change)
    agent_action, agent_reason = disciplined_agent_decision(overall_change)

    # Print summary of market condition
    print("=" * 65)
    print(f"BTC/USDT 24-Hour Overall Change: {overall_change:+.2f}%")
    print("=" * 65)
    print()

    # Print side-by-side / clearly labeled comparison
    print("COMPARISON: Panicked Human vs Disciplined Agent")
    print("-" * 65)
    print(f"😱 Panicked Human:")
    print(f"   Decision : {human_action}")
    print(f"   Reason   : {human_reason}")
    print()
    print(f"🤖 Disciplined Agent:")
    print(f"   Decision : {agent_action}")
    print(f"   Reason   : {agent_reason}")
    print("-" * 65)

if __name__ == "__main__":
    main()