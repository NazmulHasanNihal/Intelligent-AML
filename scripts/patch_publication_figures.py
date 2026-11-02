"""
patch_publication_figures.py — Applies action plan visual fixes across:
1. scripts/generate_thesis_distinct_figures.py
2. scripts/generate_publication_figures_extra.py
3. scripts/generate_all_publication_figures.py
"""

from pathlib import Path
import re

BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================================================================
# 1. PATCH generate_thesis_distinct_figures.py
# ==============================================================================
p_thesis = BASE_DIR / "scripts" / "generate_thesis_distinct_figures.py"
txt_thesis = p_thesis.read_text(encoding="utf-8")

# Add eaai_fig_dir to TARGET_DIRS
old_target = """thesis_fig_dir = BASE_DIR / "papers" / "University_CSE_Thesis" / "figures"\ndata_fig_dir = BASE_DIR / "data" / "outputs" / "figures"\nTARGET_DIRS = [thesis_fig_dir, data_fig_dir]"""
new_target = """thesis_fig_dir = BASE_DIR / "papers" / "University_CSE_Thesis" / "figures"\neaai_fig_dir = BASE_DIR / "papers" / "EAAI_Research_Paper" / "figures"\ndata_fig_dir = BASE_DIR / "data" / "outputs" / "figures"\nTARGET_DIRS = [thesis_fig_dir, eaai_fig_dir, data_fig_dir]"""
txt_thesis = txt_thesis.replace(old_target, new_target)
# If CRLF:
if old_target not in txt_thesis and "TARGET_DIRS = [thesis_fig_dir, data_fig_dir]" in txt_thesis:
    txt_thesis = re.sub(
        r'thesis_fig_dir\s*=\s*BASE_DIR[^\n]+\ndata_fig_dir\s*=\s*BASE_DIR[^\n]+\nTARGET_DIRS\s*=\s*\[thesis_fig_dir,\s*data_fig_dir\]',
        'thesis_fig_dir = BASE_DIR / "papers" / "University_CSE_Thesis" / "figures"\n'
        'eaai_fig_dir = BASE_DIR / "papers" / "EAAI_Research_Paper" / "figures"\n'
        'data_fig_dir = BASE_DIR / "data" / "outputs" / "figures"\n'
        'TARGET_DIRS = [thesis_fig_dir, eaai_fig_dir, data_fig_dir]',
        txt_thesis
    )

# Fix typo "2-Hop Ego In-Memory Cache" -> "Fast-Path 2-Hop LRU Cache (88.4% Hit Rate)"
txt_thesis = txt_thesis.replace(
    "{'head': '2-Hop Ego In-Memory Cache', 'math': '100k Node Capacity, LRU', 'desc': '88.4% Cache hit rate in live tests'}",
    "{'head': 'Fast-Path 2-Hop LRU Cache', 'math': '100k Node Capacity, LRU', 'desc': '88.4% Cache hit rate in live tests'}"
)
txt_thesis = txt_thesis.replace(
    "'tag': 'Sub-10ms Banking SLA Guaranteed'",
    "'tag': '88.4% Hit Rate | Sub-10ms SLA'"
)
txt_thesis = txt_thesis.replace(
    "'head': 'Autonomous 4-Agent Swarm'",
    "'head': 'Assisted 4-Agent Swarm'"
)

p_thesis.write_text(txt_thesis, encoding="utf-8")
print("[OK] Patched generate_thesis_distinct_figures.py")


# ==============================================================================
# 2. PATCH generate_publication_figures_extra.py
# ==============================================================================
p_extra = BASE_DIR / "scripts" / "generate_publication_figures_extra.py"
txt_extra = p_extra.read_text(encoding="utf-8")

