"""Validate autoresearch_result.json conforms to the schema defined in autoresearch-parse SKILL.md."""
import json
from pathlib import Path

import pytest


REQUIRED_TOP_LEVEL = ["ticker", "research_summary", "current_best", "leaderboard",
                       "verified_insights", "rejected_approaches", "open_hypotheses", "recommendation"]
REQUIRED_RESEARCH_SUMMARY = ["rounds_completed", "agents_run"]
REQUIRED_CURRENT_BEST = ["strategy_name", "parameters", "cagr", "max_drawdown",
                          "walk_forward", "min_ra_across_periods"]
VALID_WALK_FORWARD_PERIODS = {"5y", "3y", "2y", "1y"}


def validate_result_json(data: dict) -> list:
    """Return list of validation errors. Empty list = valid."""
    errors = []
    for key in REQUIRED_TOP_LEVEL:
        if key not in data:
            errors.append(f"Missing top-level key: '{key}'")

    rs = data.get("research_summary", {})
    for key in REQUIRED_RESEARCH_SUMMARY:
        if key not in rs:
            errors.append(f"Missing research_summary.{key}")

    cb = data.get("current_best", {})
    for key in REQUIRED_CURRENT_BEST:
        if key not in cb:
            errors.append(f"Missing current_best.{key}")

    wf = cb.get("walk_forward", {})
    for period in VALID_WALK_FORWARD_PERIODS:
        if period not in wf:
            errors.append(f"Missing current_best.walk_forward.{period}")
        else:
            entry = wf[period]
            if "cagr" not in entry:
                errors.append(f"Missing current_best.walk_forward.{period}.cagr")
            if "ra" not in entry:
                errors.append(f"Missing current_best.walk_forward.{period}.ra")

    for i, item in enumerate(data.get("rejected_approaches", [])):
        if "approach" not in item:
            errors.append(f"rejected_approaches[{i}] missing 'approach'")
        if "reason" not in item:
            errors.append(f"rejected_approaches[{i}] missing 'reason'")

    rec = data.get("recommendation", {})
    if "graduate" not in rec:
        errors.append("Missing recommendation.graduate")

    return errors


def test_sample_result_is_valid(sample_result_json):
    errors = validate_result_json(sample_result_json)
    assert errors == [], "Sample JSON has schema errors:\n" + "\n".join(errors)


def test_missing_ticker_is_invalid(sample_result_json):
    del sample_result_json["ticker"]
    errors = validate_result_json(sample_result_json)
    assert any("ticker" in e for e in errors)


def test_missing_walk_forward_period_is_invalid(sample_result_json):
    del sample_result_json["current_best"]["walk_forward"]["3y"]
    errors = validate_result_json(sample_result_json)
    assert any("3y" in e for e in errors)


def test_missing_rejected_reason_is_invalid(sample_result_json):
    sample_result_json["rejected_approaches"] = [{"approach": "SMA 10/30"}]
    errors = validate_result_json(sample_result_json)
    assert any("reason" in e for e in errors)


def test_real_result_json_if_exists(repo_root):
    """If an archive result exists, validate it against schema."""
    archive = repo_root / "archive"
    if not archive.exists():
        pytest.skip("No archive directory")
    result_files = list(archive.glob("*/autoresearch_result.json"))
    if not result_files:
        pytest.skip("No autoresearch_result.json found in archive/")
    for path in result_files:
        data = json.loads(path.read_text())
        errors = validate_result_json(data)
        assert errors == [], f"{path} has schema errors:\n" + "\n".join(errors)
