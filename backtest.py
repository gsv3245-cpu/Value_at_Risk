"""
backtest.py
-----------
Kupiec (1995) Proportion of Failures (POF) backtesting test.

Reference
---------
Kupiec, P. (1995). "Techniques for Verifying the Accuracy of Risk
Management Models." Journal of Derivatives, Vol. 3, pp. 73-84.

The POF test checks whether the observed frequency of VaR breaches
(exceptions) is statistically consistent with the model's confidence
level using a log-likelihood ratio test.

H0: p_hat = p  (model is accurate)
Ha: p_hat ≠ p  (model is over/under-estimating risk)

LR_uc = -2 × ln [ ((1-p)^(T-N) × p^N) / ((1-N/T)^(T-N) × (N/T)^N) ]

Asymptotically ~ χ²(1).  Critical value at 95% significance = 3.841
"""

import numpy as np
import pandas as pd
from scipy import stats
from var_calculator import historical_var


# ══════════════════════════════════════════════════════════════════════════════

def kupiec_pof_test(
    returns: pd.Series,
    confidence: float = 0.95,
    investment: float = 100_000,
    lookback: int = 252,          # training window (1 trading year)
) -> dict:
    """
    Run Kupiec POF backtest on a rolling 1-day Historical VaR.

    Strategy
    --------
    For each day t in the out-of-sample period (last `lookback` days):
      1. Estimate VaR using the prior `lookback` days of returns.
      2. Check if actual return on day t breaches (is worse than) the VaR.
    Count total breaches N over T out-of-sample days.
    Apply LR formula and compare to chi-square critical value.

    Returns
    -------
    dict with: T, N, expected_N, breach_rate, LR_stat, p_value,
               verdict, exceptions_series, var_series
    """
    if len(returns) < lookback + 30:
        raise ValueError("Need at least lookback + 30 return observations for backtesting.")

    p          = 1 - confidence       # expected breach probability (e.g. 0.05)
    oos_start  = lookback             # first out-of-sample index

    var_series       = []
    breach_indicator = []
    oos_dates        = returns.index[oos_start:]

    for i in range(oos_start, len(returns)):
        train   = returns.iloc[i - lookback : i]
        var_ret = np.percentile(train, p * 100)          # negative number
        actual  = returns.iloc[i]
        var_series.append(var_ret)
        breach_indicator.append(1 if actual < var_ret else 0)   # 1 = breach

    T = len(breach_indicator)
    N = sum(breach_indicator)

    # ── Kupiec LR statistic ────────────────────────────────────────────────
    p_hat = N / T

    # Guard against edge cases (no breaches or all breaches)
    if N == 0:
        LR = -2 * (T * np.log(1 - p))
    elif N == T:
        LR = -2 * (T * np.log(p))
    else:
        LR = -2 * (
            np.log(((1 - p) ** (T - N)) * (p ** N))
            - np.log(((1 - p_hat) ** (T - N)) * (p_hat ** N))
        )

    p_value       = 1 - stats.chi2.cdf(LR, df=1)
    critical_val  = stats.chi2.ppf(0.95, df=1)     # = 3.841

    # Verdict
    if LR <= critical_val:
        verdict = "PASS"
        verdict_msg = (
            f"✅ Model ACCEPTED — LR={LR:.3f} ≤ {critical_val:.3f}. "
            f"Breach rate {p_hat:.1%} is statistically consistent "
            f"with {confidence:.0%} confidence level."
        )
    else:
        verdict = "FAIL"
        verdict_msg = (
            f"❌ Model REJECTED — LR={LR:.3f} > {critical_val:.3f}. "
            f"Breach rate {p_hat:.1%} deviates significantly from "
            f"the expected {p:.1%}."
        )

    # Series for plotting
    var_series_s   = pd.Series(
        [v * investment for v in var_series],
        index=oos_dates,
        name="VaR_INR",
    )
    breach_series  = pd.Series(
        breach_indicator,
        index=oos_dates,
        name="Breach",
    )
    actual_loss    = pd.Series(
        [r * investment for r in returns.iloc[oos_start:].values],
        index=oos_dates,
        name="ActualLoss_INR",
    )

    return {
        "T"              : T,
        "N"              : N,
        "expected_N"     : round(p * T, 1),
        "breach_rate"    : p_hat,
        "expected_rate"  : p,
        "LR_stat"        : LR,
        "critical_value" : critical_val,
        "p_value"        : p_value,
        "confidence"     : confidence,
        "verdict"        : verdict,
        "verdict_msg"    : verdict_msg,
        "var_series"     : var_series_s,
        "breach_series"  : breach_series,
        "actual_loss"    : actual_loss,
    }