# Fix 1: Tri-band decay curve label (remove \textbf)
txt_extra = txt_extra.replace(
    r'label=r"\textbf{C-STGB Tri-Band Harmonic Attention} $w(\Delta t)$ (Ours)"',
    r'label="C-STGB Tri-Band Harmonic Attention $w(\Delta t)$ (Ours)"'
)
# Move diurnal resonance text lower to avoid collision
txt_extra = txt_extra.replace(
    'ax.text(24.3, 0.75, "24h Diurnal Resonance"',
    'ax.text(24.3, 0.68, "24h Diurnal Resonance"'
)

# Fix 2: Single-alert timeline 5 plain-English stages
old_events = """events = [
    (0.09, "14:15:02", "Deposit $485k", "Source S0 (ACC_9941)\\nFunds received via wire", "#1e3a8a", "above"),
    (0.28, "14:19:12", "Smurfing Fan-Out", "Dispersal to mules M1–M5\\n12-min window, λ=74.2", "#b91c1c", "below"),
    (0.48, "14:23:01", "Layering Wash", "Wash cycle (L1–L3)\\nChaff filtered (g_ij<0.10)", "#ea580c", "above"),
    (0.68, "14:27:45", "Aggregation", "Offshore sink C4\\nFlow ratio Φ_flow ≈ 0.994", "#047857", "below"),
    (0.88, "14:28:12", "Conformal Alert", "Tier 1 Quarantine Γ={1}\\nFinCEN XML generated", "#7c3aed", "above"),
]"""
new_events = """events = [
    (0.09, "14:15:02", "Stage 1: Influx $485k", "Source S0 (ACC_9941)\\nFunds received via wire", "#1e3a8a", "above"),
    (0.28, "14:19:12", "Stage 2: Smurfing", "Dispersal to mules M1–M5\\n12-min window, λ=74.2", "#b91c1c", "below"),
    (0.48, "14:23:01", "Stage 3: Layering Wash", "Wash cycle (L1–L3)\\nChaff filtered (g_ij<0.10)", "#ea580c", "above"),
    (0.68, "14:27:45", "Stage 4: Aggregation", "Offshore sink C4\\nFlow ratio Φ_flow ≈ 0.994", "#047857", "below"),
    (0.88, "14:28:12", "Stage 5: Conformal Triage", "Tier 1 Quarantine Γ={1}\\nAssisted SAR generated", "#7c3aed", "above"),
]"""
txt_extra = txt_extra.replace(old_events, new_events)
txt_extra = txt_extra.replace(
    'ax.text(0.98, y_axis - 0.055, "Time (UTC)"',
    'ax.text(0.99, y_axis - 0.055, "Time (UTC)"'
)

# Fix 3: Streaming latency waterfall - move labels above whiskers
old_waterfall_ann = """for bar, l_val, p_val in zip(bars, latencies, p99_lat):
    ax.annotate(f"{l_val:.2f} ms\\n(P99:{p_val:.2f})",
                (bar.get_x() + bar.get_width() / 2, bar.get_height()),
                xytext=(0, 4), textcoords="offset points", ha="center", va="bottom",
                fontsize=6.5, fontweight="bold", linespacing=1.1)"""

new_waterfall_ann = """for bar, l_val, p_val in zip(bars, latencies, p99_lat):
    ax.annotate(f"{l_val:.2f} ms\\n(P99:{p_val:.2f})",
                (bar.get_x() + bar.get_width() / 2, p_val),
                xytext=(0, 3), textcoords="offset points", ha="center", va="bottom",
                fontsize=6.2, fontweight="bold", linespacing=1.05)"""
txt_extra = txt_extra.replace(old_waterfall_ann, new_waterfall_ann)

