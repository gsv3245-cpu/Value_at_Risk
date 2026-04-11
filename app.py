"""
app.py — IndiaVaR: Indian Stock Risk Analyzer
=============================================
Streamlit application for Value at Risk (VaR) analysis
of NSE-listed Indian stocks.

Run with:  streamlit run app.py
"""

import warnings
warnings.filterwarnings("ignore")

import streamlit as st
import pandas as pd
import numpy as np

# ── Page config (must be first Streamlit call) ────────────────────────────
st.set_page_config(
    page_title="IndiaVaR — Stock Risk Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Project modules ───────────────────────────────────────────────────────
from data_fetcher   import search_companies, fetch_stock_data, fetch_nifty50
from var_calculator import compute_all_var
from backtest       import kupiec_pof_test
from rolling_var    import rolling_historical_var, rolling_volatility
from stress_test    import run_stress_tests, worst_historical_drawdown
from risk_metrics   import compute_all_metrics
from plots import (
    price_chart,
    return_distribution_chart,
    monte_carlo_chart,
    rolling_var_chart,
    backtest_chart,
    stress_test_chart,
    var_comparison_chart,
    rolling_volatility_chart,
)


# ══════════════════════════════════════════════════════════════════════════════
# CUSTOM CSS
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
  /* Header gradient */
  .main-header {
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
      padding: 2rem 2.5rem 1.5rem;
      border-radius: 12px;
      margin-bottom: 1.5rem;
      color: white;
  }
  .main-header h1 { font-size: 2.2rem; font-weight: 700; margin:0; }
  .main-header p  { opacity: 0.8; margin: 0.3rem 0 0; font-size: 1rem; }

  /* Metric cards */
  .metric-card {
      background: #f8f9fa;
      border-left: 4px solid #1f77b4;
      border-radius: 8px;
      padding: 1rem 1.2rem;
      margin: 0.4rem 0;
  }
  .metric-card.danger  { border-left-color: #e74c3c; }
  .metric-card.warning { border-left-color: #f39c12; }
  .metric-card.success { border-left-color: #27ae60; }
  .metric-card.purple  { border-left-color: #9b59b6; }

  .metric-label { font-size: 0.75rem; color: #666; font-weight: 600;
                  text-transform: uppercase; letter-spacing: 0.5px; }
  .metric-value { font-size: 1.5rem; font-weight: 700; color: #2c3e50; }
  .metric-sub   { font-size: 0.8rem; color: #888; }

  /* Section headers */
  .section-header {
      font-size: 1.15rem; font-weight: 700;
      color: #2c3e50; border-bottom: 2px solid #e0e0e0;
      padding-bottom: 0.4rem; margin: 1.5rem 0 1rem;
  }

  /* Verdict box */
  .verdict-pass {
      background: #d4edda; border: 1px solid #28a745;
      border-radius: 8px; padding: 1rem; color: #155724;
  }
  .verdict-fail {
      background: #f8d7da; border: 1px solid #dc3545;
      border-radius: 8px; padding: 1rem; color: #721c24;
  }

  /* Formula box */
  .formula-box {
      background: #f0f4f8; border-radius: 8px;
      padding: 0.8rem 1.2rem; font-family: monospace;
      font-size: 0.85rem; color: #2c3e50;
      border-left: 3px solid #1f77b4;
  }

  /* Tag badges */
  .badge {
      display: inline-block; padding: 2px 8px;
      border-radius: 12px; font-size: 0.72rem;
      font-weight: 600; margin: 1px;
  }
  .badge-blue   { background:#dbeafe; color:#1d4ed8; }
  .badge-green  { background:#dcfce7; color:#166534; }
  .badge-red    { background:#fee2e2; color:#991b1b; }
  .badge-orange { background:#ffedd5; color:#9a3412; }

  /* Sidebar */
  section[data-testid="stSidebar"] {
      background: #f0f4f8;
  }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HELPER: METRIC CARD
# ══════════════════════════════════════════════════════════════════════════════

def metric_card(label, value, sub="", style=""):
    st.markdown(f"""
    <div class="metric-card {style}">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-sub">{sub}</div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div class="main-header">
  <h1>📊 IndiaVaR — Stock Risk Analyzer</h1>
  <p>Value at Risk (VaR) | CVaR | Kupiec Backtesting | Stress Testing | Rolling Risk — NSE Stocks</p>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — INPUTS
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## ⚙️ Parameters")
    st.markdown("---")

    # Stock search
    st.markdown("### 🔍 Stock Search")
    stock_query = st.text_input(
        "Enter company name",
        placeholder="e.g. Reliance, HDFC Bank, Infosys...",
        help="Type any NSE-listed company name. Fuzzy matching will find the ticker."
    )

    selected_ticker  = None
    selected_company = None

    if stock_query and len(stock_query) >= 2:
        results = search_companies(stock_query, top_n=6)
        if results:
            options = {
                f"{r['company_name']}  [{r['ticker']}]  — {r['sector']}": r
                for r in results
            }
            chosen = st.selectbox("Select company", list(options.keys()))
            if chosen:
                selected_ticker  = options[chosen]["ticker"]
                selected_company = options[chosen]["company_name"]
                st.markdown(f"""
                <span class="badge badge-blue">📌 {selected_ticker}</span>
                <span class="badge badge-green">{options[chosen]['sector']}</span>
                """, unsafe_allow_html=True)
        else:
            st.warning("No matches found. Try a different name.")

    st.markdown("---")
    st.markdown("### 💰 Investment Settings")

    investment = st.number_input(
        "Investment Amount (₹)",
        min_value=10_000,
        max_value=100_000_000,
        value=100_000,
        step=10_000,
        format="%d",
        help="Total portfolio value in Indian Rupees.",
    )

    confidence = st.selectbox(
        "Confidence Level",
        options=[0.95, 0.99],
        format_func=lambda x: f"{x:.0%}",
        help="95% → worst 5% days. 99% → worst 1% days.",
    )

    horizon = st.selectbox(
        "Time Horizon",
        options=[1, 5, 10, 22],
        format_func=lambda x: {1:"1 Day",5:"1 Week (5d)",10:"2 Weeks (10d)",22:"1 Month (22d)"}[x],
    )

    data_years = st.slider(
        "Historical Data (years)", min_value=2, max_value=10, value=5
    )

    st.markdown("---")
    st.markdown("### 🧪 Stress Testing")
    
    # Toggle custom scenario
    enable_custom = st.checkbox(
        "Add Custom Scenario?",
        value=False,
        help="Enable to test an additional custom stress scenario beyond the 7 predefined Indian market crises."
    )
    
    custom_shock = None
    custom_label = None
    
    if enable_custom:
        col1, col2 = st.columns(2)
        with col1:
            custom_shock = st.number_input(
                "Custom Shock (%)",
                min_value=-99.0, max_value=-1.0,
                value=-25.0, step=1.0,
                help="Enter a custom negative shock percentage."
            )
        with col2:
            custom_label = st.text_input(
                "Scenario Name", 
                value="My Custom Scenario",
                placeholder="e.g., Bank Crisis, Oil Shock",
                help="Name your custom stress scenario."
            )

    st.markdown("---")
    run_btn = st.button("🚀 Run Analysis", type="primary", use_container_width=True)

    st.markdown("---")
    st.markdown("""
    <small>
    <b>References</b><br>
    • Kupiec (1995) — Journal of Derivatives<br>
    • Jorion (2001) — Value At Risk, McGraw-Hill<br>
    • GARCH: Srinivasan (2010) — NSE Volatility<br>
    • CVaR: Rockafellar & Uryasev (2000)<br>
    • McNeil, Frey & Embrechts (2005) — QRM
    </small>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN ANALYSIS
# ══════════════════════════════════════════════════════════════════════════════

if not run_btn:
    # Landing screen
    st.markdown("""
    <div style="text-align:center; padding:3rem 1rem; color:#666;">
        <div style="font-size:4rem;">📈</div>
        <h2 style="color:#2c3e50;">Welcome to IndiaVaR</h2>
        <p style="max-width:600px; margin:auto; font-size:1.05rem;">
            Type any NSE-listed company name in the sidebar, set your investment
            parameters, and click <b>Run Analysis</b> to get a complete risk report.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.expander("📖 What does this tool calculate?"):
        st.markdown("""
        | Module | What it does |
        |---|---|
        | **3 VaR Methods** | Historical, Parametric (GARCH), Monte Carlo |
        | **CVaR / Expected Shortfall** | Average loss beyond the VaR threshold (Basel III) |
        | **Kupiec POF Backtest** | Tests if VaR model is statistically accurate (Kupiec, 1995) |
        | **Rolling VaR** | How risk evolved through COVID, GFC, Adani crisis |
        | **Stress Testing** | COVID crash, GFC 2008, IL&FS, Adani, custom scenarios |
        | **Risk Report Card** | Sharpe, Sortino, Beta vs Nifty, Max Drawdown |
        """)

    with st.expander("🔢 Key Formulas"):
        st.markdown("""
        **Parametric VaR** (Jorion, 2001):
        """)
        st.code("VaR = -(μ - z_α × σ) × W    where z₀.₉₅ = 1.645,  z₀.₉₉ = 2.326")

        st.markdown("**CVaR / Expected Shortfall** (Rockafellar & Uryasev, 2000):")
        st.code("CVaR = Mean of all returns ≤ VaR threshold × W")

        st.markdown("**Kupiec LR Statistic** (Kupiec, 1995):")
        st.code("LR = -2 × ln[((1-p)^(T-N) × p^N) / ((1-N/T)^(T-N) × (N/T)^N)]   ~  χ²(1)")

        st.markdown("**Square-Root-of-Time Scaling:**")
        st.code("VaR_T = VaR_1d × √T")

    st.stop()


# ── Run analysis ───────────────────────────────────────────────────────────
if not selected_ticker:
    st.error("Please search and select a company from the sidebar first.")
    st.stop()

with st.spinner(f"Fetching data for {selected_company}..."):
    try:
        df, info = fetch_stock_data(selected_ticker, years=data_years)
        nifty_rets = fetch_nifty50(years=data_years)
    except Exception as e:
        st.error(f"Data fetch error: {e}")
        st.stop()

returns = df["LogReturns"]
prices  = df["Close"]

# Compute all VaR (95%)
with st.spinner("Computing VaR (all methods)..."):
    var_95 = compute_all_var(returns, confidence=0.95,       investment=investment, horizon=horizon)
    var_99 = compute_all_var(returns, confidence=0.99,       investment=investment, horizon=horizon)
    var_ch = compute_all_var(returns, confidence=confidence, investment=investment, horizon=horizon)

# Risk metrics
metrics = compute_all_metrics(returns, prices, nifty_rets)

# Rolling VaR
roll_var = rolling_historical_var(returns, window=min(252, len(returns)//2), confidence=confidence, investment=investment)
roll_vol = rolling_volatility(returns, window=30)

# Backtesting
bt_lookback = min(252, len(returns)//3)
try:
    bt = kupiec_pof_test(returns, confidence=confidence, investment=investment, lookback=bt_lookback)
except Exception as bt_err:
    bt = None

# Stress tests
current_price = float(prices.iloc[-1])
stress_df = run_stress_tests(current_price, investment, custom_shock=custom_shock, custom_label=custom_label)

# Drawdown
dd_info = worst_historical_drawdown(prices)


# ══════════════════════════════════════════════════════════════════════════════
# COMPANY INFO BAR
# ══════════════════════════════════════════════════════════════════════════════

st.markdown(f"""
<div style="background:#f8f9fa; border-radius:10px; padding:1rem 1.5rem; margin-bottom:1rem;
            border:1px solid #e0e0e0; display:flex; gap:2rem; align-items:center;">
  <div>
    <div style="font-size:1.4rem; font-weight:700; color:#2c3e50;">
      {info.get("longName", selected_company)}
    </div>
    <div style="color:#666; font-size:0.9rem;">
      {selected_ticker} &nbsp;|&nbsp; {info.get("sector","N/A")} — {info.get("industry","N/A")}
    </div>
  </div>
  <div style="margin-left:auto; text-align:right;">
    <div style="font-size:1.6rem; font-weight:700; color:#1f77b4;">₹{current_price:,.2f}</div>
    <div style="font-size:0.8rem; color:#888;">Latest Close Price</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 VaR Results",
    "🔁 Backtesting",
    "📈 Rolling Risk",
    "💥 Stress Tests",
    "🧮 Risk Metrics",
    "📚 Methodology",
])


# ──────────────────────────────────────────────────────────────────────────────
# TAB 1 — VAR RESULTS
# ──────────────────────────────────────────────────────────────────────────────
with tab1:
    st.markdown(f'<div class="section-header">1-Day VaR Summary — {confidence:.0%} Confidence | ₹{investment:,.0f} Invested</div>', unsafe_allow_html=True)

    # Three method columns
    col1, col2, col3 = st.columns(3)
    methods_display = [
        ("historical",  "📜 Historical",  "Based on actual past returns. No distributional assumption."),
        ("parametric",  "📐 Parametric",  "Normal distribution + GARCH(1,1) volatility estimate."),
        ("monte_carlo", "🎲 Monte Carlo", "10,000 simulated return paths from N(μ, σ²)."),
    ]
    for col, (key, label, desc) in zip([col1, col2, col3], methods_display):
        res = var_ch[key]
        with col:
            st.markdown(f"**{label}**")
            st.caption(desc)
            metric_card("1-Day VaR",
                        f"₹{res['var_inr_1d']:,.0f}",
                        f"({res['var_return']:.2%} return)", "danger")
            metric_card("1-Day CVaR",
                        f"₹{res['cvar_inr_1d']:,.0f}",
                        "Expected Shortfall (tail avg)", "purple")
            if horizon > 1:
                metric_card(f"{horizon}-Day VaR",
                            f"₹{res['var_inr']:,.0f}",
                            f"Scaled by √{horizon}", "warning")

    st.markdown("---")

    # Comparison chart
    st.plotly_chart(var_comparison_chart(var_95, var_99, investment), use_container_width=True)

    st.markdown("---")
    # Return distribution
    st.plotly_chart(
        return_distribution_chart(returns, var_ch, selected_company),
        use_container_width=True
    )

    # Monte Carlo distribution
    st.plotly_chart(
        monte_carlo_chart(var_ch["monte_carlo"], investment),
        use_container_width=True
    )

    # Price chart
    st.plotly_chart(price_chart(prices, selected_company), use_container_width=True)

    # Summary table
    st.markdown('<div class="section-header">Full VaR Table — 95% & 99% Confidence</div>', unsafe_allow_html=True)
    table_rows = []
    for conf_label, var_dict in [("95%", var_95), ("99%", var_99)]:
        for key, mname in [("historical","Historical"),("parametric","Parametric"),("monte_carlo","Monte Carlo")]:
            r = var_dict[key]
            table_rows.append({
                "Confidence" : conf_label,
                "Method"     : mname,
                "VaR Return" : f"{r['var_return']:.3%}",
                "1-Day VaR"  : f"₹{r['var_inr_1d']:,.0f}",
                f"{horizon}d VaR"   : f"₹{r['var_inr']:,.0f}",
                "CVaR Return": f"{r['cvar_return']:.3%}",
                "1-Day CVaR" : f"₹{r['cvar_inr_1d']:,.0f}",
            })
    st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)


# ──────────────────────────────────────────────────────────────────────────────
# TAB 2 — BACKTESTING
# ──────────────────────────────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-header">Kupiec (1995) Proportion of Failures (POF) Backtest</div>', unsafe_allow_html=True)

    with st.expander("📖 What is the Kupiec POF Test?"):
        st.markdown(f"""
        The Kupiec test checks whether the frequency of VaR breaches is statistically
        consistent with the confidence level using a **log-likelihood ratio test**.

        **Null Hypothesis (H₀):** Observed breach rate = Expected breach rate (model is accurate)

        **Formula** (Kupiec, 1995, *Journal of Derivatives*):
        """)
        st.code(
            "LR = -2 × ln[((1-p)^(T-N) × p^N) / ((1-N/T)^(T-N) × (N/T)^N)]  ~  χ²(1)\n\n"
            "T = total observations  |  N = actual breaches  |  p = 1 - confidence\n"
            "Decision: REJECT if LR > χ²(1, 0.95) = 3.841"
        )
        st.markdown(f"""
        A **95% VaR** model should produce ~{0.05*bt_lookback:.0f} breaches in {bt_lookback} days.
        Too many breaches → model underestimates risk. Too few → model is too conservative.
        """)

    if bt:
        # Verdict
        verdict_class = "verdict-pass" if bt["verdict"] == "PASS" else "verdict-fail"
        st.markdown(f'<div class="{verdict_class}">{bt["verdict_msg"]}</div>', unsafe_allow_html=True)
        st.markdown("")

        # Stats row
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Total Observations (T)", bt["T"])
        c2.metric("Actual Breaches (N)", bt["N"])
        c3.metric("Expected Breaches", bt["expected_N"])
        c4.metric("LR Statistic", f"{bt['LR_stat']:.3f}")
        c5.metric("χ² Critical (3.841)", "FAIL ❌" if bt["LR_stat"] > 3.841 else "PASS ✅")

        cols = st.columns(2)
        with cols[0]:
            metric_card("Actual Breach Rate",
                        f"{bt['breach_rate']:.2%}",
                        f"Expected: {bt['expected_rate']:.2%}", "warning")
        with cols[1]:
            metric_card("p-value",
                        f"{bt['p_value']:.4f}",
                        "Reject H₀ if p < 0.05", "danger" if bt["p_value"] < 0.05 else "success")

        st.markdown("---")
        st.plotly_chart(backtest_chart(bt, selected_company), use_container_width=True)

    else:
        st.warning("Not enough data for backtesting. Try increasing historical data years.")


# ──────────────────────────────────────────────────────────────────────────────
# TAB 3 — ROLLING RISK
# ──────────────────────────────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="section-header">Rolling VaR & Volatility — Key Indian Market Events Annotated</div>', unsafe_allow_html=True)

    st.info("Rolling 252-day window shows how risk evolved. Peaks correspond to market crises — demonstrating **volatility clustering** documented in Indian market GARCH studies (Srinivasan, 2010; PMC 2022).")

    st.plotly_chart(rolling_var_chart(roll_var, selected_company, investment), use_container_width=True)
    st.plotly_chart(rolling_volatility_chart(roll_vol, selected_company), use_container_width=True)

    # Rolling VaR stats
    st.markdown("**Rolling VaR Statistics:**")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current VaR", f"₹{roll_var['VaR_INR'].iloc[-1]:,.0f}")
    col2.metric("Peak VaR (worst day)", f"₹{roll_var['VaR_INR'].max():,.0f}")
    col3.metric("Min VaR (calmest)", f"₹{roll_var['VaR_INR'].min():,.0f}")
    col4.metric("Avg VaR over period", f"₹{roll_var['VaR_INR'].mean():,.0f}")


# ──────────────────────────────────────────────────────────────────────────────
# TAB 4 — STRESS TESTS
# ──────────────────────────────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="section-header">Indian Market Stress Test Scenarios</div>', unsafe_allow_html=True)

    st.warning("⚠️ Stress tests apply historical Indian market crisis shocks to your current investment. These are scenario-based estimates, not probability-weighted forecasts.")

    st.plotly_chart(stress_test_chart(stress_df, investment), use_container_width=True)

    # Worst drawdown from actual history
    st.markdown("---")
    st.markdown('<div class="section-header">📉 Actual Historical Drawdown for This Stock</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Max Drawdown", f"{dd_info['max_drawdown_pct']:.1f}%")
    col2.metric("Peak Date", str(dd_info['peak_date'].date()) if hasattr(dd_info['peak_date'], 'date') else str(dd_info['peak_date'])[:10])
    col3.metric("Trough Date", str(dd_info['trough_date'].date()) if hasattr(dd_info['trough_date'], 'date') else str(dd_info['trough_date'])[:10])
    col4.metric("Max Loss (₹)", f"₹{abs(dd_info['max_drawdown_pct']/100 * investment):,.0f}")

    # Stress table
    st.markdown("---")
    st.markdown("**Full Stress Test Table:**")
    display_cols = ["Scenario", "Shock (%)", "Loss (₹)", "Remaining (₹)", "Duration", "Description"]
    st.dataframe(
        stress_df[display_cols].style.format({"Loss (₹)": "₹{:,.0f}", "Remaining (₹)": "₹{:,.0f}"}),
        use_container_width=True,
        hide_index=True,
    )


# ──────────────────────────────────────────────────────────────────────────────
# TAB 5 — RISK REPORT CARD
# ──────────────────────────────────────────────────────────────────────────────
with tab5:
    st.markdown('<div class="section-header">📋 Risk Report Card</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Performance Metrics**")
        metric_card("Annualised Return",
                    f"{metrics['annualised_return']:.2%}",
                    "Compound annual return", "success" if metrics['annualised_return'] > 0 else "danger")
        metric_card("Annualised Volatility",
                    f"{metrics['annualised_volatility']:.2%}",
                    "σ × √252 (historical)", "warning")
        metric_card("Sharpe Ratio",
                    f"{metrics['sharpe_ratio']:.2f}",
                    "RFR = 6.5% (RBI repo rate proxy)", "success" if metrics['sharpe_ratio'] > 1 else "warning")
        metric_card("Sortino Ratio",
                    f"{metrics['sortino_ratio']:.2f}" if not np.isnan(metrics['sortino_ratio']) else "N/A",
                    "Downside risk-adjusted return", "success" if (not np.isnan(metrics['sortino_ratio']) and metrics['sortino_ratio'] > 1) else "warning")
        metric_card("Max Drawdown",
                    f"{metrics['max_drawdown_pct']:.1f}%",
                    "Peak-to-trough decline", "danger")

    with col2:
        st.markdown("**Market & Distribution Metrics**")
        beta_val = metrics.get("beta", np.nan)
        beta_str = f"{beta_val:.2f}" if not np.isnan(beta_val) else "N/A"
        metric_card("Beta vs Nifty 50", beta_str,
                    "Market sensitivity (1.0 = market)", "warning")
        metric_card("Skewness",
                    f"{metrics['skewness']:.3f}",
                    "Negative = left-tail risk (typical for stocks)", "warning")
        metric_card("Excess Kurtosis",
                    f"{metrics['excess_kurtosis']:.3f}",
                    "Fat tails if > 0 (common in Indian markets)", "danger" if metrics['excess_kurtosis'] > 1 else "")
        metric_card("Jarque-Bera Normality",
                    "Not Normal ❌" if not metrics['is_normal_jb'] else "Normal ✅",
                    f"p = {metrics['jb_p_value']:.4f}", "danger" if not metrics['is_normal_jb'] else "success")
        metric_card("Observations",
                    f"{metrics['n_obs']:,}" if 'n_obs' in metrics else str(len(returns)),
                    f"{data_years} years of daily data", "")

    st.markdown("---")

    # Distribution stats table
    st.markdown("**Daily Return Statistics:**")
    stat_df = pd.DataFrame([{
        "Mean Daily Return"    : f"{metrics['mean_return_daily']:.4%}",
        "Daily Std Dev"        : f"{metrics['std_daily']:.4%}",
        "Min Return (worst)"   : f"{metrics['min_return']:.4%}",
        "Max Return (best)"    : f"{metrics['max_return']:.4%}",
        "Annualised Return"    : f"{metrics['annualised_return']:.2%}",
        "Annualised Vol"       : f"{metrics['annualised_volatility']:.2%}",
    }]).T.reset_index()
    stat_df.columns = ["Metric", "Value"]
    st.dataframe(stat_df, use_container_width=True, hide_index=True)


# ──────────────────────────────────────────────────────────────────────────────
# TAB 6 — METHODOLOGY
# ──────────────────────────────────────────────────────────────────────────────
with tab6:
    st.markdown('<div class="section-header">📚 Methodology & Academic References</div>', unsafe_allow_html=True)

    st.markdown("""
    This tool implements industry-standard VaR methodologies as described in academic
    and regulatory literature. All formulas are implemented from primary sources.
    """)

    with st.expander("📐 Parametric (Variance-Covariance) VaR", expanded=True):
        st.markdown("""
        **Source:** Jorion, P. (2001). *Value At Risk: The New Benchmark for Managing Financial Risk*. McGraw-Hill.

        Assumes returns are normally distributed. Uses GARCH(1,1) for dynamic volatility:
        """)
        st.code("""
VaR_param = -(μ - z_α × σ_GARCH) × W

where:
  μ         = mean daily log return
  z_α       = 1.645 (95%)  or  2.326 (99%)  — inverse normal CDF
  σ_GARCH   = 1-step-ahead conditional volatility from GARCH(1,1)
  W         = investment value (₹)

GARCH(1,1) model:  σ²_t = ω + α × ε²_{t-1} + β × σ²_{t-1}
""")
        st.markdown("**GARCH Reference:** Srinivasan (2010), *SAGE Journal* — Forecasting BSE-30 Volatility.")

    with st.expander("📜 Historical Simulation VaR"):
        st.markdown("""
        **Source:** Cheung & Powell (2012); Halilbegovic & Vehabovic (2016).

        No distributional assumptions. Sort actual returns, take the (1-α) percentile.
        """)
        st.code("""
VaR_hist   = |Percentile(returns, 5%)| × W        # 95% confidence
CVaR_hist  = |Mean of returns ≤ VaR_return| × W   # Expected Shortfall
""")

    with st.expander("🎲 Monte Carlo Simulation VaR"):
        st.markdown("""
        **Source:** PyQuant News (2024); Ian Moore (2025 Medium).

        Generates 10,000 random return paths from N(μ, σ²) fitted to historical data.
        VaR = 5th percentile of simulated P&L distribution.
        """)
        st.code("""
r_sim ~ N(μ, σ²),   n = 10,000 simulations
VaR_mc = |Percentile(r_sim, 5%)| × W
CVaR_mc = |Mean(r_sim[r_sim ≤ VaR_return])| × W
""")

    with st.expander("🔁 CVaR / Expected Shortfall"):
        st.markdown("""
        **Source:** Rockafellar, R.T. & Uryasev, S. (2000). *Conditional Value-at-Risk
        for General Loss Distributions.* Journal of Banking and Finance.

        CVaR is preferred over VaR under Basel III regulations because it captures the
        average loss in the tail, not just the threshold.
        """)
        st.code("""
CVaR_α = E[Loss | Loss > VaR_α]
       = Mean of all returns below the VaR threshold × W
""")

    with st.expander("📊 Kupiec POF Backtesting"):
        st.markdown("""
        **Source:** Kupiec, P. (1995). "Techniques for Verifying the Accuracy of Risk
        Management Models." *Journal of Derivatives*, Vol. 3, pp. 73–84.
        """)
        st.code("""
LR_uc = -2 × ln[((1-p)^(T-N) × p^N) / ((1-N/T)^(T-N) × (N/T)^N)]

T = total out-of-sample observations
N = observed VaR breaches
p = expected breach probability = 1 - confidence

LR_uc ~ χ²(1)
Decision: REJECT model if LR_uc > 3.841 (χ²₁ at 95% significance)
""")

    with st.expander("📏 Square-Root-of-Time Scaling"):
        st.code("VaR_T = VaR_1d × √T   (valid under i.i.d. return assumption)")

    with st.expander("📈 Risk Metrics"):
        st.code("""
Sharpe  = (μ_daily - RFR_daily) / σ_daily × √252     RFR = 6.5% (RBI repo)
Sortino = (μ_daily - RFR_daily) / σ_down × √252      (downside vol only)
Beta    = Cov(stock, Nifty50) / Var(Nifty50)
MaxDD   = min( (P_t - max(P_0..t)) / max(P_0..t) )
""")

    st.markdown("---")
    st.markdown("""
    **Full Reference List:**
    - Jorion, P. (2001). *Value At Risk*, 3rd Ed. McGraw-Hill.
    - Kupiec, P. (1995). Journal of Derivatives, 3, 73–84.
    - Rockafellar & Uryasev (2000). Journal of Banking and Finance.
    - McNeil, Frey & Embrechts (2005). *Quantitative Risk Management*. Princeton UP.
    - Srinivasan, P. (2010). SAGE — Forecasting BSE-30 Volatility using GARCH.
    - Ali, F. et al. (2022). PMC — Time-varying volatility, GARCH on NSE.
    - Halilbegovic & Vehabovic (2016). European Journal of Economic Studies.
    - SEBI Working Paper — Price Discovery and Volatility on NSE Futures Market.
    """)


# ══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#888; font-size:0.8rem; padding:0.5rem;">
  IndiaVaR — Built for academic & educational purposes only. Not financial advice.<br>
  Data: Yahoo Finance (yfinance) | Methods: Kupiec (1995), Jorion (2001), Rockafellar & Uryasev (2000)
</div>
""", unsafe_allow_html=True)
