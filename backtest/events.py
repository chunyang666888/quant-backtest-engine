"""Core data structures passed between engine components."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class Bar:
    """A single OHLCV bar for one instrument."""

    symbol: str
    timestamp: Any
    open: float = 0.0
    high: float = 0.0
    low: float = 0.0
    close: float = 0.0
    volume: float = 0.0


@dataclass
class Trade:
    """A simulated, already-executed trade (post broker fill)."""

    symbol: str
    timestamp: Any
    direction: int  # +1 buy, -1 sell
    quantity: float  # always positive; sign lives in `direction`
    price: float
    commission: float
