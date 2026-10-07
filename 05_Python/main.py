# NOTE (added during a repo cleanup pass, September 2026):
#
# This file was scaffolded early in the project as a single-command entry
# point, but was never filled in. There is currently no one script that
# reproduces the full raw-to-processed pipeline end to end -- each stage
# (LST/slope/vegetation fixes, population and land-use aggregation, rainfall
# extraction, seasonal NDVI aggregation, Phase 4 dataset assembly, the
# leave-one-out jackknife, figure generation) was run as a separate script
# during development, and not every one of those scripts made it into this
# repository in its final form.
#
# Assembling a single reproducible entry point that runs the complete
# pipeline from raw data to the Phase 4 regression dataset is tracked as
# future work (see Section 7, Future Work, of CL_Research_Paper.md) rather
# than claimed here.
