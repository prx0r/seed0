"""Make the suite CWD-independent: repo root on sys.path regardless of where
pytest is invoked from. (This file exists because the --cwd-independent gate
caught relative sys.path hacks. The gate stays; the hacks go.)"""
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
for _d in (".", "scripts", "idea0", "criteria0"):
    _p = str(root / _d)
    if _p not in sys.path:
        sys.path.insert(0, _p)
