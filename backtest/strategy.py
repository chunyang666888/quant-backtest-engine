"""Strategy interface and reference implementations.

A strategy turns a stream of :class:`Bar` events into a *target signal*:

* ``1``  -> hold long (size = ``risk_fraction`` of equity)
* ``-1`` -> hold short (only if ``allow_short`` is enabled)
* ``0``  -> flat (no exposure)
"""
from __future__ import annotations

from abc import ABC, abstractmethod

from .events import Bar


class Strategy(ABC):
    """Base class. Subclass and implement :meth:`on_bar`."""

    @abstractmethod
    def on_bar(self, bar: Bar) -> int:
        raise NotImplementedError


class BuyAndHoldStrategy(Strategy):
    """Always long. Useful as a benchmark baseline."""

    def on_bar(self, bar: Bar) -> int:
        return 1


class SMACrossStrategy(Strategy):
    """Classic short/long simple-moving-average crossover."""

    def __init__(self, short: int = 10, long: int = 50) -> None:
        self.short = short
        self.long = long
        self._closes: list[float] = []

    def on_bar(self, bar: Bar) -> int:
        self._closes.append(bar.close)
        n = len(self._closes)
        if n < self.long:
            return 0
        s = sum(self._closes[-self.short :]) / self.short
        l = sum(self._closes[-self.long :]) / self.long
        if s > l:
            return 1
        if s < l:
            return -1
        return 0
