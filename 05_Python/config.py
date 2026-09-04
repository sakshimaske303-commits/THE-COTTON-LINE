# NOTE (added during a repo cleanup pass, September 2026):
#
# This file was scaffolded early in the project as a placeholder for shared
# path/constant configuration, but was never filled in -- the actual scripts
# in this folder (fix_lst_pipeline.py, fix_slope_pipeline.py,
# fix_vegetation_pipeline.py) define their own paths and constants inline
# instead of importing from here.
#
# It is left in the repo empty rather than deleted so the git history stays
# honest about what was and wasn't built. Consolidating this project's full
# raw-to-processed pipeline (population/land-use aggregation, rainfall
# extraction, seasonal NDVI aggregation, Phase 4 dataset assembly, jackknife
# generation) into a single reproducible entry point is tracked as future
# work -- see Section 8 of CL_Research_Paper.md.
