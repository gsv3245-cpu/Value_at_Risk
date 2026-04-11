# 📊 IndiaVaR — Indian Stock Risk Analyzer

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.32+-red.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A professional-grade **Streamlit web application** for Value at Risk (VaR) analysis of NSE-listed Indian stocks. Combines three quantitative methodologies (Historical Simulation, GARCH Parametric, Monte Carlo), statistical backtesting, and interactive visualization.

---

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/gsv3245-cpu/Value_at_Risk.git
cd Value_at_Risk

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
streamlit run app.py
```

Visit: http://localhost:8501

---

## 🎯 Features

| Module | Description |
|---|---|
| **Stock Search** | Fuzzy name-to-ticker resolution for NSE stocks (e.g. type "Reliance" → `RELIANCE.NS`) |
| **3 VaR Methods** | Historical Simulation, Parametric (GARCH), Monte Carlo (10,000 paths) |
| **CVaR / ES** | Expected Shortfall — average loss beyond VaR (Basel III measure) |
| **Kupiec Backtest** | POF test (Kupiec, 1995) — validates if breach rate matches confidence level |
| **Rolling VaR** | 252-day rolling risk with COVID, GFC, Adani, IL&FS event annotations |
| **Stress Testing** | 7 Indian market scenarios + custom user-defined shock |
| **Risk Report Card** | Sharpe, Sortino, Beta vs Nifty 50, Max Drawdown, Kurtosis |

---

## 🔢 Key Formulas

**Parametric VaR** (Jorion, 2001):
```
VaR = -(μ - z_α × σ_GARCH) × W
```

**CVaR / Expected Shortfall** (Rockafellar & Uryasev, 2000):
```
CVaR = Mean of returns ≤ VaR threshold × W
```

**Kupiec POF LR Statistic** (Kupiec, 1995):
```
LR = -2 × ln[((1-p)^(T-N) × p^N) / ((1-N/T)^(T-N) × (N/T)^N)]  ~  χ²(1)
Reject if LR > 3.841
```

**Square-Root-of-Time Scaling:**
```
VaR_T = VaR_1d × √T
```

---

## 🗂️ Project Structure

```
IndiaVaR/
├── app.py                   ← Streamlit UI (main entry point)
├── requirements.txt
├── README.md
├── data/
│   └── nse_tickers.csv      ← Company name → NSE ticker mapping
└── engine/
    ├── __init__.py
    ├── data_fetcher.py      ← yfinance + fuzzy name matching
    ├── var_calculator.py    ← All 3 VaR methods + CVaR
    ├── backtest.py          ← Kupiec POF backtesting test
    ├── rolling_var.py       ← Rolling VaR + volatility
    ├── stress_test.py       ← Indian market stress scenarios
    ├── risk_metrics.py      ← Sharpe, Sortino, Beta, Drawdown
    └── plots.py             ← All Plotly charts
```

---

## 🧪 Tech Stack

- **Python 3.10+**
- `streamlit` — Web UI
- `yfinance` — NSE/BSE market data
- `arch` — GARCH(1,1) volatility modelling
- `scipy` — Statistical tests (chi-square, normal distribution)
- `plotly` — Interactive charts
- `rapidfuzz` — Fuzzy company name matching
- `pandas`, `numpy` — Data processing

---

## 📚 Academic References

1. Jorion, P. (2001). *Value At Risk: The New Benchmark for Managing Financial Risk*. McGraw-Hill.
2. Kupiec, P. (1995). "Techniques for Verifying the Accuracy of Risk Management Models." *Journal of Derivatives*, 3, 73–84.
3. Rockafellar, R.T. & Uryasev, S. (2000). "Conditional Value-at-Risk for General Loss Distributions." *Journal of Banking and Finance*.
4. McNeil, Frey & Embrechts (2005). *Quantitative Risk Management*. Princeton University Press.
5. Srinivasan, P. (2010). "Forecasting BSE-30 Volatility using GARCH Models." *SAGE Journals*.
6. Ali, F. et al. (2022). "Modelling time-varying volatility using GARCH models: evidence from the Indian stock market." *PMC*.
7. Halilbegovic & Vehabovic (2016). "Backtesting Value at Risk — Kupiec POF Test." *European Journal of Economic Studies*.

---

## ⚠️ Disclaimer

For **academic and educational purposes only**. Not financial advice.
Data sourced from Yahoo Finance via `yfinance`.

---

*Built by a Finance & Data Science student at Vidyashilp University, Bengaluru.*
