"""
compile_all_pdfs.py — Master PDF compilation script using Tectonic.
Compiles:
1. IEEE Research Paper: papers/IEEE_Research_Paper/main.tex -> main.pdf
2. IEEE Supplementary: papers/IEEE_Research_Paper/supplementary.tex -> supplementary.pdf
3. IEEE Cover Letter: papers/IEEE_Research_Paper/Cover_Letter_IEEE_TIFS.tex -> Cover_Letter_IEEE_TIFS.pdf
4. University CSE Thesis: papers/University_CSE_Thesis/main.tex -> main.pdf
"""

import subprocess
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
TECTONIC_EXE = BASE_DIR / "tools" / "tectonic" / "tectonic.exe"

if not TECTONIC_EXE.exists():
    print(f"Error: Tectonic not found at {TECTONIC_EXE}")
    sys.exit(1)

TARGETS = [
    {
        "name": "IEEE Research Paper (Main Manuscript)",
        "cwd": BASE_DIR / "papers" / "IEEE_Research_Paper",
        "file": "main.tex",
        "out_pdf": BASE_DIR / "papers" / "IEEE_Research_Paper" / "main.pdf"
    },
    {
        "name": "IEEE Supplementary Material",
        "cwd": BASE_DIR / "papers" / "IEEE_Research_Paper",
        "file": "supplementary.tex",
        "out_pdf": BASE_DIR / "papers" / "IEEE_Research_Paper" / "supplementary.pdf"
    },
    {
        "name": "IEEE Cover Letter",
        "cwd": BASE_DIR / "papers" / "IEEE_Research_Paper",
        "file": "Cover_Letter_IEEE_TIFS.tex",
        "out_pdf": BASE_DIR / "papers" / "IEEE_Research_Paper" / "Cover_Letter_IEEE_TIFS.pdf"
    },
    {
        "name": "University CSE Thesis Monograph",
        "cwd": BASE_DIR / "papers" / "University_CSE_Thesis",
        "file": "main.tex",
        "out_pdf": BASE_DIR / "papers" / "University_CSE_Thesis" / "main.pdf"
    }
]

print("==============================================================================")
print(f"[*] Starting PDF Compilation with Tectonic ({TECTONIC_EXE.name})")
print("==============================================================================")

success_count = 0
for t in TARGETS:
    print(f"\n[+] Compiling: {t['name']}...")
    print(f"   Directory: {t['cwd']}")
    print(f"   Source:    {t['file']}")
    
    cmd = [str(TECTONIC_EXE), t["file"]]
    res = subprocess.run(cmd, cwd=str(t["cwd"]), capture_output=True, text=True)
    
    if res.returncode == 0:
        size_kb = t["out_pdf"].stat().st_size / 1024 if t["out_pdf"].exists() else 0
        print(f"   [SUCCESS] -> Generated: {t['out_pdf'].name} ({size_kb:.1f} KB)")
        success_count += 1
    else:
        print(f"   [FAILED] (Exit Code: {res.returncode})")
        print("--- STDERR ---")
        print(res.stderr[:1000])
        print("--- STDOUT ---")
        print(res.stdout[:1000])

print("\n==============================================================================")
print(f"[DONE] Compilation Complete: {success_count}/{len(TARGETS)} Documents Successfully Built!")
print("==============================================================================")
