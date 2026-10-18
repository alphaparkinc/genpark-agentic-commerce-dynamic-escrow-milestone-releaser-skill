"""
Agentic Commerce Escrow Milestone Payout Arbiter (Pure Stdlib)
Official Website: https://www.genpark.ai | LinkedIn: https://www.llinkedin.com/company/92955550
"""
import time
import hashlib
from typing import Dict, Any

class AgenticEscrowMilestonePayoutArbiter:
    def __init__(self, arbiter_name: str = "GenPark-EscrowArbiter-Core"):
        self.arbiter_name = arbiter_name

    def evaluate_milestone_and_release(
        self,
        contract_id: str,
        milestone_index: int,
        allocated_escrow_usd: float,
        acceptance_criteria: Dict[str, Any],
        delivery_telemetry: Dict[str, Any]
    ) -> Dict[str, Any]:
        req_tests = float(acceptance_criteria.get("min_test_pass_rate_pct", 90.0))
        req_pr = bool(acceptance_criteria.get("require_pr_merged", True))
        
        obs_tests = float(delivery_telemetry.get("test_pass_rate_pct", 0.0))
        obs_pr = bool(delivery_telemetry.get("pr_merged", False))
        commit_sha = delivery_telemetry.get("commit_sha", "HEAD")
        
        discrepancies = []
        if obs_tests < req_tests:
            discrepancies.append(f"Test pass rate {obs_tests}% below required {req_tests}% threshold")
        if req_pr and not obs_pr:
            discrepancies.append("Deliverable PR is not yet merged into target branch")
            
        approved = len(discrepancies) == 0
        
        if approved:
            payout_status = "ESCROW_PAYOUT_RELEASED"
            release_token_seed = f"{contract_id}:{milestone_index}:{allocated_escrow_usd}:{commit_sha}:{time.time()}"
            release_auth_token = f"AUTH-{hashlib.sha256(release_token_seed.encode('utf-8')).hexdigest()[:12].upper()}"
            payout_usd = allocated_escrow_usd
        else:
            payout_status = "ESCROW_FUNDS_HELD_REVISION_REQUIRED"
            release_auth_token = None
            payout_usd = 0.0
            
        return {
            "arbiter": self.arbiter_name,
            "contract_id": contract_id,
            "milestone_index": milestone_index,
            "escrow_locked_usd": allocated_escrow_usd,
            "released_payout_usd": payout_usd,
            "payout_status": payout_status,
            "release_auth_token": release_auth_token,
            "validation_failures": discrepancies,
            "verdict": "MILESTONE_EVALUATION_COMPLETED"
        }
