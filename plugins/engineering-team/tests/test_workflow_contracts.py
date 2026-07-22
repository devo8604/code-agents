from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path
from pathlib import PurePosixPath


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
FIXTURES = Path(__file__).resolve().parent / "fixtures" / "workflow_contract_scenarios.json"
ORCHESTRATOR = PLUGIN_ROOT / "skills" / "orchestrate-system-change" / "SKILL.md"
LEDGER = ORCHESTRATOR.parent / "references" / "orchestration-ledger.md"
GATE = PLUGIN_ROOT / "skills" / "review-system-change" / "references" / "gate-record.md"
BOOTSTRAP = PLUGIN_ROOT / "skills" / "bootstrap-project-context" / "SKILL.md"
REFRESH = BOOTSTRAP.parent / "references" / "refresh-protocol.md"


def valid_plan(plan: dict) -> bool:
    criteria = plan.get("acceptance_criteria")
    packages = plan.get("work_packages")
    return bool(
        plan.get("plan_id")
        and plan.get("outcome")
        and criteria
        and packages
        and all(item.get("id") and item.get("verification") for item in criteria)
        and all(
            item.get("id")
            and "dependencies" in item
            and item.get("owner")
            and item.get("owned_paths")
            and "exclusions" in item
            and item.get("criteria_ids")
            for item in packages
        )
    )


def valid_receipt(receipt: dict | None) -> bool:
    required = {
        "receipt_id", "command", "working_directory", "started_at",
        "finished_at", "exit_code", "evidence", "evidence_sha256",
    }
    if not receipt or not required.issubset(receipt) or receipt["exit_code"] != 0:
        return False
    digest = hashlib.sha256(receipt["evidence"].encode()).hexdigest()
    return digest == receipt["evidence_sha256"]


def valid_reviewer(gate: dict) -> bool:
    reviewer = gate.get("reviewer")
    return bool(
        reviewer
        and reviewer.get("identity")
        and reviewer.get("role")
        and reviewer.get("independence")
        and reviewer.get("implementation_owners") is not None
    )


def accepted_risk_authorized(finding: dict, authorized_acceptors: list[str]) -> bool:
    required = {
        "root_key", "rationale", "residual_impact", "risk_acceptor",
        "approval_receipt",
    }
    has_review_bound = bool(finding.get("expiry") or finding.get("review_condition"))
    receipt = finding.get("approval_receipt")
    receipt_required = {
        "receipt_id", "trusted_source", "approver_identity", "authority",
        "decision", "finding_id", "scope_ids", "timestamp", "content_digest",
        "readback_verified",
    }
    return bool(
        finding.get("disposition") == "accepted_risk"
        and required.issubset(finding)
        and has_review_bound
        and finding["risk_acceptor"] in authorized_acceptors
        and isinstance(receipt, dict)
        and receipt_required.issubset(receipt)
        and receipt["approver_identity"] == finding["risk_acceptor"]
        and receipt["finding_id"] == finding.get("finding_id")
        and receipt["decision"] == "accept"
        and receipt["readback_verified"] is True
    )


def path_within_scope(path: str, roots: tuple[str, ...]) -> bool:
    candidate = PurePosixPath(path)
    if candidate.is_absolute() or ".." in candidate.parts:
        return False
    return any(candidate == PurePosixPath(root) or PurePosixPath(root) in candidate.parents
               for root in roots)


def loop_result(scenario: dict) -> str:
    seen: set[str] = set()
    previous: set[str] | None = None
    repeated_root_cycles = 0
    for index, roots in enumerate(scenario["iterations"], start=1):
        current = set(roots)
        new_roots = current - seen
        if len(seen | new_roots) > scenario["max_distinct_findings"]:
            return "checkpoint"
        seen |= new_roots
        if not current:
            return "converged"
        repeated_root_cycles = repeated_root_cycles + 1 if previous == current else 0
        if repeated_root_cycles >= 2:
            return "non_convergent"
        if index >= scenario["max_iterations"]:
            return "checkpoint"
        previous = current
    return "incomplete"


def seal_ledger(records: list[dict]) -> list[dict]:
    sealed: list[dict] = []
    prior_digest = "GENESIS"
    for record in records:
        candidate = {**record, "prior_digest": prior_digest}
        encoded = json.dumps(candidate, sort_keys=True, separators=(",", ":")).encode()
        candidate["digest"] = hashlib.sha256(encoded).hexdigest()
        sealed.append(candidate)
        prior_digest = candidate["digest"]
    return sealed


