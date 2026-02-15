"""Synthetic market data generators for demos and tests.

No external files are required: data is produced from a Geometric Brownian
Motion process so the examples and test-suite run out of the box.
"""
from __future__ import annotations

import numpy as np

from .events import Bar


def generate_gbm(
    symbol: str = "DEMO",
    n: int = 500,
    s0: float = 100.0,
    mu: float = 0.05,
    sigma: float = 0.20,
    dt: float = 1 / 252,
    seed: int = 42,
) -> list[Bar]:
    """Return ``n`` bars following GBM log-returns."""
    rng = np.random.default_rng(seed)
    rets = rng.normal((mu - 0.5 * sigma**2) * dt, sigma * np.sqrt(dt), n)
    prices = s0 * np.exp(np.cumsum(rets))
    bars: list[Bar] = []
    for i, p in enumerate(prices):
        bars.append(
            Bar(
                symbol=symbol,
                timestamp=i,
                open=float(p),
                high=float(p * 1.01),
                low=float(p * 0.99),
                close=float(p),
                volume=1000.0,
            )
        )
    return bars
