"""
scripts/test_ch5_figures.py
Executes all 7 Chapter 5 scripts and reports status.
"""
import subprocess
import sys
from pathlib import Path

scripts = [
    "fig5_1_operational_workflow.py",
    "fig5_2_conformal_mechanism.py",
    "fig5_3_conformal_conveyor.py",
    "fig5_4_aci_drift_convergence.py",
    "fig5_5_queue_dynamics.py",
    "fig5_6_fairness_audit.py",
    "fig5_7_compliance_alert_funnel.py"
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
    print("\n--- ALL 7 CHAPTER 5 SCRIPTS EXECUTED CLEANLY WITH EXIT CODE 0 ---")
else:
    sys.exit(1)

