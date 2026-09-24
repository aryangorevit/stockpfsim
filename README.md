# Vityrathi Project: Stock Portfolio Simulator

Terminal-based Python project for learning how trading
decisions, portfolio allocation, and synthetic market conditions affect returns.
It uses hard-coded company data and values only. It does not connect to a broker, use live
prices, or handle real money, as it is a simulator just to train.

## Features

- View a fictional market and price history
- Buy and sell shares with cash and holdings validation
- Track positions, fees, transactions, equity, and returns
- Advance a seeded stochastic market simulation
- Compare low-, medium-, and high-volatility scenarios
- Calculate total return, drawdown, and volatility
- Save/load state as JSON and export an equity curve as CSV
- Optionally plot an equity curve with Matplotlib
- Run automated tests with pytest

## Technology and Python concepts

The core application uses Python's standard library: dataclasses, modules,
packages, lists, tuples, dictionaries, loops, conditionals, exceptions,
file handling, JSON, CSV, and `random.Random`. Classes have focused
responsibilities for stocks, portfolios, transactions, markets, trading,
simulation, analysis, storage, and reporting.

## Project structure

```text
main.py                  # repository-level launcher
modules/
  models/                # Stock, Position, Transaction, Portfolio
  market/                # market quotes and price updates
  trading/               # validated buy/sell operations
  simulation/            # repeatable multi-day simulations
  analysis/              # return, drawdown, volatility, comparisons
  storage/               # JSON persistence and CSV export
  reports/               # terminal reports and optional charting
tests/                   # behavior-focused pytest tests
statement.md             # project statement and scope
```

## Installation and running

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1

python main.py
```

Running with no arguments opens the interactive menu. For a repeatable
non-interactive run:

```bash
python main.py --days 30 --seed 7 --save state.json --csv equity.csv
python main.py --days 30 --seed 7 --plot equity.png
python -m pytest -q
```

## Simulation method

Each stock uses a simple percentage-change model:

```text
new_price = old_price * (1 + drift + random_gaussian_change)
```

Prices are rounded for display and are never allowed to become zero or
negative. Each stock receives its own random draw. A supplied seed makes a run
reproducible; the model is deliberately easy to explain in a first-year
programming project.

## Example output

```text
Simulation report
=================
Initial equity: 10000.00
Final equity: 9952.22
Return: -0.48%
Max drawdown: 0.48%
Volatility: 0.14%
Trades: 1
```

## Testing, limitations, and future work

Tests cover price updates, valid and invalid trades, portfolio values,
simulation length, analysis, scenario comparison, and JSON/CSV persistence.
The simulator is educational: it has no live data, tax treatment, order book,
slippage model, authentication, or financial advice. Possible future work
includes richer order types, configurable portfolios, more chart types, and a
database-backed experiment history.

## References

The general idea of a fictional market simulator was used as conceptual
inspiration. This implementation, data set, terminology, documentation, and
source code were designed independently.
