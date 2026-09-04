import os
from dotenv import load_dotenv
from google import genai
from compare_agent import fetch_btc_klines, panicked_human_decision, disciplined_agent_decision
from panic_check import run_panic_check

load_dotenv()
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("=" * 70)
print("BITCOIN PANIC AGENT: LIVE HACKATHON DEMO")
print("=" * 70)
print("Fetching live market data from Binance API (BTC/USDT 24h Klines)...")

klines = fetch_btc_klines()
if not klines:
    raise SystemExit("Failed to fetch live data. Please check your network connection.")

oldest_open = float(klines[0][1])
newest_close = float(klines[-1][4])
overall_change = ((newest_close - oldest_open) / oldest_open) * 100
current_price = newest_close

panic_status = (
    f"PANIC ZONE: BTC dropped {abs(overall_change):.2f}% in 24h"
    if overall_change <= -2.99
    else f"Mild dip: {overall_change:.2f}%"
    if overall_change <= 0.0
    else f"BTC is up +{overall_change:.2f}% - no panic"
)

human_action, human_reason = panicked_human_decision(overall_change)
agent_action, agent_reason = disciplined_agent_decision(overall_change)

print("\n" + "=" * 70)
print("LIVE MARKET SUMMARY REPORT")
print("=" * 70)
print(f"Current BTC Price  : ${current_price:,.2f}")
print(f"24h Overall Change : {overall_change:+.2f}%")
print(f"Market Status      : {panic_status}")
print("=" * 70)

print("\nDECISION COMPARISON: HUMAN VS AGENT")
print("-" * 70)

print("Panicked Human:")
print(f"Action : {human_action}")
print(f"Reason : {human_reason}")

print()

print("Disciplined Agent:")
print(f"Action : {agent_action}")
print(f"Reason : {agent_reason}")

print("-" * 70)

print("\nGEMINI MARKET REASONING:")
print("-" * 70)

gemini_prompt = (
    f"BTC/USDT is currently ${current_price:,.2f}, "
    f"having moved {overall_change:+.2f}% in the last 24 hours.\n\n"
    "Give a short, clear analysis in exactly this format:\n\n"
    "Bull Case: (one sentence, the optimistic read on this move)\n"
    "Bear Case: (one sentence, the cautious/risk read on this move)\n\n"
    "Keep each case to one sentence. No extra commentary."
)

gemini_response = gemini_client.models.generate_content(
    model="gemini-3.5-flash",
    contents=gemini_prompt
)

print(gemini_response.text)
print("-" * 70)

hourly_closes = [float(candle[4]) for candle in klines]
hourly_volumes = [float(candle[5]) for candle in klines]

hourly_changes = [
    ((hourly_closes[i] - hourly_closes[i - 1]) / hourly_closes[i - 1]) * 100
    for i in range(1, len(hourly_closes))
]

result = run_panic_check(
    overall_change,
    hourly_changes,
    hourly_volumes,
    current_price
)

print("\nPANIC CHECK")
print("-" * 70)

print(
    f"Price Shock       : "
    f"{'YES' if result['shock'][0] else 'no'} — "
    f"{result['shock'][1]}"
)

print(
    f"Trend Confirmed   : "
    f"{'YES' if result['trend'][0] else 'no'} — "
    f"{result['trend'][1]}"
)

print(
    f"Volume Confirmed  : "
    f"{'YES' if result['volume'][0] else 'no'} — "
    f"{result['volume'][1]}"
)

print(
    f"Bear Case Stronger: "
    f"{'YES' if result['bull_bear'][0] else 'no'}"
)

print("-" * 70)

print(
    f"PANIC SIGNAL : "
    f"{'YES' if result['panic_signal'] else 'NO'}"
)

print(
    f"RISK GATE    : "
    f"{'PASSED' if result['risk_gate_passed'] else 'FAILED'}"
)

print("-" * 70)

takeaway = (
    "Takeaway: Panic selling locks in permanent losses, whereas trimming risk rationally (25%) protects capital while keeping you positioned for the recovery."
    if overall_change <= -2.99
    else "Takeaway: Normal market volatility below the 2.99% shock threshold should be ignored rather than triggering emotional liquidations."
    if overall_change < 0.0
    else "Takeaway: In an ongoing uptrend, staying fully invested prevents missing out on momentum gains due to premature fear."
)

print("\nHACKATHON TAKEAWAY:")
print(takeaway)
print("=" * 70)