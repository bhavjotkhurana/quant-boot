"""
Week 1 — Normalized Price Performance Chart
============================================
Quantamental Investing Bootcamp | 8-Week Series

What this script does:
    Fetches daily adjusted closing prices for a 5-stock watchlist via yfinance,
    normalizes each series to a base of 100 from its first available trading day
    (so performance is directly comparable regardless of price level), and plots
    all five lines on a single chart.  The chart is saved as a PNG and displayed.

Watchlist:
    FE   — FirstEnergy Corp.      (regulated electric utility, Ohio)
    RACE — Ferrari N.V.           (luxury/performance automotive)
    COUR — Coursera Inc.          (online education platform)
    CRWV — CoreWeave Inc.         (AI-focused cloud infrastructure; IPO Mar 2025)
    JPM  — JPMorgan Chase & Co.   (largest U.S. bank by assets)

Note on CRWV:
    CoreWeave IPO'd in March 2025, so its line will be shorter than the others.
    The normalization handles this automatically — each ticker is anchored to
    its own first available close, so a later start date is not a problem.
"""

import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd

# ── Configuration ─────────────────────────────────────────────────────────────

TICKERS     = ["FE", "RACE", "COUR", "CRWV", "JPM"]
START_DATE  = "2024-01-01"
OUTPUT_FILE = "week1/output/normalized_prices.png"

# Palette: one distinct color per ticker (colorblind-friendly set)
COLORS = {
    "FE":   "#4878CF",   # steel blue
    "RACE": "#D65F5F",   # brick red
    "COUR": "#6ACC65",   # leaf green
    "CRWV": "#B47CC7",   # purple
    "JPM":  "#C4AD66",   # gold
}

# ── Data fetching ──────────────────────────────────────────────────────────────

def fetch_closing_prices(tickers: list[str], start: str) -> pd.DataFrame:
    """
    Download adjusted closing prices for all tickers in a single API call.
    Returns a DataFrame with one column per ticker, NaN where data is absent
    (e.g., pre-IPO dates for CRWV).
    """
    raw = yf.download(
        tickers,
        start=start,
        auto_adjust=True,   # use split/dividend-adjusted closes
        progress=False,
    )
    # yfinance returns a MultiIndex when >1 ticker; select the "Close" level
    prices = raw["Close"] if isinstance(raw.columns, pd.MultiIndex) else raw
    return prices[tickers]   # enforce consistent column order

# ── Normalization ──────────────────────────────────────────────────────────────

def normalize_to_100(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Re-base each column so that its first non-NaN value equals 100.
    This makes percentage-from-entry performance directly comparable across
    tickers regardless of their nominal share prices or IPO dates.
    """
    first_valid = prices.apply(lambda col: col.dropna().iloc[0])
    return (prices / first_valid) * 100

# ── Plotting ───────────────────────────────────────────────────────────────────

def plot_normalized_prices(normalized: pd.DataFrame, output_path: str) -> None:
    """Render the five normalized price series and save + display the chart."""
    fig, ax = plt.subplots(figsize=(12, 6))

    for ticker in normalized.columns:
        series = normalized[ticker].dropna()
        ax.plot(
            series.index,
            series.values,
            label=ticker,
            color=COLORS[ticker],
            linewidth=1.8,
        )

    # ── Formatting ──
    ax.set_title(
        "Normalized Price Performance (Base = 100)",
        fontsize=15,
        fontweight="bold",
        pad=14,
    )
    ax.set_xlabel("Date", fontsize=11)
    ax.set_ylabel("Indexed Price (100 = first trading day)", fontsize=11)

    # Horizontal reference line at 100 (break-even from entry)
    ax.axhline(100, color="gray", linewidth=0.8, linestyle="--", alpha=0.6)

    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.0f"))
    ax.legend(title="Ticker", fontsize=10, title_fontsize=10)
    ax.grid(axis="y", linestyle=":", alpha=0.4)
    ax.grid(axis="x", linestyle=":", alpha=0.2)

    fig.tight_layout()

    # Save then display
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    print(f"Chart saved → {output_path}")
    plt.show()

# ── Main ───────────────────────────────────────────────────────────────────────

def main() -> None:
    import os
    os.makedirs("week1/output", exist_ok=True)

    print(f"Fetching data for {TICKERS} from {START_DATE} …")
    prices     = fetch_closing_prices(TICKERS, START_DATE)
    normalized = normalize_to_100(prices)

    # Quick sanity check
    print("\nFirst available date per ticker:")
    for ticker in TICKERS:
        first_date = prices[ticker].first_valid_index()
        print(f"  {ticker:<5} {first_date.date() if first_date else 'N/A'}")

    plot_normalized_prices(normalized, OUTPUT_FILE)


if __name__ == "__main__":
    main()
