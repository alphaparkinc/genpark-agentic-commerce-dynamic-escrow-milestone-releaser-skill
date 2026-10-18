from client import AgenticEscrowMilestonePayoutArbiter

def main():
    arbiter = AgenticEscrowMilestonePayoutArbiter()
    crit = {"min_test_pass_rate_pct": 90.0, "require_pr_merged": True}
    telem = {"test_pass_rate_pct": 98.5, "pr_merged": True, "commit_sha": "a1b2c3d4"}
    res = arbiter.evaluate_milestone_and_release("AGR-CORP-401", 1, 3200.0, crit, telem)
    print("--- Digital Escrow Milestone Arbiter ---")
    print(f"Contract: {res['contract_id']} (Milestone {res['milestone_index']})")
    print(f"Status: {res['payout_status']} | Payout: ${res['released_payout_usd']}")
    print(f"Authorization Token: {res['release_auth_token']}")

if __name__ == "__main__":
    main()
