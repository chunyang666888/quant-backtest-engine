"""Lightweight event-driven backtesting engine for quantitative trading strategies.

Public API::

    from backtest import BacktestEngine, SMACrossStrategy, generate_gbm
    engine = BacktestEngine(initial_cash=1_000_000)
    result = engine.run(generate_gbm("DEMO", n=600), SMACrossStrategy(20, 50))
"""
from .engine import BacktestEngine
from .metrics import (
    annualized_return,
    cagr,
    max_drawdown,
    sharpe_ratio,
    sortino_ratio,
)
from .strategy import BuyAndHoldStrategy, SMACrossStrategy, Strategy
from .data import generate_gbm
from .events import Bar, Trade

__all__ = [
    "BacktestEngine",
    "sharpe_ratio",
    "sortino_ratio",
    "max_drawdown",
    "cagr",
    "annualized_return",
    "Strategy",
    "SMACrossStrategy",
    "BuyAndHoldStrategy",
    "generate_gbm",
    "Bar",
    "Trade",
]
