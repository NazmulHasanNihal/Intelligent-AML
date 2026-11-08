"""
scripts/build_ch6_figures.py
Extracts and builds standalone scripts for all Chapter 6 figures:
- fig6_1_forensic_swarm.py
- fig6_2_ast_grammar_pipeline.py
- fig6_3_15node_forensic_progression.py
- fig6_4_single_alert_timeline.py
- fig6_5_merkle_audit_tree.py
"""

import os
from pathlib import Path

OUT_DIR = Path("scripts/figures")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. Figure 6.1: Forensic Swarm
# -----------------------------------------------------------------------------
with open("scripts/redesign_fig6_1_forensic_swarm.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("def generate_figure():")
end_idx = text.find("def main():")
body = text[idx:end_idx]
body = body.replace("def generate_figure():", "def generate():")

fig6_1_code = f'''"""
Figure 6.1: Multi-Agent Forensic Reasoning and Dual-Governance Pipeline
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

if __name__ == "__main__":
    fig = generate()
    save_figure(fig, "fig_forensic_swarm", pad_inches=0.10)
    save_figure(fig, "fig20_multi_agent_forensic_swarm", pad_inches=0.10)
    plt.close(fig)
'''
with open(OUT_DIR / "fig6_1_forensic_swarm.py", "w", encoding="utf-8") as f:
    f.write(fig6_1_code.strip() + "\n")
print("Created fig6_1_forensic_swarm.py")

# -----------------------------------------------------------------------------
# 2. Figure 6.2: AST Grammar Pipeline
# -----------------------------------------------------------------------------
with open("scripts/redesign_fig6_2_ast_grammar.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("def generate_figure():")
end_idx = text.find("def main():")
body = text[idx:end_idx]
body = body.replace("def generate_figure():", "def generate():")

fig6_2_code = f'''"""
Figure 6.2: AST Grammar Compiler and Anti-Hallucination SAR Pipeline
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

if __name__ == "__main__":
    fig = generate()
    save_figure(fig, "fig_ast_grammar_pipeline", pad_inches=0.10)
    plt.close(fig)
'''
with open(OUT_DIR / "fig6_2_ast_grammar_pipeline.py", "w", encoding="utf-8") as f:
    f.write(fig6_2_code.strip() + "\n")
print("Created fig6_2_ast_grammar_pipeline.py")

# -----------------------------------------------------------------------------
# 3. Figure 6.3: 15-Node Forensic Progression
# -----------------------------------------------------------------------------
with open("scripts/redesign_fig6_3_forensic_progression.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("def generate_figure_6_3():")
body = text[idx:]
body = body.replace("def generate_figure_6_3():", "def generate():")
idx_save = body.find("for d in TARGET_DIRS:")
body = body[:idx_save] + 'save_figure(fig, "fig_15node_forensic_progression", pad_inches=0.15)\n    save_figure(fig, "15_node_subgraph", pad_inches=0.15)\n    plt.close(fig)\n\nif __name__ == "__main__":\n    generate()\n'

fig6_3_code = f'''"""
Figure 6.3: Worked 3-Stage Forensic Progression of a 15-Node Incident
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
with open(OUT_DIR / "fig6_3_15node_forensic_progression.py", "w", encoding="utf-8") as f:
    f.write(fig6_3_code.strip() + "\n")
print("Created fig6_3_15node_forensic_progression.py")

# -----------------------------------------------------------------------------
# 4. Figure 6.4: Single Alert Timeline
# -----------------------------------------------------------------------------
with open("scripts/redesign_fig6_4_single_alert_timeline.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("def generate_figure_6_4():")
body = text[idx:]
body = body.replace("def generate_figure_6_4():", "def generate():")
idx_save = body.find("for d in TARGET_DIRS:")
body = body[:idx_save] + 'save_figure(fig, "fig_single_alert_timeline", pad_inches=0.15)\n    plt.close(fig)\n\nif __name__ == "__main__":\n    generate()\n'

fig6_4_code = f'''"""
Figure 6.4: Chronological Forensic Timeline of the 15-Node Laundering Case
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
with open(OUT_DIR / "fig6_4_single_alert_timeline.py", "w", encoding="utf-8") as f:
    f.write(fig6_4_code.strip() + "\n")
print("Created fig6_4_single_alert_timeline.py")

# -----------------------------------------------------------------------------
# 5. Figure 6.5: Merkle Audit Tree
# -----------------------------------------------------------------------------
with open("scripts/generate_all_8_new_figures.py", "r", encoding="utf-8") as f:
    text = f.read()

idx_start = text.find("def make_fig_6_5():")
idx_end = text.find("def make_fig_9_3():")
snippet = text[idx_start:idx_end]
snippet = snippet.replace("def make_fig_6_5():", "def generate():")
snippet = snippet.replace('save_fig(fig, "fig_6_5_merkle_audit_tree")', 'save_figure(fig, "fig_6_5_merkle_audit_tree", pad_inches=0.12)')

fig6_5_code = f'''"""
Figure 6.5: Tamper-Evident SHA-256 Merkle Tree and WORM Archival Ledger
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
with open(OUT_DIR / "fig6_5_merkle_audit_tree.py", "w", encoding="utf-8") as f:
    f.write(fig6_5_code.strip() + "\n")
print("Created fig6_5_merkle_audit_tree.py")

print("\n--- ALL 5 CHAPTER 6 FIGURE SCRIPTS BUILT SUCCESSFULLY ---")

