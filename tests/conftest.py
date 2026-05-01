import json
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).parent.parent


@pytest.fixture
def repo_root():
    return REPO_ROOT


@pytest.fixture
def skills_dir():
    return REPO_ROOT / "skills"


@pytest.fixture
def sample_result_json():
    """Minimal valid autoresearch_result.json for schema tests."""
    return {
        "ticker": "QQQ",
        "research_summary": {
            "rounds_completed": 1,
            "agents_run": 4,
            "strategies_tested": 4,
        },
        "current_best": {
            "strategy_name": "SmaCross_50_200",
            "parameters": {},
            "cagr": 9.57,
            "max_drawdown": -20.71,
            "sharpe": None,
            "robustness_score": None,
            "walk_forward": {
                "5y": {"cagr": 9.57, "ra": 0.46},
                "3y": {"cagr": 14.21, "ra": 0.82},
                "2y": {"cagr": 19.60, "ra": 1.45},
                "1y": {"cagr": None, "ra": None},
            },
            "min_ra_across_periods": 0.46,
        },
        "leaderboard": [
            {
                "rank": 1,
                "strategy_name": "SmaCross_50_200",
                "cagr": 9.57,
                "max_drawdown": -20.71,
                "calmar": 0.46,
                "trades": 4,
            }
        ],
        "verified_insights": ["Slow SMA crossovers halve max drawdown vs buy-and-hold"],
        "rejected_approaches": [
            {"approach": "SMA 10/30", "reason": "Commission drag, whipsaws in trending asset"}
        ],
        "open_hypotheses": ["SMA 30/100 intermediate speed"],
        "recommendation": {
            "graduate": "SmaCross_50_200",
            "confidence": "medium",
        },
    }
