# Quantamental Investing Bootcamp

An 8-week project-based series building up a quantitative + fundamental ("quantamental") investing toolkit from scratch.  Each week adds one deliverable; the repo accumulates into a full research framework by week 8.

## Structure

```
quant-boot/
├── week1/   normalized price chart
├── week2/   …
└── …
```

## Watchlist

| Ticker | Company | Sector |
|--------|---------|--------|
| FE | FirstEnergy Corp. | Regulated Utility |
| RACE | Ferrari N.V. | Luxury Automotive |
| COUR | Coursera Inc. | Online Education |
| CRWV | CoreWeave Inc. | AI Cloud Infrastructure |
| JPM | JPMorgan Chase & Co. | Banking |

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install yfinance matplotlib pandas
```

## Week 1 — Normalized Price Performance

```bash
python week1/normalized_prices.py
```

Outputs `week1/output/normalized_prices.png` (gitignored) and opens an interactive chart window.
