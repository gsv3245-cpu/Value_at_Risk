"""
stress_test.py
--------------
Applies historical Indian market crisis shocks to a stock's
current price to estimate potential losses under stress scenarios.

Scenarios calibrated from actual Nifty 50 drawdowns:
  - COVID Crash: Nifty fell ~38% peak-to-trough (Jan–Mar 2020)
  - GFC 2008:    Nifty fell ~60% peak-to-trough (Jan 2008–Mar 2009)
  - IL&FS:       NBFC/banking sector ~15% (Sep–Oct 2018)
  - Adani Crisis: Adani stocks fell >50%; sector contagion ~20% (Jan 2023)
  - Russia-Ukraine: Global commodity shock ~12% (Feb–Mar 2022)
  - Flash Crash:  Intraday-style 5% sudden drop
"""

import numpy as np
import pandas as pd


# ── Predefined Indian market stress scenarios ──────────────────────────────

STRESS_SCENARIOS = [
    {
        "name"        : "COVID-19 Crash (Mar 2020)",
        "shock_pct"   : -38.0,
        "duration"    : "~40 trading days",
        "description" : "Nifty 50 fell ~38% from Jan to Mar 2020. Worst single-month crash since 2008.",
        "color"       : "#e74c3c",
    },
    {
        "name"        : "Global Financial Crisis (2008–09)",
        "shock_pct"   : -60.0,
        "duration"    : "~12 months",
        "description" : "Nifty 50 lost ~60% peak-to-trough. Worst bear market in Indian stock history.",
        "color"       : "#c0392b",
    },
    {
        "name"        : "Russia-Ukraine War (Feb 2022)",
        "shock_pct"   : -12.0,
        "duration"    : "~3 weeks",
        "description" : "Global commodity shock and FII outflows drove ~12% correction.",
        "color"       : "#e67e22",
    },
    {
        "name"        : "IL&FS Default Crisis (Sep 2018)",
        "shock_pct"   : -15.0,
        "duration"    : "~6 weeks",
        "description" : "NBFC liquidity crisis following IL&FS default. Banking & finance stocks hit hard.",
        "color"       : "#f39c12",
    },
    {
        "name"        : "Adani Group Selloff (Jan 2023)",
        "shock_pct"   : -20.0,
        "duration"    : "~2 weeks",
        "description" : "Hindenburg Research report triggered ~20% broad market contagion fear.",
        "color"       : "#d35400",
    },
    {
        "name"        : "Demonetisation Shock (Nov 2016)",
        "shock_pct"   : -8.0,
        "duration"    : "~1 month",
        "description" : "Surprise demonetisation announcement caused ~8% market correction.",
        "color"       : "#8e44ad",
    },
    {
        "name"        : "Flash Crash Scenario (−5%)",
        "shock_pct"   : -5.0,
        "duration"    : "1 day",
        "description" : "Sudden single-day 5% drop (e.g. circuit-breaker trigger, FII panic selling).",
        "color"       : "#2980b9",
    },
]


def run_stress_tests(
    current_price : float,
    investment    : float = 100_000,
    custom_shock  : float | None = None,
    custom_label  : str = "Custom Scenario",
) -> pd.DataFrame:
    """
    Apply all stress scenarios to a current investment.

    Parameters
    ----------
    current_price : latest closing price of the stock
    investment    : total INR investment value
    custom_shock  : optional user-defined shock percentage (negative)
    custom_label  : label for the custom scenario

    Returns
    -------
    pd.DataFrame with columns:
        Scenario, Shock_pct, Loss_INR, Remaining_INR, Duration, Description
    """
    scenarios = list(STRESS_SCENARIOS)   # copy

    if custom_shock is not None:
        scenarios.append({
            "name"        : custom_label,
            "shock_pct"   : float(custom_shock),
            "duration"    : "User-defined",
            "description" : "Custom user-defined stress scenario.",
            "color"       : "#1abc9c",
        })

    rows = []
    for sc in scenarios:
        shock     = sc["shock_pct"] / 100.0
        loss      = abs(shock) * investment
        remaining = investment + (shock * investment)
        rows.append({
            "Scenario"      : sc["name"],
            "Shock (%)"     : sc["shock_pct"],
            "Loss (₹)"      : round(loss, 2),
            "Remaining (₹)" : round(max(remaining, 0), 2),
            "Duration"      : sc["duration"],
            "Description"   : sc["description"],
            "color"         : sc["color"],
        })

    return pd.DataFrame(rows)


def worst_historical_drawdown(
    prices: pd.Series,
) -> dict:
    """
    Compute max drawdown from historical price series.

    Max Drawdown = (Trough - Peak) / Peak
    """
    roll_max     = prices.cummax()
    drawdown     = (prices - roll_max) / roll_max
    max_dd       = drawdown.min()
    max_dd_end   = drawdown.idxmin()
    max_dd_start = prices[:max_dd_end].idxmax()

    return {
        "max_drawdown_pct" : max_dd * 100,
        "peak_date"        : max_dd_start,
        "trough_date"      : max_dd_end,
        "drawdown_series"  : drawdown,
    }
