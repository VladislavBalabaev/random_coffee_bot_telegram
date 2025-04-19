# Notes for Developers

## Code Quality Guide

Tools used:

- [`black`](https://black.readthedocs.io/) – code formatter
- [`isort`](https://pycqa.github.io/isort/) – import sorter
- [`mypy`](http://mypy-lang.org/) – static type checker

Install all dev tools:

```bash
pip install -r requirements.txt -r requirements-dev.txt
```

### Format & Lint

```basn
ruff format src/ tests/
ruff check src/ tests/
```

### Type Check

```bash
mypy src/
```

### Run Tests (Optional)

```bash
pytest
```
