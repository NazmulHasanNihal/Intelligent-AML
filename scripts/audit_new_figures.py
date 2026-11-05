import fitz
from pathlib import Path
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

fig_paths = [
    Path('papers/University_CSE_Thesis/figures/fig1_operational_architecture_flowchart.pdf'),
    Path('papers/University_CSE_Thesis/figures/fig21_adversarial_camouflage_topology.pdf'),
    Path('papers/University_CSE_Thesis/figures/fig_lit_evolution_frontier.pdf'),
    Path('papers/University_CSE_Thesis/figures/fig3_1_tensor_flow.pdf'),
    Path('papers/University_CSE_Thesis/figures/fig_canonical_invariants.pdf'),
    Path('papers/University_CSE_Thesis/figures/fig_12d_toy_model_schematic.pdf'),
    Path('papers/University_CSE_Thesis/figures/fig4_1_duckdb_arrow_pipeline.pdf'),
    Path('papers/University_CSE_Thesis/figures/fig4_2_database_erd.pdf'),
    Path('papers/University_CSE_Thesis/figures/fig_12d_toy_model_schematic.pdf'),
    Path('papers/University_CSE_Thesis/figures/fig4_1_duckdb_arrow_pipeline.pdf'),
    Path('papers/University_CSE_Thesis/figures/fig4_2_database_erd.pdf'),
]

for p in fig_paths:
    doc = fitz.open(p)
    page = doc[0]
    rect = page.rect
    words = page.get_text('words')
    
    # Check bounds
    clipped = [w for w in words if w[0] < 5 or w[1] < 5 or w[2] > rect.width - 5 or w[3] > rect.height - 5]
    
    # Check horizontal collisions on same line
    collisions = []
    lines = {}
    for w in words:
        y_approx = round(w[1], 1)
        lines.setdefault(y_approx, []).append(w)
        
    for y, line_words in lines.items():
        line_words.sort(key=lambda x: x[0])
        for i in range(len(line_words) - 1):
            w1 = line_words[i]
            w2 = line_words[i+1]
            # If w1 right > w2 left by more than 1.5 pt and not identical box
            if w1[2] - w2[0] > 1.5:
                collisions.append((w1[4], w2[4], w1[2] - w2[0]))
                
    print(f"=== {p.name} ===")
    print(f"Dimensions: {rect.width:.1f} x {rect.height:.1f} pt")
    print(f"Total words: {len(words)}")
    print(f"Boundary clipped words (<5pt to edge): {len(clipped)}")
    if clipped:
        for c in clipped[:5]:
            print(f"  Clipped: {c[4]} at bbox {c[:4]}")
    print(f"Collisions detected: {len(collisions)}")
    if collisions:
        for c in collisions[:5]:
            print(f"  Collision between '{c[0]}' and '{c[1]}' overlap={c[2]:.2f}pt")

