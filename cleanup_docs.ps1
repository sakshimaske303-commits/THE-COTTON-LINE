# cleanup_docs.ps1
# Removes the redundant planning-doc files now that CL_Development_Log.md
# is the only running doc until Project Report / Research Paper / Executive
# Summary get built at the end. Run this from anywhere -- it uses the full
# path so it doesn't matter what folder you're sitting in.

$root = "D:\SAKSHI_RESEARCH\SAKSHI_RESEARCH\SAKSHI QGIS\THE_COTTON_LINE"

$toDelete = @(
    "$root\01_Project _Journal\00_Project_Roadmap.md",
    "$root\01_Project _Journal\01_Project_Log.md",
    "$root\01_Project _Journal\02_Decision_Log.md",
    "$root\08_Documentation\Architecture\PROJECT_ARCHITECTURE.md"
)

foreach ($f in $toDelete) {
    if (Test-Path $f) {
        Remove-Item $f -Force
        Write-Host "deleted: $f"
    } else {
        Write-Host "already gone: $f"
    }
}

Write-Host "`nDone. Only CL_Development_Log.md remains as a running doc."
Write-Host "Project Report / Research Paper / Executive Summary come at the end."
