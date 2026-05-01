---
name: investment-strategy-chart
description: Use when creating matplotlib/strategy charts. Use when user asks to "draw", "chart", "plot", or "visualize" a strategy, backtest result, or price series. Optionally uploads to a chat platform.
---

# Strategy Chart

Generate matplotlib charts for backtesting strategy results. Chart generation is standalone; upload to your chat platform is optional.

## Step 1: Generate Chart

```python
import matplotlib
matplotlib.use("Agg")  # Non-interactive backend — required for headless environments
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

### Strategy Chart Layout

3-panel layout for backtesting charts:

```
Panel 1 (3x height): Price + Equity curve + Buy/Sell markers + Stats box
Panel 2 (1.5x):      Drawdown fill
Panel 3 (1x):        VIX or volatility indicator with threshold lines
```

```python
fig, axes = plt.subplots(3, 1, figsize=(16, 12),
                         gridspec_kw={"height_ratios": [3, 1.5, 1]})
```

## Step 2: Upload (Optional)

Once the chart is saved to `/tmp/chart.png`, upload it to your platform of choice.

### Slack (3-step files API)

Requires `SLACK_BOT_TOKEN` env var (`xoxb-` bot token with `files:write` scope).

```bash
SLACK_TOKEN=$SLACK_BOT_TOKEN

# 2a. Get upload URL
RESPONSE=$(curl -s -X POST "https://slack.com/api/files.getUploadURLExternal" \
  -H "Authorization: Bearer $SLACK_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "filename=chart.png&length=$(wc -c < /tmp/chart.png | tr -d ' ')")
UPLOAD_URL=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['upload_url'])")
FILE_ID=$(echo "$RESPONSE" | python3 -c "import sys,json; print(json.load(sys.stdin)['file_id'])")

# 2b. Upload file
curl -s -X POST "$UPLOAD_URL" -F "file=@/tmp/chart.png"

# 2c. Complete upload to channel
curl -s -X POST "https://slack.com/api/files.completeUploadExternal" \
  -H "Authorization: Bearer $SLACK_TOKEN" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d '{
    "files": [{"id": "'$FILE_ID'", "title": "Chart Title"}],
    "channel_id": "YOUR_CHANNEL_ID",
    "initial_comment": "Description of the chart"
  }'
```

### Discord

Requires `DISCORD_BOT_TOKEN` and a channel webhook URL or channel ID.

```bash
curl -s -X POST "https://discord.com/api/v10/channels/YOUR_CHANNEL_ID/messages" \
  -H "Authorization: Bot $DISCORD_BOT_TOKEN" \
  -F "content=Description of the chart" \
  -F "file=@/tmp/chart.png"
```

### Save locally

If you don't need to upload, the chart is already at `/tmp/chart.png`. Copy it wherever needed:

```bash
cp /tmp/chart.png ~/charts/$(date +%Y-%m-%d)-strategy.png
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Forgetting `matplotlib.use("Agg")` | Required for non-interactive (headless) chart generation |
| Not closing figure | Always `plt.close()` after `savefig` to free memory |
| Slack: MCP tool for images | MCP `slack_send_message` can't attach files — use files API |
| Slack: using `xoxp-` token | Use `xoxb-` bot token |
| Slack: bot token not set | Set `SLACK_BOT_TOKEN` in your shell profile (`~/.zshrc`) or Claude Code env settings |