def valid_ledger_chain(records: list[dict]) -> bool:
    prior_digest = "GENESIS"
    for record in records:
        candidate = {key: value for key, value in record.items() if key != "digest"}
        if candidate.get("prior_digest") != prior_digest:
            return False
        encoded = json.dumps(candidate, sort_keys=True, separators=(",", ":")).encode()
        if hashlib.sha256(encoded).hexdigest() != record.get("digest"):
            return False
        prior_digest = record["digest"]
    return True


class WorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.scenarios = json.loads(FIXTURES.read_text(encoding="utf-8"))

    def test_incomplete_plan_is_rejected_before_execution(self) -> None:
        self.assertFalse(valid_plan(self.scenarios["incomplete_plan"]))

    def test_bootstrap_refresh_reconciles_git_drift_and_full_tree(self) -> None:
        contract = BOOTSTRAP.read_text(encoding="utf-8") + REFRESH.read_text(encoding="utf-8")
        for phrase in (
            "Project context freshness", "current `HEAD`", "current-tree rescan",
            "uncommitted and untracked", "human-policy", "Invalidate or refresh",
        ):
            self.assertIn(phrase, contract)

    def test_audit_and_remediation_scopes_remain_separate(self) -> None:
        scenario = self.scenarios["scope_separation"]
        audit_roots = tuple(scenario["audit_scope"])
        write_roots = tuple(scenario["remediation_write_scope"])
        self.assertNotEqual(audit_roots, write_roots)
        self.assertTrue(any(path.startswith("deploy/") for path in scenario["audit_observed"]))
        self.assertTrue(all(path_within_scope(path, write_roots) for path in scenario["writes"]))
        self.assertFalse(path_within_scope("src/../deploy/service.yaml", ("src",)))
        self.assertFalse(path_within_scope("src-unauthorized/file", ("src",)))
        self.assertFalse(path_within_scope("/src/file", ("src",)))

    def test_missing_reviewer_fails_closed(self) -> None:
        self.assertFalse(valid_reviewer(self.scenarios["missing_reviewer"]))

    def test_missing_and_forged_receipts_fail_closed(self) -> None:
        receipts = self.scenarios["receipts"]
        self.assertTrue(valid_receipt(receipts["valid"]))
        self.assertFalse(valid_receipt(receipts["forged"]))
        self.assertFalse(valid_receipt(receipts["missing"]))

    def test_accepted_risk_requires_named_authority(self) -> None:
        scenario = self.scenarios["accepted_risk"]
        self.assertFalse(
            accepted_risk_authorized(scenario["finding"], scenario["authorized_acceptors"])
        )

    def test_convergence_and_non_convergence_are_bounded(self) -> None:
        self.assertEqual(loop_result(self.scenarios["convergence"]), "converged")
        self.assertEqual(
            loop_result(self.scenarios["non_convergence"]), "non_convergent"
        )

    def test_distinct_finding_budget_counts_root_key_union(self) -> None:
        scenario = self.scenarios["distinct_finding_budget"]
        self.assertEqual(loop_result(scenario), "checkpoint")
        flattened = [root for iteration in scenario["iterations"] for root in iteration]
        self.assertGreater(len(flattened), len(set(flattened)))
        self.assertEqual(len(set(flattened)), 3)

    def test_resume_uses_persistent_ledger_not_conversation(self) -> None:
        scenario = self.scenarios["resume_context_loss"]
        self.assertTrue(scenario["ledger_path"].startswith(".codex/"))
        sealed = seal_ledger(scenario["records"])
        self.assertTrue(valid_ledger_chain(sealed))
        transitions = [
            record for record in scenario["records"]
            if record["record_type"] == "transition"
        ]
        self.assertEqual(
            [record["sequence"] for record in transitions],
            list(range(1, len(transitions) + 1)),
        )
        recovered = transitions[-1]["next_status"]
        self.assertEqual(recovered, scenario["expected_status"])
        self.assertNotEqual(recovered, scenario["conversation_claimed_status"])
        sealed[1]["next_status"] = "complete"
        self.assertFalse(valid_ledger_chain(sealed))

    def test_checked_in_contracts_state_required_fail_closed_rules(self) -> None:
        orchestrator = ORCHESTRATOR.read_text(encoding="utf-8")
        ledger = LEDGER.read_text(encoding="utf-8")
        gate = GATE.read_text(encoding="utf-8")
        for phrase in (
            "audit_scope", "remediation_write_scope", "project-approved",
            "append-only", "max_distinct_findings", "max_elapsed_minutes",
            "fail closed",
        ):
            self.assertIn(phrase, orchestrator + ledger)
        for phrase in (
            "comparison_base", "result_revision", "root_key", "risk_acceptor",
            "evidence_sha256", "invalidation triggers", "whole-plan",
        ):
            self.assertIn(phrase, gate)


if __name__ == "__main__":
    unittest.main()
