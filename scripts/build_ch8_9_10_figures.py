"""
scripts/build_ch8_9_10_figures.py
Extracts and builds standalone scripts for Chapters 8, 9, 10 & UI (8 scripts).
"""

import os
from pathlib import Path

OUT_DIR = Path("scripts/figures")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. Figure 8.1: System Architecture
# -----------------------------------------------------------------------------
with open("scripts/patch_vector_figures_text.py", "r", encoding="utf-8") as f:
    text_patch = f.read()

idx_start = text_patch.find("def patch_system_architecture():")
snippet = text_patch[idx_start:]
snippet = snippet.replace("def patch_system_architecture():", "def generate():")

fig8_1_code = f'''"""
Figure 8.1: System Architecture of Intelligent-AML Production Serving
Standalone publication script for C-STGB monograph.
"""
import sys
import fitz
from pathlib import Path
import shutil

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import TARGET_DIRS

{snippet}

if __name__ == "__main__":
    generate()
'''
with open(OUT_DIR / "fig8_1_system_architecture.py", "w", encoding="utf-8") as f:
    f.write(fig8_1_code.strip() + "\n")
print("Created fig8_1_system_architecture.py")

# -----------------------------------------------------------------------------
# 2. Figure 8.2: Sequence Lifeline
# -----------------------------------------------------------------------------
with open("scripts/redesign_fig8_2_sequence_lifeline.py", "r", encoding="utf-8") as f:
    text_8_2 = f.read()

idx = text_8_2.find("def generate_figure_8_2():")
end_idx = text_8_2.find('if __name__ == "__main__":')
body = text_8_2[idx:end_idx]
body = body.replace("def generate_figure_8_2():", "def generate():")

fig8_2_code = f'''"""
Figure 8.2: Real-Time Operational UML Sequence Lifeline
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

{body}

if __name__ == "__main__":
    fig = generate()
    save_figure(fig, "fig8_2_uml_sequence_lifeline", pad_inches=0.10)
    plt.close(fig)
'''
with open(OUT_DIR / "fig8_2_sequence_lifeline.py", "w", encoding="utf-8") as f:
    f.write(fig8_2_code.strip() + "\n")
print("Created fig8_2_sequence_lifeline.py")

# -----------------------------------------------------------------------------
# 3. Figure 8.3: FastAPI K8s Topology
# -----------------------------------------------------------------------------
with open("scripts/redesign_fig8_3_cloud_native_k8s.py", "r", encoding="utf-8") as f:
    text_8_3 = f.read()

idx = text_8_3.find("def generate_figure_8_3():")
end_idx = text_8_3.find('if __name__ == "__main__":')
body = text_8_3[idx:end_idx]
body = body.replace("def generate_figure_8_3():", "def generate():")

fig8_3_code = f'''"""
Figure 8.3: Enterprise Cloud-Native Deployment Topology and Kubernetes Orchestration
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

{body}

if __name__ == "__main__":
    fig = generate()
    save_figure(fig, "fig8_1_fastapi_k8s_topology", pad_inches=0.10)
    save_figure(fig, "fig8_3_cloud_native_k8s", pad_inches=0.10)
    plt.close(fig)
'''
with open(OUT_DIR / "fig8_3_fastapi_k8s_topology.py", "w", encoding="utf-8") as f:
    f.write(fig8_3_code.strip() + "\n")
print("Created fig8_3_fastapi_k8s_topology.py")

# -----------------------------------------------------------------------------
# 4. Figure 9.1: Enterprise Deployment Lifecycle
# -----------------------------------------------------------------------------
with open("scripts/redesign_fig9_1_enterprise_lifecycle.py", "r", encoding="utf-8") as f:
    text_9_1 = f.read()

idx = text_9_1.find("def generate_figure_9_1():")
end_idx = text_9_1.find('if __name__ == "__main__":')
body = text_9_1[idx:end_idx]
body = body.replace("def generate_figure_9_1():", "def generate():")

fig9_1_code = f'''"""
Figure 9.1: Enterprise Production Deployment Lifecycle for Tier-1 Banking Infrastructure
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

{body}

if __name__ == "__main__":
    fig = generate()
    save_figure(fig, "fig_enterprise_deployment_lifecycle", pad_inches=0.10)
    save_figure(fig, "fig_26week_roadmap_gantt", pad_inches=0.10)
    plt.close(fig)
'''
with open(OUT_DIR / "fig9_1_enterprise_lifecycle.py", "w", encoding="utf-8") as f:
    f.write(fig9_1_code.strip() + "\n")
print("Created fig9_1_enterprise_lifecycle.py")

# -----------------------------------------------------------------------------
# 5. Figure 9.2: Regulatory Shields
# -----------------------------------------------------------------------------
with open("scripts/redesign_fig9_2_regulatory_shields.py", "r", encoding="utf-8") as f:
    text_9_2 = f.read()

idx = text_9_2.find("def generate_fig9_2():")
body = text_9_2[idx:]
body = body.replace("def generate_fig9_2():", "def generate():")
idx_save = body.find("for d in TARGET_DIRS:")
body = body[:idx_save] + 'save_figure(fig, "fig_regulatory_shields", pad_inches=0.10)\n    plt.close(fig)\n\nif __name__ == "__main__":\n    generate()\n'

