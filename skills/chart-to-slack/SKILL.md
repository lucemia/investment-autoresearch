---
name: chart-to-slack
description: Use when creating matplotlib/strategy charts and uploading images to Slack. Use when user asks to "draw", "chart", "plot", "visualize" and "send" or "post" to Slack.
---

# Chart to Slack

Generate matplotlib charts and upload to Slack via 3-step files API.

## Environment

```bash
# Bot token from .env in project root (auto-loaded by Django)
SLACK_BOT_TOKEN=xoxb-...  # or read from .env
```

## Channel IDs

Find your channel ID in Slack: right-click any channel → **View channel details** → copy the ID at the bottom.

| Channel      | ID            |
|--------------|---------------|
| #investment  | YOUR_CHANNEL_ID |

## Step 1: Generate Chart

```python
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt

# ... create figure ...
plt.savefig("/tmp/chart.png", dpi=150, bbox_inches="tight",
            facecolor=fig.get_facecolor(), edgecolor="none")
plt.close()
```

### Dark Theme Palette

```python
colors = {
    "bg": "#1a1a2e", "panel": "#16213e", "text": "#e0e0e0",
    "grid": "#2a2a4a", "equity": "#00d4aa", "price": "#6c7b95",
    "buy": "#00ff88", "sell": "#ff4466", "drawdown": "#ff6b6b",
    "vix": "#ffa726",
}
fig.patch.set_facecolor(colors["bg"])
for ax in axes:
    ax.set_facecolor(colors["panel"])
    ax.tick_params(colors=colors["text"])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
```

## Step 2: Upload to Slack (3-step files API)

Read token from environment variable:

```bash
# Read from environment variable (set in your shell profile or Claude Code settings)
SLACK_TOKEN=$SLACK_BOT_TOKEN
```

### 2a. Get upload URL

```bash
RESPONSE=$(curl -s -X POST "https://slack.com/api/files.getUploadURLExternal" \
  -H "Authorization: Bearer $SLACK_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "filename=chart.png&length=$(wc -c < /tmp/chart.png | tr -d ' ')")
UPLOAD_URL=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['upload_url'])")
FILE_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['file_id'])")
```

### 2b. Upload file

```bash
curl -s -X POST "$UPLOAD_URL" -F "file=@/tmp/chart.png"
```

### 2c. Complete upload to channel

```bash
curl -s -X POST "https://slack.com/api/files.completeUploadExternal" \
  -H "Authorization: Bearer $SLACK_TOKEN" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d '{
    "files": [{"id": "'$FILE_ID'", "title": "Chart Title"}],
    "channel_id": "YOUR_CHANNEL_ID",
    "initial_comment": "Description of the chart"
  }'
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Bot token not set | Set `SLACK_BOT_TOKEN` in your shell profile (`~/.zshrc`) or Claude Code env settings |
| MCP Slack tool for images | MCP `slack_send_message` can't attach files — use files API |
| Forgetting `matplotlib.use("Agg")` | Required for non-interactive (headless) chart generation |
| Not closing figure | Always `plt.close()` after `savefig` to free memory |
| Using `xoxp-` token | Use `xoxb-` bot token from `.env` |

## Strategy Chart Layout (Investment Project)

For backtesting strategy charts, use 3-panel layout:

```
Panel 1 (3x height): Price + Equity curve + Buy/Sell markers + Stats box
Panel 2 (1.5x):      Drawdown fill
Panel 3 (1x):         VIX with threshold lines
```

```python
fig, axes = plt.subplots(3, 1, figsize=(16, 12),
                         gridspec_kw={"height_ratios": [3, 1.5, 1]})
```
