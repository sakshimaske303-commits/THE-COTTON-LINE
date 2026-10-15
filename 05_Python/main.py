"""Use run_all.py:

    python 05_Python/run_all.py
    python 05_Python/run_all.py --full
"""
import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).with_name("run_all.py")), run_name="__main__")
