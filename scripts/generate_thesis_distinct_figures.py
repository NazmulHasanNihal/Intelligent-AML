"""
generate_thesis_distinct_figures.py — Generates distinct research-grade diagrams for:
- Fig 3.1: C-STGB Tensor Flow and Computational Data-Path (fig3_1_tensor_flow)
- Fig 4.1: DuckDB / PyArrow Zero-Copy Streaming Ingestion Pipeline (fig4_1_duckdb_arrow_pipeline)
- Fig 8.1: Enterprise FastAPI & Kubernetes Production Topology (fig8_1_fastapi_k8s_topology)
"""

import sys
from pathlib import Path
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
thesis_fig_dir = BASE_DIR / "papers" / "University_CSE_Thesis" / "figures"
data_fig_dir = BASE_DIR / "data" / "outputs" / "figures"
TARGET_DIRS = [thesis_fig_dir, data_fig_dir]

for d in TARGET_DIRS:
    d.mkdir(parents=True, exist_ok=True)


def save_fig(fig, stem):
    for d in TARGET_DIRS:
        fig.savefig(d / f"{stem}.pdf", bbox_inches="tight", pad_inches=0.04)
        fig.savefig(d / f"{stem}.png", dpi=300, bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)
    print(f" [OK] Generated: {stem}.pdf & .png")


# ==============================================================================
# 1. FIG 3.1: TENSOR FLOW & COMPUTATIONAL DATA-PATH (7.16" x 3.40")
# ==============================================================================
print("Generating Fig 3.1: C-STGB Tensor Flow...")
fig, ax = plt.subplots(figsize=(7.16, 3.40))
ax.axis('off')
ax.set_xlim([-0.005, 1.005])
ax.set_ylim([-0.008, 1.008])

# Base border
ax.add_patch(patches.FancyBboxPatch(
    (0.00, 0.00), 1.00, 1.00,
    boxstyle='round,pad=0.004,rounding_size=0.008',
    facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=0.8
))

# Header banner
ax.add_patch(patches.FancyBboxPatch(
    (0.008, 0.916), 0.984, 0.076,
    boxstyle='round,pad=0.003,rounding_size=0.006',
    facecolor='#0f172a', edgecolor='#0f172a', linewidth=0.5
))
ax.text(0.50, 0.954, 'C-STGB Computational Tensor Flow: End-to-End Deep Architectural Pipeline',
        ha='center', va='center', fontsize=9.2, fontweight='bold', color='#ffffff')

