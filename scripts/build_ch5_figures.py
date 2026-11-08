"""
scripts/build_ch5_figures.py
Extracts and builds standalone scripts for all Chapter 5 figures:
- fig5_1_operational_workflow.py
- fig5_2_conformal_mechanism.py
- fig5_3_conformal_conveyor.py
- fig5_4_aci_drift_convergence.py
- fig5_5_queue_dynamics.py
- fig5_6_fairness_audit.py
- fig5_7_compliance_alert_funnel.py
"""

import os
from pathlib import Path

OUT_DIR = Path("scripts/figures")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. Figure 5.1: Operational Workflow
# -----------------------------------------------------------------------------
with open("scripts/patch_vector_figures_text.py", "r", encoding="utf-8") as f:
    text = f.read()

idx_start = text.find("def patch_operational_workflow():")
idx_end = text.find("def patch_system_architecture():")
snippet = text[idx_start:idx_end]
snippet = snippet.replace("def patch_operational_workflow():", "def generate():")

fig5_1_code = f'''"""
Figure 5.1: Fast-Path Latency Workflow and Selective Triage
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
with open(OUT_DIR / "fig5_1_operational_workflow.py", "w", encoding="utf-8") as f:
    f.write(fig5_1_code.strip() + "\n")
print("Created fig5_1_operational_workflow.py")

# -----------------------------------------------------------------------------
# 2. Figure 5.2: Conformal Risk Mechanism
# -----------------------------------------------------------------------------
with open("scripts/redesign_fig5_2_conformal_mechanism.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("def generate_figure_5_2():")
body = text[idx:]
body = body.replace("def generate_figure_5_2():", "def generate():")
body = body.replace('generate_figure_5_2()', 'generate()')
# Replace save loop with save_figure
idx_save = body.find("for d in TARGET_DIRS:")
body = body[:idx_save] + 'save_figure(fig, "fig19_conformal_risk_mechanism", pad_inches=0.15)\n    save_figure(fig, "fig_conformal_mechanism_proof", pad_inches=0.15)\n    plt.close(fig)\n\nif __name__ == "__main__":\n    generate()\n'

fig5_2_code = f'''"""
Figure 5.2: Class-Conditional Conformal Calibration Mechanism
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
with open(OUT_DIR / "fig5_2_conformal_mechanism.py", "w", encoding="utf-8") as f:
    f.write(fig5_2_code.strip() + "\n")
print("Created fig5_2_conformal_mechanism.py")

# -----------------------------------------------------------------------------
# 3. Figure 5.3: Conformal Conveyor Funnel
# -----------------------------------------------------------------------------
with open("scripts/redesign_fig5_3_conformal_conveyor.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("def generate_figure_5_3():")
body = text[idx:]
body = body.replace("def generate_figure_5_3():", "def generate():")
idx_save = body.find("for d in TARGET_DIRS:")
body = body[:idx_save] + 'save_figure(fig, "fig_conformal_conveyor_funnel", pad_inches=0.15)\n    plt.close(fig)\n\nif __name__ == "__main__":\n    generate()\n'

fig5_3_code = f'''"""
Figure 5.3: 3-Tier Conformal Risk Control Triage Conveyor Funnel
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

