"""Event-driven backtest engine tying strategy, broker and portfolio together.

The engine walks a bar stream, asks the strategy for a target signal, then
rebalances the portfolio toward that signal using the simulated broker. Equity
is marked to market every bar and summary metrics are produced at the end.
"""
from __future__ import annotations

import numpy as np

from .broker import SimulatedBroker
from .events import Bar, Trade
from .portfolio import Portfolio
from .strategy import Strategy
from . import metrics


class BacktestEngine:
    def __init__(
        self,
        initial_cash: float = 1_000_000,
        commission: float = 0.0005,
        slippage: float = 0.0005,
        risk_fraction: float = 0.95,
        allow_short: bool = False,
    ) -> None:
        self.initial_cash = initial_cash
        self.broker = SimulatedBroker(commission, slippage)
        self.risk_fraction = risk_fraction
        self.allow_short = allow_short
        self.portfolio = Portfolio(initial_cash)
        self.trades: list[Trade] = []
        self.equity_curve: list[float] = []

    def run(self, bars: list[Bar], strategy: Strategy) -> dict:
        for bar in bars:
            signal = strategy.on_bar(bar)
            self._rebalance(bar, signal)
            self.equity_curve.append(self.portfolio.equity(bar.close))
        return self.results()

    def _rebalance(self, bar: Bar, signal: int) -> None:
        equity = self.portfolio.equity(bar.close)
        target_value = signal * self.risk_fraction * equity
        if not self.allow_short and target_value < 0:
            target_value = 0.0
        target_shares = target_value / bar.close if bar.close > 0 else 0.0
        delta = target_shares - self.portfolio.position
        if abs(delta) < 1e-9:
            return
        is_buy = delta > 0
        fill = self.broker.fill_price(bar.close, is_buy)
        commission = self.broker.commission_for(abs(delta), fill)
        trade = Trade(
            symbol=bar.symbol,
            timestamp=bar.timestamp,
            direction=1 if is_buy else -1,
            quantity=abs(delta),
            price=fill,
            commission=commission,
        )
        self.portfolio.apply_trade(trade)
        self.trades.append(trade)

    def results(self) -> dict:
        eq = np.array(self.equity_curve, dtype=float)
        if eq.size == 0:
            return {}
        rets = np.diff(eq) / eq[:-1]
        return {
            "final_equity": float(eq[-1]),
            "total_return": float(eq[-1] / eq[0] - 1),
            "cagr": metrics.cagr(eq),
            "sharpe": metrics.sharpe_ratio(rets),
            "sortino": metrics.sortino_ratio(rets),
            "max_drawdown": metrics.max_drawdown(eq),
            "n_trades": len(self.trades),
            "equity_curve": eq,
        }
