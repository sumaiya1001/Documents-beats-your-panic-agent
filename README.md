# Beats Your Panic - AI Trading Agent

An AI trading agent designed to help make better decisions when the crypto market suddenly gets scary.

## The Problem

As a new trader, I noticed that whenever Bitcoin started dropping, my first reaction was often to think about selling everything. Sometimes the drop was significant, but sometimes it was just normal market movement.

I built Beats Your Panic to compare those two reactions using real BTC/USDT market data: a Panicked Human that reacts emotionally and a Disciplined Agent that checks the market before deciding what to do.

The goal isn't to predict Bitcoin perfectly. It's to show what can happen when a trading decision is based on evidence instead of panic.

## How It Works

The Panicked Human sells everything when the market falls enough to trigger fear and then stays out during a short cooldown. The Disciplined Agent holds during normal volatility and reduces the position by 25% when the defined panic threshold is reached.

Before treating a drop as a real panic event, the agent runs a Panic Check using price shock, trend, volume, and Gemini bull/bear reasoning.

```text
Real BTC/USDT Market Data
          |
          v
     Panic Check
          |
    +-----+-----+
    |           |
    v           v
 Bull Case    Bear Case
    |           |
    +-----+-----+
          |
          v
     Risk / Panic Gate
          |
     +----+----+
     |         |
     v         v
   HOLD /    PANIC?
    TRIM
```

The historical backtest uses the same market conditions for both strategies and compares their results.

## Binance Agent OS / MCP

I connected the project to Binance's official Agent OS MCP server through VS Code. The connection was authenticated successfully, the MCP server reached a running state, and Binance tools were discovered, including public market-data tools such as Symbol Price Ticker and Kline Data.

For the current paper-trading demo, the Python agent still uses Binance's public REST API for its executable market-data path. I kept the MCP connection separate because the project doesn't need access to an account that can place real trades.

## The Scripts

`fetch_price.py` gets the current BTC/USDT price from Binance's public API.

`fetch_history.py` downloads historical BTC/USDT data used by the backtest.

`compare_agent.py` contains the Panicked Human and Disciplined Agent decision models.

`panic_check.py` evaluates price shock, trend, volume, and bull/bear reasoning before the Risk Gate makes the final decision.

`simulate_outcome.py` runs the historical backtest.

`main_agent.py` runs the live demonstration, combining market data, the two decision models, Gemini reasoning, the Panic Check, and the final risk decision.

## Running the Project

Requirements:

* Python 3.8+
* Gemini API key
* Internet connection

Install the dependency:

```text
pip install requests
```

Create a `.env` file:

```text
GEMINI_API_KEY=your_key_here
```

Run the live demo:

```text
python main_agent.py
```

Run the backtest:

```text
python simulate_outcome.py
```

## Backtest

Period: August 27 to September 3, 2026
Asset: BTC/USDT
Starting balance: $10,000

| Date  | BTC/USDT Daily Change |
| ----- | --------------------- |
| 08-27 | +1.55%                |
| 08-28 | -3.00%                |
| 08-29 | +0.49%                |
| 08-30 | -0.70%                |
| 08-31 | +1.16%                |
| 09-01 | -1.45%                |
| 09-02 | -0.13%                |
| 09-03 | +5.27%                |

```text
😱 Panicked Human ended with:    $10,263.47
🤖 Disciplined Agent ended with: $10,393.73
🏆 Disciplined Agent outperformed by $130.26 (+1.27%)
```

On the main drop, the Panicked Human sold everything and then missed part of the recovery during the fear cooldown. The Disciplined Agent reduced its position by 25% and remained exposed to the market.

The $130.26 difference is from this specific historical test and should not be interpreted as evidence of long-term profitability.

## Panic Check

The Panic Check prevents a single price movement from automatically becoming a panic decision.

In the live demo, BTC was down 2.17%. The simulated Panicked Human sold everything, while the Disciplined Agent held.

The Panic Check produced:

```text
Price Shock       : no
Trend Confirmed   : YES
Volume Confirmed  : no
Bear Case Stronger: no

PANIC SIGNAL : NO
RISK GATE    : FAILED
```

The other signals didn't confirm the move, so the Risk Gate stayed off.

## Why Gemini Is Used

Gemini provides the Bull Case and Bear Case for the current market movement. The Python logic evaluates the measurable panic conditions and applies the Risk Gate, so the final decision does not depend entirely on an LLM response.

## A Real Bug I Found

While building the backtest, I found that Binance's raw data could contain a move around -2.997% while the displayed value rounded to -3.00%. A strict comparison against exactly -3.0% could therefore produce an unexpected result.

I adjusted the implementation to use a small tolerance around the threshold instead of relying on the rounded display value.

## Why This Project

A lot of trading projects focus on finding the next coin to buy or predicting where the price will go. Beats Your Panic focuses on a different problem: what happens when the market suddenly drops and the easiest thing to do is panic?

Instead of trying to predict the future, the agent slows the decision down by checking several signals before deciding whether a move actually deserves a panic response.

## Why Paper Trading

Beats Your Panic is a demonstration project, not a real-money trading system.

The current executable agent uses Binance's public market-data API and does not place real orders. The Binance Agent OS / MCP connection provides the agent-facing integration environment, while the Python application remains focused on paper trading.

## Project Structure

```text
beats-your-panic/
│
├── fetch_price.py
├── fetch_history.py
├── compare_agent.py
├── panic_check.py
├── simulate_outcome.py
├── main_agent.py
├── .env
└── README.md
```

## Limitations

This is a short demonstration rather than a production trading system. The backtest covers one historical period, so the results do not establish long-term performance.

Future improvements could include longer backtests, transaction fees and slippage, more assets and market conditions, out-of-sample testing, and deeper Agent OS MCP integration.

## Hackathon

Project: Beats Your Panic - AI Trading Agent

Hackathon: Binance Agent OS Mini Hackathon

Track: Track A

## Built With

Python, Binance public market-data API, Binance Agent OS / MCP, Gemini, and historical BTC/USDT market data.
