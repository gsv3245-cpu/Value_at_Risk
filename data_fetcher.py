"""
data_fetcher.py
---------------
Handles stock name → NSE ticker resolution (fuzzy matching)
and downloads historical OHLCV data via yfinance.
"""

import os
import pandas as pd
import numpy as np
import yfinance as yf
from rapidfuzz import process, fuzz
from datetime import datetime, timedelta

# ── Load ticker map ────────────────────────────────────────────────────────────
_CSV_PATH = os.path.join(os.path.dirname(__file__), "nse_tickers.csv")

def _load_ticker_map() -> pd.DataFrame:
    df = pd.read_csv(_CSV_PATH)
    df["company_name_lower"] = df["company_name"].str.lower().str.strip()
    return df

_TICKER_DF = _load_ticker_map()


def search_companies(query: str, top_n: int = 8) -> list[dict]:
    """
    Fuzzy-search company names.
    Returns list of dicts: {company_name, ticker, sector, score}
    """
    if not query or len(query) < 2:
        return []

    query_lower = query.lower().strip()
    names = _TICKER_DF["company_name_lower"].tolist()

    results = process.extract(
        query_lower,
        names,
        scorer=fuzz.WRatio,
        limit=top_n
    )

    output = []
    seen_tickers = set()
    for match_name, score, idx in results:
        if score < 40:
            continue
        row = _TICKER_DF.iloc[idx]
        if row["ticker"] in seen_tickers:
            continue
        seen_tickers.add(row["ticker"])
        output.append({
            "company_name": row["company_name"],
            "ticker": row["ticker"],
            "sector": row["sector"],
            "score": score,
        })

    return output


def get_ticker_for_name(name: str) -> str | None:
    """Return best-matching NSE ticker for a company name."""
    results = search_companies(name, top_n=1)
    if results and results[0]["score"] >= 50:
        return results[0]["ticker"]
    return None


def fetch_stock_data(
    ticker: str,
    years: int = 5
) -> tuple[pd.DataFrame, dict]:
    """
    Download adjusted close price data from yfinance.

    Returns
    -------
    df   : DataFrame with columns [Close, Returns, LogReturns]
    info : dict with company metadata
    """
    end_date   = datetime.today()
    start_date = end_date - timedelta(days=years * 365 + 10)

    raw = yf.download(
        ticker,
        start=start_date.strftime("%Y-%m-%d"),
        end=end_date.strftime("%Y-%m-%d"),
        progress=False,
        auto_adjust=True,
    )

    if raw.empty or len(raw) < 60:
        raise ValueError(f"Insufficient data for ticker '{ticker}'. Try a different name.")

    # Flatten MultiIndex columns if present
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = raw.columns.get_level_values(0)

    df = pd.DataFrame(index=raw.index)
    df["Close"] = raw["Close"].squeeze()
    df.dropna(inplace=True)

    # Simple percentage returns
    df["Returns"]    = df["Close"].pct_change()
    # Log returns  (preferred for VaR — see Jorion 2001)
    df["LogReturns"] = np.log(df["Close"] / df["Close"].shift(1))
    df.dropna(inplace=True)

    # Company info
    try:
        yf_info  = yf.Ticker(ticker).info
        info = {
            "longName"  : yf_info.get("longName", ticker),
            "sector"    : yf_info.get("sector", "N/A"),
            "industry"  : yf_info.get("industry", "N/A"),
            "marketCap" : yf_info.get("marketCap", None),
            "currency"  : yf_info.get("currency", "INR"),
        }
    except Exception:
        info = {"longName": ticker, "sector": "N/A",
                "industry": "N/A", "marketCap": None, "currency": "INR"}

    return df, info


def fetch_nifty50(years: int = 5) -> pd.Series:
    """Download Nifty 50 log returns for beta calculation."""
    end_date   = datetime.today()
    start_date = end_date - timedelta(days=years * 365 + 10)
    raw = yf.download(
        "^NSEI",
        start=start_date.strftime("%Y-%m-%d"),
        end=end_date.strftime("%Y-%m-%d"),
        progress=False,
        auto_adjust=True,
    )
    if raw.empty:
        return pd.Series(dtype=float)
    if isinstance(raw.columns, pd.MultiIndex):
        raw.columns = raw.columns.get_level_values(0)
    close = raw["Close"].squeeze()
    return np.log(close / close.shift(1)).dropna()


def get_all_companies() -> list[dict]:
    """Return full list for dropdown display."""
    return _TICKER_DF[["company_name", "ticker", "sector"]].to_dict("records")
