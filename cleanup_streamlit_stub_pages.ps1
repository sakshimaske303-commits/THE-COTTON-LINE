# cleanup_streamlit_stub_pages.ps1
# Removes every page file that's no longer part of the dashboard:
# (1) the 8 empty placeholder pages left over from the original
#     "climate-resilient Vidarbha" skeleton, before the Entry 1 pivot
#     to THE COTTON LINE -- all 0 bytes, none of them match the
#     project as it actually turned out.
# (2) the first-draft page files, superseded by the leaner 9-page
#     restructure matched against all 7 sibling dashboards (their
#     content is folded into the new files, nothing is lost).
# Run once -- after this, 06_Streamlit/pages should only have the 9
# real, current pages.

$root = "D:\SAKSHI_RESEARCH\SAKSHI_RESEARCH\SAKSHI QGIS\THE_COTTON_LINE\06_Streamlit\pages"

$toDelete = @(
    # pre-pivot stubs
    "$root\01_Study_Area.py",
    "$root\02_Environmental_Dashboard.py",
    "$root\03_Socioeconomic_Dashboard.py",
    "$root\04_Spatial_analysis.py",
    "$root\05_Priority_Ranking.py",
    "$root\06_Intervention_Simulator.py",
    "$root\07_Policy_Recommendations.py",
    "$root\08_Downloads.py",
    # first-draft dashboard pages, superseded by the restructure
    "$root\2_Study_Design.py",
    "$root\3_Data_Methodology.py",
    "$root\4_Cotton_Signature_NDVI.py",
    "$root\5_Agrarian_Land_Structure.py",
    "$root\6_Climate_Controls.py",
    "$root\7_Spatial_Discontinuity_Regression.py",
    "$root\8_Historical_Institutional_Context.py",
    "$root\9_Ground_Truth.py",
    "$root\10_Interactive_Maps.py",
    "$root\11_Findings_Conclusion.py"
)

foreach ($f in $toDelete) {
    if (Test-Path $f) {
        Remove-Item $f -Force
        Write-Host "deleted: $f"
    } else {
        Write-Host "already gone: $f"
    }
}

Write-Host "`nDone. 06_Streamlit/pages now only has the 9 current pages."
