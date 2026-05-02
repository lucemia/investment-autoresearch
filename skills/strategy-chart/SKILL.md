---
name: investment-autoresearch:strategy-chart
description: Use when creating matplotlib/strategy charts. Use when user asks to "draw", "chart", "plot", or "visualize" a strategy, backtest result, or price series.
---

# Strategy Chart

Generate matplotlib charts for backtesting strategy results. Chart is saved to `/tmp/chart.png`.

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

## Step 2: Save

The chart is saved to `/tmp/chart.png`. Copy it wherever needed:

```bash
cp /tmp/chart.png ~/charts/$(date +%Y-%m-%d)-strategy.png
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Forgetting `matplotlib.use("Agg")` | Required for non-interactive (headless) chart generation |
| Not closing figure | Always `plt.close()` after `savefig` to free memory |
