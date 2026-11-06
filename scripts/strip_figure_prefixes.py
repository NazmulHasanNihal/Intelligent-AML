import re
from pathlib import Path
import subprocess

scripts_to_fix = [
    ("scripts/redesign_fig7_9_leave_one_out.py", r"Figure 7\.9:\s*"),
    ("scripts/redesign_fig7_15_streaming_latency.py", r"Figure 7\.15:\s*"),
    ("scripts/redesign_fig8_2_sequence_lifeline.py", r"Figure 8\.2:\s*"),
    ("scripts/redesign_fig8_3_cloud_native_k8s.py", r"Figure 8\.3:\s*"),
    ("scripts/redesign_fig9_1_enterprise_lifecycle.py", r"Figure 9\.1:\s*"),
    ("scripts/redesign_fig6_3_forensic_progression.py", r"Figure 6\.3:\s*"),
]

for s_path, pattern in scripts_to_fix:
    p = Path(s_path)
    if not p.exists():
        print(f"Skipping {s_path} (not found)")
        continue
    content = p.read_text(encoding="utf-8")
    
    # Also in fig6_3 replace e3b0 with 9f86d0
    if "fig6_3" in s_path:
        content = content.replace("e3b0c4...", "9f86d0...")
    
    # Strip figure number prefix from string literals
    new_content = re.sub(pattern, "", content)
    p.write_text(new_content, encoding="utf-8")
    print(f"Stripped prefix in {s_path}")

# Also fix glyph in fig9_2 script
p92 = Path("scripts/redesign_fig9_2_regulatory_shields.py")
t92 = p92.read_text(encoding="utf-8")
t92 = t92.replace("Γ(u) ⊆ {0, 1}", "Γ(u) ⊆ {0, 1}").replace("⊆", "in")
t92 = t92.replace("['Arial', 'Helvetica', 'DejaVu Sans']", "['DejaVu Sans', 'Arial', 'Helvetica']")
p92.write_text(t92, encoding="utf-8")
print("Fixed font and symbol in fig9_2!")