stages_31 = [
    {
        'id': 'STEP 1: INVARIANT TENSORS',
        'title': '12-D Canonical Space',
        'badge_bg': '#1e3a8a', 'badge_fg': '#dbeafe', 'card_bg': '#f8fafc', 'border': '#93c5fd',
        'x': 0.010, 'w': 0.233,
        'blocks': [
            {'head': 'Graph Ingress & History', 'math': r'$G_t = (V_t, E_t), \; \mathbf{X} \in \mathbb{R}^{|V| \times d_v}$', 'desc': 'Chronological window slicing'},
            {'head': 'Kirchhoff Mass Balance', 'math': r'$\tilde{\Phi}_{\mathrm{flow}} = \log(1 + \Phi_{\mathrm{flow}}(u,t))$', 'desc': 'Conduit flow conservation'},
            {'head': 'Hawkes Burst & Taint', 'math': r'$\lambda_u(t) = \mu_u + \sum \alpha e^{-\beta \Delta t}$', 'desc': 'Forward/reverse PageRank taint'}
        ],
        'out': r'$\mathbf{z}_{\mathrm{inv}}(u,t) \in \mathbb{R}^{12}$',
        'tag': 'Canonical Physics-Guided Invariants'
    },
    {
        'id': 'STEP 2: TEMPORAL GNN',
        'title': 'BurstAwareHGT & Edge Gate',
        'badge_bg': '#065f46', 'badge_fg': '#dcfce7', 'card_bg': '#f8fafc', 'border': '#86efac',
        'x': 0.256, 'w': 0.233,
        'blocks': [
            {'head': 'Tri-Band Harmonic Kernel', 'math': r'$\Phi_{\mathrm{time}}(\Delta t), \; w(\Delta t) \in \mathbb{R}^3$', 'desc': 'Seconds to 90-day dormancy'},
            {'head': 'Context Edge-Trust Gate', 'math': r'$\hat{g}_{ij} = \delta_{\mathrm{fl}} + (1 - \delta_{\mathrm{fl}}) g_{ij}$', 'desc': 'Prunes 65.9% camouflage chaff'},
            {'head': 'Brody GATv2 Convolutions', 'math': r'$\mathbf{h}_u^{(l+1)} = \sigma(\sum \alpha_{uv} \mathbf{W}_V \mathbf{h}_v^{(l)})$', 'desc': 'Jumping Knowledge JK-cat'}
        ],
        'out': r'$\mathbf{h}_u^{(L)} \in \mathbb{R}^d$ (Graph Latent)',
        'tag': 'Spatiotemporal Representation'
    },
    {
        'id': 'STEP 3: GRAPH-SMOTE & FUSION',
        'title': 'Bilinear Link & Adaptive Gate',
        'badge_bg': '#9a3412', 'badge_fg': '#ffedd5', 'card_bg': '#f8fafc', 'border': '#fdba74',
        'x': 0.502, 'w': 0.233,
        'blocks': [
            {'head': 'Typology Latent SMOTE', 'math': r'$\mathbf{h}_{\mathrm{syn}} = (1-\rho)\mathbf{h}_u + \rho\mathbf{h}_v, \; u,v \in C_k$', 'desc': 'Minority manifold clustering'},
            {'head': 'Bilinear Link Predictor', 'math': r'$\hat{\mathbf{A}}_{\mathrm{syn}} = \sigma(\mathbf{h}_{\mathrm{syn}}^T \mathbf{W}_{\mathrm{edge}} \mathbf{h}_w)$', 'desc': 'Quarantined to Train Split'},
            {'head': 'Evidence Fusion Gate', 'math': r'$\alpha_u = \sigma(\mathbf{w}_\alpha^T [\mathbf{h}_u \,\|\, \mathbf{z}_{\mathrm{inv}}] + b_\alpha)$', 'desc': 'Cold-start: 89.60% F1 preserved'}
        ],
        'out': r'$\mathbf{h}_u^* = \alpha_u \mathbf{h}_u + (1-\alpha_u)\mathbf{z}_{\mathrm{inv}}$',
        'tag': 'Fused Cold-Start Immune Space'
    },
    {
        'id': 'STEP 4: META-STACK & CRC',
        'title': 'ResMLPNet & 3-Tier CRC',
        'badge_bg': '#4c1d95', 'badge_fg': '#f3e8ff', 'card_bg': '#f8fafc', 'border': '#d8b4fe',
        'x': 0.748, 'w': 0.242,
        'blocks': [
            {'head': 'ResMLPNet Meta-Learner', 'math': r'18-D Meta: $\mathrm{KL}(p_{\mathrm{tree}} \,\|\, p_{\mathrm{gnn}})$', 'desc': 'Stream 1 + Stream 2 + Stream 3'},
            {'head': 'Cost-Sensitive Bayes Head', 'math': r'$\tau^* = \arg\min_\tau (15 \cdot \mathrm{FN} + 1 \cdot \mathrm{FP})$', 'desc': 'Asymmetric legal risk loss'},
            {'head': 'Class-Conditional CRC', 'math': r'$\hat{q}^{(0)}, \hat{q}^{(1)} \to 1-\alpha \geq 0.99$', 'desc': '3-Tier: T1 / T2 Review / T3 STP'}
        ],
        'out': r'$\hat{p}_u \in [0, 1], \; \Gamma(u) \subseteq \{0, 1\}$',
        'tag': 'Finite-Sample Conformal Triage'
    }
]

y_bottom = 0.018
card_h = 0.885

