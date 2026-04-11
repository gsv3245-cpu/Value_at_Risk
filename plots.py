"""
plots.py
--------
All Plotly visualisations for the IndiaVaR Streamlit app.
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from rolling_var import INDIA_MARKET_EVENTS


# ── Colour palette ─────────────────────────────────────────────────────────
C_PRIMARY   = "#1f77b4"
C_DANGER    = "#e74c3c"
C_WARNING   = "#f39c12"
C_SUCCESS   = "#27ae60"
C_DARK      = "#2c3e50"
C_LIGHT     = "#ecf0f1"
C_CVAR      = "#9b59b6"
C_MC        = "#16a085"

TEMPLATE = "plotly_white"


# ══════════════════════════════════════════════════════════════════════════════
# 1. PRICE CHART
# ══════════════════════════════════════════════════════════════════════════════

def price_chart(prices: pd.Series, company_name: str) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=prices.index, y=prices.values,
        mode="lines", name="Close Price",
        line=dict(color=C_PRIMARY, width=1.8),
        fill="tozeroy", fillcolor="rgba(31,119,180,0.08)",
    ))
    fig.update_layout(
        title=f"{company_name} — Historical Price (₹)",
        xaxis_title="Date", yaxis_title="Price (₹)",
        template=TEMPLATE, height=340,
        margin=dict(l=40, r=20, t=50, b=40),
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# 2. RETURN DISTRIBUTION WITH VAR / CVaR LINES
# ══════════════════════════════════════════════════════════════════════════════

def return_distribution_chart(
    returns    : pd.Series,
    var_results: dict,
    company_name: str,
) -> go.Figure:
    """
    Histogram of daily log returns with VaR and CVaR vertical lines
    from all three methods, plus a normal distribution overlay.
    """
    hist_res = var_results["historical"]
    param_res= var_results["parametric"]
    mc_res   = var_results["monte_carlo"]

    # Normal overlay
    mu    = returns.mean()
    sigma = returns.std()
    x_norm= np.linspace(returns.min(), returns.max(), 300)
    y_norm= (1/(sigma * np.sqrt(2*np.pi))) * np.exp(-0.5*((x_norm-mu)/sigma)**2)
    # Scale to match histogram
    bin_width = (returns.max() - returns.min()) / 60
    y_norm_scaled = y_norm * len(returns) * bin_width

    fig = go.Figure()

    # Histogram
    fig.add_trace(go.Histogram(
        x=returns, nbinsx=60, name="Daily Returns",
        marker_color="rgba(31,119,180,0.65)",
        marker_line=dict(color="white", width=0.3),
    ))

    # Normal overlay
    fig.add_trace(go.Scatter(
        x=x_norm, y=y_norm_scaled,
        mode="lines", name="Normal Fit",
        line=dict(color=C_DARK, width=1.5, dash="dot"),
    ))

    # VaR lines
    lines = [
        (hist_res["var_return"],  C_DANGER,   "VaR — Historical"),
        (param_res["var_return"], C_WARNING,  "VaR — Parametric"),
        (mc_res["var_return"],    C_MC,       "VaR — Monte Carlo"),
        (hist_res["cvar_return"], C_CVAR,     "CVaR — Historical"),
    ]
    for val, color, label in lines:
        fig.add_vline(
            x=val, line_width=1.8, line_dash="dash", line_color=color,
            annotation_text=label, annotation_position="top right",
            annotation_font_size=9,
        )

    fig.update_layout(
        title=f"{company_name} — Return Distribution with VaR & CVaR",
        xaxis_title="Daily Log Return",
        yaxis_title="Frequency",
        template=TEMPLATE, height=400,
        legend=dict(orientation="h", y=-0.25),
        margin=dict(l=40, r=20, t=50, b=80),
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# 3. MONTE CARLO SIMULATION DISTRIBUTION
# ══════════════════════════════════════════════════════════════════════════════

def monte_carlo_chart(mc_result: dict, investment: float) -> go.Figure:
    """Histogram of 10,000 simulated 1-day P&L outcomes."""
    sim_pnl = mc_result["sim_returns"] * investment
    var_pnl = mc_result["var_return"]  * investment
    cvar_pnl= mc_result["cvar_return"] * investment

    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=sim_pnl, nbinsx=80,
        marker_color="rgba(22,160,133,0.6)",
        marker_line=dict(color="white", width=0.2),
        name="Simulated P&L",
    ))
    fig.add_vline(
        x=var_pnl, line_dash="dash", line_color=C_DANGER, line_width=2,
        annotation_text=f"VaR ₹{abs(var_pnl):,.0f}",
        annotation_position="top left", annotation_font_size=10,
    )
    fig.add_vline(
        x=cvar_pnl, line_dash="dash", line_color=C_CVAR, line_width=2,
        annotation_text=f"CVaR ₹{abs(cvar_pnl):,.0f}",
        annotation_position="top left", annotation_font_size=10,
    )
    fig.update_layout(
        title=f"Monte Carlo — 10,000 Simulated 1-day P&L Outcomes",
        xaxis_title="1-Day P&L (₹)",
        yaxis_title="Frequency",
        template=TEMPLATE, height=360,
        margin=dict(l=40, r=20, t=50, b=40),
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# 4. ROLLING VAR CHART WITH ANNOTATIONS
# ══════════════════════════════════════════════════════════════════════════════

def rolling_var_chart(
    rolling_df   : pd.DataFrame,
    company_name : str,
    investment   : float,
) -> go.Figure:
    """Rolling 252-day Historical VaR (₹) with Indian market event annotations."""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=rolling_df.index, y=rolling_df["VaR_INR"],
        mode="lines", name="Rolling VaR (₹)",
        line=dict(color=C_DANGER, width=1.8),
        fill="tozeroy", fillcolor="rgba(231,76,60,0.08)",
    ))
    fig.add_trace(go.Scatter(
        x=rolling_df.index, y=rolling_df["CVaR_INR"],
        mode="lines", name="Rolling CVaR (₹)",
        line=dict(color=C_CVAR, width=1.4, dash="dot"),
    ))

    # Annotate Indian market events using shapes
    for event in INDIA_MARKET_EVENTS:
        edate = pd.Timestamp(event["date"])
        if rolling_df.index.min() <= edate <= rolling_df.index.max():
            fig.add_shape(
                type="line",
                x0=edate, x1=edate,
                y0=0, y1=1,
                yref="paper",
                line=dict(color=event["color"], width=1, dash="dot"),
            )
            fig.add_annotation(
                x=edate,
                y=1,
                yref="paper",
                text=event["label"],
                showarrow=False,
                textangle=-60,
                font=dict(size=8),
            )

    fig.update_layout(
        title=f"{company_name} — Rolling 252-Day VaR & CVaR (₹{investment:,.0f} invested)",
        xaxis_title="Date", yaxis_title="VaR / CVaR (₹)",
        template=TEMPLATE, height=400,
        legend=dict(orientation="h", y=-0.2),
        margin=dict(l=40, r=20, t=50, b=70),
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# 5. BACKTESTING BREACH CHART
# ══════════════════════════════════════════════════════════════════════════════

def backtest_chart(bt_result: dict, company_name: str) -> go.Figure:
    """Plot actual losses vs rolling VaR with breach markers."""
    var_s    = bt_result["var_series"]
    actual   = bt_result["actual_loss"]
    breaches = bt_result["breach_series"]

    fig = go.Figure()

    # Actual daily P&L
    fig.add_trace(go.Bar(
        x=actual.index, y=actual.values,
        name="Daily P&L (₹)",
        marker_color=np.where(actual.values < 0, "rgba(231,76,60,0.4)", "rgba(39,174,96,0.4)").tolist(),
    ))

    # Rolling VaR line (shown as negative — it's a loss threshold)
    fig.add_trace(go.Scatter(
        x=var_s.index, y=-var_s.values,
        mode="lines", name="VaR Threshold (₹)",
        line=dict(color=C_DANGER, width=2),
    ))

    # Breach markers
    breach_dates = breaches[breaches == 1].index
    breach_vals  = actual[breach_dates]
    fig.add_trace(go.Scatter(
        x=breach_dates, y=breach_vals.values,
        mode="markers", name=f"VaR Breaches ({len(breach_dates)})",
        marker=dict(color=C_DANGER, size=6, symbol="x"),
    ))

    fig.update_layout(
        title=f"{company_name} — Kupiec Backtesting: Actual P&L vs VaR Threshold",
        xaxis_title="Date", yaxis_title="P&L (₹)",
        template=TEMPLATE, height=420,
        legend=dict(orientation="h", y=-0.2),
        margin=dict(l=40, r=20, t=50, b=70),
        barmode="overlay",
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# 6. STRESS TEST BAR CHART
# ══════════════════════════════════════════════════════════════════════════════

def stress_test_chart(stress_df: pd.DataFrame, investment: float) -> go.Figure:
    """Horizontal bar chart of stress test losses."""
    df_sorted = stress_df.sort_values("Loss (₹)")

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=df_sorted["Scenario"],
        x=df_sorted["Loss (₹)"],
        orientation="h",
        marker_color=df_sorted["color"].tolist(),
        text=[f"₹{v:,.0f}  ({s:.0f}%)"
              for v, s in zip(df_sorted["Loss (₹)"], df_sorted["Shock (%)"])],
        textposition="outside",
    ))
    fig.update_layout(
        title=f"Stress Test — Potential Losses on ₹{investment:,.0f} Investment",
        xaxis_title="Potential Loss (₹)",
        template=TEMPLATE, height=420,
        margin=dict(l=220, r=80, t=50, b=40),
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# 7. VAR COMPARISON BAR CHART (all methods, 95% vs 99%)
# ══════════════════════════════════════════════════════════════════════════════

def var_comparison_chart(
    var_95: dict,
    var_99: dict,
    investment: float,
) -> go.Figure:
    """Side-by-side bar chart comparing all 3 methods at 95% and 99%."""
    methods = ["Historical", "Parametric", "Monte Carlo"]
    keys    = ["historical", "parametric", "monte_carlo"]

    vals_95 = [var_95[k]["var_inr_1d"] for k in keys]
    vals_99 = [var_99[k]["var_inr_1d"] for k in keys]

    fig = go.Figure(data=[
        go.Bar(name="95% VaR", x=methods, y=vals_95,
               marker_color=C_WARNING,
               text=[f"₹{v:,.0f}" for v in vals_95], textposition="outside"),
        go.Bar(name="99% VaR", x=methods, y=vals_99,
               marker_color=C_DANGER,
               text=[f"₹{v:,.0f}" for v in vals_99], textposition="outside"),
    ])
    fig.update_layout(
        barmode="group",
        title=f"1-Day VaR Comparison — ₹{investment:,.0f} Investment",
        yaxis_title="VaR (₹)",
        template=TEMPLATE, height=380,
        margin=dict(l=40, r=20, t=50, b=40),
    )
    return fig


# ══════════════════════════════════════════════════════════════════════════════
# 8. ROLLING VOLATILITY CHART
# ══════════════════════════════════════════════════════════════════════════════

def rolling_volatility_chart(
    roll_vol: pd.Series,
    company_name: str,
) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=roll_vol.index, y=roll_vol.values * 100,
        mode="lines", name="30-Day Rolling Vol (%)",
        line=dict(color=C_WARNING, width=1.6),
        fill="tozeroy", fillcolor="rgba(243,156,18,0.1)",
    ))
    # Annotate events using shapes
    for event in INDIA_MARKET_EVENTS:
        edate = pd.Timestamp(event["date"])
        if roll_vol.index.min() <= edate <= roll_vol.index.max():
            fig.add_shape(
                type="line",
                x0=edate, x1=edate,
                y0=0, y1=1,
                yref="paper",
                line=dict(color=event["color"], width=1, dash="dot"),
            )
            fig.add_annotation(
                x=edate,
                y=1,
                yref="paper",
                text=event["label"],
                showarrow=False,
                textangle=-60,
                font=dict(size=7),
            )
    fig.update_layout(
        title=f"{company_name} — 30-Day Rolling Annualised Volatility (%)",
        xaxis_title="Date", yaxis_title="Annualised Volatility (%)",
        template=TEMPLATE, height=340,
        margin=dict(l=40, r=20, t=50, b=40),
    )
    return fig
