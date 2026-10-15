"""Markdown documents to PDF via headless Chrome/Edge.

    pip install markdown
    python 05_Python/07_export_pdfs.py      (set CHROME=<path> if not found)
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[1]
DOCS = ["CL_Research_Paper.md", "CL_Executive_Summary.md", "CL_Development_Log.md"]
CSS = """
body{font-family:Georgia,'Times New Roman',serif;font-size:10.5pt;line-height:1.45;color:#111;max-width:none;margin:0}
h1{font-size:17pt;line-height:1.25;margin:0 0 6pt}h2{font-size:13pt;margin:16pt 0 4pt;border-bottom:1px solid #ccc}
h3{font-size:11.5pt;margin:12pt 0 3pt}p{margin:4pt 0 6pt;text-align:justify}
table{border-collapse:collapse;font-size:8.6pt;margin:6pt 0;width:100%}th,td{border:1px solid #bbb;padding:3pt 4pt;vertical-align:top}
th{background:#f1f0ec}img{max-width:100%;display:block;margin:8pt auto}code{font-size:8.8pt;background:#f4f4f2;padding:0 2px}
blockquote{border-left:3px solid #bbb;margin:6pt 0;padding:2pt 8pt;color:#444}hr{border:0;border-top:1px solid #ccc}
@page{size:A4;margin:18mm 17mm}
"""


def find_chrome():
    for c in [os.environ.get("CHROME"), shutil.which("chrome"), shutil.which("chromium"), shutil.which("google-chrome"),
              shutil.which("msedge"), r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
              *[str(p) for p in Path("/opt/pw-browsers").glob("chromium-*/chrome-linux/chrome")]]:
        if c and Path(c).exists():
            return c
    sys.exit("Chrome/Chromium/Edge not found; set CHROME=<path>.")


def blank_before_lists(text):
    """Python-Markdown needs a blank line before a list; GitHub does not. Insert one."""
    out, prev = [], ""
    for line in text.splitlines():
        is_item = line.lstrip().startswith(("- ", "* ")) or line.lstrip()[:3].rstrip(". ").isdigit() and ". " in line[:5]
        prev_item = prev.lstrip().startswith(("- ", "* ")) or prev.lstrip()[:3].rstrip(". ").isdigit() and ". " in prev[:5]
        if is_item and prev.strip() and not prev_item and not line.startswith("    "):
            out.append("")
        out.append(line)
        prev = line
    return "\n".join(out)


chrome = find_chrome()
for doc in DOCS:
    src = ROOT / doc
    html = markdown.markdown(blank_before_lists(src.read_text(encoding="utf-8")), extensions=["tables", "fenced_code"])
    tmp = ROOT / (src.stem + "._print.html")
    tmp.write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{html}</body></html>",
                   encoding="utf-8")
    pdf = ROOT / (src.stem + ".pdf")
    subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", tmp.resolve().as_uri()], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    tmp.unlink()
    print("wrote", pdf.name)
