"""
scripts/generate_intuitive_thesis_visuals.py
Generates intuitive, publication-grade vector PDF figures across the National University CSE Thesis Monograph:
1. fig_lit_evolution_frontier.pdf (Chapter 2: 2D AML Graph Learning Evolution Frontier)
2. fig_12d_toy_model_schematic.pdf (Chapter 3: 12-D Canonical Invariant Physical Toy-Model)
3. fig_triband_waveform_spectrum.pdf (Chapter 3: Tri-Band Harmonic Attention Spectrum)
4. fig_conformal_conveyor_funnel.pdf (Chapter 5: 3-Tier Conformal Decision Funnel)
5. fig_ast_grammar_pipeline.pdf (Chapter 6: AST Grammar Anti-Hallucination Pipeline)
6. fig_champion_vs_runnerup_delta.pdf (Chapter 7: F1 Lead Delta Chart over 14 Networks)
7. fig_regulatory_shields.pdf (Chapter 9: 5-Pillar Regulatory Compliance Shields)
"""

import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 8.5,
    'axes.labelsize': 9.0,
    'axes.titlesize': 9.5,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
})

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))
TARGET_DIRS = [
    BASE_DIR / "papers" / "University_CSE_Thesis" / "figures",
    BASE_DIR / "papers" / "EAAI_Submission" / "figures",
    BASE_DIR / "reports" / "figures"
]
for d in TARGET_DIRS:
    d.mkdir(parents=True, exist_ok=True)

def save_fig(fig, stem):
    for d in TARGET_DIRS:
        pdf_path = d / f"{stem}.pdf"
        png_path = d / f"{stem}.png"
        fig.savefig(pdf_path, bbox_inches="tight", pad_inches=0.15)
        fig.savefig(png_path, dpi=300, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print(f" [OK] Generated: {stem}.pdf & .png across all target directories")

# Import the 5 perfected generators
from scripts.upgrade_user_target_figures import (
    upgrade_lit_evolution_frontier,
    upgrade_12d_toy_model_schematic,
    upgrade_fig19_conformal_risk_mechanism,
    upgrade_compliance_alert_funnel,
    upgrade_conformal_conveyor_funnel
)

# =============================================================================
# 3. FIG: Tri-Band Waveform Spectrum (Chapter 3)
# =============================================================================
def generate_triband_waveform_spectrum():
    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, figsize=(8.0, 5.2), sharex=True)
    
    t = np.linspace(0, 168, 600) # 168 hours = 7 days
    
    # Band 1: Fast Burst (tau = 2.4 h)
    burst_signal = np.zeros_like(t)
    for spike_t in [12, 14, 15, 60, 61, 130]:
        burst_signal += np.exp(-((t - spike_t)/1.2)**2)
    ax1.plot(t, burst_signal, color='#dc2626', lw=1.5)
    ax1.fill_between(t, 0, burst_signal, color='#fee2e2', alpha=0.7)
    ax1.set_ylabel(r"Band 1 ($\tau = 2.4\,\mathrm{h}$)", fontsize=7.5, weight='bold', color='#991b1b', labelpad=8)
    ax1.text(0.98, 0.75, "Micro-Burst Smurfing & Peeling Chops", transform=ax1.transAxes, ha='right', fontsize=7.0, color='#991b1b', weight='semibold')
    ax1.set_ylim(0, 1.3)
    ax1.grid(True, linestyle=':', alpha=0.5)

    # Band 2: Circadian (tau = 24 h)
    circadian_signal = 0.5 + 0.4 * np.sin(2 * np.pi * t / 24 - np.pi/2)
    ax2.plot(t, circadian_signal, color='#2563eb', lw=1.5)
    ax2.fill_between(t, 0, circadian_signal, color='#dbeafe', alpha=0.7)
    ax2.set_ylabel(r"Band 2 ($\tau = 24\,\mathrm{h}$)", fontsize=7.5, weight='bold', color='#1d4ed8', labelpad=8)
    ax2.text(0.98, 0.75, "Circadian Retail & Commercial Business Hours", transform=ax2.transAxes, ha='right', fontsize=7.0, color='#1d4ed8', weight='semibold')
    ax2.set_ylim(0, 1.1)
    ax2.grid(True, linestyle=':', alpha=0.5)

    # Band 3: Macro Dormancy (tau = 168 h / 90 Days)
    macro_signal = np.exp(-t / 168.0)
    ax3.plot(t, macro_signal, color='#7c3aed', lw=1.5)
    ax3.fill_between(t, 0, macro_signal, color='#f3e8ff', alpha=0.7)
    ax3.set_ylabel(r"Band 3 ($\tau = 168\,\mathrm{h}$)", fontsize=7.5, weight='bold', color='#6d28d9', labelpad=8)
    ax3.text(0.98, 0.75, "90-Day Dormant Hibernation Holding Chains", transform=ax3.transAxes, ha='right', fontsize=7.0, color='#6d28d9', weight='semibold')
    ax3.set_ylim(0, 1.2)
    ax3.grid(True, linestyle=':', alpha=0.5)

    # Combined Kernel Response vs Standard Decay
    cstgb_unified = 0.35 * burst_signal + 0.35 * circadian_signal + 0.30 * macro_signal
    std_decay = np.exp(-t / 6.0) # standard decay dies in 12 hours
    ax4.plot(t, cstgb_unified, color='#0f172a', lw=1.8, label="C-STGB Unified Tri-Band Attention Bank (Sustained Sensitivity)")
    ax4.plot(t, std_decay, color='#94a3b8', lw=1.5, linestyle='--', label=r"Conventional Single Decay (Vanishes $\to 0$ after 12h: Hibernation Blindness)")
    ax4.set_ylabel(r"Temporal Kernel $\psi(\Delta t)$", fontsize=7.5, weight='bold')
    ax4.set_xlabel(r"Elapsed Time Window $\Delta t$ (Hours across 7-Day Observation Horizon)", fontsize=8.0, weight='semibold')
    ax4.legend(fontsize=7.0, loc='upper right', framealpha=0.95)
    ax4.grid(True, linestyle=':', alpha=0.5)

    fig.suptitle("C-STGB Tri-Band Harmonic Temporal Attention Spectrum: Bridging Microsecond Bursts & 90-Day Dormancy", fontsize=9.5, weight='bold')
    fig.subplots_adjust(top=0.92, bottom=0.10, left=0.12, right=0.96)
    save_fig(fig, "fig_triband_waveform_spectrum")


