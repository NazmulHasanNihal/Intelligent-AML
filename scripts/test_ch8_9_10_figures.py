"""
scripts/test_ch8_9_10_figures.py
Executes all 8 Chapter 8, 9, 10 & UI scripts and reports status.
"""
import subprocess
import sys
from pathlib import Path

scripts = [
    "fig8_1_system_architecture.py",
    "fig8_2_sequence_lifeline.py",
    "fig8_3_fastapi_k8s_topology.py",
    "fig9_1_enterprise_lifecycle.py",
    "fig9_2_regulatory_shields.py",
    "fig9_3_multibank_split_gnn.py",
    "fig10_1_hyperparam_sensitivity.py",
    "fig10_2_ui_mock_consoles.py"
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
    print("\n--- ALL 8 CHAPTER 8, 9, 10 & UI SCRIPTS EXECUTED CLEANLY WITH EXIT CODE 0 ---")
else:
    sys.exit(1)

