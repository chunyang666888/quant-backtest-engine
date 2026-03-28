import numpy as np

from backtest import metrics


def test_sharpe_positive_for_uptrend():
    r = np.array([0.01, 0.02, 0.015, 0.005, 0.01])
    assert metrics.sharpe_ratio(r) > 0


def test_max_drawdown_at_new_lows():
    eq = np.array([100.0, 120.0, 90.0, 110.0, 80.0])
    # worst peak-to-trough: 80 / 120 - 1 = -33.33%
    assert abs(metrics.max_drawdown(eq) - (-0.3333)) < 0.01


def test_cagr_basic():
    eq = np.array([100.0, 100.0, 100.0, 200.0])
    # 4 bars over 1 "year" -> (2)^(1/4) - 1
    assert abs(metrics.cagr(eq, periods_per_year=1) - (2**0.25 - 1)) < 1e-6


def test_sortino_only_uses_downside():
    r = np.array([0.02, 0.03, -0.01, -0.02, 0.01])
    assert metrics.sortino_ratio(r) > 0