for s in stages_31:
    x0, w0 = s['x'], s['w']
    ax.add_patch(patches.FancyBboxPatch(
        (x0, y_bottom), w0, card_h,
        boxstyle='round,pad=0.005,rounding_size=0.008',
        facecolor=s['card_bg'], edgecolor=s['border'], linewidth=1.1
    ))
    ax.add_patch(patches.FancyBboxPatch(
        (x0 + 0.005, y_bottom + card_h - 0.088), w0 - 0.010, 0.082,
        boxstyle='round,pad=0.003,rounding_size=0.006',
        facecolor=s['badge_bg'], edgecolor=s['badge_bg'], linewidth=0.5
    ))
    ax.text(x0 + w0/2, y_bottom + card_h - 0.028, s['id'], ha='center', va='center', fontsize=6.5, fontweight='bold', color='#ffffff')
    ax.text(x0 + w0/2, y_bottom + card_h - 0.062, s['title'], ha='center', va='center', fontsize=5.8, color=s['badge_fg'], style='italic')

    block_h = 0.208
    y_top = y_bottom + card_h - 0.102
    for i, b in enumerate(s['blocks']):
        y_blk = y_top - (i * (block_h + 0.014)) - block_h
        ax.add_patch(patches.FancyBboxPatch(
            (x0 + 0.006, y_blk), w0 - 0.012, block_h,
            boxstyle='round,pad=0.003,rounding_size=0.005',
            facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=0.65
        ))
        ax.plot([x0 + 0.014], [y_blk + block_h - 0.032], marker='s', markersize=3.0, color=s['badge_bg'])
        ax.text(x0 + 0.022, y_blk + block_h - 0.032, b['head'], ha='left', va='center', fontsize=5.8, fontweight='bold', color='#0f172a')
        ax.text(x0 + w0/2, y_blk + block_h - 0.104, b['math'], ha='center', va='center', fontsize=5.7, color='#0f172a',
                bbox=dict(boxstyle='round,pad=0.12', facecolor='#f8fafc', edgecolor='#e2e8f0', lw=0.4))
        ax.text(x0 + w0/2, y_blk + 0.034, b['desc'], ha='center', va='center', fontsize=5.1, color='#475569')

    y_out = y_bottom + 0.052
    ax.add_patch(patches.FancyBboxPatch((x0 + 0.006, y_out), w0 - 0.012, 0.046, boxstyle='round,pad=0.003,rounding_size=0.004', facecolor='#f1f5f9', edgecolor='#cbd5e1', linewidth=0.6))
    ax.text(x0 + 0.014, y_out + 0.023, 'Out:', ha='left', va='center', fontsize=5.4, fontweight='bold', color='#334155')
    ax.text(x0 + w0/2 + 0.008, y_out + 0.023, s['out'], ha='center', va='center', fontsize=5.6, fontweight='bold', color='#0f172a')

    y_tag = y_bottom + 0.010
    ax.add_patch(patches.FancyBboxPatch((x0 + 0.006, y_tag), w0 - 0.012, 0.036, boxstyle='round,pad=0.002,rounding_size=0.004', facecolor='#ffffff', edgecolor=s['border'], linewidth=0.7))
    ax.text(x0 + w0/2, y_tag + 0.018, s['tag'], ha='center', va='center', fontsize=5.1, fontweight='bold', color=s['badge_bg'])

arrow_y = y_bottom + card_h / 2
for x_start, x_end in [(0.243, 0.255), (0.489, 0.501), (0.735, 0.747)]:
    ax.annotate('', xy=(x_end, arrow_y), xytext=(x_start, arrow_y),
                arrowprops=dict(arrowstyle='->', color='#64748b', lw=1.2, mutation_scale=9))

plt.subplots_adjust(left=0.005, right=0.995, top=0.99, bottom=0.01)
save_fig(fig, "fig3_1_tensor_flow")


# ==============================================================================
# 2. FIG 4.1: DUCKDB / ARROW STREAMING DATA PIPELINE (7.16" x 3.40")
# ==============================================================================
print("Generating Fig 4.1: DuckDB / Arrow Streaming Ingestion Pipeline...")
fig, ax = plt.subplots(figsize=(7.16, 3.40))
ax.axis('off')
ax.set_xlim([-0.005, 1.005])
ax.set_ylim([-0.008, 1.008])

ax.add_patch(patches.FancyBboxPatch(
    (0.00, 0.00), 1.00, 1.00,
    boxstyle='round,pad=0.004,rounding_size=0.008',
    facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=0.8
))

ax.add_patch(patches.FancyBboxPatch(
    (0.008, 0.916), 0.984, 0.076,
    boxstyle='round,pad=0.003,rounding_size=0.006',
    facecolor='#0f172a', edgecolor='#0f172a', linewidth=0.5
))
ax.text(0.50, 0.954, 'Vectorized Omni-Channel Streaming Data Pipeline: DuckDB, PyArrow & LRU Subgraph Cache',
        ha='center', va='center', fontsize=9.2, fontweight='bold', color='#ffffff')

