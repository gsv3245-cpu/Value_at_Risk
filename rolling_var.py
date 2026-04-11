"""
rolling_var.py
--------------
Computes rolling Historical VaR over a sliding window.
Useful for visualising how risk evolved through key Indian market events.

Volatility clustering reference:
  - Srinivasan (2010): GARCH evidence on BSE-30
  - PMC (2022): NSE volatility persistence
"""

import numpy as np
import pandas as pd


# Indian market events for annotation on rolling VaR chart
INDIA_MARKET_EVENTS = [
    {"date": "2018-09-21", "label": "IL&FS Default",      "color": "orange"},
    {"date": "2020-03-23", "label": "COVID-19 Crash",     "color": "red"},
    {"date": "2020-11-01", "label": "COVID Recovery",     "color": "green"},
    {"date": "2022-02-24", "label": "Russia-Ukraine War", "color": "orange"},
    {"date": "2023-01-24", "label": "Adani Crisis",       "color": "red"},
    {"date": "2024-06-04", "label": "Election Result",    "color": "blue"},
]


def rolling_historical_var(
    returns: pd.Series,
    window: int = 252,
    confidence: float = 0.95,
    investment: float = 100_000,
) -> pd.DataFrame:
    """
    Compute rolling Historical VaR and CVaR over a sliding window.

    Parameters
    ----------
    returns    : pd.Series of log returns (daily)
    window     : rolling window size in trading days (default 252 = 1 year)
    confidence : VaR confidence level
    investment : portfolio value in INR

    Returns
    -------
    pd.DataFrame with columns: [VaR_pct, CVaR_pct, VaR_INR, CVaR_INR]
    """
    alpha = 1 - confidence

    var_pct_list  = []
    cvar_pct_list = []
    dates         = []

    for i in range(window, len(returns) + 1):
        window_returns = returns.iloc[i - window : i]
        var_ret  = np.percentile(window_returns, alpha * 100)
        cvar_ret = window_returns[window_returns <= var_ret].mean()
        var_pct_list.append(abs(var_ret))
        cvar_pct_list.append(abs(cvar_ret))
        dates.append(returns.index[i - 1])

    df = pd.DataFrame({
        "VaR_pct"  : var_pct_list,
        "CVaR_pct" : cvar_pct_list,
        "VaR_INR"  : [v * investment for v in var_pct_list],
        "CVaR_INR" : [c * investment for c in cvar_pct_list],
    }, index=dates)

    return df


def rolling_volatility(
    returns: pd.Series,
    window: int = 30,
    annualise: bool = True,
) -> pd.Series:
    """
    Compute rolling annualised volatility.

    Parameters
    ----------
    window   : rolling window in trading days (default 30)
    annualise: multiply by √252 for annualised vol
    """
    roll_vol = returns.rolling(window).std(ddof=1)
    if annualise:
        roll_vol = roll_vol * np.sqrt(252)
    return roll_vol.dropna()
