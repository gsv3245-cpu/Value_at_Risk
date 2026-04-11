"""
var_calculator.py
-----------------
Implements all three VaR methods and CVaR (Expected Shortfall).

References
----------
- Jorion, P. (2001). Value At Risk. McGraw-Hill.
- Rockafellar & Uryasev (2000). CVaR for General Loss Distributions.
- McNeil, Frey & Embrechts (2005). Quantitative Risk Management.
"""

import numpy as np
import pandas as pd
from scipy import stats
from arch import arch_model
import warnings

warnings.filterwarnings("ignore")


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def _z_score(confidence: float) -> float:
    """Z-score for given confidence level (one-tailed)."""
    return stats.norm.ppf(1 - (1 - confidence))


def scale_var_to_horizon(var_1d: float, horizon: int) -> float:
    """
    Scale 1-day VaR to multi-day VaR using the square-root-of-time rule.
    VaR_T = VaR_1d × √T
    Valid under i.i.d. returns assumption.
    """
    return var_1d * np.sqrt(horizon)


# ══════════════════════════════════════════════════════════════════════════════
# METHOD 1: HISTORICAL SIMULATION
# ══════════════════════════════════════════════════════════════════════════════

def historical_var(
    returns: pd.Series,
    confidence: float = 0.95,
    investment: float = 100_000,
    horizon: int = 1,
) -> dict:
    """
    Historical Simulation VaR.

    Sort actual log returns worst-to-best; the (1-confidence) percentile
    is the VaR return. No distributional assumption needed.
    (Cheung & Powell, 2012; Halilbegovic & Vehabovic, 2016)
    """
    alpha     = 1 - confidence
    var_ret   = np.percentile(returns, alpha * 100)          # e.g. 5th pct
    cvar_ret  = returns[returns <= var_ret].mean()           # ES = avg of tail

    var_1d    = abs(var_ret) * investment
    cvar_1d   = abs(cvar_ret) * investment
    var_Td    = scale_var_to_horizon(var_1d, horizon)
    cvar_Td   = scale_var_to_horizon(cvar_1d, horizon)

    return {
        "method"      : "Historical Simulation",
        "var_return"  : var_ret,
        "cvar_return" : cvar_ret,
        "var_inr_1d"  : var_1d,
        "cvar_inr_1d" : cvar_1d,
        "var_inr"     : var_Td,
        "cvar_inr"    : cvar_Td,
        "confidence"  : confidence,
        "horizon"     : horizon,
        "n_obs"       : len(returns),
    }


# ══════════════════════════════════════════════════════════════════════════════
# METHOD 2: PARAMETRIC (VARIANCE-COVARIANCE)
# ══════════════════════════════════════════════════════════════════════════════

