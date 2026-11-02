"""
compile_all_pdfs.py — Master PDF compilation script using Tectonic.
Compiles:
1. Elsevier EAAI Research Paper Suite:
   - papers/EAAI_Research_Paper/Anonymized_Manuscript.tex -> Anonymized_Manuscript.pdf
   - papers/EAAI_Research_Paper/Anonymized_Supplementary.tex -> Anonymized_Supplementary.pdf
   - papers/EAAI_Research_Paper/Title_Page.tex -> Title_Page.pdf
   - papers/EAAI_Research_Paper/Cover_Letter_EAAI.tex -> Cover_Letter_EAAI.pdf
   - papers/EAAI_Research_Paper/Highlights.tex -> Highlights.pdf
   - papers/EAAI_Research_Paper/Declaration_of_Generative_AI.tex -> Declaration_of_Generative_AI.pdf
   - papers/EAAI_Research_Paper/Declaration_of_Competing_Interests.tex -> Declaration_of_Competing_Interests.pdf
   - papers/EAAI_Research_Paper/ORCID_Information.tex -> ORCID_Information.pdf
2. University CSE Thesis Monograph:
   - papers/University_CSE_Thesis/main.tex -> main.pdf
"""

import argparse
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

EAAI_TARGETS = [
    {
        "suite": "Elsevier EAAI",
        "name": "EAAI Blinded Main Manuscript (cas-sc)",
        "cwd": BASE_DIR / "papers" / "EAAI_Research_Paper",
        "file": "Anonymized_Manuscript.tex",
        "out_pdf": BASE_DIR / "papers" / "EAAI_Research_Paper" / "Anonymized_Manuscript.pdf"
    },
    {
        "suite": "Elsevier EAAI",
        "name": "EAAI Blinded Supplementary Material",
        "cwd": BASE_DIR / "papers" / "EAAI_Research_Paper",
        "file": "Anonymized_Supplementary.tex",
        "out_pdf": BASE_DIR / "papers" / "EAAI_Research_Paper" / "Anonymized_Supplementary.pdf"
    },
    {
        "suite": "Elsevier EAAI",
        "name": "EAAI Unanonymized Title Page",
        "cwd": BASE_DIR / "papers" / "EAAI_Research_Paper",
        "file": "Title_Page.tex",
        "out_pdf": BASE_DIR / "papers" / "EAAI_Research_Paper" / "Title_Page.pdf"
    },
    {
        "suite": "Elsevier EAAI",
        "name": "EAAI Editorial Cover Letter",
        "cwd": BASE_DIR / "papers" / "EAAI_Research_Paper",
        "file": "Cover_Letter_EAAI.tex",
        "out_pdf": BASE_DIR / "papers" / "EAAI_Research_Paper" / "Cover_Letter_EAAI.pdf"
    },
    {
        "suite": "Elsevier EAAI",
        "name": "EAAI Highlights",
        "cwd": BASE_DIR / "papers" / "EAAI_Research_Paper",
        "file": "Highlights.tex",
        "out_pdf": BASE_DIR / "papers" / "EAAI_Research_Paper" / "Highlights.pdf"
    },
    {
        "suite": "Elsevier EAAI",
        "name": "EAAI Declaration of Generative AI",
        "cwd": BASE_DIR / "papers" / "EAAI_Research_Paper",
        "file": "Declaration_of_Generative_AI.tex",
        "out_pdf": BASE_DIR / "papers" / "EAAI_Research_Paper" / "Declaration_of_Generative_AI.pdf"
    },
    {
        "suite": "Elsevier EAAI",
        "name": "EAAI Declaration of Competing Interests",
        "cwd": BASE_DIR / "papers" / "EAAI_Research_Paper",
        "file": "Declaration_of_Competing_Interests.tex",
        "out_pdf": BASE_DIR / "papers" / "EAAI_Research_Paper" / "Declaration_of_Competing_Interests.pdf"
    },
    {
        "suite": "Elsevier EAAI",
        "name": "EAAI Author ORCID Verification File",
        "cwd": BASE_DIR / "papers" / "EAAI_Research_Paper",
        "file": "ORCID_Information.tex",
        "out_pdf": BASE_DIR / "papers" / "EAAI_Research_Paper" / "ORCID_Information.pdf"
    },
]

THESIS_TARGETS = [
    {
        "suite": "University Thesis",
        "name": "National University CSE Thesis Monograph",
        "cwd": BASE_DIR / "papers" / "University_CSE_Thesis",
        "file": "main.tex",
        "out_pdf": BASE_DIR / "papers" / "University_CSE_Thesis" / "main.pdf"
    }
]

def main():
    parser = argparse.ArgumentParser(description="Compile Intelligent-AML academic publications and thesis.")
    parser.add_argument(
        "--suite",
        choices=["all", "eaai", "thesis"],
        default="all",
        help="Publication suite to compile (default: all)"
    )
    args = parser.parse_args()

    targets = []
    if args.suite in ["all", "eaai"]:
        targets.extend(EAAI_TARGETS)
    if args.suite in ["all", "thesis"]:
        targets.extend(THESIS_TARGETS)

    print("==============================================================================")
    print(f"[*] Starting PDF Compilation with Tectonic ({TECTONIC_EXE.name})")
    print(f"[*] Selected Suite: {args.suite.upper()} ({len(targets)} targets)")
    print("==============================================================================")

    success_count = 0
    for t in targets:
        print(f"\n[+] Compiling: [{t['suite']}] {t['name']}...")
        print(f"   Directory: {t['cwd'].relative_to(BASE_DIR)}")
        print(f"   Source:    {t['file']}")
        
        cmd = [str(TECTONIC_EXE), t["file"]]
        res = subprocess.run(cmd, cwd=str(t["cwd"]), capture_output=True, text=True, encoding="utf-8", errors="replace")
        
        if res.returncode == 0:
            size_kb = t["out_pdf"].stat().st_size / 1024 if t["out_pdf"].exists() else 0
            print(f"   [SUCCESS] -> Generated: {t['out_pdf'].name} ({size_kb:.1f} KB)")
            success_count += 1
        else:
            print(f"   [FAILED] (Exit Code: {res.returncode})")
            print("--- STDERR ---")
            print(res.stderr[:1200])
            print("--- STDOUT ---")
            print(res.stdout[:1200])

        # Automatically clean intermediate LaTeX build artifacts
        for ext in [".aux", ".bbl", ".blg", ".log", ".out", ".abs"]:
            for junk in t["cwd"].glob(f"*{ext}"):
                try:
                    junk.unlink()
                except Exception:
                    pass

    print("\n==============================================================================")
    print(f"[DONE] Compilation Complete: {success_count}/{len(targets)} Documents Successfully Built!")
    print("==============================================================================")

    if success_count < len(targets):
        sys.exit(1)

if __name__ == "__main__":
    main()