stages_41 = [
    {
        'id': 'TIER 1: MULTI-RAIL INGRESS',
        'title': 'Banking Message Stream',
        'badge_bg': '#0f766e', 'badge_fg': '#ccfbf1', 'card_bg': '#f8fafc', 'border': '#5eead4',
        'x': 0.010, 'w': 0.233,
        'blocks': [
            {'head': 'SWIFT MT103 / MT700 (LC)', 'math': 'Tag 32A, 50K, 59 (ISO 20022)', 'desc': 'Cross-border wire & trade LC'},
            {'head': 'Domestic RTGS & BEFTN', 'math': '18-Digit TrxRef / Batch ACH', 'desc': 'Real-time gross settlement'},
            {'head': 'Mobile Money (bKash/Nagad)', 'math': 'Micro-Deposits, High Velocity', 'desc': '31,200+ msg/s Kafka / Redpanda'}
        ],
        'out': r'Raw Stream $S_{\mathrm{tx}}$ (Ingress)',
        'tag': 'Multi-Rail Financial Protocols'
    },
    {
        'id': 'TIER 2: DUCKDB ENGINE',
        'title': 'Columnar SQL & Invariants',
        'badge_bg': '#c2410c', 'badge_fg': '#ffedd5', 'card_bg': '#f8fafc', 'border': '#fdba74',
        'x': 0.256, 'w': 0.233,
        'blocks': [
            {'head': 'Vectorized Schema Discovery', 'math': 'DuckDB Zero-Copy Parquet/SQL', 'desc': 'Dynamic schema normalization'},
            {'head': '12-D Invariant SQL Kernel', 'math': r'$\sum A_{\mathrm{out}} / (\sum A_{\mathrm{in}} + \epsilon)$', 'desc': 'Vectorized mass-balance flow'},
            {'head': 'Causal Temporal Slicing', 'math': r'Window: $t_e \in [t - W_{\mathrm{ego}}, t]$', 'desc': 'Zero lookahead forward leak'}
        ],
        'out': r'Relational Invariants $\mathbf{Z}_{\mathrm{inv}}$',
        'tag': 'Columnar Analytical Execution'
    },
    {
        'id': 'TIER 3: PYARROW ZERO-COPY',
        'title': 'RecordBatch C-Interface',
        'badge_bg': '#1d4ed8', 'badge_fg': '#dbeafe', 'card_bg': '#f8fafc', 'border': '#93c5fd',
        'x': 0.502, 'w': 0.233,
        'blocks': [
            {'head': 'Zero-Copy Shared Memory', 'math': r'PyArrow RecordBatch $\to$ Tensor', 'desc': '0.12 ms IPC serialization bypass'},
            {'head': 'Ego-Graph Construction', 'math': r'Neighborhood: $\mathcal{N}_K(u)$', 'desc': '2-hop neighborhood extraction'},
            {'head': 'Hawkes Point Intensity', 'math': r'Recurrence: $\lambda_u(t)$ Vectorized', 'desc': 'Sub-millisecond update rate'}
        ],
        'out': 'HeteroData PyG Tensor Graph',
        'tag': 'Zero-Copy Memory Transport'
    },
    {
        'id': 'TIER 4: LRU CAUSAL CACHE',
        'title': 'Fast-Path Memory Store',
        'badge_bg': '#047857', 'badge_fg': '#d1fae5', 'card_bg': '#f8fafc', 'border': '#6ee7b7',
        'x': 0.748, 'w': 0.242,
        'blocks': [
            {'head': '2-Hop Ego In-Memory Cache', 'math': '100k Node Capacity, LRU', 'desc': '88.4% Cache hit rate in live tests'},
            {'head': 'Sub-Millisecond Fast-Path', 'math': 'Latency: 0.45 ms Hit vs 2.1 ms', 'desc': 'Thread-safe RLock concurrency'},
            {'head': 'Online Graph Eviction', 'math': 'OrderedDict + Adjacency Index', 'desc': 'Continuous streaming state'}
        ],
        'out': r'Ego Subgraph $G_t^{(K)}(u)$',
        'tag': 'Sub-10ms Banking SLA Guaranteed'
    }
]

