import subprocess
import sys

scripts = [
    "scripts/redesign_fig6_3_forensic_progression.py",
    "scripts/redesign_fig7_9_leave_one_out.py",
    "scripts/redesign_fig7_15_streaming_latency.py",
    "scripts/redesign_fig8_2_sequence_lifeline.py",
    "scripts/redesign_fig8_3_cloud_native_k8s.py",
    "scripts/redesign_fig9_1_enterprise_lifecycle.py",
    "scripts/redesign_fig9_2_regulatory_shields.py"
]

for s in scripts:
    print(f"Running {s}...")
    res = subprocess.run([sys.executable, s], capture_output=True, text=True)
    if res.returncode == 0:
        print(f"SUCCESS: {s}")
    else:
        print(f"FAILED: {s}\n{res.stderr}")

print("Batch figure execution complete!")

