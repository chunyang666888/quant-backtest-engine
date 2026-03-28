import os
import sys

# Make the top-level `backtest` package importable when running pytest.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
