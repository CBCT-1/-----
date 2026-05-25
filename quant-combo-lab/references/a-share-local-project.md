# A-Share Local Project Reference

Use this reference for local A-share quant projects with cached daily bars.

## Expected Project Shape

Common files:

- `run_full_a_cache.py`: local A-share cache update/audit and optional scanner.
- `run_parallel_backfill.py`: per-code fallback backfill for stale/missing rows.
- `run_strategy_lab_2025.py`: medium-size strategy combination search.
- `run_massive_full_market_search.py`: larger strategy search over many specs.
- `run_active_models_2y_backtest.py`: active-model comparison backtest.
- `run_top1_trade_signal.py` and `run_model3_trade_signal.py`: frozen daily manual tickets.

Common data:

- `data/a_share/history/*.parquet`
- `data/a_share/tradable_universe_<date>.csv`
- `results/*`

## Data Hygiene

Before interpreting a current-day model report:

1. Confirm the latest local date equals the intended signal date.
2. Audit cache status if possible. For this project, `run_parallel_backfill.py --date <date>` writes `results/full_a_scan/parallel_audit_after_<date>.csv`.
3. If a full universe refresh fails, copying the previous universe snapshot to the current date can be acceptable for same-market continuity, but label this clearly.
4. Re-run tail backfill with fewer workers if parallel BaoStock calls leave stale rows.

## Execution Integrity

Backtest and live recommendation cadence must match:

- Monthly model: rank daily for observation, trade monthly plus stop/take-profit triggers.
- Weekly model: trade weekly plus stop triggers.
- Daily scanner: only valid as a daily trading model if the backtest also rebalances daily.

Do not mix a daily rank with a monthly backtest as if it were a daily switch instruction.

## Output Requirements

For each candidate model report:

- model name and exact parameters
- data start/end dates
- annual return
- maximum drawdown
- Calmar and Sharpe when available
- final equity from small-account capital
- trade count and total costs
- latest manual orders
- explicit sell/hold conditions

Always flag whether the candidate is mainboard-only or includes ChiNext/other boards.
