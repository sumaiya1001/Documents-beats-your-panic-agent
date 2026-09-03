from compare_agent import fetch_btc_klines, panicked_human_decision, disciplined_agent_decision

def main():
    print("=" * 70)
    print(" 🚀 BITCOIN PANIC AGENT: LIVE HACKATHON DEMO 🚀")
    print("=" * 70)
    print("Fetching live market data from Binance API (BTC/USDT 24h Klines)...")
    
    # 1. Fetch live historical klines (24 hourly candles)
    klines = fetch_btc_klines()
    if not klines:
        print("Failed to fetch live data. Please check your network connection.")
        return

    # 2. Extract price and calculate 24h overall % change
    oldest_open = float(klines[0][1])
    newest_close = float(klines[-1][4])
    overall_change = ((newest_close - oldest_open) / oldest_open) * 100
    current_price = newest_close

    # 3. Determine panic status based on overall change
    if overall_change < -3.0:
        panic_status = f"⚠️ PANIC ZONE: BTC dropped {abs(overall_change):.2f}% in 24h"
    elif overall_change <= 0.0:
        panic_status = f"🟡 Mild dip: {overall_change:.2f}%"
    else:
        panic_status = f"🟢 BTC is up +{overall_change:.2f}% - no panic"

    # 4. Run decision functions
    human_action, human_reason = panicked_human_decision(overall_change)
    agent_action, agent_reason = disciplined_agent_decision(overall_change)

    # 5. Print visually clean hackathon summary report
    print("\n" + "=" * 70)
    print(" 📊 LIVE MARKET SUMMARY REPORT")
    print("=" * 70)
    print(f" • Current BTC Price : ${current_price:,.2f}")
    print(f" • 24h Overall Change: {overall_change:+.2f}%")
    print(f" • Market Status     : {panic_status}")
    print("=" * 70)

    print("\n" + " 🥊 DECISION COMPARISON: HUMAN VS AGENT")
    print("-" * 70)
    print(f" 😱 Panicked Human:")
    print(f"    Action : {human_action}")
    print(f"    Reason : {human_reason}")
    print()
    print(f" 🤖 Disciplined Agent:")
    print(f"    Action : {agent_action}")
    print(f"    Reason : {agent_reason}")
    print("-" * 70)

    # 6. Generate educational takeaway message
    if overall_change < -3.0:
        takeaway = "Takeaway: Panic selling locks in permanent losses, whereas trimming risk rationally (25%) protects capital while keeping you positioned for the recovery."
    elif overall_change < 0.0:
        takeaway = "Takeaway: Normal market volatility (-3% to 0%) should be ignored rather than triggering emotional liquidations."
    else:
        takeaway = "Takeaway: In an ongoing uptrend, staying fully invested prevents missing out on momentum gains due to premature fear."

    print(f"\n 💡 HACKATHON TAKEAWAY:")
    print(f" {takeaway}")
    print("=" * 70)

if __name__ == "__main__":
    main()