{body}
'''
with open(OUT_DIR / "fig5_3_conformal_conveyor.py", "w", encoding="utf-8") as f:
    f.write(fig5_3_code.strip() + "\n")
print("Created fig5_3_conformal_conveyor.py")

# -----------------------------------------------------------------------------
# 4. Figure 5.4: ACI Drift Convergence
# -----------------------------------------------------------------------------
with open("scripts/generate_all_8_new_figures.py", "r", encoding="utf-8") as f:
    text = f.read()

idx_start = text.find("def make_fig_5_6():")
idx_end = text.find("def make_fig_5_7():")
snippet = text[idx_start:idx_end]
snippet = snippet.replace("def make_fig_5_6():", "def generate():")
snippet = snippet.replace('save_fig(fig, "fig_5_6_aci_drift_convergence")', 'save_figure(fig, "fig_5_6_aci_drift_convergence", pad_inches=0.12)')

fig5_4_code = f'''"""
Figure 5.4: Empirical Illicit Coverage under Non-Stationary Concept Drift
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

{snippet}

if __name__ == "__main__":
    generate()
'''
with open(OUT_DIR / "fig5_4_aci_drift_convergence.py", "w", encoding="utf-8") as f:
    f.write(fig5_4_code.strip() + "\n")
print("Created fig5_4_aci_drift_convergence.py")

# -----------------------------------------------------------------------------
# 5. Figure 5.5: Queue Dynamics
# -----------------------------------------------------------------------------
with open("scripts/generate_final_10_of_10_figures.py", "r", encoding="utf-8") as f:
    text = f.read()

start_m = 'print("4. FIXING FIGURE 5.4: CONFORMAL RISK VS AUTOMATION & COVERAGE")'
idx_start = text.find(start_m)
idx_end = text.find('save_fig(fig, ["fig_conformal_coverage_reliability", "fig4_conformal_queue_dynamics"])', idx_start) + len('save_fig(fig, ["fig_conformal_coverage_reliability", "fig4_conformal_queue_dynamics"])')
snippet = text[idx_start:idx_end]
snippet = snippet.replace('save_fig(fig, ["fig_conformal_coverage_reliability", "fig4_conformal_queue_dynamics"])', 'save_figure(fig, "fig4_conformal_queue_dynamics", pad_inches=0.12)\n    save_figure(fig, "fig_conformal_coverage_reliability", pad_inches=0.12)\n    plt.close(fig)')

# Ensure snippet is indented inside def generate()
snippet_indented = "\n".join("    " + line for line in snippet.splitlines())

fig5_5_code = f'''"""
Figure 5.5: Empirical Verification of 3-Tier Conformal Risk Control
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
with open(OUT_DIR / "fig5_5_queue_dynamics.py", "w", encoding="utf-8") as f:
    f.write(fig5_5_code.strip() + "\n")
print("Created fig5_5_queue_dynamics.py")

# -----------------------------------------------------------------------------
# 6. Figure 5.6: Fairness Audit
# -----------------------------------------------------------------------------
with open("scripts/generate_all_8_new_figures.py", "r", encoding="utf-8") as f:
    text = f.read()

idx_start = text.find("def make_fig_5_7():")
idx_end = text.find("def make_fig_6_5():")
snippet = text[idx_start:idx_end]
snippet = snippet.replace("def make_fig_5_7():", "def generate():")
snippet = snippet.replace('save_fig(fig, "fig_5_7_fairness_audit")', 'save_figure(fig, "fig_5_7_fairness_audit", pad_inches=0.12)')

fig5_6_code = f'''"""
Figure 5.6: Algorithmic Fairness and Non-Discrimination Audit
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

{snippet}

if __name__ == "__main__":
    generate()
'''
with open(OUT_DIR / "fig5_6_fairness_audit.py", "w", encoding="utf-8") as f:
    f.write(fig5_6_code.strip() + "\n")
print("Created fig5_6_fairness_audit.py")

# -----------------------------------------------------------------------------
# 7. Figure 5.7: Compliance Alert Funnel
# -----------------------------------------------------------------------------
with open("scripts/redesign_fig5_5_compliance_funnel.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("def generate_figure_5_5():")
body = text[idx:]
body = body.replace("def generate_figure_5_5():", "def generate():")
idx_save = body.find("for d in TARGET_DIRS:")
body = body[:idx_save] + 'save_figure(fig, "fig_compliance_alert_funnel", pad_inches=0.15)\n    plt.close(fig)\n\nif __name__ == "__main__":\n    generate()\n'

fig5_7_code = f'''"""
Figure 5.7: Operational Compliance Triage Funnel and Workload Reduction
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

{body}
'''
with open(OUT_DIR / "fig5_7_compliance_alert_funnel.py", "w", encoding="utf-8") as f:
    f.write(fig5_7_code.strip() + "\n")
print("Created fig5_7_compliance_alert_funnel.py")

print("\n--- ALL 7 CHAPTER 5 FIGURE SCRIPTS BUILT SUCCESSFULLY ---")

