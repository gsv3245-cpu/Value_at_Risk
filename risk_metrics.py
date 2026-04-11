"""
risk_metrics.py
---------------
Additional risk and performance metrics:
  - Annualised Return & Volatility
  - Sharpe Ratio  (RFR = 6.5% — RBI repo rate proxy for India)
  - Beta vs Nifty 50
  - Max Drawdown
  - Skewness & Kurtosis (distribution shape)
  - Sortino Ratio

References
----------
- Sharpe, W. (1966). Mutual Fund Performance. Journal of Business.
- Jensen, M. (1968). Performance of Mutual Funds. Journal of Finance.
"""

import numpy as np
import pandas as pd
from scipy import stats as scipy_stats


# Indian risk-free rate (RBI repo rate proxy, approx)
INDIA_RFR_ANNUAL = 0.065   # 6.5% p.a.
INDIA_RFR_DAILY  = INDIA_RFR_ANNUAL / 252


# ══════════════════════════════════════════════════════════════════════════════

def annualised_return(returns: pd.Series) -> float:
    """Compound annualised return from daily log returns."""
    total_log_ret = returns.sum()
    n_days        = len(returns)
    return float(np.exp(total_log_ret * (252 / n_days)) - 1)


def annualised_volatility(returns: pd.Series) -> float:
    """Annualised volatility from daily log returns: σ × √252."""
    return float(returns.std(ddof=1) * np.sqrt(252))


def sharpe_ratio(returns: pd.Series) -> float:
    """
    Sharpe Ratio = (μ_daily - RFR_daily) / σ_daily × √252
    Uses 6.5% RFR (RBI repo rate proxy for India).
    """
    excess = returns.mean() - INDIA_RFR_DAILY
    sigma  = returns.std(ddof=1)
    if sigma == 0:
        return 0.0
    return float((excess / sigma) * np.sqrt(252))


def sortino_ratio(returns: pd.Series) -> float:
    """
    Sortino Ratio = (μ - RFR) / downside_deviation × √252
    Only penalises downside volatility.
    """
    excess           = returns.mean() - INDIA_RFR_DAILY
    negative_returns = returns[returns < 0]
    if len(negative_returns) == 0:
        return np.nan
    downside_std = negative_returns.std(ddof=1)
    if downside_std == 0:
        return np.nan
    return float((excess / downside_std) * np.sqrt(252))


def beta_vs_nifty(stock_returns: pd.Series, nifty_returns: pd.Series) -> float:
    """
    Beta = Cov(stock, market) / Var(market)
    Align on common dates before calculation.
    """
    aligned = pd.concat(
        [stock_returns.rename("stock"), nifty_returns.rename("nifty")],
        axis=1
    ).dropna()
    if len(aligned) < 30:
        return np.nan
    cov    = np.cov(aligned["stock"], aligned["nifty"])
    var_m  = np.var(aligned["nifty"], ddof=1)
    if var_m == 0:
        return np.nan
    return float(cov[0, 1] / var_m)


def max_drawdown(prices: pd.Series) -> float:
    """Max Drawdown = min( (P_t - max(P_0..t)) / max(P_0..t) )"""
    roll_max = prices.cummax()
    dd       = (prices - roll_max) / roll_max
    return float(dd.min())


def distribution_stats(returns: pd.Series) -> dict:
    """
    Return distribution shape statistics.
    Indian markets are known for fat tails (excess kurtosis > 0)
    and slight negative skew.
    """
    skew = float(scipy_stats.skew(returns))
    kurt = float(scipy_stats.kurtosis(returns))   # excess kurtosis (Fisher)
    jb_stat, jb_p = scipy_stats.jarque_bera(returns)

    return {
        "skewness"         : skew,
        "excess_kurtosis"  : kurt,
        "is_normal_jb"     : jb_p > 0.05,
        "jb_p_value"       : jb_p,
        "min_return"       : float(returns.min()),
        "max_return"       : float(returns.max()),
        "mean_return_daily": float(returns.mean()),
        "std_daily"        : float(returns.std(ddof=1)),
    }


def compute_all_metrics(
    stock_returns : pd.Series,
    prices        : pd.Series,
    nifty_returns : pd.Series | None = None,
) -> dict:
    """Return all risk metrics in a single dict."""
    m = {
        "annualised_return"    : annualised_return(stock_returns),
        "annualised_volatility": annualised_volatility(stock_returns),
        "sharpe_ratio"         : sharpe_ratio(stock_returns),
        "sortino_ratio"        : sortino_ratio(stock_returns),
        "max_drawdown_pct"     : max_drawdown(prices) * 100,
        "beta"                 : beta_vs_nifty(stock_returns, nifty_returns)
                                 if nifty_returns is not None else np.nan,
        **distribution_stats(stock_returns),
    }
    return m
