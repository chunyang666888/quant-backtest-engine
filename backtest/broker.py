"""Simulated broker: fills orders with commission + slippage."""
from __future__ import annotations


class SimulatedBroker:
    def __init__(
        self, commission: float = 0.0005, slippage: float = 0.0005
    ) -> None:
        self.commission = commission  # fraction of notional per trade
        self.slippage = slippage  # fraction added/subtracted to fill price

    def fill_price(self, market_price: float, is_buy: bool) -> float:
        sign = 1 if is_buy else -1
        return market_price * (1 + sign * self.slippage)

    def commission_for(self, quantity: float, price: float) -> float:
        return abs(quantity) * price * self.commission
