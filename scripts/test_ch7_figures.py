"""
scripts/test_ch7_figures.py
Executes all 17 Chapter 7 scripts and reports status.
"""
import subprocess
import sys
from pathlib import Path

scripts = [
    "fig7_1_class_imbalance_log.py",
    "fig7_2_temporal_split.py",
    "fig7_3_champion_delta.py",
    "fig7_4_critical_difference.py",
    "fig7_5_radar_benchmark.py",
    "fig7_6_pr_roc_curves.py",
    "fig7_7_ablation_component_study.py",
    "fig7_8_ablation_waterfall.py",
    "fig7_9_leave_one_out_impact.py",
    "fig7_10_invariant_tornado.py",
    "fig7_11_camouflage_robustness.py",
    "fig7_12_edge_gate_distribution.py",
    "fig7_13_tsne_manifold.py",
    "fig7_14_zero_shot_heatmap.py",
    "fig7_15_streaming_latency_waterfall.py",
    "fig7_16_fastpath_latency_comparison.py",
    "fig7_17_all_datasets_pr_curves.py"
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
    print("\n--- ALL 17 CHAPTER 7 SCRIPTS EXECUTED CLEANLY WITH EXIT CODE 0 ---")
else:
    sys.exit(1)

