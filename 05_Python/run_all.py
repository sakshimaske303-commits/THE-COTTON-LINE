"""Rebuild every table, result and figure.

    python 05_Python/run_all.py          # from the processed data in the repository
    python 05_Python/run_all.py --full   # plus the 30 m masked rebuild from raw scenes

Steps that read 02_Data_Raw/ run only when that raw data is present; otherwise the
processed tables already in the repository are used.
"""
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RAW = HERE.parent / "02_Data_Raw"
steps = ["01_build_taluka_geometry.py"]
if any((RAW / "Population").glob("*.zip")):
    steps += ["02_build_census_stats.py"]
steps += ["03_build_eo_climate_stats.py"]
if "--full" in sys.argv:
    steps += ["03b_build_eo_30m_masked.py"]
if (RAW / "Terrain").exists():
    steps += ["03c_sample_elevation.py"]
steps += ["04_build_analysis_dataset.py", "robustness_checks.py", "05_make_figures.py", "06_make_interactive.py",
          "08_field_bridge.py"]
for s in steps:
    print(f"\n===== {s}")
    r = subprocess.run([sys.executable, str(HERE / s)], cwd=HERE)
    if r.returncode:
        sys.exit(f"{s} failed")
print("\nAll steps finished.")
