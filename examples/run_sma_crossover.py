"""Run a SMA crossover strategy (and a buy&hold baseline) on synthetic data."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backtest.data import generate_gbm
from backtest.engine import BacktestEngine
from backtest.strategy import BuyAndHoldStrategy, SMACrossStrategy


def main() -> None:
    bars = generate_gbm("DEMO", n=600, seed=7)
    configs = [
        ("SMA(20,50)", SMACrossStrategy(20, 50)),
        ("Buy & Hold", BuyAndHoldStrategy()),
    ]
    for name, strat in configs:
        engine = BacktestEngine(initial_cash=1_000_000)
        res = engine.run(bars, strat)
        print(f"\n=== {name} ===")
        print(f"Final equity : {res['final_equity']:,.2f}")
        print(f"Total return : {res['total_return'] * 100:6.2f}%")
        print(f"CAGR         : {res['cagr'] * 100:6.2f}%")
        print(f"Sharpe       : {res['sharpe']:6.2f}")
        print(f"Sortino      : {res['sortino']:6.2f}")
        print(f"Max Drawdown : {res['max_drawdown'] * 100:6.2f}%")
        print(f"Trades       : {res['n_trades']}")


if __name__ == "__main__":
    main()
