import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def check_price_shock(pct_change):
    if abs(pct_change) >= 2.99:
        return True, f"Price moved {pct_change:+.2f}% — shock-level move (>=2.99%)"
    else:
        return False, f"Price moved {pct_change:+.2f}% — within normal daily range"


def check_trend_confirmation(recent_changes):
    if len(recent_changes) < 2:
        return False, "Not enough data to confirm a trend"

    today = recent_changes[-1]
    previous_days = recent_changes[:-1]

    same_direction = sum(
        1 for c in previous_days if (c < 0) == (today < 0)
    )

    ratio = same_direction / len(previous_days)

    if ratio >= 0.5:
        return (
            True,
            f"{same_direction}/{len(previous_days)} prior periods moved the same direction — trend confirmed",
        )
    else:
        return (
            False,
            f"Only {same_direction}/{len(previous_days)} prior periods agree — likely an isolated move, not a trend",
        )


def check_volume(volumes):
    if len(volumes) < 2:
        return False, "Not enough volume data"

    latest_volume = volumes[-1]
    previous_volumes = volumes[:-1]

    avg_volume = sum(previous_volumes) / len(previous_volumes)

    ratio = latest_volume / avg_volume if avg_volume > 0 else 0

    if ratio >= 1.5:
        return True, f"Volume is {ratio:.1f}x the recent average — high conviction move"
    else:
        return False, f"Volume is {ratio:.1f}x the recent average — thin/low-conviction move"


def check_bull_bear_validity(pct_change, current_price):
    prompt = (
        f"BTC/USDT is at ${current_price:,.2f}, "
        f"having moved {pct_change:+.2f}% recently.\n\n"
        "Which is more credible right now: the Bull Case or the Bear Case?\n\n"
        "Respond in exactly this format:\n"
        "Verdict: (Bull or Bear)\n"
        "Reason: (one sentence)"
    )

    response = gemini_client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
    )

    text = response.text
    is_bear = "Verdict: Bear" in text

    return is_bear, text


def run_panic_check(pct_change, recent_changes, volumes, current_price):
    shock = check_price_shock(pct_change)
    trend = check_trend_confirmation(recent_changes)
    volume = check_volume(volumes)
    bull_bear = check_bull_bear_validity(pct_change, current_price)

    panic_signal = shock[0] and trend[0] and bull_bear[0]
    risk_gate_passed = panic_signal and volume[0]

    return {
        "panic_signal": panic_signal,
        "risk_gate_passed": risk_gate_passed,
        "shock": shock,
        "trend": trend,
        "volume": volume,
        "bull_bear": bull_bear,
    }