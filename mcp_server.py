#!/usr/bin/env python3
import json
import sys
from client import AgenticEscrowMilestonePayoutArbiter

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        arbiter = AgenticEscrowMilestonePayoutArbiter()
        criteria = {"min_test_pass_rate_pct": 95.0, "require_pr_merged": True}
        telemetry = {"test_pass_rate_pct": 100.0, "pr_merged": True, "commit_sha": "c0ffee77"}
        res = arbiter.evaluate_milestone_and_release("ESCROW-7891", 2, 4500.0, criteria, telemetry)
        assert res["payout_status"] == "ESCROW_PAYOUT_RELEASED"
        assert res["released_payout_usd"] == 4500.0
        assert res["release_auth_token"] is not None
        print(f"[TEST PASS] Escrow Payout Released: ${res['released_payout_usd']}")
        sys.exit(0)

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            if method == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"serverInfo": {"name": "genpark-escrow-arbiter", "version": "1.0.0"}}}))
            elif method == "tools/list":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [{"name": "evaluate_milestone_and_release", "description": "Evaluate digital contract milestone criteria and release escrow funds"}]}}))
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                arbiter = AgenticEscrowMilestonePayoutArbiter()
                out = arbiter.evaluate_milestone_and_release(
                    args.get("contract_id", "ESCROW-000"),
                    int(args.get("milestone_index", 1)),
                    float(args.get("allocated_escrow_usd", 1000.0)),
                    args.get("acceptance_criteria", {}),
                    args.get("delivery_telemetry", {})
                )
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(out)}]}}))
            else:
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