# Fix 4: Roadmap Gantt - separate Phase 2 & Phase 3 headers at Week 20
old_gantt_pills = """ax.add_patch(patches.FancyBboxPatch((1.5, 7.85), 9.0, 0.65, boxstyle="round,pad=0.08", facecolor="#dbeafe", edgecolor="#1565c0", lw=0.8))
ax.text(6.0, 8.17, "Phase 1: Shadow (W1–W12)", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#1565c0")

ax.add_patch(patches.FancyBboxPatch((12.5, 7.85), 7.0, 0.65, boxstyle="round,pad=0.08", facecolor="#ccfbf1", edgecolor="#00796b", lw=0.8))
ax.text(16.0, 8.17, "Phase 2: Pilot (W13–W20)", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#00796b")

ax.add_patch(patches.FancyBboxPatch((20.5, 7.85), 5.0, 0.65, boxstyle="round,pad=0.08", facecolor="#fee2e2", edgecolor="#c62828", lw=0.8))
ax.text(23.0, 8.17, "Phase 3: STP (W21–W26)", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#c62828")"""

new_gantt_pills = """ax.add_patch(patches.FancyBboxPatch((1.0, 7.85), 9.5, 0.65, boxstyle="round,pad=0.08", facecolor="#dbeafe", edgecolor="#1565c0", lw=0.8))
ax.text(5.75, 8.17, "Phase 1: Shadow (W1–W12)", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#1565c0")

ax.add_patch(patches.FancyBboxPatch((12.2, 7.85), 7.2, 0.65, boxstyle="round,pad=0.08", facecolor="#ccfbf1", edgecolor="#00796b", lw=0.8))
ax.text(15.8, 8.17, "Phase 2: Pilot (W13–W20)", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#00796b")

ax.add_patch(patches.FancyBboxPatch((20.4, 7.85), 5.2, 0.65, boxstyle="round,pad=0.08", facecolor="#fee2e2", edgecolor="#c62828", lw=0.8))
ax.text(23.0, 8.17, "Phase 3: STP (W21–W26)", ha="center", va="center", fontsize=7.2, fontweight="bold", color="#c62828")"""
txt_extra = txt_extra.replace(old_gantt_pills, new_gantt_pills)

# Fix 5: Stepwise Cumulative Ablation Waterfall Chart aligned with Table 7.4
# (26.40% -> 54.80% -> 68.50% -> 76.20% -> 86.12% -> 89.80% -> 91.42%)
old_ablation_code = """# Baseline start, incremental deltas, final total
deltas = [10.33, 35.22, 14.65, 10.84, 19.06, 0.82, 0.50]
# Cumulative values:
# 10.33 -> 45.55 -> 60.20 -> 71.04 -> 90.10 -> 90.92 -> 91.42"""

new_ablation_code = """# Baseline start, incremental deltas, final total exactly matching Table 7.4
deltas = [26.40, 28.40, 13.70, 7.70, 9.92, 3.68, 1.62]
# Cumulative values:
# 26.40 -> 54.80 -> 68.50 -> 76.20 -> 86.12 -> 89.80 -> 91.42"""
txt_extra = txt_extra.replace(old_ablation_code, new_ablation_code)
txt_extra = txt_extra.replace(
    'ax.text(x_pos[i], h + 1.2, f"{h:.2f}%\\n(+81.09 pp)"',
    'ax.text(x_pos[i], h + 1.2, f"{h:.2f}%\\n(+65.02 pp)"'
)

# Fix 6: 15-node progression panel (c) text layout
old_prog_fields = """sar_fields = [
    ("Case Identifier", "SAR-2026-B8F91A04", "#0f172a"),
    ("Primary Subject", "ACC_9941 (Source S0)", "#b91c1c"),
    ("Triage Set", "Tier 1: Quarantine Hold", "#b91c1c"),
    ("Primary Typology", "Smurfing & Peeling Chain", "#c2410c"),
    ("Mass Flow Balance", "Φ_flow = 0.9942 (Pass-Through)", "#0f766e"),
    ("Merkle Receipt Seal", "SHA-256 e3b0c4... (Verified)", "#15803d"),
    ("Compliance Standard", "Fed SR 26-2 & BSA Aligned", "#4338ca")
]

y_field = 0.82
for label, val, c_val in sar_fields:
    ax_c.text(0.06, y_field, label + ":", ha="left", va="center", fontsize=5.6, fontweight="bold", color="#334155")
    ax_c.text(0.94, y_field, val, ha="right", va="center", fontsize=5.6, fontweight="bold", color=c_val)
    y_field -= 0.105"""

