"""
scripts/test_ch3_figures.py
Executes all 10 Chapter 3 scripts and reports status.
"""
import subprocess
import sys
from pathlib import Path

scripts = [
    "fig3_1_tensor_flow.py",
    "fig3_2_canonical_invariants.py",
    "fig3_3_12d_toy_model.py",
    "fig3_4_triband_decay.py",
    "fig3_5_triband_spectrum.py",
    "fig3_6_graphsmote_pipeline.py",
    "fig3_7_gradient_dynamics.py",
    "fig3_8_algorithm1_flowchart.py",
    "fig3_9_canonical_violins.py",
    "fig3_10_spectral_coldstart.py"
]

all_ok = True
for s in scripts:
    p = Path("scripts/figures") / s
    print(f"Running {s}...")
    res = subprocess.run([sys.executable, str(p)], capture_output=True, text=True)
    if res.returncode == 0:
        print(f"  [OK] {s}: {res.stdout.strip().splitlines()[-1] if res.stdout else 'Success'}")
    else:
        print(f"  [FAIL] {s}:")
        print("STDOUT:", res.stdout)
        print("STDERR:", res.stderr)
        all_ok = False

if all_ok:
    print("\n--- ALL 10 CHAPTER 3 SCRIPTS EXECUTED CLEANLY WITH EXIT CODE 0 ---")
else:
    sys.exit(1)