for s in stages_41:
    x0, w0 = s['x'], s['w']
    ax.add_patch(patches.FancyBboxPatch(
        (x0, y_bottom), w0, card_h,
        boxstyle='round,pad=0.005,rounding_size=0.008',
        facecolor=s['card_bg'], edgecolor=s['border'], linewidth=1.1
    ))
    ax.add_patch(patches.FancyBboxPatch(
        (x0 + 0.005, y_bottom + card_h - 0.088), w0 - 0.010, 0.082,
        boxstyle='round,pad=0.003,rounding_size=0.006',
        facecolor=s['badge_bg'], edgecolor=s['badge_bg'], linewidth=0.5
    ))
    ax.text(x0 + w0/2, y_bottom + card_h - 0.028, s['id'], ha='center', va='center', fontsize=6.5, fontweight='bold', color='#ffffff')
    ax.text(x0 + w0/2, y_bottom + card_h - 0.062, s['title'], ha='center', va='center', fontsize=5.8, color=s['badge_fg'], style='italic')

    block_h = 0.208
    y_top = y_bottom + card_h - 0.102
    for i, b in enumerate(s['blocks']):
        y_blk = y_top - (i * (block_h + 0.014)) - block_h
        ax.add_patch(patches.FancyBboxPatch(
            (x0 + 0.006, y_blk), w0 - 0.012, block_h,
            boxstyle='round,pad=0.003,rounding_size=0.005',
            facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=0.65
        ))
        ax.plot([x0 + 0.014], [y_blk + block_h - 0.032], marker='s', markersize=3.0, color=s['badge_bg'])
        ax.text(x0 + 0.022, y_blk + block_h - 0.032, b['head'], ha='left', va='center', fontsize=5.8, fontweight='bold', color='#0f172a')
        ax.text(x0 + w0/2, y_blk + block_h - 0.104, b['math'], ha='center', va='center', fontsize=5.7, color='#0f172a',
                bbox=dict(boxstyle='round,pad=0.12', facecolor='#f8fafc', edgecolor='#e2e8f0', lw=0.4))
        ax.text(x0 + w0/2, y_blk + 0.034, b['desc'], ha='center', va='center', fontsize=5.1, color='#475569')

    y_out = y_bottom + 0.052
    ax.add_patch(patches.FancyBboxPatch((x0 + 0.006, y_out), w0 - 0.012, 0.046, boxstyle='round,pad=0.003,rounding_size=0.004', facecolor='#f1f5f9', edgecolor='#cbd5e1', linewidth=0.6))
    ax.text(x0 + 0.014, y_out + 0.023, 'Out:', ha='left', va='center', fontsize=5.4, fontweight='bold', color='#334155')
    ax.text(x0 + w0/2 + 0.008, y_out + 0.023, s['out'], ha='center', va='center', fontsize=5.6, fontweight='bold', color='#0f172a')

    y_tag = y_bottom + 0.010
    ax.add_patch(patches.FancyBboxPatch((x0 + 0.006, y_tag), w0 - 0.012, 0.036, boxstyle='round,pad=0.002,rounding_size=0.004', facecolor='#ffffff', edgecolor=s['border'], linewidth=0.7))
    ax.text(x0 + w0/2, y_tag + 0.018, s['tag'], ha='center', va='center', fontsize=5.1, fontweight='bold', color=s['badge_bg'])

arrow_y = y_bottom + card_h / 2
for x_start, x_end in [(0.243, 0.255), (0.489, 0.501), (0.735, 0.747)]:
    ax.annotate('', xy=(x_end, arrow_y), xytext=(x_start, arrow_y),
                arrowprops=dict(arrowstyle='->', color='#64748b', lw=1.2, mutation_scale=9))

plt.subplots_adjust(left=0.005, right=0.995, top=0.99, bottom=0.01)
save_fig(fig, "fig4_1_duckdb_arrow_pipeline")


# ==============================================================================
# 3. FIG 8.1: FASTAPI & KUBERNETES PRODUCTION TOPOLOGY (7.16" x 3.40")
# ==============================================================================
print("Generating Fig 8.1: Enterprise FastAPI & Kubernetes Production Topology...")
fig, ax = plt.subplots(figsize=(7.16, 3.40))
ax.axis('off')
ax.set_xlim([-0.005, 1.005])
ax.set_ylim([-0.008, 1.008])

