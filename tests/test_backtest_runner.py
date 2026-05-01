"""Smoke tests for the example backtest runner."""
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
EXAMPLES_DIR = REPO_ROOT / "examples"
RUNNER = EXAMPLES_DIR / "backtest_runner.py"


def run_runner(*args):
    """Run the example backtest runner and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        [sys.executable, str(RUNNER), *args],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        timeout=60,
    )
    return result.returncode, result.stdout, result.stderr


def test_runner_exists():
    assert RUNNER.exists(), "examples/backtest_runner.py not found"


def test_buy_and_hold_prints_required_fields():
    code, stdout, stderr = run_runner("--ticker", "QQQ", "--strategy", "BuyAndHold", "--period", "1y")
    assert code == 0, f"Runner exited {code}. stderr: {stderr}"
    assert "Return (Ann.) [%]" in stdout, "Missing 'Return (Ann.) [%]' in output"
    assert "Max. Drawdown [%]" in stdout, "Missing 'Max. Drawdown [%]' in output"


def test_unknown_strategy_exits_nonzero():
    code, stdout, stderr = run_runner("--ticker", "QQQ", "--strategy", "NonExistent", "--period", "1y")
    assert code != 0, "Expected non-zero exit for unknown strategy"
    assert "ERROR" in stderr, "Expected ERROR message in stderr"


def test_unknown_ticker_module_exits_nonzero():
    code, stdout, stderr = run_runner("--ticker", "FAKEXYZ", "--strategy", "BuyAndHold", "--period", "1y")
    assert code != 0, "Expected non-zero exit for unknown ticker module"


@pytest.mark.parametrize("period", ["1y", "2y", "3y", "5y"])
def test_all_periods_work(period):
    code, stdout, stderr = run_runner("--ticker", "QQQ", "--strategy", "BuyAndHold", "--period", period)
    assert code == 0, f"Runner failed for period={period}. stderr: {stderr}"
    assert "Return (Ann.) [%]" in stdout
