# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-04-11

### Added
- **Core VaR Methods**: Historical Simulation, Parametric GARCH, Monte Carlo (10k simulations)
- **Model Backtesting**: Kupiec POF test with LR statistic and p-value
- **Rolling Analysis**: 252-day rolling VaR and volatility with event annotations
- **Risk Metrics**: Sharpe, Sortino, Beta, Max Drawdown, Skewness, Kurtosis
- **Stress Testing**: 7 historical Indian market scenarios + custom shocks
- **Interactive Dashboard**: 5 tabs with Plotly visualizations
- **Fuzzy Search**: Company name → NSE ticker resolution (RapidFuzz)
- **Live Data**: Yahoo Finance API integration for real-time pricing
- **Documentation**: Comprehensive PDF guide and GitHub documentation

### Technical Details
- Python 3.11.9
- Streamlit 1.56.0
- ARCH 8.0.0 for GARCH modeling
- yfinance 1.2.1 for market data
- Plotly 6.7.0 for visualizations
- RapidFuzz 3.14.5 for fuzzy matching

### Market Events Annotated
- COVID-19 Crash (Mar 2020): -38%
- Global Financial Crisis (2008-09): -60%
- Russia-Ukraine War (Feb 2022): -12%
- IL&FS Default (Sep 2018): -15%
- Adani Crisis (Jan 2023): -20%
- Demonetisation (Nov 2016): -8%
- Flash Crash: -5%

### Academic References
- Jorion (2001) - Value at Risk
- Rockafellar & Uryasev (2000) - CVaR
- Kupiec (1995) - POF Testing
- Srinivasan (2010) - GARCH BSE
- Sharpe (1966), Jensen (1968), Sortino (1994)

---

## Future Roadmap

### v1.1.0 (Planned)
- [ ] Real-time streaming updates
- [ ] Multi-asset portfolio VaR
- [ ] User authentication
- [ ] Historical backtest storage

### v1.2.0 (Planned)
- [ ] Advanced Greeks calculation
- [ ] Machine learning regime detection
- [ ] Database integration (PostgreSQL)
- [ ] REST API with FastAPI

### v2.0.0 (Future)
- [ ] Mobile app version
- [ ] Regulatory compliance templates
- [ ] Performance benchmarking suite
- [ ] Automated reporting

---

## Known Issues

None currently reported.

---

## Support

For issues, questions, or feature requests, please open a GitHub issue.
