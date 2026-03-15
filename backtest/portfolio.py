"""Portfolio tracks cash, position and marks to market."""
from __future__ import annotations

from .events import Trade


class Portfolio:
    def __init__(self, initial_cash: float = 1_000_000) -> None:
        self.cash = initial_cash
        self.position = 0.0  # signed shares

    def apply_trade(self, trade: Trade) -> None:
        # direction +1 buy, -1 sell; cash impact always subtracts commission.
        self.cash -= trade.direction * trade.quantity * trade.price + trade.commission
        self.position += trade.direction * trade.quantity

    def equity(self, market_price: float) -> float:
        return self.cash + self.position * market_price
