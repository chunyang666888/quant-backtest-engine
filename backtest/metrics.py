"""Performance metrics for backtest evaluation.

All functions accept ``numpy`` arrays and return plain ``float`` values so the
results are JSON / tabular friendly.
"""
from __future__ import annotations

import numpy as np


def annualized_return(
    equity_curve: np.ndarray, periods_per_year: int = 252
) -> float:
    equity = np.asarray(equity_curve, dtype=float)
    if equity.size < 2 or equity[0] <= 0:
        return 0.0
    total = equity[-1] / equity[0]
    years = equity.size / periods_per_year
    return float(total ** (1.0 / years) - 1.0)


def sharpe_ratio(
    returns: np.ndarray,
    risk_free: float = 0.0,
    periods_per_year: int = 252,
) -> float:
    r = np.asarray(returns, dtype=float)
    if r.std(ddof=1) == 0:
        return 0.0
    excess = r - risk_free / periods_per_year
    return float(np.sqrt(periods_per_year) * excess.mean() / excess.std(ddof=1))


def sortino_ratio(
    returns: np.ndarray,
    risk_free: float = 0.0,
    periods_per_year: int = 252,
) -> float:
    r = np.asarray(returns, dtype=float)
    excess = r - risk_free / periods_per_year
    downside = excess[excess < 0]
    if downside.size == 0 or downside.std(ddof=1) == 0:
        return 0.0
    return float(np.sqrt(periods_per_year) * excess.mean() / downside.std(ddof=1))


def max_drawdown(equity_curve: np.ndarray) -> float:
    equity = np.asarray(equity_curve, dtype=float)
    running_max = np.maximum.accumulate(equity)
    drawdown = equity / running_max - 1.0
    return float(drawdown.min())


def cagr(equity_curve: np.ndarray, periods_per_year: int = 252) -> float:
    return annualized_return(equity_curve, periods_per_year)
