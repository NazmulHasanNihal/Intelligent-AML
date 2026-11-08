"""
scripts/build_ch4_figures.py
Extracts and builds standalone scripts for all Chapter 4 figures:
- fig4_1_duckdb_arrow_pipeline.py
- fig4_2_database_erd.py
- fig4_3_causal_slicing.py
"""

import os
from pathlib import Path

OUT_DIR = Path("scripts/figures")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. Figure 4.1
# -----------------------------------------------------------------------------
with open("scripts/redesign_fig4_1_data_pipeline.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("def generate_figure_4_1():")
end_idx = text.find("def save_to_all(")
body = text[idx:end_idx]
body = body.replace("def generate_figure_4_1():", "def generate():")

fig4_1_code = f'''"""
Figure 4.1: Vectorized Streaming Data Engineering Architecture
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
    save_figure(fig, "fig4_1_duckdb_arrow_pipeline", pad_inches=0.15)
    plt.close(fig)
'''

with open(OUT_DIR / "fig4_1_duckdb_arrow_pipeline.py", "w", encoding="utf-8") as f:
    f.write(fig4_1_code.strip() + "\n")
print("Created fig4_1_duckdb_arrow_pipeline.py")

# -----------------------------------------------------------------------------
# 2. Figure 4.2
# -----------------------------------------------------------------------------
with open("scripts/redesign_fig4_2_database_erd.py", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("def generate_figure_4_2():")
end_idx = text.find("def save_to_all(")
body = text[idx:end_idx]
body = body.replace("def generate_figure_4_2():", "def generate():")

fig4_2_code = f'''"""
Figure 4.2: Relational Database Schema and Causal Index Architecture
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
    save_figure(fig, "fig4_2_database_erd", pad_inches=0.15)
    plt.close(fig)
'''

with open(OUT_DIR / "fig4_2_database_erd.py", "w", encoding="utf-8") as f:
    f.write(fig4_2_code.strip() + "\n")
print("Created fig4_2_database_erd.py")

# -----------------------------------------------------------------------------
# 3. Figure 4.3: Causal Slicing
# -----------------------------------------------------------------------------
with open("scripts/generate_all_8_new_figures.py", "r", encoding="utf-8") as f:
    text = f.read()

idx_start = text.find("def make_fig_4_3():")
idx_end = text.find("def make_fig_5_6():")
snippet = text[idx_start:idx_end]
snippet = snippet.replace("def make_fig_4_3():", "def generate():")
snippet = snippet.replace('save_fig(fig, "fig_4_3_causal_slicing")', 'save_figure(fig, "fig_4_3_causal_slicing", pad_inches=0.12)')

fig4_3_code = f'''"""
Figure 4.3: Time-Causal 2-Hop Ego-Graph Extraction Window
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

{snippet}

if __name__ == "__main__":
    generate()
'''
with open(OUT_DIR / "fig4_3_causal_slicing.py", "w", encoding="utf-8") as f:
    f.write(fig4_3_code.strip() + "\n")
print("Created fig4_3_causal_slicing.py")

print("\n--- ALL 3 CHAPTER 4 FIGURE SCRIPTS BUILT SUCCESSFULLY ---")

