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


def test_strategy_files_exist():
    """Each strategy must have its own file under examples/strategies/qqq/"""
    qqq_dir = REPO_ROOT / "examples" / "strategies" / "qqq"
    assert (qqq_dir / "__init__.py").exists(), "Missing examples/strategies/qqq/__init__.py"
    for name in ["BuyAndHold", "SmaCross", "SmaCross_10_30", "SmaCross_50_200", "RsiStrategy"]:
        path = qqq_dir / f"{name}.py"
        assert path.exists(), f"Missing: examples/strategies/qqq/{name}.py"


def test_strategy_file_class_name_matches_filename():
    """Each strategy file must contain a class with the same name as the file."""
    qqq_dir = REPO_ROOT / "examples" / "strategies" / "qqq"
    for name in ["BuyAndHold", "SmaCross", "SmaCross_10_30", "SmaCross_50_200", "RsiStrategy"]:
        content = (qqq_dir / f"{name}.py").read_text()
        assert f"class {name}(" in content, f"examples/strategies/qqq/{name}.py must define class {name}"


@pytest.mark.network
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
    assert "ERROR" in stderr, "Expected ERROR message in stderr"


@pytest.mark.network
@pytest.mark.parametrize("period", ["1y", "2y", "3y", "5y"])
def test_all_periods_work(period):
    code, stdout, stderr = run_runner("--ticker", "QQQ", "--strategy", "BuyAndHold", "--period", period)
    assert code == 0, f"Runner failed for period={period}. stderr: {stderr}"
    assert "Return (Ann.) [%]" in stdout


PLUGIN_RUNNER = REPO_ROOT / "backtest_runner.py"


def test_plugin_runner_exists():
    assert PLUGIN_RUNNER.exists(), "backtest_runner.py not found at plugin root"


def test_plugin_runner_uses_cwd_for_path():
    """Plugin runner must use os.getcwd() so Claude can call it from any project dir."""
    content = PLUGIN_RUNNER.read_text()
    assert "os.getcwd()" in content, "Plugin runner must use os.getcwd() for sys.path"


@pytest.mark.network
def test_plugin_runner_works_with_cwd_as_examples():
    """Plugin runner finds strategies/ when cwd is set to examples/ directory."""
    result = subprocess.run(
        [sys.executable, str(PLUGIN_RUNNER),
         "--ticker", "QQQ", "--strategy", "BuyAndHold", "--period", "1y"],
        cwd=str(REPO_ROOT / "examples"),
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, f"Plugin runner failed: {result.stderr}"
    assert "Return (Ann.) [%]" in result.stdout