ax.add_patch(patches.FancyBboxPatch(
    (0.00, 0.00), 1.00, 1.00,
    boxstyle='round,pad=0.004,rounding_size=0.008',
    facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=0.8
))

ax.add_patch(patches.FancyBboxPatch(
    (0.008, 0.916), 0.984, 0.076,
    boxstyle='round,pad=0.003,rounding_size=0.006',
    facecolor='#0f172a', edgecolor='#0f172a', linewidth=0.5
))
ax.text(0.50, 0.954, 'Enterprise Cloud-Native Deployment Topology: FastAPI Microservices, Kubernetes & WORM Vault',
        ha='center', va='center', fontsize=9.2, fontweight='bold', color='#ffffff')

stages_81 = [
    {
        'id': 'INGRESS & SECURITY TIER',
        'title': 'TLS 1.3 & API Gateway',
        'badge_bg': '#334155', 'badge_fg': '#f1f5f9', 'card_bg': '#f8fafc', 'border': '#94a3b8',
        'x': 0.010, 'w': 0.233,
        'blocks': [
            {'head': 'Core Banking System (CBS)', 'math': 'Temenos T24 / Finacle / Flexcube', 'desc': 'ISO 20022 clearing webhooks'},
            {'head': 'Nginx / Envoy Ingress', 'math': 'mTLS 1.3, Rate-Limit, WAF', 'desc': 'Path sanitization & anti-CSRF'},
            {'head': 'JWT Authentication & RBAC', 'math': 'Maker, Checker, Compliance Auditor', 'desc': 'Four-Eyes Dual Sign-Off gate'}
        ],
        'out': 'Authenticated REST/WS Streams',
        'tag': 'Zero-Trust Banking Boundary'
    },
    {
        'id': 'FASTAPI WORKER POOL',
        'title': 'Asynchronous Orchestration',
        'badge_bg': '#0284c7', 'badge_fg': '#e0f2fe', 'card_bg': '#f8fafc', 'border': '#7dd3fc',
        'x': 0.256, 'w': 0.233,
        'blocks': [
            {'head': 'FastAPI Async Engine', 'math': 'Uvicorn ASGI Workers, Python 3.12', 'desc': 'Sub-millisecond routing loop'},
            {'head': 'Fast-Path LRU Subgraph L1', 'math': 'Capacity: 100k, 0.45 ms Hit', 'desc': 'Distributed Redis L2 Cache'},
            {'head': '3-Tier Conformal Arbiter', 'math': 'Zero-Divergence Operational Triage', 'desc': 'Instant Tier-3 STP Auto-Clear'}
        ],
        'out': 'Triage Verdict: T1 / T2 / T3',
        'tag': 'High-Throughput Microservice Tier'
    },
    {
        'id': 'INFERENCE & AGENT SWARM',
        'title': 'C-STGB Pods & 4 AI Detectives',
        'badge_bg': '#7c3aed', 'badge_fg': '#ede9fe', 'card_bg': '#f8fafc', 'border': '#c4b5fd',
        'x': 0.502, 'w': 0.233,
        'blocks': [
            {'head': 'C-STGB Neural Pods', 'math': 'Triton / TorchScript Inference', 'desc': 'Zero-GPU commodity CPU native'},
            {'head': 'Autonomous 4-Agent Swarm', 'math': r'Investigator $\to$ Drafter $\to$ Auditor', 'desc': 'Sub-30s regulatory dossier'},
            {'head': 'Compiler AST Grammar', 'math': r'$\mathcal{V}(\mathcal{T}) \subseteq \mathcal{V}_{\mathrm{sub}}$ (Prop 6.1)', 'desc': '0% AI entity hallucination'}
        ],
        'out': 'Sealed SAR/STR Regulatory Dossier',
        'tag': 'Deterministic AI Investigation'
    },
    {
        'id': 'GOVERNANCE & CLIENT TIER',
        'title': 'WORM Ledger & React 18 UI',
        'badge_bg': '#059669', 'badge_fg': '#d1fae5', 'card_bg': '#f8fafc', 'border': '#6ee7b7',
        'x': 0.748, 'w': 0.242,
        'blocks': [
            {'head': 'Cryptographic WORM Vault', 'math': 'SHA-256 Merkle Receipts (FRE 902(11))', 'desc': 'Immutable tamper-evident ledger'},
            {'head': 'PostgreSQL Cold Archival', 'math': 'Case Management & Audit Trail', 'desc': 'Statutory SLA countdown docket'},
            {'head': 'React 18 Command Center', 'math': 'Cytoscape 2D + Three.js 3D WebGL', 'desc': 'Real-time WebSocket telemetry'}
        ],
        'out': 'Court-Admissible Evidentiary Record',
        'tag': 'Federal Reserve SR 26-2 Aligned'
    }
]

