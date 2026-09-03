from compare_agent import panicked_human_decision, disciplined_agent_decision

def main():
    # Hardcoded list of 10 fake daily percentage changes for BTC
    daily_changes = [-1.2, -4.5, 2.1, -0.8, 1.5, -3.2, 0.5, 3.8, -1.9, 2.4]

    # Starting balance for both traders ($10,000, fully invested)
    human_balance = 10000.0
    agent_balance = 10000.0

    # Tracking cash state and fear cooldown for panicked human:
    # When human sells, they stay in cash for today AND miss the immediate next day (cooldown = 1 extra day out).
    human_cooldown = 0

    print("=" * 75)
    print(" 10-DAY TRADING SIMULATION (Updated Fear Cooldown): Panicked Human vs Agent ")
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
    print(" FINAL RESULTS AFTER 10 DAYS (Updated Fear Cooldown) ")
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

if __name__ == "__main__":
    main()
