"""
Week 1 — Morning Brief
======================
Quantamental Investing Bootcamp | 8-Week Series

What this script does:
    Prints a compact terminal summary of the watchlist's most recent closing
    prices: last close, daily % change, and total return since each ticker's
    normalized base date.  Designed to run in a few seconds each morning as a
    quick gut-check before the market opens.

    No chart is produced — output is plain terminal text with color coding
    (green = positive, red = negative).

Run:
    python week1/morning_brief.py
"""

import yfinance as yf
import pandas as pd

# ── Configuration ──────────────────────────────────────────────────────────────

TICKERS    = ["FE", "RACE", "COUR", "CRWV", "JPM"]
START_DATE = "2024-01-01"

COMPANY_NAMES = {
    "FE":   "FirstEnergy Corp.",
    "RACE": "Ferrari N.V.",
    "COUR": "Coursera Inc.",
    "CRWV": "CoreWeave Inc.",
    "JPM":  "JPMorgan Chase & Co.",
}

# ── ANSI helpers ───────────────────────────────────────────────────────────────

GREEN = "\033[92m"
RED   = "\033[91m"
BOLD  = "\033[1m"
DIM   = "\033[2m"
RESET = "\033[0m"

def color_pct(value: float) -> str:
    """Return a sign-prefixed, color-coded percentage string (width-stable)."""
    sign = "+" if value >= 0 else ""
    color = GREEN if value >= 0 else RED
    return f"{color}{sign}{value:.2f}%{RESET}"

# ── Data ───────────────────────────────────────────────────────────────────────

def fetch_prices() -> pd.DataFrame:
    """
    Fetch adjusted closes from START_DATE to today for all tickers in one call.
    The full history is needed so we can anchor each ticker's return to its own
    first available close (the same base used in the normalized price chart).
    """
    raw = yf.download(
        TICKERS,
        start=START_DATE,
        auto_adjust=True,
        progress=False,
    )
    prices = raw["Close"] if isinstance(raw.columns, pd.MultiIndex) else raw
    return prices[TICKERS]

def compute_stats(prices: pd.DataFrame) -> list[dict]:
    """
    For each ticker return a stats dict with:
        last_date — date of the most recent available close
        last      — most recent adjusted close ($)
        day_chg   — % change vs the prior session
        base_ret  — % return since first available close (normalized base)
    """
    rows = []
    for ticker in TICKERS:
        col = prices[ticker].dropna()

        if len(col) < 2:
            rows.append({"ticker": ticker, "error": "insufficient data"})
            continue

        rows.append({
            "ticker":    ticker,
            "last_date": col.index[-1].date(),
            "last":      col.iloc[-1],
            "day_chg":   (col.iloc[-1] / col.iloc[-2] - 1) * 100,
            "base_ret":  (col.iloc[-1] / col.iloc[0]  - 1) * 100,
            "base_date": col.index[0].date(),
        })
    return rows

# ── Display ────────────────────────────────────────────────────────────────────

def print_brief(rows: list[dict]) -> None:
    """Render the morning brief table to stdout."""

    # Use the most recent close date across all tickers as the report date
    valid_dates = [r["last_date"] for r in rows if "last_date" in r]
    report_date = max(valid_dates).strftime("%a %b %d %Y") if valid_dates else "N/A"

    W = 66  # table width

    # ── Header ──
    print()
    print(BOLD + "─" * W + RESET)
    print(BOLD + f"  Quant Watchlist  │  {report_date}  │  prev close" + RESET)
    print(BOLD + "─" * W + RESET)
    print(f"  {'TICKER':<6}  {'COMPANY':<24}  {'LAST':>9}  {'DAY':>8}  {'VS BASE':>9}")
    print("  " + "─" * (W - 4))

    # ── Rows ──
    for r in rows:
        if "error" in r:
            print(f"  {r['ticker']:<6}  {'— ' + r['error']}")
            continue

        # CRWV has a later base date — flag it so the return is not misleading
        ticker_label = r["ticker"] + (" *" if r["ticker"] == "CRWV" else "  ")

        # Raw (uncolored) strings for fixed-width alignment, then colorize
        last_str     = f"${r['last']:.2f}"
        day_str      = color_pct(r["day_chg"])
        base_ret_str = color_pct(r["base_ret"])

        print(
            f"  {BOLD}{ticker_label:<8}{RESET}"
            f"{COMPANY_NAMES[r['ticker']]:<24}"
            f"  {last_str:>9}"
            f"  {day_str:>8}"    # ANSI codes don't affect visual width
            f"  {base_ret_str:>9}"
        )

    # ── Footer ──
    print("  " + "─" * (W - 4))
    crwv_base = next((r["base_date"] for r in rows if r["ticker"] == "CRWV" and "base_date" in r), None)
    if crwv_base:
        print(DIM + f"  * CRWV base date: {crwv_base} (IPO).  All others base from {START_DATE}." + RESET)
    print()

# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    print("Fetching latest closes …", end="\r")
    prices = fetch_prices()
    rows   = compute_stats(prices)
    print_brief(rows)


if __name__ == "__main__":
    main()
