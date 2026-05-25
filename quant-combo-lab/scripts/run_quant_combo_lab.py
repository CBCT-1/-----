from __future__ import annotations

import argparse
import subprocess
import sys
from datetime import date
from pathlib import Path

import pandas as pd


def run(command: list[str], cwd: Path, timeout: int | None = None) -> None:
    print(f"running: {' '.join(command)}", flush=True)
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=timeout)
    if completed.stdout:
        print(completed.stdout, flush=True)
    if completed.stderr:
        print(completed.stderr, file=sys.stderr, flush=True)
    if completed.returncode != 0:
        raise RuntimeError(f"command failed ({completed.returncode}): {' '.join(command)}")


def read_summary(path: Path, source: str) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame()
    df = pd.read_csv(path)
    if "strategy" not in df.columns:
        first = df.columns[0]
        if first.startswith("Unnamed") or first in {"", "index"}:
            df = df.rename(columns={first: "strategy"})
        else:
            df.insert(0, "strategy", df[first].astype(str))
    df["source"] = source
    return df


def normalize_summary(frames: list[pd.DataFrame]) -> pd.DataFrame:
    frames = [frame for frame in frames if not frame.empty]
    if not frames:
        return pd.DataFrame()
    df = pd.concat(frames, ignore_index=True, sort=False)
    for column in ["annual_return", "max_drawdown", "calmar", "sharpe", "final_equity", "trade_count", "total_cost"]:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")
        else:
            df[column] = pd.NA
    df["objective"] = (
        df["annual_return"].clip(lower=-1).fillna(-1)
        + 0.45 * df["calmar"].replace([float("inf"), float("-inf")], pd.NA).fillna(0)
        + 0.25 * df["sharpe"].fillna(0)
        + 0.75 * df["max_drawdown"].fillna(-1)
        - 0.0005 * df["trade_count"].fillna(0)
    )
    keep = [
        "source",
        "strategy",
        "annual_return",
        "max_drawdown",
        "calmar",
        "sharpe",
        "final_equity",
        "trade_count",
        "total_cost",
        "objective",
    ]
    return df[[column for column in keep if column in df.columns]].sort_values(
        ["objective", "annual_return", "max_drawdown"], ascending=[False, False, False]
    )


def pct(value: object) -> str:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "n/a"
    if pd.isna(number):
        return "n/a"
    return f"{number:.2%}"


def write_report(summary: pd.DataFrame, out_dir: Path, project: Path, start: str, end: str) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "combined_strategy_summary.csv"
    md_path = out_dir / "combined_strategy_report.md"
    summary.to_csv(csv_path, index=False, encoding="utf-8-sig")
    lines = [
        "# Quant Combo Lab Report",
        "",
        f"Project: `{project}`",
        f"Window: {start} to {end}",
        "",
        "| Rank | Source | Strategy | Annual return | Max drawdown | Calmar | Sharpe | Final equity | Trades |",
        "|---:|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for rank, row in enumerate(summary.head(30).itertuples(index=False), start=1):
        lines.append(
            f"| {rank} | {getattr(row, 'source', '')} | `{getattr(row, 'strategy', '')}` | "
            f"{pct(getattr(row, 'annual_return', None))} | {pct(getattr(row, 'max_drawdown', None))} | "
            f"{getattr(row, 'calmar', float('nan')):.2f} | {getattr(row, 'sharpe', float('nan')):.2f} | "
            f"{getattr(row, 'final_equity', float('nan')):.0f} | {getattr(row, 'trade_count', float('nan')):.0f} |"
        )
    lines.extend(
        [
            "",
            "## Files",
            "",
            f"- `{csv_path}`",
            "- Inspect each source report before freezing a model.",
            "- Verify that execution frequency matches live recommendation frequency.",
        ]
    )
    md_path.write_text("\n".join(lines), encoding="utf-8")
    return md_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Run broad local quant combination tests and merge summaries.")
    parser.add_argument("--project", default=".", help="project directory containing strategy scripts")
    parser.add_argument("--start", default="2025-01-01")
    parser.add_argument("--end", default=date.today().isoformat())
    parser.add_argument("--max-specs", type=int, default=6000)
    parser.add_argument("--seed", type=int, default=20260512)
    parser.add_argument("--skip-run", action="store_true", help="only merge existing summary files")
    parser.add_argument("--skip-lab", action="store_true")
    parser.add_argument("--skip-massive", action="store_true")
    parser.add_argument("--include-active", action="store_true", help="also merge active model two-year summary if present")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    if not project.exists():
        raise FileNotFoundError(project)

    py = sys.executable
    if not args.skip_run:
        lab_script = project / "run_strategy_lab_2025.py"
        if lab_script.exists() and not args.skip_lab:
            run([py, str(lab_script), "--start", args.start, "--end", args.end, "--max-specs", str(args.max_specs)], project)
        massive_script = project / "run_massive_full_market_search.py"
        if massive_script.exists() and not args.skip_massive:
            run(
                [
                    py,
                    str(massive_script),
                    "--start",
                    args.start,
                    "--end",
                    args.end,
                    "--max-specs",
                    str(args.max_specs),
                    "--seed",
                    str(args.seed),
                ],
                project,
            )
        active_script = project / "run_active_models_2y_backtest.py"
        if active_script.exists() and args.include_active:
            run([py, str(active_script), "--end", args.end], project)

    frames = [
        read_summary(project / "results" / "strategy_lab_2025" / "strategy_lab_summary.csv", "strategy_lab_2025"),
        read_summary(project / "results" / "massive_full_market_search" / "massive_full_market_summary.csv", "massive_full_market_search"),
    ]
    if args.include_active:
        frames.extend(
            [
                read_summary(
                    project / "results" / "active_daily_models" / "active_models_2y_backtest_summary_mainboard.csv",
                    "active_mainboard",
                ),
                read_summary(
                    project / "results" / "active_daily_models" / "active_models_2y_backtest_summary_script_original.csv",
                    "active_script_original",
                ),
            ]
        )
    summary = normalize_summary(frames)
    if summary.empty:
        raise RuntimeError("No summary CSV files found. Run the project strategy scripts first.")
    report = write_report(summary, project / "results" / "quant_combo_lab", project, args.start, args.end)
    print(report.read_text(encoding="utf-8"), flush=True)


if __name__ == "__main__":
    main()
