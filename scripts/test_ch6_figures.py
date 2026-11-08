"""
scripts/test_ch6_figures.py
Executes all 5 Chapter 6 scripts and reports status.
"""
import subprocess
import sys
from pathlib import Path

scripts = [
    "fig6_1_forensic_swarm.py",
    "fig6_2_ast_grammar_pipeline.py",
    "fig6_3_15node_forensic_progression.py",
    "fig6_4_single_alert_timeline.py",
    "fig6_5_merkle_audit_tree.py"
]

all_ok = True
for s in scripts:
    p = Path("scripts/figures") / s
    print(f"Running {s}...")
    res = subprocess.run([sys.executable, str(p)], capture_output=True, text=True)
    if res.returncode == 0:
        last_line = res.stdout.strip().splitlines()[-1] if res.stdout.strip() else 'Success'
        print(f"  [OK] {s}: {last_line}")
    else:
        print(f"  [FAIL] {s}:")
        print("STDOUT:", res.stdout)
        print("STDERR:", res.stderr)
        all_ok = False

if all_ok:
    print("\n--- ALL 5 CHAPTER 6 SCRIPTS EXECUTED CLEANLY WITH EXIT CODE 0 ---")
else:
    sys.exit(1)

