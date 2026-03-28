from backtest.data import generate_gbm
from backtest.engine import BacktestEngine
from backtest.strategy import BuyAndHoldStrategy, SMACrossStrategy


def test_run_produces_metrics():
    bars = generate_gbm("DEMO", n=300, seed=1)
    engine = BacktestEngine(initial_cash=1_000_000)
    res = engine.run(bars, BuyAndHoldStrategy())
    assert res["n_trades"] >= 1
    assert res["final_equity"] > 0
    assert len(res["equity_curve"]) == 300


def test_long_only_no_negative_position():
    bars = generate_gbm("DEMO", n=300, seed=2)
    engine = BacktestEngine(allow_short=False)
    engine.run(bars, SMACrossStrategy(5, 20))
    assert engine.portfolio.position >= -1e-9


def test_allow_short_can_go_negative():
    bars = generate_gbm("DEMO", n=300, seed=3, mu=-0.5)
    engine = BacktestEngine(allow_short=True, risk_fraction=0.9)
    engine.run(bars, SMACrossStrategy(5, 20))
    # strategy should have taken at least one short at some point
    assert any(t.direction == -1 for t in engine.trades)
