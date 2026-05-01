"""Validate all SKILL.md files and plugin.json have required fields."""
import json
import re
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
PLUGIN_JSON = REPO_ROOT / ".claude-plugin" / "plugin.json"

SKILL_DIRS = [d for d in SKILLS_DIR.iterdir() if d.is_dir()] if SKILLS_DIR.exists() else []


def test_plugin_json_is_valid():
    assert PLUGIN_JSON.exists(), "plugin.json not found"
    data = json.loads(PLUGIN_JSON.read_text())
    assert "name" in data, "plugin.json missing 'name'"
    assert "version" in data, "plugin.json missing 'version'"
    assert "description" in data, "plugin.json missing 'description'"


def test_plugin_json_version_semver():
    data = json.loads(PLUGIN_JSON.read_text())
    version = data["version"]
    assert re.match(r"^\d+\.\d+\.\d+$", version), f"version '{version}' is not semver"


@pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=[d.name for d in SKILL_DIRS])
def test_skill_md_exists(skill_dir):
    skill_md = skill_dir / "SKILL.md"
    assert skill_md.exists(), f"Missing SKILL.md in {skill_dir.name}"


@pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=[d.name for d in SKILL_DIRS])
def test_skill_md_has_frontmatter(skill_dir):
    skill_md = skill_dir / "SKILL.md"
    content = skill_md.read_text()
    assert content.startswith("---"), f"{skill_dir.name}/SKILL.md missing frontmatter (---)"
    end = content.index("---", 3)
    frontmatter = content[3:end]
    assert "name:" in frontmatter, f"{skill_dir.name}/SKILL.md frontmatter missing 'name:'"
    assert "description:" in frontmatter, f"{skill_dir.name}/SKILL.md frontmatter missing 'description:'"


@pytest.mark.parametrize("skill_dir", SKILL_DIRS, ids=[d.name for d in SKILL_DIRS])
def test_skill_md_name_matches_dir(skill_dir):
    skill_md = skill_dir / "SKILL.md"
    content = skill_md.read_text()
    end = content.index("---", 3)
    frontmatter = content[3:end]
    name_match = re.search(r"^name:\s*(.+)$", frontmatter, re.MULTILINE)
    assert name_match, f"{skill_dir.name}/SKILL.md frontmatter 'name:' not parseable"
    name = name_match.group(1).strip()
    assert name == skill_dir.name, (
        f"{skill_dir.name}/SKILL.md name='{name}' does not match directory name '{skill_dir.name}'"
    )
