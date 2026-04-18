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


def _validate_ticker(ticker: str) -> tuple[bool, dict | None]:
    """
    Validate if a ticker exists by attempting to fetch data from yfinance.
    Returns (is_valid, info_dict)
    """
    try:
        ticker_clean = ticker.strip().upper()
        # Ensure it has .NS suffix for NSE
        if not ticker_clean.endswith(".NS"):
            ticker_clean = f"{ticker_clean}.NS"
        
        # Try to fetch 1 day of data
        test_data = yf.download(
            ticker_clean,
            period="1d",
            progress=False,
            auto_adjust=True
        )
        
        if test_data.empty or len(test_data) == 0:
            return False, None
        
        # Get company info
        try:
            yf_info = yf.Ticker(ticker_clean).info
            info = {
                "company_name": yf_info.get("longName", ticker_clean),
                "ticker": ticker_clean,
                "sector": yf_info.get("sector", "Unknown"),
                "score": 100,  # Direct ticker match = perfect score
                "is_direct_match": True,
            }
        except:
            info = {
                "company_name": ticker_clean,
                "ticker": ticker_clean,
                "sector": "Unknown",
                "score": 100,
                "is_direct_match": True,
            }
        
        return True, info
    except Exception:
        return False, None


def search_companies(query: str, top_n: int = None) -> list[dict]:
    """
    Fuzzy-search company names OR validate direct ticker input.
    Returns list of dicts: {company_name, ticker, sector, score, is_direct_match}
    
    - Fuzzy matches company names from CSV
    - Also checks if query is a valid NSE ticker symbol
    - If top_n is None, returns ALL matches
    """
    if not query or len(query) < 2:
        return []

    query_clean = query.strip()
    
    # Check if user typed a ticker symbol (has .NS or is uppercase letters/numbers)
    if query_clean.isupper() or ".NS" in query_clean.upper():
        is_valid, info = _validate_ticker(query_clean)
        if is_valid and info:
            return [info]  # Return direct match first
    
    # Fall back to fuzzy search in CSV
    query_lower = query_clean.lower().strip()
    names = _TICKER_DF["company_name_lower"].tolist()

    results = process.extract(
        query_lower,
        names,
        scorer=fuzz.WRatio,
        limit=top_n if top_n else len(names)  # None = all results
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
            "is_direct_match": False,
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