def parametric_var(
    returns: pd.Series,
    confidence: float = 0.95,
    investment: float = 100_000,
    horizon: int = 1,
    use_garch: bool = True,
) -> dict:
    """
    Parametric (Variance-Covariance) VaR.

    Standard: VaR = -(μ - z_α × σ) × W
    GARCH variant: uses GARCH(1,1) conditional volatility estimate
    instead of the rolling historical σ — more accurate for Indian
    markets which exhibit volatility clustering
    (Srinivasan, 2010; PMC Article 2022 on NSE GARCH).
    """
    mu    = returns.mean()
    sigma = returns.std(ddof=1)
    z     = stats.norm.ppf(1 - confidence)          # negative for left tail

    garch_sigma = sigma
    garch_fitted = False

    if use_garch and len(returns) >= 100:
        try:
            # Fit GARCH(1,1) on percentage returns (arch package prefers this)
            pct_returns = returns * 100
            am  = arch_model(pct_returns, vol="Garch", p=1, q=1, dist="normal", rescale=False)
            res = am.fit(disp="off", show_warning=False)
            # 1-step ahead conditional volatility (last forecast)
            fc  = res.forecast(horizon=1, reindex=False)
            garch_sigma = float(np.sqrt(fc.variance.values[-1, 0])) / 100
            garch_fitted = True
        except Exception:
            garch_sigma = sigma

    # VaR return = μ + z × σ  (z is negative, so this is a loss)
    var_ret  = mu + z * garch_sigma
    # CVaR (parametric) = μ - σ × φ(z) / α
    alpha    = 1 - confidence
    cvar_ret = mu - garch_sigma * stats.norm.pdf(z) / alpha

    var_1d   = abs(var_ret)  * investment
    cvar_1d  = abs(cvar_ret) * investment
    var_Td   = scale_var_to_horizon(var_1d,  horizon)
    cvar_Td  = scale_var_to_horizon(cvar_1d, horizon)

    return {
        "method"       : "Parametric (GARCH)" if garch_fitted else "Parametric",
        "var_return"   : var_ret,
        "cvar_return"  : cvar_ret,
        "var_inr_1d"   : var_1d,
        "cvar_inr_1d"  : cvar_1d,
        "var_inr"      : var_Td,
        "cvar_inr"     : cvar_Td,
        "confidence"   : confidence,
        "horizon"      : horizon,
        "mu"           : mu,
        "sigma"        : garch_sigma,
        "sigma_static" : sigma,
        "garch_used"   : garch_fitted,
        "n_obs"        : len(returns),
    }


# ══════════════════════════════════════════════════════════════════════════════
# METHOD 3: MONTE CARLO SIMULATION
# ══════════════════════════════════════════════════════════════════════════════

def monte_carlo_var(
    returns: pd.Series,
    confidence: float = 0.95,
    investment: float = 100_000,
    horizon: int = 1,
    n_simulations: int = 10_000,
    seed: int = 42,
) -> dict:
    """
    Monte Carlo VaR.

    Generates n_simulations random return paths from N(μ, σ²),
    parameterised from historical data. VaR = percentile of simulated
    1-day P&L distribution.
    (PyQuant News, 2024; Ian Moore Medium, 2025)
    """
    np.random.seed(seed)
    mu    = returns.mean()
    sigma = returns.std(ddof=1)

    # Simulate returns for 1 day across n_simulations paths
    sim_returns = np.random.normal(loc=mu, scale=sigma, size=n_simulations)

    alpha    = 1 - confidence
    var_ret  = np.percentile(sim_returns, alpha * 100)
    cvar_ret = sim_returns[sim_returns <= var_ret].mean()

    var_1d   = abs(var_ret)  * investment
    cvar_1d  = abs(cvar_ret) * investment
    var_Td   = scale_var_to_horizon(var_1d,  horizon)
    cvar_Td  = scale_var_to_horizon(cvar_1d, horizon)

    return {
        "method"        : "Monte Carlo",
        "var_return"    : var_ret,
        "cvar_return"   : cvar_ret,
        "var_inr_1d"    : var_1d,
        "cvar_inr_1d"   : cvar_1d,
        "var_inr"       : var_Td,
        "cvar_inr"      : cvar_Td,
        "confidence"    : confidence,
        "horizon"       : horizon,
        "mu"            : mu,
        "sigma"         : sigma,
        "n_simulations" : n_simulations,
        "sim_returns"   : sim_returns,   # kept for plotting
        "n_obs"         : len(returns),
    }


# ══════════════════════════════════════════════════════════════════════════════
# CONVENIENCE WRAPPER
# ══════════════════════════════════════════════════════════════════════════════

def compute_all_var(
    returns: pd.Series,
    confidence: float = 0.95,
    investment: float = 100_000,
    horizon: int = 1,
) -> dict:
    """Run all three methods and return combined results dict."""
    hist   = historical_var(returns, confidence, investment, horizon)
    param  = parametric_var(returns, confidence, investment, horizon, use_garch=True)
    mc     = monte_carlo_var(returns, confidence, investment, horizon)

    return {"historical": hist, "parametric": param, "monte_carlo": mc}
