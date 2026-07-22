#!/usr/bin/env python3
"""Validate a project's documentation-evidence ledger without dependencies."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


ID_PATTERN = re.compile(r"^[a-z][a-z0-9._-]*$")
CONFIDENCE_VALUES = {"verified", "inferred", "unresolved"}
VOLATILITY_MAX_DAYS = {
    "rapid": 30,
    "living": 120,
    "versioned": 400,
    "immutable": 1100,
}


def parse_date(value: object, field: str, errors: list[str]) -> date | None:
    if not isinstance(value, str):
        errors.append(f"{field} must be an ISO date string (YYYY-MM-DD)")
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        errors.append(f"{field} must be a valid ISO date (YYYY-MM-DD)")
        return None


def require_string(data: dict, field: str, prefix: str, errors: list[str]) -> str | None:
    value = data.get(field)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"{prefix}.{field} must be a non-empty string")
        return None
    return value.strip()


def validate_project_evidence(value: object, prefix: str, errors: list[str]) -> None:
    if not isinstance(value, list) or not value:
        errors.append(f"{prefix}.project_evidence must be a non-empty array")
        return
    for index, item in enumerate(value):
        item_prefix = f"{prefix}.project_evidence[{index}]"
        if not isinstance(item, dict):
            errors.append(f"{item_prefix} must be an object")
            continue
        require_string(item, "locator", item_prefix, errors)
        require_string(item, "value", item_prefix, errors)


def validate_target(value: object, prefix: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        errors.append(f"{prefix}.target must be an object")
        return
    require_string(value, "product", f"{prefix}.target", errors)
    require_string(value, "version", f"{prefix}.target", errors)
    for optional in ("region", "partition", "edition", "configuration"):
        if optional in value and (not isinstance(value[optional], str) or not value[optional].strip()):
            errors.append(f"{prefix}.target.{optional} must be a non-empty string when present")


def validate_source(
    value: object,
    prefix: str,
    required: bool,
    confidence: object,
    as_of: date,
    errors: list[str],
    warnings: list[str],
) -> None:
    if not isinstance(value, dict):
        if confidence == "verified" or required:
            errors.append(f"{prefix}.source must be an object")
        else:
            warnings.append(f"{prefix}.source is absent for a non-verified optional claim")
        return

    source_type = require_string(value, "type", f"{prefix}.source", errors)
    url = require_string(value, "url", f"{prefix}.source", errors)
    require_string(value, "title", f"{prefix}.source", errors)
    require_string(value, "version", f"{prefix}.source", errors)
    require_string(value, "section", f"{prefix}.source", errors)
    require_string(value, "authority_evidence", f"{prefix}.source", errors)
    require_string(value, "target_match_evidence", f"{prefix}.source", errors)
    require_string(value, "freshness_rationale", f"{prefix}.source", errors)
    volatility = require_string(value, "volatility", f"{prefix}.source", errors)

    if (confidence == "verified" or required) and source_type != "primary":
        errors.append(f"{prefix}.source.type must be 'primary' for a required or verified claim")
    if volatility and volatility not in VOLATILITY_MAX_DAYS:
        errors.append(
            f"{prefix}.source.volatility must be one of {sorted(VOLATILITY_MAX_DAYS)}"
        )
    if url:
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.netloc:
            errors.append(f"{prefix}.source.url must be an absolute HTTPS URL")

    retrieved = parse_date(value.get("retrieved_at"), f"{prefix}.source.retrieved_at", errors)
    valid_until = parse_date(value.get("valid_until"), f"{prefix}.source.valid_until", errors)
    if retrieved and retrieved > as_of:
        errors.append(f"{prefix}.source.retrieved_at cannot be after validation date {as_of}")
    if retrieved and valid_until and valid_until < retrieved:
        errors.append(f"{prefix}.source.valid_until cannot precede retrieved_at")
    if retrieved and valid_until and volatility in VOLATILITY_MAX_DAYS:
        validity_days = (valid_until - retrieved).days
        maximum_days = VOLATILITY_MAX_DAYS[volatility]
        if validity_days > maximum_days:
            exception = value.get("validity_exception")
            if not isinstance(exception, str) or not exception.strip():
                errors.append(
                    f"{prefix}.source validity window is {validity_days} days, exceeding "
                    f"the {maximum_days}-day {volatility!r} default; add a non-empty "
                    "validity_exception or shorten the window"
                )
    if "validity_exception" in value and (
        not isinstance(value["validity_exception"], str)
        or not value["validity_exception"].strip()
    ):
        errors.append(
            f"{prefix}.source.validity_exception must be a non-empty string when present"
        )
    if valid_until and valid_until < as_of:
        message = f"{prefix}.source expired on {valid_until}"
        if required:
            errors.append(message)
        else:
            warnings.append(message)


def validate_claim(
    claim: object,
    index: int,
    seen_ids: set[str],
    as_of: date,
    errors: list[str],
    warnings: list[str],
) -> None:
    prefix = f"claims[{index}]"
    if not isinstance(claim, dict):
        errors.append(f"{prefix} must be an object")
        return

    claim_id = require_string(claim, "id", prefix, errors)
    if claim_id:
        if not ID_PATTERN.fullmatch(claim_id):
            errors.append(f"{prefix}.id has an invalid format: {claim_id!r}")
        if claim_id in seen_ids:
            errors.append(f"{prefix}.id is duplicated: {claim_id!r}")
        seen_ids.add(claim_id)

    require_string(claim, "claim", prefix, errors)
    require_string(claim, "evidence", prefix, errors)
    require_string(claim, "decision", prefix, errors)

    required = claim.get("required")
    if not isinstance(required, bool):
        errors.append(f"{prefix}.required must be a boolean")
        required = True

    confidence = claim.get("confidence")
    if confidence not in CONFIDENCE_VALUES:
        errors.append(f"{prefix}.confidence must be one of {sorted(CONFIDENCE_VALUES)}")
    elif required and confidence != "verified":
        errors.append(f"{prefix} is required but confidence is {confidence!r}")
    elif confidence != "verified":
        warnings.append(f"{prefix} remains {confidence!r}")

    validate_project_evidence(claim.get("project_evidence"), prefix, errors)
    validate_target(claim.get("target"), prefix, errors)
    validate_source(claim.get("source"), prefix, required, confidence, as_of, errors, warnings)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger", type=Path, help="Path to documentation-evidence.json")
    parser.add_argument(
        "--as-of",
        type=date.fromisoformat,
        default=date.today(),
        metavar="YYYY-MM-DD",
        help="Validation date used for deterministic tests (default: today)",
    )
    parser.add_argument(
        "--allow-empty",
        action="store_true",
        help="Allow a ledger with no claims (use only while bootstrapping)",
    )
    args = parser.parse_args()

    try:
        data = json.loads(args.ledger.read_text(encoding="utf-8"))
    except OSError as exc:
        print(f"ERROR: cannot read {args.ledger}: {exc}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print(f"ERROR: invalid JSON in {args.ledger}: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(data, dict):
        print("ERROR: ledger root must be an object", file=sys.stderr)
        return 1

    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    generated = parse_date(data.get("generated_at"), "generated_at", errors)
    if generated and generated > args.as_of:
        errors.append(f"generated_at cannot be after validation date {args.as_of}")
    require_string(data, "scope", "ledger", errors)

    claims = data.get("claims")
    if not isinstance(claims, list):
        errors.append("claims must be an array")
        claims = []
    elif not claims and not args.allow_empty:
        errors.append("claims must contain at least one entry")

    seen_ids: set[str] = set()
    for index, claim in enumerate(claims):
        validate_claim(claim, index, seen_ids, args.as_of, errors, warnings)

    for warning in warnings:
        print(f"WARN: {warning}", file=sys.stderr)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        f"Validated {len(claims)} documentation claim(s) as of {args.as_of}"
        f" with {len(warnings)} warning(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
