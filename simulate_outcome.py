from compare_agent import panicked_human_decision, disciplined_agent_decision
from fetch_history import get_daily_history
from panic_check import run_panic_check

def main():
    # Pull real daily BTC/USDT history and slice out the real crash week (Aug 27 - Sep 3, 2026)
    full_history = get_daily_history(days=30)
    if not full_history:
        print("Failed to fetch history data.")
        return

    week = [day for day in full_history if "2026-08-27" <= day["date"] <= "2026-09-03"]
    if len(week) != 8:
        print(f"Expected 8 days for Aug 27-Sep 3, got {len(week)}. Check date filtering.")
        return

    daily_changes = [day["pct_change"] for day in week]
    daily_volumes = [day["volume"] for day in week]
    daily_prices = [day["close"] for day in week]

    # Starting balance for both traders ($10,000, fully invested)
    human_balance = 10000.0
    agent_balance = 10000.0

    # Tracking cash state and fear cooldown for panicked human:
    # When human sells, they stay in cash for today AND miss the immediate next day (cooldown = 1 extra day out).
    human_cooldown = 0

    print("=" * 75)
    print(" 8-DAY TRADING SIMULATION (Real Aug 27-Sep 3 Crash Week): Panicked Human vs Agent ")
    print("=" * 75)
    print(f"{'Day':<5} | {'BTC %':<8} | {'Panicked Human':<24} | {'Disciplined Agent':<25}")
    print("-" * 75)

    for day, pct in enumerate(daily_changes, start=1):
        # --- 1. Panicked Human Strategy ---
        h_action, h_reason = panicked_human_decision(pct)
        
        if human_cooldown > 0:
            # Human is currently sitting in cash due to fear cooldown
            human_cooldown -= 1
            h_display_action = "IN CASH (Fear)"
            # Balance stays safe in cash (0% change today)
        else:
            # Human was invested at start of today
            if h_action == "SELL EVERYTHING":
                # Participates in today's drop, converts to cash, and triggers fear cooldown (misses today + 1 extra day)
                human_balance += human_balance * (pct / 100)
                human_cooldown = 1  # 1 means miss immediate next day as well
                h_display_action = "SELL EVERYTHING"
            else:
                # Normal invested day
                human_balance += human_balance * (pct / 100)
                h_display_action = h_action

        # --- 2. Disciplined Agent Strategy ---
        a_action, a_reason = disciplined_agent_decision(pct)
        
        if a_action == "REDUCE POSITION 25%":
            # Reduce invested amount by 25% for that day only (75% exposed to market change, 25% in cash)
            agent_balance += agent_balance * (pct / 100) * 0.75
        else:
            # Stay 100% invested
            agent_balance += agent_balance * (pct / 100) * 1.0

        # Format day log
        human_status = f"${human_balance:,.2f} ({h_display_action})"
        agent_status = f"${agent_balance:,.2f} ({a_action})"
        print(f"Day {day:<2} | {pct:+5.1f}%   | {human_status:<24} | {agent_status:<25}")

    print("=" * 75)
    print(" FINAL RESULTS AFTER 8 DAYS (Real Aug 27-Sep 3 Crash Week) ")
    print("=" * 75)
    print(f"😱 Panicked Human ended with:    ${human_balance:,.2f}")
    print(f"🤖 Disciplined Agent ended with: ${agent_balance:,.2f}")
    
    diff = agent_balance - human_balance
    pct_diff = (diff / human_balance) * 100 if human_balance > 0 else 0
    
    if diff >= 0:
        print(f"🏆 Disciplined Agent outperformed by ${diff:,.2f} (+{pct_diff:.2f}%)")
    else:
        print(f"🏆 Panicked Human outperformed by ${abs(diff):,.2f} ({pct_diff:.2f}%)")
    print("=" * 75)

    # --- 3. Panic Check on the crash day (Day 2, Aug 28, -3.00%) ---
    crash_index = 1  # Day 2 in the list (0-indexed)
    crash_pct = daily_changes[crash_index]
    crash_price = daily_prices[crash_index]
    changes_up_to_crash = daily_changes[:crash_index + 1]
    volumes_up_to_crash = daily_volumes[:crash_index + 1]

    result = run_panic_check(crash_pct, changes_up_to_crash, volumes_up_to_crash, crash_price)

    print("\n" + "=" * 75)
    print(" 🚨 PANIC CHECK — Day 2 (Aug 28 Crash, -3.00%)")
    print("=" * 75)
    print(f" • Price Shock       : {'YES' if result['shock'][0] else 'no'} — {result['shock'][1]}")
    print(f" • Trend Confirmed   : {'YES' if result['trend'][0] else 'no'} — {result['trend'][1]}")
    print(f" • Volume Confirmed  : {'YES' if result['volume'][0] else 'no'} — {result['volume'][1]}")
    print(f" • Bear Case Stronger: {'YES' if result['bull_bear'][0] else 'no'}")
    print("-" * 75)
    print(f" 🔔 PANIC SIGNAL : {'YES' if result['panic_signal'] else 'NO'}")
    print(f" 🛡️  RISK GATE    : {'PASSED' if result['risk_gate_passed'] else 'FAILED'}")
    print("=" * 75)

if __name__ == "__main__":
    main()