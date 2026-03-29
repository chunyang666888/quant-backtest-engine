# quant-backtest-engine
![tests](https://github.com/chunyang666888/quant-backtest-engine/actions/workflows/ci.yml/badge.svg)


> Lightweight, dependency-light **event-driven backtesting engine** for quantitative trading strategies — written in clean, typed Python with a full test suite.

[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](#running-tests)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](#license)

## Why this repo exists

Recruiters in quant / trading-system roles look for **evidence of engineering discipline**, not just finance intuition: clean modules, type hints, tests, and reproducible results. This engine separates concerns into `strategy → broker → portfolio → engine`, so you can drop in your own alpha without rewriting the plumbing.

## Features

- Event-driven loop (`Bar` → strategy signal → simulated fill → portfolio update → equity mark-to-market)
- Pluggable strategies via a single `on_bar(bar) -> int` method
- Simulated broker with **commission + slippage**
- Long-only by default; `allow_short=True` for long/short signals
- Built-in performance metrics: **Sharpe, Sortino, Max Drawdown, CAGR**
- Zero external data files — synthetic GBM generator for demos & CI

## Installation

```bash
pip install -r requirements.txt
# or
pip install -e .
```

## Quick start

```python
from backtest.data import generate_gbm
from backtest.engine import BacktestEngine
from backtest.strategy import SMACrossStrategy

bars = generate_gbm("DEMO", n=600, seed=7)
engine = BacktestEngine(initial_cash=1_000_000)
result = engine.run(bars, SMACrossStrategy(short=20, long=50))

print(result["sharpe"], result["max_drawdown"], result["final_equity"])
```

Or run the bundled demo:

```bash
python examples/run_sma_crossover.py
```

## Architecture

```
Bar ──▶ Strategy.on_bar() ──▶ signal (1 / -1 / 0)
                                │
                                ▼
                         Engine._rebalance()
                                │
                                ▼
                    Broker.fill_price()  ──▶ Trade
                                │
                                ▼
                    Portfolio.apply_trade() ──▶ equity mark-to-market
```

| Module | Responsibility |
|--------|----------------|
| `events.py`     | `Bar`, `Trade` data structures |
| `strategy.py`   | `Strategy` interface + `SMACrossStrategy`, `BuyAndHoldStrategy` |
| `broker.py`     | Simulated fills (commission + slippage) |
| `portfolio.py`  | Cash / position bookkeeping |
| `engine.py`     | Orchestration + summary metrics |
| `metrics.py`    | Sharpe / Sortino / MaxDD / CAGR |
| `data.py`       | Synthetic GBM data generator |

## Running tests

```bash
pytest -q
```

## Project structure

```
quant-backtest-engine/
├── backtest/          # package source
│   ├── events.py
│   ├── strategy.py
│   ├── broker.py
│   ├── portfolio.py
│   ├── engine.py
│   ├── metrics.py
│   └── data.py
├── examples/
│   └── run_sma_crossover.py
├── tests/
│   ├── test_metrics.py
│   └── test_engine.py
├── requirements.txt
├── pyproject.toml
└── README.md
```

## Roadmap

- [ ] CSV / Pandas OHLCV data feed
- [ ] Multi-asset portfolio & correlation-based sizing
- [ ] Walk-forward / parameter sweep harness
- [ ] Live paper-trading adapter (WebSocket)

## License

MIT — free for personal and commercial use.
