# Development Setup & Deployment

## Local Development

### 1. Clone Repository
```bash
git clone https://github.com/gsv3245-cpu/Value_at_Risk.git
cd Value_at_Risk
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Locally
```bash
streamlit run app.py
```

Visit: http://localhost:8501

---

## Code Style & Quality

### Follow PEP 8
```bash
pip install flake8
flake8 *.py
```

### Type Checking
```bash
pip install mypy
mypy *.py
```

### Formatting
```bash
pip install black
black *.py
```

---

## Testing

Run tests (when available):
```bash
pip install pytest
pytest tests/
```

---

## Deployment Options

### Option 1: Streamlit Cloud (Recommended)
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy directly from repository

### Option 2: Heroku
```bash
pip install heroku
heroku create your-app-name
git push heroku main
```

### Option 3: Docker
```bash
docker build -t indiavar .
docker run -p 8501:8501 indiavar
```

---

## Data Updates

The app uses live Yahoo Finance data. No manual data updates needed.

To update NSE ticker mappings:
```bash
# Re-download latest ticker list:
python -c "from data_fetcher import _load_ticker_map; _load_ticker_map()"
```

---

## Common Issues & Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'arch'"
**Solution**: `pip install arch`

### Issue: "No such file or directory: nse_tickers.csv"
**Solution**: Ensure nse_tickers.csv is in same directory as app.py

### Issue: Streamlit app not loading
**Solution**:
```bash
streamlit cache clear
streamlit run app.py
```

### Issue: yfinance data fetch fails
**Solution**: Check internet connection; Yahoo Finance may have rate limiting. Try again in a few minutes.

---

## Performance Optimization

### For Large Backtests
- Reduce Monte Carlo simulations from 10,000 to 5,000
- Use shorter rolling windows (126 days instead of 252)
- Cache yfinance downloads

### Memory Management
```python
import streamlit as st

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_stock_data(ticker):
    # Your code here
    pass
```

---

## Security Notes

- No sensitive data stored locally
- All API calls via yfinance (read-only)
- No financial data transmitted externally
- HTTPS recommended for production deployment

---

## Contribution Workflow

1. **Fork** the repository
2. **Create branch**: `git checkout -b feature/xyz`
3. **Make changes** with clear commits
4. **Push**: `git push origin feature/xyz`
5. **Create Pull Request** with description
6. **Code Review**: Address feedback
7. **Merge**: Approved PRs merged to main

---

## Release Checklist

- [ ] Update requirements.txt
- [ ] Update README.md with new features
- [ ] Test all 5 dashboard tabs
- [ ] Verify Kupiec POF test works
- [ ] Check Monte Carlo convergence
- [ ] Test with 3+ different stocks
- [ ] Verify stress testing scenarios
- [ ] Update CHANGELOG
- [ ] Tag version on GitHub
- [ ] Create release notes

---

For questions, open an issue on GitHub.
