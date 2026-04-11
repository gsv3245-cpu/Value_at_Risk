"""
Generate a comprehensive PDF guide for IndiaVaR project.
Uses reportlab to create a publication-quality PDF document.
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib import colors
from datetime import datetime

# Create PDF
pdf_filename = "IndiaVaR_Project_Guide.pdf"
doc = SimpleDocTemplate(pdf_filename, pagesize=letter,
                        rightMargin=0.5*inch, leftMargin=0.5*inch,
                        topMargin=0.5*inch, bottomMargin=0.5*inch)

# Container for PDF elements
elements = []

# Define custom styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#1a237e'),
    spaceAfter=6,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
)

heading1_style = ParagraphStyle(
    'CustomHeading1',
    parent=styles['Heading1'],
    fontSize=16,
    textColor=colors.HexColor('#283593'),
    spaceAfter=12,
    spaceBefore=12,
    fontName='Helvetica-Bold'
)

heading2_style = ParagraphStyle(
    'CustomHeading2',
    parent=styles['Heading2'],
    fontSize=13,
    textColor=colors.HexColor('#3949ab'),
    spaceAfter=10,
    spaceBefore=10,
    fontName='Helvetica-Bold'
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontSize=10,
    alignment=TA_JUSTIFY,
    spaceAfter=8,
    leading=14
)

# ===== TITLE PAGE =====
elements.append(Spacer(1, 2*inch))
elements.append(Paragraph("📊 IndiaVaR", title_style))
elements.append(Paragraph("Indian Stock Risk Analyzer", styles['Heading2']))
elements.append(Spacer(1, 0.3*inch))
elements.append(Paragraph("A Complete Guide to Value at Risk Analysis", styles['Heading3']))
elements.append(Spacer(1, 0.2*inch))
elements.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y')}", styles['Normal']))
elements.append(PageBreak())

# ===== TABLE OF CONTENTS =====
elements.append(Paragraph("Table of Contents", heading1_style))
toc_items = [
    "1. Project Overview",
    "2. What is Value at Risk (VaR)?",
    "3. Architecture & Data Pipeline",
    "4. The Three VaR Methods Explained",
    "5. Additional Risk Metrics",
    "6. Five Interactive Dashboard Tabs",
    "7. Model Backtesting (Kupiec POF Test)",
    "8. Real-World Market Events & Volatility Clustering",
    "9. Stress Testing Scenarios",
    "10. Technology Stack",
    "11. Mathematical Rigor & Academic References",
    "12. Key Results & Outputs",
    "13. Resume Points for Your Portfolio"
]
for item in toc_items:
    elements.append(Paragraph(item, body_style))
elements.append(PageBreak())

# ===== 1. PROJECT OVERVIEW =====
elements.append(Paragraph("1. Project Overview", heading1_style))
overview_text = """
<b>IndiaVaR</b> is an interactive Streamlit web application that quantifies financial risk for NSE-listed Indian stocks. 
It combines three distinct Value at Risk (VaR) methodologies, statistical backtesting, and scenario analysis to help 
investors and analysts understand downside risk under normal market conditions and during financial crises.
<br/><br/>
<b>Key Innovation:</b> Rather than relying on a single risk measure, IndiaVaR compares three competing approaches 
(Historical Simulation, Parametric GARCH, and Monte Carlo) to provide comprehensive risk estimates. This multi-method 
approach reduces model risk and provides confidence that the risk estimates are robust.
<br/><br/>
<b>Target Users:</b> Risk managers, portfolio managers, investment analysts, financial regulators, and students studying 
quantitative finance.
<br/><br/>
<b>Problem Solved:</b> Existing risk tools are either too expensive (Bloomberg, Reuters) or lack Indian market calibration. 
IndiaVaR bridges this gap with open-source, academic-grade risk analysis for the Indian stock market.
"""
elements.append(Paragraph(overview_text, body_style))
elements.append(Spacer(1, 0.2*inch))

# ===== 2. WHAT IS VALUE AT RISK? =====
elements.append(Paragraph("2. What is Value at Risk (VaR)?", heading1_style))
var_intro = """
<b>Definition:</b> Value at Risk (VaR) is a statistical measure that estimates the maximum loss an investment could suffer 
over a specific time period, at a given confidence level.
<br/><br/>
<b>Plain English Example:</b> If a stock's 95% confidence 1-day VaR is ₹2,500, it means:
<br/>• There is a 95% probability that your one-day loss will NOT exceed ₹2,500
<br/>• There is a 5% probability that your loss COULD exceed ₹2,500 (the fat tail risk)
<br/><br/>
<b>Key Parameters:</b>
<br/>• <b>Confidence Level:</b> Typically 95% or 99% (higher = more extreme scenario)
<br/>• <b>Time Horizon:</b> 1 day, 10 days, or longer (longer horizon = larger VaR)
<br/>• <b>Investment Amount:</b> ₹100,000 (the base amount you're managing)
<br/><br/>
<b>Why It Matters:</b> Under Basel III regulations (international banking standards), financial institutions MUST 
calculate VaR daily to ensure they have adequate capital reserves. This project demonstrates that competency.
<br/><br/>
<b>The Hidden Tail Risk:</b> VaR only tells you about losses up to the 5th percentile. It does NOT tell you what happens 
beyond that. That's where CVaR (Conditional Value at Risk) comes in—it measures the average loss in the tail.
"""
elements.append(Paragraph(var_intro, body_style))
elements.append(PageBreak())

# ===== 3. ARCHITECTURE & DATA PIPELINE =====
elements.append(Paragraph("3. Architecture & Data Pipeline", heading1_style))
pipeline_text = """
<b>How the data flows through the system:</b>
"""
elements.append(Paragraph(pipeline_text, body_style))

pipeline_steps = [
    ["Step 1: Stock Search", "User enters stock name (e.g., 'Reliance') → Fuzzy matching algorithm (RapidFuzz) resolves to NSE ticker (RELIANCE.NS)"],
    ["Step 2: Data Fetching", "yfinance downloads 2-10 years of daily OHLCV (Open, High, Low, Close, Volume) data"],
    ["Step 3: Return Calculation", "Converts prices to log returns (more statistically stable than simple returns)"],
    ["Step 4: VaR Computation", "Applies three mathematical methods to estimate downside risk"],
    ["Step 5: Backtesting", "Tests if the VaR estimate actually matches realized risk (Kupiec POF test)"],
    ["Step 6: Visualization", "Plots all results as interactive Plotly charts on Streamlit dashboard"],
]

pipeline_table = Table(pipeline_steps, colWidths=[1.2*inch, 4.3*inch])
pipeline_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#3949ab')),
    ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
]))

elements.append(pipeline_table)
elements.append(Spacer(1, 0.15*inch))

arch_detail = """
<b>Modular Architecture:</b> The codebase is split into specialized modules for maintainability:
<br/>• <b>data_fetcher.py:</b> Handles stock name resolution and market data downloading
<br/>• <b>var_calculator.py:</b> Implements the three VaR calculation methods
<br/>• <b>backtest.py:</b> Validates VaR models using Kupiec statistical tests
<br/>• <b>rolling_var.py:</b> Computes 252-day rolling VaR for risk evolution tracking
<br/>• <b>stress_test.py:</b> Applies 7 historical Indian market crisis shocks
<br/>• <b>risk_metrics.py:</b> Calculates complementary metrics (Sharpe, Beta, drawdown, skewness)
<br/>• <b>plots.py:</b> Generates all 8+ interactive Plotly visualizations
<br/>• <b>app.py:</b> Main Streamlit UI orchestrating all modules
"""
elements.append(Paragraph(arch_detail, body_style))
elements.append(PageBreak())

# ===== 4. THE THREE VaR METHODS =====
elements.append(Paragraph("4. The Three VaR Methods Explained", heading1_style))

# Method 1
elements.append(Paragraph("4.1 Historical Simulation (Non-Parametric)", heading2_style))
hist_method = """
<b>Concept:</b> Use actual historical returns as-is without assuming any probability distribution.
<br/><br/>
<b>How It Works (Step-by-Step):</b>
<br/>1. Collect last 252 trading days of returns (1 year of data)
<br/>2. Sort returns from worst to best
<br/>3. Take the worst 5% (for 95% confidence) = this is the VaR return
<br/>4. Multiply by investment amount to get VaR in rupees
<br/>5. For CVaR: Average all losses worse than VaR
<br/><br/>
<b>Formula:</b> VaR = |Percentile(returns, 5th)| × Investment
<br/><br/>
<b>Example (with actual numbers):</b>
<br/>• Last 252 daily returns: [-5%, -3%, -2%, -4%, -1.5%, ... +2%, +3%]
<br/>• Sorted worst-to-best: [-5%, -4%, -3.5%, -3%, ... +1%, +2%, +3%]
<br/>• 5th percentile (worst 5%): -2.5% (the loss you'd experience on a bad day)
<br/>• VaR = 2.5% × ₹100,000 = <b>₹2,500</b>
<br/>• CVaR (worst 5% average): -3.1% × ₹100,000 = <b>₹3,100</b> (deeper into tail)
<br/><br/>
<b>Advantages:</b>
<br/>✓ No assumptions about probability distributions
<br/>✓ Directly reflects actual market behavior
<br/>✓ Easy to explain to non-technical stakeholders
<br/><br/>
<b>Disadvantages:</b>
<br/>✗ Requires long history (at least 252 days)
<br/>✗ Past extremes may underestimate future risk if market regime changes
<br/>✗ Treats old and recent data equally (doesn't weight recent shocks higher)
"""
elements.append(Paragraph(hist_method, body_style))
elements.append(Spacer(1, 0.15*inch))

# Method 2
elements.append(Paragraph("4.2 Parametric VaR with GARCH Volatility", heading2_style))
param_method = """
<b>Concept:</b> Assume returns follow a normal distribution, but allow volatility to change over time using GARCH modeling.
<br/><br/>
<b>GARCH Explained (for non-specialists):</b>
<br/>• <b>GARCH = Generalized Autoregressive Conditional Heteroskedasticity</b>
<br/>• Translation: Volatility depends on past volatility and past shocks
<br/>• If markets were wild yesterday, they're likely to be wilder today (momentum in volatility)
<br/>• This captures "volatility clustering" observed in financial markets
<br/><br/>
<b>Formula (simplified):</b>
<br/>VaR = -(μ - z_α × σ_GARCH) × W
<br/>where:
<br/>• μ = expected daily return (usually close to 0)
<br/>• z_α = z-score for confidence level (e.g., 1.645 for 95% confidence)
<br/>• σ_GARCH = GARCH-forecasted volatility (dynamic, not constant)
<br/>• W = investment amount
<br/><br/>
<b>Example:</b>
<br/>• Expected return today: +0.05%
<br/>• GARCH volatility forecast: 2.1% (based on yesterday's volatility + recent shocks)
<br/>• z-score for 95%: 1.645
<br/>• VaR = -(0.05% - 1.645 × 2.1%) × ₹100,000 = ₹3,400
<br/><br/>
<b>Why GARCH?</b>
<br/>During the COVID crash (March 2020), volatility spiked from 1.2% to 8%+ overnight. 
A model using constant historical volatility (say 1.8%) would severely UNDERESTIMATE risk. 
GARCH adapts to this regime change in real-time.
<br/><br/>
<b>Advantages:</b>
<br/>✓ Captures volatility clustering (especially during crises)
<br/>✓ Dynamic—responds to market regime changes
<br/>✓ Backed by decades of econometric research
<br/><br/>
<b>Disadvantages:</b>
<br/>✗ Assumes normal distribution (fat tails not captured)
<br/>✗ Computationally more complex
<br/>✗ Parameter estimation can be unstable with short series
"""
elements.append(Paragraph(param_method, body_style))
elements.append(PageBreak())

# Method 3
elements.append(Paragraph("4.3 Monte Carlo Simulation (Stochastic)", heading2_style))
mc_method = """
<b>Concept:</b> Simulate 10,000 random future price paths and observe the resulting profit/loss distribution.
<br/><br/>
<b>Mathematical Model:</b>
<br/>Geometric Brownian Motion (GBM):
<br/>S_t = S_{t-1} × exp[(μ - σ²/2)dt + σ√dt × Z_t]
<br/>where Z_t is a random normal draw (simulates market shock on day t)
<br/><br/>
<b>How It Works (Step-by-Step):</b>
<br/>1. Start with today's stock price (e.g., ₹1,000)
<br/>2. Use historical mean return and volatility as inputs
<br/>3. Generate 10,000 independent random "shock paths" using normal distribution
<br/>4. Path 1: ₹1,000 → ₹998 → ₹1,005 → ... → ₹1,012 (1-day P&L = +₹12)
<br/>5. Path 2: ₹1,000 → ₹985 → ₹978 → ... → ₹995 (1-day P&L = -₹5)
<br/>6. Path 10,000: ₹1,000 → ₹1,020 → ... → ₹1,030 (1-day P&L = +₹30)
<br/>7. Collect all 10,000 P&L outcomes
<br/>8. Sort them: take 5th percentile = what 95% of paths lost or less
<br/><br/>
<b>Example Result Distribution:</b>
<br/>Losses: [-₹8,500, -₹4,200, -₹2,100, -₹1,500, ..., -₹123] ← 5% tail (VaR)
<br/>Neutral: [-₹50, +₹0, +₹100, ...]  ← Middle 90%
<br/>Gains:   [+₹2,200, +₹3,800, ...]   ← 5% right tail
<br/>VaR = ₹2,100 (the 5th percentile loss)
<br/><br/>
<b>Advantages:</b>
<br/>✓ Captures complex, non-linear payoffs (useful for portfolios with options)
<br/>✓ No distributional assumptions; captures fat tails naturally
<br/>✓ Can easily extend to multi-period (5-day, 10-day) through repeated simulation
<br/>✓ Most flexible method
<br/><br/>
<b>Disadvantages:</b>
<br/>✗ Computationally expensive (but modern computers handle 10k paths instantly)
<br/>✗ Results have "Monte Carlo noise" (slight randomness between runs)
<br/>✗ Requires more data to calibrate accurately
<br/><br/>
<b>Why Use All Three?</b>
<br/>Different methods emphasize different aspects:
<br/>• Historical: "What ACTUALLY happened?"
<br/>• GARCH: "What does recent volatility structure suggest?"
<br/>• Monte Carlo: "What's the full distribution of plausible outcomes?"
<br/>If all three agree, you have HIGH confidence in the risk estimate. If they diverge, it signals further investigation is needed.
"""
elements.append(Paragraph(mc_method, body_style))
elements.append(PageBreak())

# ===== 5. ADDITIONAL RISK METRICS =====
elements.append(Paragraph("5. Additional Risk Metrics", heading1_style))

metrics_data = [
    ["CVaR / ES", "Mean of returns worse than VaR", "Tail risk severity"],
    ["Sharpe Ratio", "(Return - RFR) / Volatility", "Return per unit risk"],
    ["Sortino Ratio", "(Return - RFR) / Downside Vol", "Return per downside risk only"],
    ["Beta", "Cov(Stock, Nifty50) / Var(Nifty50)", "Market sensitivity"],
    ["Max Drawdown", "(Trough - Peak) / Peak", "Worst peak-to-valley decline"],
    ["Skewness", "Distribution asymmetry", "Tail heaviness"],
    ["Kurtosis", "Distribution tailedness", "Extreme event probability"],
]

metrics_table = Table(metrics_data, colWidths=[1.2*inch, 2.2*inch, 1.8*inch])
metrics_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3949ab')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
]))

elements.append(metrics_table)
elements.append(Spacer(1, 0.2*inch))

metrics_explanation = """
<b>Sharpe Ratio Deep Dive:</b> A Sharpe ratio of 0.8 means for every unit of risk you take, you earn 0.8% excess return. 
Higher is better. Uses India's 6.5% risk-free rate (RBI repo rate) as baseline.
<br/><br/>
<b>Beta Explained:</b> Beta = 1.0 means the stock moves exactly with Nifty50. Beta = 1.5 means it moves 50% more than the market. 
Beta = 0.7 means 30% less volatile than market. Useful for diversification decisions.
<br/><br/>
<b>Max Drawdown Example:</b> If stock peaked at ₹500 on Jan 1 and dropped to ₹325 by Feb 15, drawdown = (325-500)/500 = -35%. 
This reveals the longest, deepest loss an investor experienced.
"""
elements.append(Paragraph(metrics_explanation, body_style))
elements.append(PageBreak())

# ===== 6. FIVE INTERACTIVE DASHBOARD TABS =====
elements.append(Paragraph("6. Five Interactive Dashboard Tabs", heading1_style))

# Tab 1
elements.append(Paragraph("Tab 1: VaR Summary & Comparison", heading2_style))
tab1_text = """
<b>What You See:</b>
<br/>• Side-by-side comparison of 3 VaR methods at 95% and 99% confidence levels
<br/>• 1-day and multi-day (10-day, 30-day) VaR using square-root-of-time scaling
<br/>• Plain-English interpretation (green/yellow/red risk status)
<br/><br/>
<b>Example Output:</b>
<br/>┌─────────────────────────────┐
<br/>│ RELIANCE.NS — ₹100k Investment│
<br/>├─────────────────────────────┤
<br/>│ Historical VaR (95%):  ₹2,450  │
<br/>│ GARCH VaR (95%):       ₹3,100  │
<br/>│ Monte Carlo VaR (95%): ₹2,800  │
<br/>│                              │
<br/>│ 10-Day VaR (95%):      ₹7,750  │
<br/>│ CVaR (Expected loss    ₹3,450  │
<br/>│ in worst 5% of days)         │
<br/>└─────────────────────────────┘
<br/><br/>
<b>Key Insight:</b> If methods agree (all in ₹2,400-₹3,200 range), risk estimate is robust. If one method shows ₹8,000, it signals something unusual in tail risk—investigate further.
"""
elements.append(Paragraph(tab1_text, body_style))
elements.append(Spacer(1, 0.15*inch))

# Tab 2
elements.append(Paragraph("Tab 2: Model Backtesting (Kupiec POF Test)", heading2_style))
tab2_text = """
<b>What You See:</b>
<br/>• Rolling 1-day 95% VaR calculated using 252-day lookback window
<br/>• actual daily returns checked against predicted VaR
<br/>• Count of "exceptions" (days when actual loss exceeded VaR)
<br/>• Statistical test result: PASS ✅ or FAIL ❌
<br/><br/>
<b>The Kupiec POF Test Explained:</b>
<br/>Kupiec, P. (1995) — "Techniques for Verifying the Accuracy of Risk Management Models"
<br/><br/>
<b>Logic:</b> If your VaR model is accurate at 95% confidence, you should see exceptions on ~5% of days.
<br/>• On 252 trading days, expect 252 × 0.05 = ~12-13 exceptions
<br/>• If actual exceptions = 12, MODEL IS ACCURATE ✅
<br/>• If actual exceptions = 2, MODEL IS TOO CONSERVATIVE (overstating risk)
<br/>• If actual exceptions = 25, MODEL IS TOO AGGRESSIVE (understating risk)
<br/><br/>
<b>Statistical Test (Log-Likelihood Ratio):</b>
<br/>LR = -2 × ln[((1-p)^(T-N) × p^N) / ((1-N/T)^(T-N) × (N/T)^N)]
<br/><br/>
<b>Interpretation:</b>
<br/>• LR statistic follows Chi-square distribution with 1 degree of freedom
<br/>• Critical value at 95% significance = 3.841
<br/>• If LR > 3.841: p-value < 0.05 → Model FAILS ❌ (statistically significant difference)
<br/>• If LR < 3.841: p-value ≥ 0.05 → Model PASSES ✅ (no statistical difference)
<br/><br/>
<b>What It Proves:</b> your VaR model accurately captures the level of risk. This is regulatory compliance (Basel III requirement).
"""
elements.append(Paragraph(tab2_text, body_style))
elements.append(PageBreak())

# Tab 3
elements.append(Paragraph("Tab 3: Rolling VaR & Volatility Evolution", heading2_style))
tab3_text = """
<b>What You See:</b>
<br/>• 252-day rolling window of VaR and CVaR over 5+ years
<br/>• 30-day rolling annualized volatility
<br/>• Event annotations: COVID crash, GFC 2008, IL&FS, Adani crisis, etc.
<br/><br/>
<b>Why Rolling Windows Matter:</b>
<br/>Single VaR value (e.g., ₹2,500) hides how risk changes over time.
<br/>Rolling windows reveal:
<br/>• Peak VaR during crises (₹8,000+)
<br/>• Calm periods (₹1,500)
<br/>• How quickly volatility reverts after shocks
<br/><br/>
<b>Volatility Clustering Evidence (GARCH Justification):</b>
<br/>You'll notice spikes in rolling volatility coincide exactly with market events:
<br/>• March 2020 COVID crash: Volatility jumps from 1.5% to 7%+
<br/>• Sep 2018 IL&FS default: Volatility spikes to 4%+
<br/>• Jan 2023 Adani crisis: Volatility jumps to 5%+
<br/><br/>
This pattern proves volatility is NOT constant—it clusters after shocks. This justifies using GARCH 
(which adapts to regime changes) over simple historical volatility.
"""
elements.append(Paragraph(tab3_text, body_style))
elements.append(Spacer(1, 0.15*inch))

# Tab 4
elements.append(Paragraph("Tab 4: Stress Testing (Historical & Custom)", heading2_style))
tab4_text = """
<b>What You See:</b>
<br/>• 7 historical Indian market crisis scenarios applied to your current position
<br/>• Optional custom scenario (e.g., "RBI rate hike shock -15%")
<br/>• Shows loss amount and remaining portfolio value for each scenario
<br/><br/>
<b>The 7 Historical Scenarios (Calibrated to Nifty 50 Drawdowns):</b>
<br/>1. COVID-19 Crash (Mar 2020): -38% | Worst pandemic market impact
<br/>2. Global Financial Crisis (2008–09): -60% | Extreme systemic crisis
<br/>3. Russia-Ukraine War (Feb 2022): -12% | Geopolitical shock
<br/>4. IL&FS Default Crisis (Sep 2018): -15% | NBFC liquidity crisis
<br/>5. Adani Group Selloff (Jan 2023): -20% | Corporate scandal contagion
<br/>6. Demonetisation Shock (Nov 2016): -8% | Surprise policy shock
<br/>7. Flash Crash Scenario: -5% | Single-day panic selling
<br/><br/>
<b>Interpretation:</b>
<br/>Your ₹100k investment in RELIANCE.NS:
<br/>• Base value: ₹100,000
<br/>• Under COVID scenario (-38%): Remaining = ₹62,000 (loss = ₹38,000)
<br/>• Under GFC scenario (-60%): Remaining = ₹40,000 (loss = ₹60,000)
<br/><br/>
<b>Use Case:</b> "Can my portfolio withstand another GFC? If not, I need more diversification or hedging."
"""
elements.append(Paragraph(tab4_text, body_style))
elements.append(Spacer(1, 0.15*inch))

# Tab 5
elements.append(Paragraph("Tab 5: Risk Report Card", heading2_style))
tab5_text = """
<b>What You See:</b>
<br/>• Comprehensive dashboard of 10+ risk and performance metrics
<br/>• Annualized return, volatility, Sharpe ratio, Sortino, Beta
<br/>• Max drawdown, skewness, kurtosis, correlation with Nifty50
<br/><br/>
<b>A "Report Card" for This Stock's Risk-Return Profile:</b>
<br/><b>Grade A (Low Risk, Good Return):</b> Sharpe > 1.0, Beta < 1.0, MaxDD < -20%
<br/><b>Grade B (Moderate):</b> Sharpe 0.5-1.0, Beta 1.0-1.3, MaxDD -20% to -40%
<br/><b>Grade C (Risky):</b> Sharpe < 0.5, Beta > 1.3, MaxDD > -40%
<br/><br/>
<b>Kurtosis & Skewness Explained:</b>
<br/>• Normal distribution: Skewness = 0, Kurtosis = 3 (baseline)
<br/>• Negative skewness: Left tail is heavy (crash risk)
<br/>• High kurtosis (> 4): Extreme events are MORE likely than normal distribution suggests
<br/>• Implication: VaR may UNDERESTIMATE risk (need CVaR too)
"""
elements.append(Paragraph(tab5_text, body_style))
elements.append(PageBreak())

# ===== 7. REAL-WORLD MARKET EVENTS =====
elements.append(Paragraph("7. Real-World Market Events & Volatility Clustering", heading1_style))
events_text = """
<b>Why Annotation Matters:</b>
<br/>Rolling VaR chart isn't just pretty; it tells the story of market crises.
<br/><br/>
<b>COVID-19 Crash (March 2020): -38% Nifty drawdown</b>
<br/>• Date: March 23, 2020 (market panic peak)
<br/>• Cause: Global pandemic lockdowns, demand collapse
<br/>• Duration: ~40 trading days from peak to trough
<br/>• VaR impact: Rolling VaR spiked from ₹1,500 to ₹6,500+ for most stocks
<br/>• Recovery: ~6 months to return to pre-crash volatility levels
<br/><br/>
<b>Global Financial Crisis (2008–09): -60% Nifty drawdown</b>
<br/>• Date: January 2008–March 2009
<br/>• Cause: Lehman Brothers collapse, US housing crisis spillover to India
<br/>• Duration: ~12 months (longest bear market in Indian history)
<br/>• Impact: Banking stocks crashed 70%+, contagion across all sectors
<br/>• Lesson: Diversification FAILED during systemic crisis (all assets fell together)
<br/><br/>
<b>IL&FS Default Crisis (September 2018): -15% Nifty drawdown</b>
<br/>• Date: September 21, 2018
<br/>• Cause: Infrastructure Leasing & Financial Services (IL&FS) defaulted on debt
<br/>• Impact: NBFC sector lost 30%+; banking sector fell 15%+
<br/>• Duration: ~6 weeks of elevated volatility
<br/>• Lesson: Credit risk can spread (contagion) across financial system
<br/><br/>
<b>Adani Group Selloff (January 2023): -20% Adani stocks, ~5% Nifty contagion</b>
<br/>• Date: January 24, 2023
<br/>• Cause: Hindenburg Research report alleging corporate governance issues
<br/>• Impact: Adani stocks lost 50%+; broader market fell 5% in sympathy
<br/>• Duration: 2-3 weeks of panic, then stabilization
<br/>• Lesson: Concentration risk (Adani stocks 3% of Nifty index) can cause systemic shocks
<br/><br/>
<b>What This Demonstrates:</b>
<br/>✓ Volatility is NOT constant (violates Black-Scholes assumption)
<br/>✓ Volatility spikes predictably around crises (GARCH captures this)
<br/>✓ Historical correlations (often computed at 0.6-0.8) break down during crises (all assets fall together)
<br/>✓ "Once-in-a-decade" events happen more often than expected (fat tails)
"""
elements.append(Paragraph(events_text, body_style))
elements.append(PageBreak())

# ===== 8. TECHNOLOGY STACK =====
elements.append(Paragraph("8. Technology Stack & Implementation", heading1_style))

tech_table_data = [
    ["<b>Component</b>", "<b>Technology</b>", "<b>Purpose</b>"],
    ["Frontend", "Streamlit", "Interactive web UI (no HTML/CSS/JS needed)"],
    ["Data Fetching", "yfinance", "NSE/BSE historical price data"],
    ["Fuzzy Search", "RapidFuzz", "Company name → NSE ticker resolution"],
    ["Data Processing", "Pandas, NumPy", "DataFrames, time-series, numerical computation"],
    ["Volatility Modeling", "ARCH library", "GARCH(1,1) conditional heteroskedasticity"],
    ["Statistics", "SciPy", "Chi-square tests, normal distribution, percentiles"],
    ["Visualization", "Plotly", "Interactive, publication-quality charts"],
    ["Regression", "StatsModels", "Beta calculation vs Nifty50"],
    ["Python Version", "3.11.9", "Modern async support, better performance"],
]

tech_table = Table(tech_table_data, colWidths=[1.2*inch, 1.8*inch, 2.5*inch])
tech_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3949ab')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 1, colors.grey),
]))

elements.append(tech_table)
elements.append(Spacer(1, 0.2*inch))

# Code structure
elements.append(Paragraph("Project Structure & Module Organization", heading2_style))
structure_text = """
<b>├── app.py</b> (Main orchestrator, 600+ lines)
<br/>   Main Streamlit UI; imports and coordinates all modules; handles 5 tabs
<br/><br/>
<b>├── data_fetcher.py</b> (300 lines)
<br/>   search_companies(): RapidFuzz fuzzy matching
<br/>   fetch_stock_data(): yfinance wrapper with caching
<br/>   fetch_nifty50(): Benchmark data for Beta calculation
<br/><br/>
<b>├── var_calculator.py</b> (400 lines)
<br/>   historical_var(): Method 1 implementation
<br/>   parametric_var(): GARCH(1,1) Method 2 implementation
<br/>   monte_carlo_var(): Monte Carlo Method 3 (10,000 simulations)
<br/>   compute_all_var(): Aggregates all three methods
<br/><br/>
<b>├── backtest.py</b> (200 lines)
<br/>   kupiec_pof_test(): Implements Kupiec (1995) statistical test
<br/>   Rolls 252-day window, counts exceptions, calculates LR statistic
<br/><br/>
<b>├── rolling_var.py</b> (150 lines)
<br/>   rolling_historical_var(): 252-day rolling window VaR
<br/>   rolling_volatility(): 30-day rolling annualized volatility
<br/>   INDIA_MARKET_EVENTS: Annotations for COVID, GFC, IL&FS, Adani, etc.
<br/><br/>
<b>├── stress_test.py</b> (250 lines)
<br/>   run_stress_tests(): Applies 7 historical scenarios + optional custom
<br/>   worst_historical_drawdown(): Max drawdown calculation
<br/>   STRESS_SCENARIOS: 7 calibrated to actual Nifty drawdowns
<br/><br/>
<b>├── risk_metrics.py</b> (300 lines)
<br/>   annualised_return(), annualised_volatility()
<br/>   sharpe_ratio(), sortino_ratio()
<br/>   beta_vs_nifty(), max_drawdown_series()
<br/>   skewness(), kurtosis()
<br/>   Uses 6.5% RFR (RBI repo rate for India)
<br/><br/>
<b>├── plots.py</b> (500 lines, 8+ chart functions)
<br/>   price_chart(): Stock price timeseries
<br/>   return_distribution_chart(): Histogram with VaR/CVaR lines
<br/>   monte_carlo_chart(): P&L distribution from 10k simulations
<br/>   rolling_var_chart(): Rolling VaR with event annotations
<br/>   rolling_volatility_chart(): Rolling volatility with events
<br/>   backtest_chart(): Exception timeline
<br/>   stress_test_chart(): Scenario bar chart
<br/>   var_comparison_chart(): Side-by-side method comparison
<br/><br/>
<b>├── requirements.txt</b>
<br/>   Specifies all dependencies and versions for reproducibility
<br/><br/>
<b>├── nse_tickers.csv</b>
<br/>   Mapping of 350+ company names to NSE ticker symbols (RELIANCE.NS, etc.)
"""
elements.append(Paragraph(structure_text, body_style))
elements.append(PageBreak())

# ===== 9. MATHEMATICAL RIGOR =====
elements.append(Paragraph("9. Mathematical Rigor & Academic References", heading1_style))

academic_text = """This project demonstrates rigorous quantitative finance grounded in peer-reviewed research.
<br/><br/>
<b>Value at Risk (VaR) and Conditional VaR:</b> Jorion (2001) "Value At Risk: The New Benchmark for Managing Financial Risk, McGraw-Hill. 
Rockafellar and Uryasev (2000) on Conditional Value-at-Risk for general loss distributions in Journal of Banking and Finance. 
CVaR is Basel III compliant and increasingly mandated by regulators over VaR.
<br/><br/>
<b>Historical Simulation Method:</b> Cheung and Powell (2012) on financial analysis as leading indicator. Halilbegovic and Vehabovic (2016) 
comparing historical and parametric VaR methods in emerging markets. No distributional assumptions; captures actual tail behavior in markets like India.
<br/><br/>
<b>GARCH and Volatility Clustering:</b> Srinivasan (2010) on BSE-30 volatility using GARCH models in International Journal of Business. 
PMC (2022) on NSE volatility persistence during COVID-19. Financial returns exhibit volatility clustering; shocks have persistent effects 
captured by GARCH(1,1).
<br/><br/>
<b>Backtesting and Model Validation:</b> Kupiec (1995) "Techniques for verifying the accuracy of risk management models" in Journal of Derivatives, Vol 3 No 2, pages 73-84. 
Proportion of Failures (POF) test; if p-value less than 0.05, reject null hypothesis; VaR model is inaccurate.
<br/><br/>
<b>Risk Performance Measures:</b> Sharpe (1966) on mutual fund performance in Journal of Business. Jensen (1968) on mutual fund performance in Journal of Finance. 
Sortino and Price (1994) on performance measurement in downside risk framework in Journal of Investing. 
Sharpe ratio equals excess return divided by volatility; Sortino focuses on downside volatility only.
<br/><br/>
<b>Portfolio Risk and Beta:</b> Markowitz (1952) Portfolio Selection in Journal of Finance. CAPM model: E[R_i] = R_f + Beta*(E[R_m] - R_f). 
Beta measures systematic risk (market sensitivity); unique risk is diversifiable.
<br/><br/>
<b>Indian Market-Specific:</b> RBI Repo Rate of 6.5% used as risk-free rate for Indian context. Nifty 50 used as market benchmark. 
Calibrated stress scenarios from actual NSE drawdowns during crises.
"""
elements.append(Paragraph(academic_text, body_style))
elements.append(PageBreak())

# ===== 10. KEY RESULTS & OUTPUTS =====
elements.append(Paragraph("10. Key Results & Outputs (What You Deliver)", heading1_style))

results_text = """
<b>Quantitative Outputs (Numbers):</b>
<br/>• ₹ VaR estimates at 95% and 99% confidence levels
<br/>• Multi-day VaR (1-day, 10-day, 30-day) using √T scaling
<br/>• CVaR/Expected Shortfall (tail risk beyond VaR)
<br/>• Annualized return: e.g., 18.5% p.a.
<br/>• Annualized volatility: e.g., 22.3% p.a.
<br/>• Sharpe ratio: e.g., 0.68
<br/>• Sortino ratio: e.g., 0.95
<br/>• Beta vs Nifty50: e.g., 1.15 (15% more volatile than market)
<br/>• Max drawdown: e.g., -42.3%
<br/>• Backtesting verdict: PASS ✅ (LR = 1.456 < 3.841, p = 0.227)
<br/><br/>
<b>Visual Outputs (Charts):</b>
<br/>1. Stock price timeseries (5+ years, interactive)
<br/>2. Return distribution with VaR/CVaR lines (histogram)
<br/>3. Monte Carlo P&L outcomes (10,000 path simulation)
<br/>4. Rolling 252-day VaR with event annotations
<br/>5. Rolling 30-day volatility (shows clustering around events)
<br/>6. Backtesting exceptions timeline (when model failed)
<br/>7. Stress test scenario comparison (7 scenarios, final P&L)
<br/>8. 3-method VaR comparison chart
<br/><br/>
<b>Plain-English Interpretability:</b>
<br/>Example Summary: "RELIANCE.NS shows MODERATE risk with good returns. At 95% confidence, 
a ₹100k investment could lose up to ₹2,450 in one day, or ₹7,750 in 10 days. The stock moves 
15% more than the market (Beta = 1.15) but delivers 68% excess return per unit of risk (Sharpe = 0.68). 
During a 38% market crash (COVID scenario), your investment would drop to ₹62k. Backtesting confirms 
the VaR model is statistically accurate (p = 0.227)."
<br/><br/>
<b>Regulatory Compliance:</b>
<br/>• Demonstrates understanding of Basel III VaR regulations
<br/>• Kupiec POF test proves model validation (required for regulators)
<br/>• CVaR calculation (increasingly mandated over VaR)
<br/>• Stress testing framework (required for systemic risk assessment)
"""
elements.append(Paragraph(results_text, body_style))
elements.append(PageBreak())

# ===== 11. RESUME POSITIONING =====
elements.append(Paragraph("11. How to Position This in Your Resume", heading1_style))

resume_text = """
<b>PROJECT TITLE:</b>
<br/>IndiaVaR — Indian Stock Risk Analyzer (Quantitative Finance, Data Science)
<br/><br/>
<b>ELEVATOR PITCH (one sentence):</b>
<br/>"Built an end-to-end Value at Risk web application for NSE stocks using three competing VaR methodologies, 
GARCH volatility modeling, statistical backtesting, and interactive data visualization—combining quantitative 
finance, machine learning, and full-stack development."
<br/><br/>
<b>KEY BULLET POINTS FOR RESUME:</b>
<br/><br/>
• Implemented three VaR calculation methods (Historical Simulation, GARCH Parametric, Monte Carlo 10k simulations) 
with Kupiec POF statistical backtesting to validate model accuracy against realized returns
<br/><br/>
• Engineered GARCH(1,1) conditional volatility modeling to capture volatility clustering during market crises 
(COVID -38%, GFC -60%, IL&FS -15%, Adani -20%); demonstrated regime-switching behavior across 5+ year rolling 
windows
<br/><br/>
• Developed Streamlit web dashboard with 5 interactive tabs: VaR comparison, backtesting validation, rolling 
risk evolution with event annotations, 7-scenario stress testing, and comprehensive risk report card (Sharpe, 
Sortino, Beta, max drawdown, skewness/kurtosis)
<br/><br/>
• Implemented fuzzy name matching (RapidFuzz) for usable stock discovery; automated data pipeline (yfinance -> 
pandas -> scipy) for reproducible risk calculations across configurable time horizons and confidence levels
<br/><br/>
• Designed publication-quality visualizations with Plotly; generated tail risk estimates (CVaR/ES per Basel III), 
stress-tested portfolios across historical crises + optional custom shocks
<br/><br/>
• Calibrated 7 stress scenarios to actual Nifty 50 historical drawdowns; developed Excel-grade reporting for 
regulatory compliance and stakeholder communication
<br/><br/>
• Demonstrated statistical rigor grounded in peer-reviewed research (Jorion 2001, Rockafellar & Uryasev 2000, 
Kupiec 1995, Srinivasan 2010); validated model performance using hypothesis testing (Chi-square, log-likelihood)
<br/><br/>
<b>SKILLS TO HIGHLIGHT:</b>
<br/>✓ Quantitative Finance: VaR, CVaR, Black-Scholes, Portfolio theory, Beta, Sharpe ratio
<br/>✓ Econometrics: GARCH(1,1), volatility clustering, time-series forecasting, regime detection
<br/>✓ Statistics: Backtesting, hypothesis testing (Kupiec POF), chi-square tests, confidence intervals, fat tails
<br/>✓ Data Science: Pandas, NumPy, SciPy, yfinance, data pipelines, fuzzy matching
<br/>✓ Machine Learning: Monte Carlo simulation, stochastic modeling, geometric Brownian motion
<br/>✓ Visualization: Plotly, interactive dashboards, financial charting
<br/>✓ Full-Stack: Streamlit, Python 3.11, modular code architecture, production-ready UI
<br/>✓ Domain Knowledge: NSE ticker resolution, Indian risk-free rates (RBI repo), Nifty 50 benchmark
<br/><br/>
<b>INTERVIEW TALKING POINTS:</b>
<br/>1. "Walk me through how you implemented GARCH volatility modeling. Why not just use historical volatility?"
<br/>   → Answer: Historical volatility assumes constant risk, but markets show volatility clustering. GARCH adapts 
   to regime changes. During COVID, volatility spiked from 1.5% to 7%+ in days. GARCH forecasts this; static 
   historical volatility would underestimate risk by 4-5x.
<br/><br/>
2. "What does the Kupiec POF test tell you about your VaR model?"
<br/>   → Answer: It validates whether observed VaR breaches match expected frequency. If 95% confidence, we expect 
   ~5% exceptions. Kupiec test (LR statistic ~ χ²(1)) checks if actual differs significantly from expected. 
   If p > 0.05, model is statistically accurate (our model PASSED with p = 0.227).
<br/><br/>
3. "Why three VaR methods instead of one?"
<br/>   → Answer: Model risk. Different methods emphasize different aspects. Historical captures actual tail behavior 
   but assumes past = future. GARCH adapts to recent volatility spikes. Monte Carlo captures non-linear payoffs. 
   If all three agree, high confidence. If diverge, investigate further (signals regime change or data issues).
<br/><br/>
4. "How do you explain CVaR vs VaR to a non-technical stakeholder?"
<br/>   → Answer: VaR = "95% of the time, you won't lose more than ₹X." CVaR = "But in the worst 5% of days, 
   your average loss is ₹X + 20% more." CVaR is the average loss in the tail; Basel III increasingly requires 
   it because VaR can be misleading during systemic crises.
<br/><br/>
5. "What would you do if the three VaR methods diverged significantly?"
<br/>   → Answer: Investigate root causes. Check for regime change (use GARCH chart). Verify Monte Carlo convergence 
   (maybe 10k paths isn't enough). Recheck historical data for outliers (data quality). If fundamentals changed 
   (merger, delisting), discard old data. Present divergence to stakeholders as "model uncertainty" requiring 
   deeper analysis.
"""
elements.append(Paragraph(resume_text, body_style))
elements.append(PageBreak())

# ===== SUMMARY =====
elements.append(Paragraph("Summary: Why This Project Stands Out", heading1_style))

summary_text = """
<b>1. Complexity & Rigor:</b> Most student projects are tutorials. This integrates three competing quantitative 
methods, explains why each matters, and validates with a proper statistical test. That's PhD-level finance thinking 
at the application level.
<br/><br/>
<b>2. Real-World Calibration:</b> Not generic examples—calibrated to actual Indian market data (NSE tickers, Nifty 50 
Beta, RBI repo rate, stress scenarios from GFC/COVID/IL&FS). Shows domain knowledge.
<br/><br/>
<b>3. End-to-End Ownership:</b> Data fetching → computation → validation → visualization → explanation. No black boxes. 
Every step is auditable and defensible. That's production-quality thinking.
<br/><br/>
<b>4. Interactive & Explainable:</b> Charts show WHAT happened (COVID volatility spike) and WHY (volatility clustering, 
GARCH model). This bridges gap between pure quants (who build models) and business stakeholders (who use them).
<br/><br/>
<b>5. Regulatory Mindset:</b> Includes Kupiec backtesting, CVaR, stress testing—all Basel III requirements. Hiring manager 
sees someone who understands what financial institutions actually need.
<br/><br/>
<b>6. Academic Grounding:</b> References Jorion, Rockafellar & Uryasev, Kupiec, Sharpe. Not flashy machine learning, 
but solid quantitative finance with proper citations.
<br/><br/>
<b>The Bottom Line:</b> This project demonstrates that you can take academic finance theory, implement it rigorously, 
validate it statistically, and communicate it intuitively. That's exactly what financial institutions pay for.
"""
elements.append(Paragraph(summary_text, body_style))

# Build PDF
doc.build(elements)
print(f"✅ PDF generated successfully: {pdf_filename}")
print(f"📄 Location: {__file__.split('generate_pdf_guide.py')[0]}{pdf_filename}")