new_prog_fields = """sar_fields = [
    ("Case Identifier", "SAR-2026-B8F91A04", "#0f172a"),
    ("Primary Subject", "ACC_9941 (Source S0)", "#b91c1c"),
    ("Triage Set", "Tier 1: Quarantine Hold", "#b91c1c"),
    ("Typology", "Smurfing & Peeling Chain", "#c2410c"),
    ("Flow Balance", "Pass-Through (0.994)", "#0f766e"),
    ("Merkle Seal", "SHA-256 e3b0c4... (WORM)", "#15803d"),
    ("Compliance", "Fed SR 26-2 & BSA Aligned", "#4338ca")
]

y_field = 0.82
for label, val, c_val in sar_fields:
    ax_c.text(0.05, y_field, label + ":", ha="left", va="center", fontsize=5.3, fontweight="bold", color="#334155")
    ax_c.text(0.95, y_field, val, ha="right", va="center", fontsize=5.3, fontweight="bold", color=c_val)
    y_field -= 0.105"""
txt_extra = txt_extra.replace(old_prog_fields, new_prog_fields)
txt_extra = txt_extra.replace(
    'ax_c.text(0.50, 0.05, "Autonomous 4-Agent Generation\\n100% AST Grammar Validated"',
    'ax_c.text(0.50, 0.05, "Assisted 4-Agent Generation\\n100% AST Grammar Validated"'
)

p_extra.write_text(txt_extra, encoding="utf-8")
print("[OK] Patched generate_publication_figures_extra.py")


# ==============================================================================
# 3. PATCH generate_all_publication_figures.py
# ==============================================================================
p_all = BASE_DIR / "scripts" / "generate_all_publication_figures.py"
txt_all = p_all.read_text(encoding="utf-8")

# Fix 1: PR/ROC curve clamping <= 1.00
txt_all = txt_all.replace(
    'prec_cstgb = prec_cstgb_raw * (0.9312 / np.trapezoid(prec_cstgb_raw, rec_vals))',
    'prec_cstgb = np.clip(prec_cstgb_raw * (0.9312 / np.trapezoid(prec_cstgb_raw, rec_vals)), 0.0, 1.0)'
)
txt_all = txt_all.replace(
    'prec_xgb = prec_xgb_raw * (0.8900 / np.trapezoid(prec_xgb_raw, rec_vals))',
    'prec_xgb = np.clip(prec_xgb_raw * (0.8900 / np.trapezoid(prec_xgb_raw, rec_vals)), 0.0, 1.0)'
)
txt_all = txt_all.replace(
    'prec_cat = prec_cat_raw * (0.8800 / np.trapezoid(prec_cat_raw, rec_vals))',
    'prec_cat = np.clip(prec_cat_raw * (0.8800 / np.trapezoid(prec_cat_raw, rec_vals)), 0.0, 1.0)'
)

# Fix 2: Radar chart title 13 -> 14 datasets
txt_all = txt_all.replace(
    'ax.set_title("13-Dataset Multi-Criteria Radar Benchmark", fontweight="bold", fontsize=9.5, y=1.14)',
    'ax.set_title("14-Dataset Multi-Criteria Radar Benchmark", fontweight="bold", fontsize=9.5, y=1.14)'
)

# Fix 3: Figure 20 Multi-agent swarm wording: "Assisted" and DuckDB Hydration
txt_all = txt_all.replace(
    'ax.text(0.50, 0.952, "Autonomous Multi-Agent Forensic Swarm Sequence Protocol & Fed SR 26-2 Audit Trail"',
    'ax.text(0.50, 0.952, "Assisted Multi-Agent Forensic Swarm Sequence Protocol & Fed SR 26-2 Audit Trail"'
)

p_all.write_text(txt_all, encoding="utf-8")
print("[OK] Patched generate_all_publication_figures.py")
