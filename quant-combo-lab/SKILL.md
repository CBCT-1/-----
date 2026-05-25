---
name: quant-combo-lab
description: Build, run, and summarize broad local quantitative strategy combination tests. Use when Codex is asked to create many quant model variants, backtest multiple trading strategies or parameter combinations, compare annual return and drawdown, search for high-return low-drawdown portfolios, or package/re-run an A-share/local-market strategy lab from cached OHLCV data.
---

# Quant Combo Lab

## Core Rule

Keep the backtest execution frequency identical to the intended trading frequency. A monthly model must be backtested as monthly rebalancing; a weekly model as weekly; a daily scanner as daily. Do not report daily-changing rankings as daily trade instructions unless the simulation also trades daily.

## Workflow

1. Confirm the target universe, tradability constraints, cash/lot rules, rebalance frequency, and risk controls.
2. Verify local data coverage before testing. Prefer local cached OHLCV/parquet data; update or audit missing rows before running broad searches.
3. Generate many strategy specs by varying:
   - score formula: momentum windows, low volatility, pullback, RSI, liquidity, trend-stack, anti-overheat.
   - filter profile: liquidity, mainboard-only, near-high, pullback band, low-volatility, price/cash affordability.
   - execution: daily, weekly, monthly.
   - allocation: one-lot rank fill, one-lot each, single-fill, rank-fill.
   - risk controls: stop loss, trailing stop, take profit, cooldown.
4. Simulate with realistic small-account execution: initial cash, 100-share lots, commission/minimum commission, stamp duty on sells, transfer fee, and slippage.
5. Rank results by annual return first, then drawdown, Calmar, Sharpe, trade count, and cost. Always show maximum drawdown beside return.
6. Save reproducible artifacts: summary CSV, top orders CSV, equity curves, trades, and a markdown report.
7. Freeze any selected model by recording its exact name, parameters, data window, metrics, and script path.

## Bundled Script

Use `scripts/run_quant_combo_lab.py` when the project already has local strategy lab scripts. It detects common files such as:

- `run_strategy_lab_2025.py`
- `run_massive_full_market_search.py`
- `run_active_models_2y_backtest.py`

Example:

```powershell
python C:\Users\lhc\.codex\skills\quant-combo-lab\scripts\run_quant_combo_lab.py --project "E:\Documents\New project" --end 2026-05-21 --max-specs 6000
```

Fast smoke test:

```powershell
python C:\Users\lhc\.codex\skills\quant-combo-lab\scripts\run_quant_combo_lab.py --project "E:\Documents\New project" --end 2026-05-21 --max-specs 200
```

The script writes combined outputs under `results/quant_combo_lab/`.

## A-Share Local Project Notes

For the current A-share project, read `references/a-share-local-project.md` before editing strategy scripts or interpreting results.

Important defaults:

- Manual recommendations only. Never log in to a brokerage account or place orders.
- Respect the user's tradability limits. Default to mainboard-only when the user cannot buy ChiNext/STAR/Beijing/Neeq.
- Keep data refresh separate from strategy evaluation. If today's cache is stale, say so and either update it or label the backtest date clearly.
- Distinguish "rank/watchlist" from "trade action." A Top1 monthly model can show a daily rank, but it should only trade on monthly rebalance or risk triggers.
