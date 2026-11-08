"""
scripts/build_ch3_figures.py
Extracts and builds standalone scripts for all Chapter 3 figures:
- fig3_1_tensor_flow.py
- fig3_2_canonical_invariants.py
- fig3_3_12d_toy_model.py
- fig3_4_triband_decay.py
- fig3_5_triband_spectrum.py
- fig3_6_graphsmote_pipeline.py
- fig3_7_gradient_dynamics.py
- fig3_8_algorithm1_flowchart.py
- fig3_9_canonical_violins.py
- fig3_10_spectral_coldstart.py
"""

import os
from pathlib import Path

OUT_DIR = Path("scripts/figures")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. Figure 3.1
# -----------------------------------------------------------------------------
with open("scripts/redesign_fig3_1_neural_tensor_flow.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("def generate_new_fig3_1():")
body = text[idx:]
body = body.replace("def generate_new_fig3_1():", "def generate():")
body = body.replace('save_to_all(fig, "fig3_1_tensor_flow")', 'save_figure(fig, "fig3_1_tensor_flow", pad_inches=0.15)')
body = body.replace("generate_new_fig3_1()", "generate()")

fig3_1_code = f'''"""
Figure 3.1: End-to-End Architectural Dataflow of C-STGB
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as mlines

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

{body}
'''

with open(OUT_DIR / "fig3_1_tensor_flow.py", "w", encoding="utf-8") as f:
    f.write(fig3_1_code.strip() + "\n")
print("Created fig3_1_tensor_flow.py")

# -----------------------------------------------------------------------------
# 2. Figure 3.2
# -----------------------------------------------------------------------------
with open("scripts/redesign_fig3_2_canonical_invariants.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("def generate_new_fig3_2():")
body = text[idx:]
body = body.replace("def generate_new_fig3_2():", "def generate():")
body = body.replace('save_to_all(fig, "fig_canonical_invariants")', 'save_figure(fig, "fig_canonical_invariants", pad_inches=0.15)')
body = body.replace("generate_new_fig3_2()", "generate()")

fig3_2_code = f'''"""
Figure 3.2: Universal 12-Dimensional Canonical Invariant Space
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

with open(OUT_DIR / "fig3_2_canonical_invariants.py", "w", encoding="utf-8") as f:
    f.write(fig3_2_code.strip() + "\n")
print("Created fig3_2_canonical_invariants.py")

# -----------------------------------------------------------------------------
# 3. Figure 3.3
# -----------------------------------------------------------------------------
with open("scripts/redesign_fig3_3_toy_models.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("def generate_figure_3_3():")
end_idx = text.find("def save_to_all(")
body = text[idx:end_idx]
body = body.replace("def generate_figure_3_3():", "def generate():")
body = body.replace('save_to_all(fig, "fig_12d_toy_model_schematic")', 'save_figure(fig, "fig_12d_toy_model_schematic", pad_inches=0.15)')

fig3_3_code = f'''"""
Figure 3.3: 12-Dimensional Canonical Invariant Physical Toy-Model Schematic
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
    generate()
'''

with open(OUT_DIR / "fig3_3_12d_toy_model.py", "w", encoding="utf-8") as f:
    f.write(fig3_3_code.strip() + "\n")
print("Created fig3_3_12d_toy_model.py")

# -----------------------------------------------------------------------------
# 4. Figure 3.4
# -----------------------------------------------------------------------------
with open("scripts/redesign_fig3_4_triband_decay.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("def generate_fig3_4():")
body = text[idx:]
body = body.replace("def generate_fig3_4():", "def generate():")
body = body.replace('save_to_all(fig, "fig_triband_decay_comparison")', 'save_figure(fig, "fig_triband_decay_comparison", pad_inches=0.15)')
body = body.replace("generate_fig3_4()", "generate()")

fig3_4_code = f'''"""
Figure 3.4: Tri-Band Continuous Harmonic Temporal Decay Comparison
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

{body}
'''

with open(OUT_DIR / "fig3_4_triband_decay.py", "w", encoding="utf-8") as f:
    f.write(fig3_4_code.strip() + "\n")
print("Created fig3_4_triband_decay.py")

# -----------------------------------------------------------------------------
# 5. Figure 3.5
# -----------------------------------------------------------------------------
with open("scripts/redesign_fig3_5_triband_spectrum.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("def generate_fig3_5():")
body = text[idx:]
body = body.replace("def generate_fig3_5():", "def generate():")
body = body.replace('save_to_all(fig, "fig_triband_waveform_spectrum")', 'save_figure(fig, "fig_triband_waveform_spectrum", pad_inches=0.15)')
body = body.replace("generate_fig3_5()", "generate()")

fig3_5_code = f'''"""
Figure 3.5: Tri-Band Multi-Scale Harmonic Attention Spectrum
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

{body}
'''

with open(OUT_DIR / "fig3_5_triband_spectrum.py", "w", encoding="utf-8") as f:
    f.write(fig3_5_code.strip() + "\n")
print("Created fig3_5_triband_spectrum.py")

# -----------------------------------------------------------------------------
# 6. Figure 3.6: GraphSMOTE Pipeline
# -----------------------------------------------------------------------------
with open("scripts/generate_all_publication_figures.py", "r", encoding="utf-8") as f:
    text = f.read()

start_m = "# FIGURE 18: Three-Step Typology-Clustered Latent GraphSMOTE Pipeline"
idx_start = text.find(start_m)
idx_end = text.find('save_all_formats(fig, "fig18_graphsmote_synthesis_pipeline")', idx_start) + len('save_all_formats(fig, "fig18_graphsmote_synthesis_pipeline")')
snippet = text[idx_start:idx_end]
snippet = snippet.replace('save_all_formats(fig, "fig18_graphsmote_synthesis_pipeline")', 'save_figure(fig, "fig18_graphsmote_synthesis_pipeline", pad_inches=0.12)\n    plt.close(fig)')

fig3_6_code = f'''"""
Figure 3.6: Three-Step Typology-Clustered Latent GraphSMOTE Pipeline
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

def generate():
    setup_plt(font_size=8.5, title_size=9.6, label_size=8.5)
    {snippet}

if __name__ == "__main__":
    generate()
'''
with open(OUT_DIR / "fig3_6_graphsmote_pipeline.py", "w", encoding="utf-8") as f:
    f.write(fig3_6_code.strip() + "\n")
print("Created fig3_6_graphsmote_pipeline.py")

# -----------------------------------------------------------------------------
# 7. Figure 3.7: Gradient Dynamics
# -----------------------------------------------------------------------------
with open("scripts/generate_all_8_new_figures.py", "r", encoding="utf-8") as f:
    text = f.read()

idx_start = text.find("def make_fig_3_10():")
idx_end = text.find("def make_fig_4_3():")
snippet = text[idx_start:idx_end]
snippet = snippet.replace("def make_fig_3_10():", "def generate():")
snippet = snippet.replace('save_fig(fig, "fig_3_10_gradient_dynamics")', 'save_figure(fig, "fig_3_10_gradient_dynamics", pad_inches=0.12)')

fig3_7_code = f'''"""
Figure 3.7: Gradient Magnitude Dynamics of Cost-Sensitive Focal Tversky Loss
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
with open(OUT_DIR / "fig3_7_gradient_dynamics.py", "w", encoding="utf-8") as f:
    f.write(fig3_7_code.strip() + "\n")
print("Created fig3_7_gradient_dynamics.py")

# -----------------------------------------------------------------------------
# 8. Figure 3.8: Algorithm 1 Flowchart
# -----------------------------------------------------------------------------
with open("scripts/generate_final_10_of_10_figures.py", "r", encoding="utf-8") as f:
    text = f.read()

start_m = 'print("7. FIXING ALGORITHM 1 FLOWCHART (Fig 3.5) LANE 2 BANNER")'
idx_start = text.find(start_m)
idx_end = text.find('save_fig(fig, "fig_algorithm1_flowchart")', idx_start) + len('save_fig(fig, "fig_algorithm1_flowchart")')
snippet = text[idx_start:idx_end]
snippet = snippet.replace('save_fig(fig, "fig_algorithm1_flowchart")', 'save_figure(fig, "fig_algorithm1_flowchart", pad_inches=0.12)\n    plt.close(fig)')

fig3_8_code = f'''"""
Figure 3.8: C-STGB Dual-Lane Execution Lifecycle: Training and Inference
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

def generate():
    setup_plt(font_size=8.5, title_size=9.5, label_size=8.5)
    {snippet}

if __name__ == "__main__":
    generate()
'''
with open(OUT_DIR / "fig3_8_algorithm1_flowchart.py", "w", encoding="utf-8") as f:
    f.write(fig3_8_code.strip() + "\n")
print("Created fig3_8_algorithm1_flowchart.py")

# -----------------------------------------------------------------------------
# 9. Figure 3.9: Empirical Violins of Canonical Invariants
# -----------------------------------------------------------------------------
with open("scripts/generate_publication_figures_extra.py", "r", encoding="utf-8") as f:
    text = f.read()

start_m = 'print("[8/12] Generating fig_canonical_invariants_empirical...")'
idx_start = text.find(start_m)
idx_end = text.find('save_all(fig, "fig_canonical_invariants_empirical")', idx_start) + len('save_all(fig, "fig_canonical_invariants_empirical")')
snippet = text[idx_start:idx_end]
snippet = snippet.replace('save_all(fig, "fig_canonical_invariants_empirical")', 'save_figure(fig, "fig_canonical_invariants_empirical", pad_inches=0.12)\n    plt.close(fig)')

fig3_9_code = f'''"""
Figure 3.9: Empirical Separability Distributions of Canonical Invariants
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

def generate():
    setup_plt(font_size=8.5, title_size=9.8, label_size=8.5)
    {snippet}

if __name__ == "__main__":
    generate()
'''
with open(OUT_DIR / "fig3_9_canonical_violins.py", "w", encoding="utf-8") as f:
    f.write(fig3_9_code.strip() + "\n")
print("Created fig3_9_canonical_violins.py")

# -----------------------------------------------------------------------------
# 10. Figure 3.10: Spectral Cold-Start Convergence
# -----------------------------------------------------------------------------
with open("scripts/generate_all_publication_figures.py", "r", encoding="utf-8") as f:
    text = f.read()

start_m = "# FIGURE 22: Tri-Band Spectral Attention & Cold-Start Inductive Fusion"
idx_start = text.find(start_m)
idx_end = text.find('save_all_formats(fig, "fig22_triband_spectral_coldstart")', idx_start) + len('save_all_formats(fig, "fig22_triband_spectral_coldstart")')
snippet = text[idx_start:idx_end]
snippet = snippet.replace('save_all_formats(fig, "fig22_triband_spectral_coldstart")', 'save_figure(fig, "fig22_triband_spectral_coldstart", pad_inches=0.12)\n    plt.close(fig)')

# Define colors used in script
fig3_10_code = f'''"""
Figure 3.10: Evidence-Adaptive Gating and Spectral Cold-Start Convergence
Standalone publication script for C-STGB monograph.
"""
import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import setup_plt, save_figure

C_CSTGB = "#dc2626"
C_GCN   = "#475569"
C_HGT   = "#2563eb"

def generate():
    setup_plt(font_size=8.5, title_size=9.5, label_size=8.5)
    {snippet}

if __name__ == "__main__":
    generate()
'''
with open(OUT_DIR / "fig3_10_spectral_coldstart.py", "w", encoding="utf-8") as f:
    f.write(fig3_10_code.strip() + "\n")
print("Created fig3_10_spectral_coldstart.py")

print("\n--- ALL 10 CHAPTER 3 FIGURE SCRIPTS BUILT SUCCESSFULLY ---")

