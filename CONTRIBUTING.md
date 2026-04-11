# Contributing to IndiaVaR

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on improving the project

## How to Contribute

### Reporting Bugs

1. Check if the issue already exists
2. Provide clear description of the bug
3. Include steps to reproduce
4. Share expected vs actual behavior
5. Include Python version and environment details

### Suggesting Features

1. Check if feature already exists
2. Describe the feature clearly
3. Explain why it would be useful
4. Provide example usage if applicable

### Submitting Code

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/description`
3. Make changes following PEP 8 style
4. Add docstrings to functions
5. Test thoroughly before submitting
6. Commit with clear messages: `git commit -m "Add descriptive message"`
7. Push to branch: `git push origin feature/description`
8. Open a Pull Request with detailed description

## Code Style

- Follow PEP 8 guidelines
- Use 4 spaces for indentation
- Limit lines to 88 characters (Black formatter)
- Add docstrings to all functions
- Type hints are appreciated

Example:
```python
def calculate_var(
    returns: pd.Series,
    confidence: float = 0.95,
    investment: float = 100_000,
) -> dict:
    """
    Calculate Value at Risk using Historical Simulation.
    
    Parameters
    ----------
    returns : pd.Series
        Daily log returns
    confidence : float
        Confidence level (e.g., 0.95 for 95%)
    investment : float
        Investment amount in INR
        
    Returns
    -------
    dict
        VaR estimate and related metrics
    """
    # Implementation
    pass
```

## Pull Request Process

1. Update README.md with any new features
2. Update requirements.txt if adding dependencies
3. Ensure all tests pass
4. Request review from maintainers
5. Address feedback promptly
6. Squash commits before merging

## Testing

Before submitting a PR:

```bash
# Check code style
flake8 *.py

# Type checking
mypy *.py

# Format code
black *.py

# Run tests
pytest tests/
```

## Documentation

If adding features, update:
- README.md (with examples)
- Docstrings (in code)
- DEVELOPMENT.md (if setup changes)
- CHANGELOG.md (describe changes)

## Questions?

- Open a GitHub discussion
- Check existing issues
- Review documentation in `IndiaVaR_Project_Guide.pdf`

---

Thank you for contributing to IndiaVaR! 🚀