fig9_2_code = f'''"""
Figure 9.2: 5-Pillar Global Regulatory Compliance Shield Infographic
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

{body}
'''
with open(OUT_DIR / "fig9_2_regulatory_shields.py", "w", encoding="utf-8") as f:
    f.write(fig9_2_code.strip() + "\n")
print("Created fig9_2_regulatory_shields.py")

# -----------------------------------------------------------------------------
# 6. Figure 9.3: Multi-Bank Split-GNN
# -----------------------------------------------------------------------------
with open("scripts/generate_all_8_new_figures.py", "r", encoding="utf-8") as f:
    text_8new = f.read()

idx_start = text_8new.find("def make_fig_9_3():")
idx_end = text_8new.find('if __name__ == "__main__":')
snippet = text_8new[idx_start:idx_end]
snippet = snippet.replace("def make_fig_9_3():", "def generate():")
snippet = snippet.replace('save_fig(fig, "fig_9_3_multibank_split_gnn")', 'save_figure(fig, "fig_9_3_multibank_split_gnn", pad_inches=0.12)')

fig9_3_code = f'''"""
Figure 9.3: Multi-Bank Blind Spot vs. Privacy-Preserving Federated Split-GNN
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

{snippet}

if __name__ == "__main__":
    generate()
'''
with open(OUT_DIR / "fig9_3_multibank_split_gnn.py", "w", encoding="utf-8") as f:
    f.write(fig9_3_code.strip() + "\n")
print("Created fig9_3_multibank_split_gnn.py")

# -----------------------------------------------------------------------------
# 7. Figure 10.1: Hyperparameter Sensitivity
# -----------------------------------------------------------------------------
with open("scripts/generate_final_10_of_10_figures.py", "r", encoding="utf-8") as f:
    text_f10 = f.read()

start_m = 'print("12. GENERATING 4-PANEL HYPERPARAMETER SENSITIVITY CURVES (Appendix C.1)")'
idx_start = text_f10.find(start_m)
idx_end = text_f10.find('save_fig(fig, "fig_hyperparam_sensitivity_4panel")', idx_start) + len('save_fig(fig, "fig_hyperparam_sensitivity_4panel")')
snippet = text_f10[idx_start:idx_end]
snippet = snippet.replace('save_fig(fig, "fig_hyperparam_sensitivity_4panel")', 'save_figure(fig, "fig_hyperparam_sensitivity_4panel", pad_inches=0.12)\n    plt.close(fig)')
snippet_indented = "\n".join("    " + l for l in snippet.splitlines())

fig10_1_code = f'''"""
Figure 10.1: Four-Panel Hyperparameter Sensitivity Analysis
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

def generate():
    setup_plt(font_size=8.5, title_size=9.2, label_size=8.5)
{snippet_indented}

if __name__ == "__main__":
    generate()
'''
with open(OUT_DIR / "fig10_1_hyperparam_sensitivity.py", "w", encoding="utf-8") as f:
    f.write(fig10_1_code.strip() + "\n")
print("Created fig10_1_hyperparam_sensitivity.py")

# -----------------------------------------------------------------------------
# 8. Figure 10.2: UI Mock Consoles
# -----------------------------------------------------------------------------
fig10_2_code = '''"""
Figure 10.2: Verification and Synchronization of UI Mock Consoles
Standalone publication script for C-STGB monograph.
Synchronizes and verifies all 6 UI console PNG files across all 5 directories:
1. 01_surveillance_desk.png
2. 02_network_topology.png
3. 03_case_management.png
4. 04_case_detail_four_eyes.png
5. 05_multi_agent_sar.png
6. 06_model_governance_drift.png
"""
import sys
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import TARGET_DIRS

UI_FILES = [
    "01_surveillance_desk.png",
    "02_network_topology.png",
    "03_case_management.png",
    "04_case_detail_four_eyes.png",
    "05_multi_agent_sar.png",
    "06_model_governance_drift.png"
]

def generate():
    # Source is papers/University_CSE_Thesis/figures
    src_dir = TARGET_DIRS[0]
    print(f"Checking and synchronizing {len(UI_FILES)} UI console screenshots...")
    
    for f in UI_FILES:
        src = src_dir / f
        if not src.exists():
            print(f"  [WARN] Source file missing: {src}")
            continue
        for d in TARGET_DIRS[1:]:
            d.mkdir(parents=True, exist_ok=True)
            dst = d / f
            if not dst.exists() or src.stat().st_size != dst.stat().st_size:
                shutil.copyfile(src, dst)
        print(f"  [OK] Synchronized {f} across all 5 directories.")

if __name__ == "__main__":
    generate()
'''
with open(OUT_DIR / "fig10_2_ui_mock_consoles.py", "w", encoding="utf-8") as f:
    f.write(fig10_2_code.strip() + "\n")
print("Created fig10_2_ui_mock_consoles.py")

print("\n--- ALL 8 CHAPTER 8, 9, 10 & UI SCRIPTS BUILT SUCCESSFULLY ---")

