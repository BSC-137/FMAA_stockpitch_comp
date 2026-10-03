"""
XRO information edge: Google Trends, US vs Australia vs New Zealand.

Question: is Xero's share of search interest (vs a competitor) rising in the US,
and how does that compare with its home markets?

Run top to bottom, or cell by cell in VS Code / Jupyter (each "# %%" is a cell).
Install first:  pip install pytrends pandas matplotlib
"""

# %% 1. Imports
import time
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from pytrends.request import TrendReq


# %% 2. Configuration (change things here only, nothing below is hardcoded)
TERMS = ["Xero", "QuickBooks"]   # first term = our company, the rest = competitors (max 5)
OUR_TERM = TERMS[0]
GEOS = {"US": "US", "Australia": "AU", "New Zealand": "NZ"}   # label -> Google geo code
TIMEFRAME = "today 5-y"          # 5 years returns weekly data
CATEGORY = 0                     # 0 = all categories (narrow later if "Xero" is noisy)
PAUSE_SECONDS = 5                # polite gap between requests to avoid 429 errors
WINDOW_WEEKS = 52                # compare the latest 52 weeks vs the 52 before
SMOOTH_WEEKS = 8                 # rolling average used for the charts
OUTPUT_DIR = Path("trends_output")
OUTPUT_DIR.mkdir(exist_ok=True)


# %% 3. Fetch function with retries
def fetch_interest(terms, geo, timeframe, category=0, retries=4, pause=5):
    """Return a weekly DataFrame (rows = weeks, columns = terms) for one geo.

    Google rescales every request so its single highest point = 100. Terms in the
    SAME request share a scale (comparable). Different geos are separate requests,
    so absolute levels are NOT comparable across geos. We handle that in section 5.
    """
    for attempt in range(1, retries + 1):
        try:
            pt = TrendReq(hl="en-US", tz=0)
            pt.build_payload(kw_list=terms, cat=category, timeframe=timeframe, geo=geo)
            df = pt.interest_over_time()
            if df.empty:
                raise ValueError(f"No data returned for geo={geo}")
            # The latest week is usually incomplete and would bias the trend down
            if "isPartial" in df.columns:
                df = df[~df["isPartial"].astype(bool)].drop(columns="isPartial")
            return df
        except Exception as err:   # pytrends is unofficial, so errors are common
            wait = pause * attempt * 2
            print(f"[{geo}] attempt {attempt}/{retries} failed ({err}); retrying in {wait}s")
            time.sleep(wait)
    raise RuntimeError(f"Could not fetch Google Trends data for geo={geo}")


# %% 4. Analysis helpers
def search_share(df, our_term):
    """Our term as a % of all terms' search interest each week.

    A ratio is scale-free, so unlike the raw index it CAN be compared across
    geos. This is the main number to put on a slide.
    """
    return df[our_term] / df.sum(axis=1) * 100


def window_change(series, window):
    """Mean of the latest `window` weeks vs the `window` weeks before it."""
    if len(series) < 2 * window:
        raise ValueError(f"Need {2 * window} weeks of data, got {len(series)}")
    recent = series.tail(window).mean()
    prior = series.iloc[-2 * window:-window].mean()
    return prior, recent


def build_summary(data, our_term, window):
    """One row per geo: share of searches, then vs prior period, plus own-term growth."""
    rows = []
    for label, df in data.items():
        share_prior, share_recent = window_change(search_share(df, our_term), window)
        idx_prior, idx_recent = window_change(df[our_term], window)
        rows.append({
            "geo": label,
            f"{our_term} share prior {window}w (%)": share_prior,
            f"{our_term} share latest {window}w (%)": share_recent,
            "share change (pp)": share_recent - share_prior,
            f"{our_term} interest growth (%)": (idx_recent / idx_prior - 1) * 100,
        })
    return pd.DataFrame(rows).set_index("geo").round(1)


# %% 5. Plot helpers
def plot_results(data, our_term, smooth, out_dir):
    # Figure 1: raw interest per geo (each panel has its own 0-100 scale)
    fig, axes = plt.subplots(len(data), 1, figsize=(10, 3 * len(data)), sharex=True)
    axes = [axes] if len(data) == 1 else axes
    for ax, (label, df) in zip(axes, data.items()):
        df.rolling(smooth).mean().plot(ax=ax)
        ax.set_title(f"{label}: search interest index (own scale)")
        ax.set_ylabel("Index (0-100)")
    fig.tight_layout()
    fig.savefig(out_dir / "interest_by_geo.png", dpi=150)

    # Figure 2: share of searches, all geos on one axis (comparable because it is a ratio)
    fig2, ax2 = plt.subplots(figsize=(10, 4))
    for label, df in data.items():
        search_share(df, our_term).rolling(smooth).mean().plot(ax=ax2, label=label)
    ax2.set_title(f"{our_term} share of searches vs competitors ({smooth}-week average)")
    ax2.set_ylabel("Share of searches (%)")
    ax2.legend()
    fig2.tight_layout()
    fig2.savefig(out_dir / "share_comparison.png", dpi=150)


# %% 6. Run everything
def main():
    data = {}
    for label, code in GEOS.items():
        print(f"Fetching {label} ({code})...")
        data[label] = fetch_interest(TERMS, code, TIMEFRAME, CATEGORY, pause=PAUSE_SECONDS)
        time.sleep(PAUSE_SECONDS)

    # Save the raw data so you can cite the pull date and rebuild charts in Excel
    pd.concat(data, axis=1).to_csv(OUTPUT_DIR / "raw_trends.csv")

    summary = build_summary(data, OUR_TERM, WINDOW_WEEKS)
    summary.to_csv(OUTPUT_DIR / "summary.csv")
    print("\n", summary.to_string())

    plot_results(data, OUR_TERM, SMOOTH_WEEKS, OUTPUT_DIR)
    plt.show()
    return data, summary


if __name__ == "__main__":
    main()
