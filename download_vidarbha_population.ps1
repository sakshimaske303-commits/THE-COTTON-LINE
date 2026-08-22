# Downloads village-level Census shapefiles (IIT Bombay POCRA portal) for all 11 Vidarbha districts
# Run this from PowerShell. Saves into 02_Data_Raw\Population\

$dest = "D:\SAKSHI_RESEARCH\SAKSHI_RESEARCH\SAKSHI QGIS\THE_COTTON_LINE\02_Data_Raw\Population"
New-Item -ItemType Directory -Force -Path $dest | Out-Null

$base = "https://www.cse.iitb.ac.in/~pocra/MahaCensus_shapefile_data1.1/Shape_File_3July"
$districts = @("nagpur","wardha","bhandara","gondia","chandrapur","gadchiroli","amravati","akola","yavatmal","buldhana","washim")

foreach ($d in $districts) {
    $url = "$base/$d.zip"
    $out = Join-Path $dest "$d.zip"
    Write-Host "Downloading $d..."
    try {
        Invoke-WebRequest -Uri $url -OutFile $out -UseBasicParsing
        Write-Host "  OK -> $out"
    } catch {
        Write-Host "  FAILED: $_"
    }
}

Write-Host "`nDone. Each zip contains a village-level shapefile with 600+ census attributes (population, literacy, sex ratio, etc.)."