for s in stages_81:
    x0, w0 = s['x'], s['w']
    ax.add_patch(patches.FancyBboxPatch(
        (x0, y_bottom), w0, card_h,
        boxstyle='round,pad=0.005,rounding_size=0.008',
        facecolor=s['card_bg'], edgecolor=s['border'], linewidth=1.1
    ))
    ax.add_patch(patches.FancyBboxPatch(
        (x0 + 0.005, y_bottom + card_h - 0.088), w0 - 0.010, 0.082,
        boxstyle='round,pad=0.003,rounding_size=0.006',
        facecolor=s['badge_bg'], edgecolor=s['badge_bg'], linewidth=0.5
    ))
    ax.text(x0 + w0/2, y_bottom + card_h - 0.028, s['id'], ha='center', va='center', fontsize=6.5, fontweight='bold', color='#ffffff')
    ax.text(x0 + w0/2, y_bottom + card_h - 0.062, s['title'], ha='center', va='center', fontsize=5.8, color=s['badge_fg'], style='italic')

    block_h = 0.208
    y_top = y_bottom + card_h - 0.102
    for i, b in enumerate(s['blocks']):
        y_blk = y_top - (i * (block_h + 0.014)) - block_h
        ax.add_patch(patches.FancyBboxPatch(
            (x0 + 0.006, y_blk), w0 - 0.012, block_h,
            boxstyle='round,pad=0.003,rounding_size=0.005',
            facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=0.65
        ))
        ax.plot([x0 + 0.014], [y_blk + block_h - 0.032], marker='s', markersize=3.0, color=s['badge_bg'])
        ax.text(x0 + 0.022, y_blk + block_h - 0.032, b['head'], ha='left', va='center', fontsize=5.8, fontweight='bold', color='#0f172a')
        ax.text(x0 + w0/2, y_blk + block_h - 0.104, b['math'], ha='center', va='center', fontsize=5.7, color='#0f172a',
                bbox=dict(boxstyle='round,pad=0.12', facecolor='#f8fafc', edgecolor='#e2e8f0', lw=0.4))
        ax.text(x0 + w0/2, y_blk + 0.034, b['desc'], ha='center', va='center', fontsize=5.1, color='#475569')

    y_out = y_bottom + 0.052
    ax.add_patch(patches.FancyBboxPatch((x0 + 0.006, y_out), w0 - 0.012, 0.046, boxstyle='round,pad=0.003,rounding_size=0.004', facecolor='#f1f5f9', edgecolor='#cbd5e1', linewidth=0.6))
    ax.text(x0 + 0.014, y_out + 0.023, 'Out:', ha='left', va='center', fontsize=5.4, fontweight='bold', color='#334155')
    ax.text(x0 + w0/2 + 0.008, y_out + 0.023, s['out'], ha='center', va='center', fontsize=5.6, fontweight='bold', color='#0f172a')

    y_tag = y_bottom + 0.010
    ax.add_patch(patches.FancyBboxPatch((x0 + 0.006, y_tag), w0 - 0.012, 0.036, boxstyle='round,pad=0.002,rounding_size=0.004', facecolor='#ffffff', edgecolor=s['border'], linewidth=0.7))
    ax.text(x0 + w0/2, y_tag + 0.018, s['tag'], ha='center', va='center', fontsize=5.1, fontweight='bold', color=s['badge_bg'])

arrow_y = y_bottom + card_h / 2
for x_start, x_end in [(0.243, 0.255), (0.489, 0.501), (0.735, 0.747)]:
    ax.annotate('', xy=(x_end, arrow_y), xytext=(x_start, arrow_y),
                arrowprops=dict(arrowstyle='->', color='#64748b', lw=1.2, mutation_scale=9))

plt.subplots_adjust(left=0.005, right=0.995, top=0.99, bottom=0.01)
save_fig(fig, "fig8_1_fastapi_k8s_topology")

print("All distinct architecture figures successfully generated!")
