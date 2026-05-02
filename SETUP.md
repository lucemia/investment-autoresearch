# Setup Guide

Complete these steps once before using the plugin skills.

## 1. Install the plugin

**Option A — Claude Code marketplace (when available):**
```bash
claude plugin install gh:lucemia/investment-autoresearch
```

**Option B — Manual install (git clone):**
```bash
git clone https://github.com/lucemia/investment-autoresearch ~/.claude/plugins/cache/lucemia/investment-autoresearch
# Copy skills into your Claude Code skills directory:
for skill in ~/.claude/plugins/cache/lucemia/investment-autoresearch/skills/*/; do
  cp -r "$skill" ~/.claude/skills/"$(basename "$skill")"
done
```

## 2. Install Python dependencies

```bash
pip install backtesting yfinance
```

## 3. Configure chart uploads (optional)

### Slack

**Get a bot token:**
1. Go to https://api.slack.com/apps → Create New App
2. Add OAuth scopes: `files:write`, `chat:write`
3. Install to workspace and copy the `xoxb-` bot token

**Get your channel ID:**
Right-click any Slack channel → **View channel details** → copy the ID (starts with `C`).

**Set in your shell profile** (`~/.zshrc` or `~/.bashrc`):

```bash
export SLACK_BOT_TOKEN=xoxb-your-token-here
```

**Update the channel ID** in `skills/investment-autoresearch-strategy-chart/SKILL.md`:
Find `YOUR_CHANNEL_ID` and replace with your actual channel ID (e.g. `C0XXXXXXXXX`).

> **Note:** This edit lives inside the plugin install directory. If you reinstall or update the plugin, you will need to re-apply this change. Alternatively, set `SLACK_CHANNEL_ID` as an env var and update the skill to read from it instead.

### Discord

Set `DISCORD_BOT_TOKEN` in your shell profile and use your Discord channel ID when the skill prompts.

### Local only

Skip steps above. Charts save to `/tmp/chart.png` automatically.

## 4. Verify everything works

Run the test suite from the plugin repo:

```bash
pip install pytest && python3 -m pytest tests/ -v
```

All tests should pass. The runner smoke tests require network access for yfinance data.
