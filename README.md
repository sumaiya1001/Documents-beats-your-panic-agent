# Beats Your Panic - AI Paper-Trading Agent

## Concept
**Beats Your Panic** is an intelligent AI paper-trading agent designed to help traders overcome emotional decision-making during cryptocurrency market volatility. By fetching live market data from Binance, evaluating rigorous risk thresholds, and comparing its performance against an emotional "panicked human" trader, the agent demonstrates how disciplined risk management consistently outperforms fear-based panic selling.

---

## How It Works (Script Guide)

This repository contains several modular Python scripts:

1. **`fetch_price.py`**: Connects to the Binance public ticker API to fetch the current live BTC/USDT price and prints it in a clean currency format (`BTC/USDT: $XX,XXX.XX`).
2. **`fetch_history.py`**: Fetches the last 24 hourly candles (`klines`) for BTC/USDT, prints a formatted table of hourly prices and `% changes`, evaluates overall 24h market movement, and outputs panic status warnings (`⚠️`, `🟡`, `🟢`).
3. **`compare_agent.py`**: Implements two core decision models:
   - `panicked_human_decision()`: Sells everything on any red number.
   - `disciplined_agent_decision()`: Holds normal volatility/uptrends and trims 25% risk *only* when entering a true panic zone (`< -3%`). Also includes a manual test function (`test_decisions()`).
4. **`simulate_outcome.py`**: Simulates a 10-day paper-trading competition starting with $10,000, comparing the panicked human (who incurs fear cooldown delays when panic-selling) versus the disciplined agent.
5. **`main_agent.py`**: The main live-running hackathon demo script that fetches live Binance market data, calculates 24h performance, evaluates panic thresholds, and outputs a clean side-by-side comparison report with educational takeaways.

---

## How to Run

### Prerequisites
- Python 3.8+ installed on your system.

### Installation & Execution
1. Open your terminal / command prompt in the project directory.
2. Install the required `requests` library:
   ```bash
   pip install requests
   ```
3. Run the live hackathon demo script:
   ```bash
   python main_agent.py
   ```
4. *Optional helper scripts:*
   - Check current live price: `python fetch_price.py`
   - View hourly kline history & panic status: `python fetch_history.py`
   - Run fake scenario tests: `python -c "import compare_agent; compare_agent.test_decisions()"`
   - Run the 10-day simulation: `python simulate_outcome.py`

---

## 10-Day Simulation Results

In a simulated 10-day paper-trading challenge starting with **$10,000** across volatile daily BTC swings (`[-1.2%, -4.5%, +2.1%, -0.8%, +1.5%, -3.2%, +0.5%, +3.8%, -1.9%, +2.4%]`), the **Disciplined Agent** successfully avoided missing out on market recoveries by resisting emotional liquidations, outperforming the panicked human:

```text
===========================================================================
 FINAL RESULTS AFTER 10 DAYS (Updated Fear Cooldown)
===========================================================================
😱 Panicked Human ended with:    $9,863.61
🤖 Disciplined Agent ended with: $10,037.65
🏆 Disciplined Agent outperformed by $174.04 (+1.76%)
===========================================================================
```

---

## Hackathon Details
- **Project Name:** Beats Your Panic - AI Paper-Trading Agent
- **Hackathon:** Binance Agent OS Mini Hackathon
- **Track:** Track A
