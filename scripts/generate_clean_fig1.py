"""
generate_clean_fig1.py — Ultra-crisp, perfectly typeset Figure 1 (System Architecture)
for IEEE Transactions on Information Forensics and Security (T-IFS).
Ensures zero text collision, no broken glyphs, proper STIX mathtext, and pristine layout.
"""

import sys
import shutil
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pymupdf

BASE_DIR = Path(__file__).resolve().parent.parent

OUT_DIRS = [
    BASE_DIR / "papers" / "IEEE_Research_Paper" / "figures",
    BASE_DIR / "papers" / "University_CSE_Thesis" / "figures",
    BASE_DIR / "data" / "outputs" / "figures"
]

for d in OUT_DIRS:
    d.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'font.size': 8.5,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'mathtext.fontset': 'stix',
})

def generate_figure_1():
    print("[*] Generating Flawless Figure 1: C-STGB Architecture Blueprint...")
    fig, ax = plt.subplots(figsize=(7.16, 2.45), dpi=300)
    ax.axis('off')
    ax.set_xlim([-0.006, 1.006])
    ax.set_ylim([-0.008, 1.008])

    # Outer master border
    ax.add_patch(patches.FancyBboxPatch(
        (0.00, 0.00), 1.00, 1.00,
        boxstyle='round,pad=0.004,rounding_size=0.008',
        facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=0.8
    ))

    # Top Master Banner
    ax.add_patch(patches.FancyBboxPatch(
        (0.008, 0.916), 0.984, 0.076,
        boxstyle='round,pad=0.003,rounding_size=0.006',
        facecolor='#0f172a', edgecolor='#0f172a', linewidth=0.5
    ))
    ax.text(0.50, 0.954, 'C-STGB: Conformal Spatio-Temporal GraphBoost End-to-End Surveillance Platform',
            ha='center', va='center', fontsize=9.2, fontweight='bold', color='#ffffff')

    stages = [
        {
            'id': 'STAGE 1: STREAMING INGEST',
            'title': 'DuckDB Invariants & Hawkes',
            'badge_bg': '#1e3a8a',
            'badge_fg': '#dbeafe',
            'card_bg': '#f8fafc',
            'border': '#93c5fd',
            'x': 0.010, 'w': 0.233,
            'blocks': [
                {
                    'head': 'Continuous Ingest & Subgraphs',
                    'math': r'$G_t = (V_t, E_t), \quad N_K(u) \; (K \leq 15)$',
                    'desc': 'DuckDB / Arrow zero-copy streaming'
                },
                {
                    'head': 'Mass Flow Conservation',
                    'math': r'$\Phi_{\mathrm{flow}} = \log(1 + A_{\mathrm{out}} / [A_{\mathrm{in}} + \epsilon]) \approx 1.0$',
                    'desc': 'Layering dissipation & pass-through detector'
                },
                {
                    'head': 'Hawkes Intensity & Causal Taint',
                    'math': r'$\lambda_u(t) = \mu_u + \sum \alpha \cdot e^{-\beta \Delta t}$',
                    'desc': 'Forward & backward taint (< 0.08 ms)'
                }
            ],
            'output_tensor': r'$\mathbf{z}_{\mathrm{inv}}(u, t) \in \mathbb{R}^{12}, \; G_t^{(K)}$',
            'sla_tag': '0.45 ms SLA | DuckDB Ingest'
        },
        {
            'id': 'STAGE 2: GNN & FILTER',
            'title': 'Tri-Band & Latent GraphSMOTE',
            'badge_bg': '#065f46',
            'badge_fg': '#dcfce7',
            'card_bg': '#f8fafc',
            'border': '#86efac',
            'x': 0.256, 'w': 0.233,
            'blocks': [
                {
                    'head': 'Tri-Band Temporal Attention',
                    'math': r'$\Phi_{\mathrm{time}}(\Delta t), \; w(\Delta t) = \sum \pi_b e^{-\lambda_b \Delta t}$',
                    'desc': 'Microsecond bursts to 90-day dormancy'
                },
                {
                    'head': 'Learnable Edge-Trust Gating',
                    'math': r'$\hat{g}_{ij} = \delta_{\mathrm{floor}} + (1 - \delta_{\mathrm{floor}}) g_{ij}$',
                    'desc': 'Prunes 65.9% of adversarial chaff links'
                },
                {
                    'head': 'Typology Latent GraphSMOTE',
                    'math': r'$h_{\mathrm{syn}} = (1 - \rho) h_u + \rho h_v, \; u, v \in C_k$',
                    'desc': 'Latent interpolation & hard-negative pairs'
                }
            ],
            'output_tensor': r'$\mathbf{h}_u^{(L)} \in \mathbb{R}^d \text{ (Latent Embedding)}$',
            'sla_tag': 'Continuous Temporal Dynamics'
        },
        {
            'id': 'STAGE 3: FUSION & RISK',
            'title': 'Evidence-Adaptive Bayes Head',
            'badge_bg': '#9a3412',
            'badge_fg': '#ffedd5',
            'card_bg': '#f8fafc',
            'border': '#fdba74',
            'x': 0.502, 'w': 0.233,
            'blocks': [
                {
                    'head': 'Evidence-Adaptive Fusion Gate',
                    'math': r'$\alpha_u = \sigma(\mathbf{w}_\alpha^\top [\mathbf{h}_u \parallel \mathbf{z}_{\mathrm{inv}}] + b_\alpha)$',
                    'desc': 'Cold-start: deg(u) <= 2 shifts to z_inv'
                },
                {
                    'head': 'Unified Representation Space',
                    'math': r'$\mathbf{h}_u^* = \alpha_u \mathbf{h}_u + (1 - \alpha_u)[\mathbf{z}_{\mathrm{inv}} \parallel \mathbf{x}_u]$',
                    'desc': 'Secures 89.6% F1 on isolated entities'
                },
                {
                    'head': 'Cost-Sensitive Bayes Head',
                    'math': r'$\tau^* = \arg\min_\tau (15 \cdot \mathrm{FN} + 1 \cdot \mathrm{FP})$',
                    'desc': 'Asymmetric loss policy (C_FN / C_FP = 15)'
                }
            ],
            'output_tensor': r'$\hat{p}_u \in [0, 1], \; \mathbf{h}_u^* \in \mathbb{R}^{d^*}$',
            'sla_tag': 'Cold-Start Guarded + Bayes Risk'
        },
        {
            'id': 'STAGE 4: CONFORMAL SWARM',
            'title': 'CRC Triage & FinCEN SAR',
            'badge_bg': '#4c1d95',
            'badge_fg': '#f3e8ff',
            'card_bg': '#f8fafc',
            'border': '#d8b4fe',
            'x': 0.748, 'w': 0.242,
            'blocks': [
                {
                    'head': 'Class-Conditional CRC',
                    'math': r'$q^{(y)} = \mathrm{Quantile}(D_{\mathrm{cal}}), \; 1 - \alpha \geq 99.0\%$',
                    'desc': 'Finite-sample coverage with ACI tracking'
                },
                {
                    'head': '3-Tier Deterministic Triage',
                    'math': r'$\Gamma(u) \in \{\{1\}, \; \{0, 1\}, \; \{0\}\}$',
                    'desc': 'Routes >99.4% to straight-through tiers'
                },
                {
                    'head': 'Multi-Agent Forensic Swarm',
                    'math': r'$\mathrm{Investigator} \to \mathrm{Auditor} \to \mathrm{Drafter}$',
                    'desc': 'FinCEN Form 111 XML + SHA-256 Merkle'
                }
            ],
            'output_tensor': r'$\Gamma(u) \subseteq \{0, 1\}, \; \mathbf{XML}_{\mathrm{SAR}}$',
            'sla_tag': 'Model Risk Governance (SR 26-2)'
        }
    ]

    y_bottom = 0.018
    card_h = 0.885

    for s in stages:
        x0 = s['x']
        w0 = s['w']

        # Outer card container
        ax.add_patch(patches.FancyBboxPatch(
            (x0, y_bottom), w0, card_h,
            boxstyle='round,pad=0.005,rounding_size=0.008',
            facecolor=s['card_bg'], edgecolor=s['border'], linewidth=1.1
        ))

        # Header Pill
        ax.add_patch(patches.FancyBboxPatch(
            (x0 + 0.005, y_bottom + card_h - 0.088), w0 - 0.010, 0.082,
            boxstyle='round,pad=0.003,rounding_size=0.006',
            facecolor=s['badge_bg'], edgecolor=s['badge_bg'], linewidth=0.5
        ))
        ax.text(x0 + w0/2, y_bottom + card_h - 0.028, s['id'],
                ha='center', va='center', fontsize=7.0, fontweight='bold', color='#ffffff')
        ax.text(x0 + w0/2, y_bottom + card_h - 0.062, s['title'],
                ha='center', va='center', fontsize=6.2, color=s['badge_fg'], style='italic')

        # 3 Inner Functional Blocks
        block_h = 0.208
        y_top = y_bottom + card_h - 0.102

        for i, b in enumerate(s['blocks']):
            y_blk = y_top - (i * (block_h + 0.014)) - block_h

            ax.add_patch(patches.FancyBboxPatch(
                (x0 + 0.006, y_blk), w0 - 0.012, block_h,
                boxstyle='round,pad=0.003,rounding_size=0.005',
                facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=0.65
            ))

            # Block Header
            ax.plot([x0 + 0.014], [y_blk + block_h - 0.032], marker='s', markersize=3.0, color=s['badge_bg'])
            ax.text(x0 + 0.022, y_blk + block_h - 0.032, b['head'],
                    ha='left', va='center', fontsize=6.3, fontweight='bold', color='#0f172a')

            # Math Formula (clean STIX math in a soft pill)
            ax.text(x0 + w0/2, y_blk + block_h - 0.104, b['math'],
                    ha='center', va='center', fontsize=6.2, color='#0f172a',
                    bbox=dict(boxstyle='round,pad=0.12', facecolor='#f8fafc', edgecolor='#e2e8f0', lw=0.4))

            # Description (clean plain text)
            ax.text(x0 + w0/2, y_blk + 0.034, b['desc'],
                    ha='center', va='center', fontsize=5.6, color='#475569')

        # Output Box
        y_out = y_bottom + 0.052
        ax.add_patch(patches.FancyBboxPatch(
            (x0 + 0.006, y_out), w0 - 0.012, 0.046,
            boxstyle='round,pad=0.003,rounding_size=0.004',
            facecolor='#f1f5f9', edgecolor='#cbd5e1', linewidth=0.6
        ))
        ax.text(x0 + 0.014, y_out + 0.023, 'Out:', ha='left', va='center', fontsize=6.0, fontweight='bold', color='#334155')
        ax.text(x0 + w0/2 + 0.008, y_out + 0.023, s['output_tensor'], ha='center', va='center', fontsize=6.0, fontweight='bold', color='#0f172a')

        # Bottom SLA / Tag
        y_tag = y_bottom + 0.010
        ax.add_patch(patches.FancyBboxPatch(
            (x0 + 0.006, y_tag), w0 - 0.012, 0.036,
            boxstyle='round,pad=0.002,rounding_size=0.004',
            facecolor='#ffffff', edgecolor=s['border'], linewidth=0.7
        ))
        ax.text(x0 + w0/2, y_tag + 0.018, s['sla_tag'], ha='center', va='center', fontsize=5.5, fontweight='bold', color=s['badge_bg'])

    # Connecting Flow Arrows between stages
    arrow_y = y_bottom + card_h / 2
    for x_start, x_end in [(0.243, 0.255), (0.489, 0.501), (0.735, 0.747)]:
        ax.annotate('', xy=(x_end, arrow_y), xytext=(x_start, arrow_y),
                    arrowprops=dict(arrowstyle='->', color='#64748b', lw=1.2, mutation_scale=9))

    plt.tight_layout()
    for d in OUT_DIRS:
        fig.savefig(d / "fig6_system_architecture.pdf", bbox_inches='tight', pad_inches=0.01)
        fig.savefig(d / "fig6_system_architecture.eps", format='eps', bbox_inches='tight', pad_inches=0.01)
        fig.savefig(d / "fig6_system_architecture.png", dpi=300, bbox_inches='tight', pad_inches=0.01)
        shutil.copyfile(d / "fig6_system_architecture.pdf", d / "pipeline_cstgb.pdf")
        shutil.copyfile(d / "fig6_system_architecture.eps", d / "pipeline_cstgb.eps")
        shutil.copyfile(d / "fig6_system_architecture.pdf", d / "arch_triband.pdf")
        shutil.copyfile(d / "fig6_system_architecture.eps", d / "arch_triband.eps")
    plt.close(fig)
    print("   [SUCCESS] Generated ultra-crisp vector PDF & EPS across all target folders!")

if __name__ == '__main__':
    generate_figure_1()