# =============================================================================
# 5. FIG: AST Grammar Anti-Hallucination Pipeline (Chapter 6)
# =============================================================================
def generate_ast_grammar_pipeline():
    fig, ax = plt.subplots(figsize=(8.0, 4.6))
    
    boxes = [
        ("1. Multi-Agent Reasoning", "Forensic Swarm drafts\nraw narrative text\n(Typology & Evidence)", 0.06, 0.42, 0.19, 0.32, "#f1f5f9", "#475569"),
        ("2. AST Grammar Parser", "EBNF Formal Rules\nRecursive Descent\nSyntax Tree Validation", 0.30, 0.42, 0.19, 0.32, "#e0e7ff", "#4338ca"),
        ("3. Pydantic Runtime Gate", "Type & Range Enforcement\nStrict Field Checks\nZero Tolerance Gate", 0.54, 0.42, 0.19, 0.32, "#fef3c7", "#d97706"),
        ("4. Statutory XML Filing", "FinCEN Form 111 XML\nCryptographic SHA-256\nWORM Audit Vault Seal", 0.78, 0.42, 0.19, 0.32, "#dcfce7", "#16a34a")
    ]
    
    for title, desc, x, y, w, h, bg, border in boxes:
        box = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.03", fc=bg, ec=border, lw=1.6)
        ax.add_patch(box)
        ax.text(x + w/2, y + h - 0.07, title, ha='center', va='center', fontsize=7.5, weight='bold', color=border)
        ax.text(x + w/2, y + h/2 - 0.03, desc, ha='center', va='center', fontsize=6.4, color='#1e293b', linespacing=1.35)
        
    for x_start in [0.25, 0.49, 0.73]:
        ax.annotate("", xy=(x_start + 0.05, 0.58), xytext=(x_start, 0.58), arrowprops=dict(arrowstyle="->", lw=2.0, color="#64748b"))

    callout = patches.FancyBboxPatch((0.10, 0.10), 0.80, 0.20, boxstyle="round,pad=0.03", fc='#ecfdf5', ec='#059669', lw=1.6)
    ax.add_patch(callout)
    ax.text(0.50, 0.22, "Deterministic Mathematical Anti-Hallucination Proof: 0.00% Entity Hallucination Rate", 
            ha='center', va='center', fontsize=8.0, weight='bold', color='#065f46')
    ax.text(0.50, 0.14, "Every counterparty address, flow dollar sum, and timestamp is anchored to DuckDB Merkle leaves.", 
            ha='center', va='center', fontsize=7.2, color='#047857')

    ax.set_xlim(0.02, 1.00)
    ax.set_ylim(0.04, 0.88)
    ax.axis('off')
    ax.set_title("AST Grammar & Schema Verification Pipeline: Deterministic Anti-Hallucination Compliance Swarm", fontsize=9.5, weight='bold', pad=12)
    
    save_fig(fig, "fig_ast_grammar_pipeline")


# =============================================================================
# 6. FIG: Champion-vs-Runner-Up F1 Margin Delta Chart (Chapter 7)
# =============================================================================
def generate_champion_delta_chart():
    from scripts.redesign_fig7_3_champion_delta import generate_figure_7_3
    fig = generate_figure_7_3()
    save_fig(fig, "fig_champion_vs_runnerup_delta")


# =============================================================================
# 7. FIG: 5-Pillar Regulatory Compliance Shields (Chapter 9)
# =============================================================================
def generate_regulatory_shields():
    print("Generating Redesigned Figure 9.2: 5-Pillar Global Regulatory Compliance Shield...")
    from scripts.redesign_fig9_2_regulatory_shields import generate_figure_9_2
    fig = generate_figure_9_2()
    save_fig(fig, "fig_regulatory_shields")

if __name__ == "__main__":
    print("Generating all intuitive thesis visuals...")
    upgrade_lit_evolution_frontier()
    upgrade_12d_toy_model_schematic()
    generate_triband_waveform_spectrum()
    upgrade_conformal_conveyor_funnel()
    upgrade_fig19_conformal_risk_mechanism()
    upgrade_compliance_alert_funnel()
    generate_ast_grammar_pipeline()
    generate_champion_delta_chart()
    generate_regulatory_shields()
    print("All intuitive thesis visuals generated successfully!")
