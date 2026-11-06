import sys
import os
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

print("=== REGENERATING ALL AUDITED FIGURES ===")

scripts_to_run = [
    "scripts/redesign_fig1_2_and_fig2_1.py",
    "scripts/redesign_fig2_2_evolution_frontier.py",
    "scripts/redesign_fig5_2_conformal_mechanism.py",
    "scripts/redesign_fig7_7_ablation_progression.py",
    "scripts/redesign_fig7_9_leave_one_out.py",
    "scripts/redesign_fig7_15_streaming_latency.py",
    "scripts/redesign_fig8_2_sequence_lifeline.py",
    "scripts/redesign_fig8_3_cloud_native_k8s.py",
    "scripts/redesign_fig9_1_enterprise_lifecycle.py",
    "scripts/generate_publication_figures_extra.py",
    "scripts/generate_final_10_of_10_figures.py",
    "scripts/generate_all_publication_figures.py",
]

for script in scripts_to_run:
    print(f"\n--- Running: {script} ---")
    res = subprocess.run([sys.executable, script], cwd=str(REPO_ROOT), capture_output=True, text=True, encoding="utf-8", errors="ignore")
    if res.returncode != 0:
        print(f"FAILED {script}:\n{res.stderr}\n{res.stdout}")
        sys.exit(1)
    else:
        # print first few and last few lines
        lines = res.stdout.strip().splitlines()
        for l in lines[:3]:
            print(f"  {l}")
        if len(lines) > 6:
            print("  ...")
        for l in lines[-3:]:
            print(f"  {l}")
        print(f"  [SUCCESS] {script}")

print("\n=== ALL AUDITED FIGURES REGENERATED SUCCESSFULLY ===")

