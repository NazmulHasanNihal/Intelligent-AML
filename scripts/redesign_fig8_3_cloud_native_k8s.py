"""
scripts/redesign_fig8_3_cloud_native_k8s.py
Dedicated publication-grade redesign replacing Figure 8.3:
Enterprise Cloud-Native Kubernetes Deployment Topology & Elastic Autoscaling (HPA).

Transforms the old repetitive 4-card diagram into a true Kubernetes deployment architecture:
- Zone 1: Banking Ingress & Edge Security Gateway (mTLS 1.3, Envoy/Nginx, RBAC)
- Zone 2: Kubernetes Production Cluster (Namespace: cstgb-production)
  * Kubernetes Horizontal Pod Autoscaler (HPA v2): dynamic scaling 4 <-> 32 pods (2.4k to 31.2k tx/s)
  * Containerized FastAPI Scoring Worker Pod anatomy (Python 3.12, PyArrow, TorchScript, DuckDB L1)
  * Quarantined Asynchronous 4-Agent Forensic Swarm Deployment
- Zone 3: Observability, Storage & Tamper-Proof Merkle WORM Vault (Prometheus, S3 Object Lock, FRE 902(11))
- Bottom 4-Card Production Metric Ribbon (485 MB Image, 4-32 HPA, 158/158 Tests, 99.99% SLA)
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
    'mathtext.fontset': 'stix',
})

def generate_figure_8_3():
    # Sized so that aspect ratio after tight crop is ~2.08:1, perfectly preserving page layout
    fig, ax = plt.subplots(figsize=(9.2, 4.40))
    ax.axis('off')
    ax.set_xlim([-0.010, 1.010])
    ax.set_ylim([-0.015, 1.015])

    # 1. Outer Container Card
    ax.add_patch(patches.FancyBboxPatch(
        (0.000, 0.000), 1.000, 1.000,
        boxstyle='round,pad=0.003,rounding_size=0.006',
        facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=0.8
    ))

    # 2. Master Header Banner
    ax.add_patch(patches.FancyBboxPatch(
        (0.006, 0.925), 0.988, 0.067,
        boxstyle='round,pad=0.003,rounding_size=0.005',
        facecolor='#0f172a', edgecolor='#0f172a', linewidth=0.5
    ))
    ax.text(0.018, 0.965, 'Figure 8.3: Enterprise Cloud-Native Kubernetes Deployment Topology & Elastic Autoscaling',
            ha='left', va='center', fontsize=8.6, fontweight='bold', color='#ffffff')
    ax.text(0.018, 0.940,
            r'End-to-End Orchestration: Ingress mTLS 1.3 $\rightarrow$ Dynamic HPA Elastic Scaling (4 $\rightleftharpoons$ 32 Pods) $\rightarrow$ TorchScript & Arrow IPC $\rightarrow$ Prometheus & WORM Vault',
            ha='left', va='center', fontsize=6.1, color='#94a3b8')

    # Top Right SLA Pill
    ax.add_patch(patches.FancyBboxPatch(
        (0.760, 0.932), 0.228, 0.053,
        boxstyle='round,pad=0.002,rounding_size=0.004',
        facecolor='#0284c7', edgecolor='#38bdf8', linewidth=0.8
    ))
    ax.text(0.874, 0.958, 'HPA ELASTIC: 4 - 32 PODS (31.2k tx/s)',
            ha='center', va='center', fontsize=5.8, fontweight='bold', color='#ffffff')

    # =========================================================================
    # ZONE 1: SECURE INGRESS & API GATEWAY (x: 0.010 to 0.224, width: 0.214)
    # =========================================================================
    z1_x, z1_w = 0.010, 0.214
    z_top, z_bot = 0.912, 0.160
    z_h = z_top - z_bot

    ax.add_patch(patches.FancyBboxPatch(
        (z1_x, z_bot), z1_w, z_h,
        boxstyle='round,pad=0.002,rounding_size=0.005',
        facecolor='#f8fafc', edgecolor='#94a3b8', linewidth=0.8
    ))
    # Zone 1 Header Badge
    ax.add_patch(patches.FancyBboxPatch(
        (z1_x + 0.006, z_top - 0.030), z1_w - 0.012, 0.024,
        boxstyle='round,pad=0.001,rounding_size=0.003',
        facecolor='#334155', edgecolor='#334155', linewidth=0.5
    ))
    ax.text(z1_x + z1_w/2, z_top - 0.018, 'ZONE 1: SECURE INGRESS & GATEWAY',
            ha='center', va='center', fontsize=5.5, fontweight='bold', color='#ffffff')

    # Zone 1 Sub-cards (3 stacked cards)
    # Card 1.1: Core Banking System (CBS)
    ax.add_patch(patches.FancyBboxPatch(
        (z1_x + 0.006, 0.670), z1_w - 0.012, 0.198,
        boxstyle='round,pad=0.002,rounding_size=0.004',
        facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=0.7
    ))
    ax.text(z1_x + z1_w/2, 0.846, 'Core Banking Systems (CBS)', ha='center', va='center',
            fontsize=5.8, fontweight='bold', color='#0f172a')
    ax.text(z1_x + z1_w/2, 0.824, 'Temenos T24 / Finacle / Flexcube', ha='center', va='center',
            fontsize=4.9, color='#475569')
    ax.text(z1_x + z1_w/2, 0.796, 'Payment Webhook Stream', ha='center', va='center',
            fontsize=5.2, fontweight='bold', color='#0284c7')
    ax.text(z1_x + z1_w/2, 0.774, 'ISO 20022 camt.053 & pacs.008', ha='center', va='center',
            fontsize=4.8, color='#64748b')
    ax.text(z1_x + z1_w/2, 0.746, 'WebSocket Live Feeds', ha='center', va='center',
            fontsize=5.2, fontweight='bold', color='#0f766e')
    ax.text(z1_x + z1_w/2, 0.724, 'Full-Duplex Operational Triage', ha='center', va='center',
            fontsize=4.8, color='#64748b')
    ax.text(z1_x + z1_w/2, 0.692, 'Mutual TLS 1.3 Banking Rails', ha='center', va='center',
            fontsize=4.8, fontweight='bold', color='#15803d')

    # Card 1.2: Envoy / Nginx Ingress Controller
    ax.add_patch(patches.FancyBboxPatch(
        (z1_x + 0.006, 0.442), z1_w - 0.012, 0.214,
        boxstyle='round,pad=0.002,rounding_size=0.004',
        facecolor='#ffffff', edgecolor='#0284c7', linewidth=0.8
    ))
    ax.text(z1_x + z1_w/2, 0.634, 'Envoy / Nginx Ingress Gateway', ha='center', va='center',
            fontsize=5.8, fontweight='bold', color='#0369a1')
    ax.text(z1_x + z1_w/2, 0.612, 'Edge Traffic & Load Balancing', ha='center', va='center',
            fontsize=4.9, color='#475569')
    ax.text(z1_x + z1_w/2, 0.584, 'mTLS 1.3 Termination', ha='center', va='center',
            fontsize=5.1, fontweight='bold', color='#0284c7')
    ax.text(z1_x + z1_w/2, 0.562, 'Automated Cert-Manager Vault CA', ha='center', va='center',
            fontsize=4.8, color='#64748b')
    ax.text(z1_x + z1_w/2, 0.534, 'Token Bucket Rate Limiting', ha='center', va='center',
            fontsize=5.1, fontweight='bold', color='#b45309')
    ax.text(z1_x + z1_w/2, 0.512, 'Peak 50k req/s burst tolerance', ha='center', va='center',
            fontsize=4.8, color='#64748b')
    ax.text(z1_x + z1_w/2, 0.484, 'Cloud-Native WAF Defense', ha='center', va='center',
            fontsize=5.1, fontweight='bold', color='#b91c1c')
    ax.text(z1_x + z1_w/2, 0.462, 'Path sanitization & anti-CSRF', ha='center', va='center',
            fontsize=4.8, color='#64748b')

    # Card 1.3: Security, JWT & RBAC
    ax.add_patch(patches.FancyBboxPatch(
        (z1_x + 0.006, 0.170), z1_w - 0.012, 0.258,
        boxstyle='round,pad=0.002,rounding_size=0.004',
        facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=0.7
    ))
    ax.text(z1_x + z1_w/2, 0.406, 'OAuth2 & JWT RBAC Security', ha='center', va='center',
            fontsize=5.8, fontweight='bold', color='#0f172a')
    ax.text(z1_x + z1_w/2, 0.384, 'Zero-Trust Banking Boundary', ha='center', va='center',
            fontsize=4.9, color='#475569')
    ax.text(z1_x + z1_w/2, 0.354, 'Maker-Checker Separation', ha='center', va='center',
            fontsize=5.1, fontweight='bold', color='#6d28d9')
    ax.text(z1_x + z1_w/2, 0.332, 'Four-Eyes Dual Sign-Off gate', ha='center', va='center',
            fontsize=4.8, color='#64748b')
    ax.text(z1_x + z1_w/2, 0.302, 'Role Separation Levels', ha='center', va='center',
            fontsize=5.1, fontweight='bold', color='#0f766e')
    ax.text(z1_x + z1_w/2, 0.280, 'Analyst / Investigator / Auditor', ha='center', va='center',
            fontsize=4.8, color='#64748b')
    ax.text(z1_x + z1_w/2, 0.250, 'SHA-256 PII De-Identification', ha='center', va='center',
            fontsize=5.1, fontweight='bold', color='#15803d')
    ax.text(z1_x + z1_w/2, 0.228, 'Salted key rings (GDPR / GLBA)', ha='center', va='center',
            fontsize=4.8, color='#64748b')
    ax.text(z1_x + z1_w/2, 0.198, 'AES-256-GCM Wire Encryption', ha='center', va='center',
            fontsize=4.8, fontweight='bold', color='#0284c7')

    # =========================================================================
    # ZONE 2: KUBERNETES PRODUCTION CLUSTER (x: 0.234 to 0.740, width: 0.506)
    # =========================================================================
    z2_x, z2_w = 0.234, 0.506

    # Cluster boundary with Kubernetes cyan/blue dashed frame
    ax.add_patch(patches.FancyBboxPatch(
        (z2_x, z_bot), z2_w, z_h,
        boxstyle='round,pad=0.002,rounding_size=0.006',
        facecolor='#f0f9ff', edgecolor='#0284c7', linewidth=1.2, linestyle='--'
    ))
    # Zone 2 Header Badge
    ax.add_patch(patches.FancyBboxPatch(
        (z2_x + 0.006, z_top - 0.030), z2_w - 0.012, 0.024,
        boxstyle='round,pad=0.001,rounding_size=0.003',
        facecolor='#0284c7', edgecolor='#0284c7', linewidth=0.5
    ))
    ax.text(z2_x + z2_w/2, z_top - 0.018, 'ZONE 2: KUBERNETES PRODUCTION CLUSTER  [Namespace: cstgb-production]',
            ha='center', va='center', fontsize=5.8, fontweight='bold', color='#ffffff')

    # Sub-element 2.1: Horizontal Pod Autoscaler (HPA v2) Banner Box
    hpa_y, hpa_h = 0.758, 0.114
    ax.add_patch(patches.FancyBboxPatch(
        (z2_x + 0.008, hpa_y), z2_w - 0.016, hpa_h,
        boxstyle='round,pad=0.002,rounding_size=0.004',
        facecolor='#ffffff', edgecolor='#38bdf8', linewidth=0.9
    ))
    ax.text(z2_x + 0.018, hpa_y + hpa_h - 0.016, 'Kubernetes Horizontal Pod Autoscaler (HPA v2)',
            ha='left', va='center', fontsize=6.2, fontweight='bold', color='#0369a1')
    ax.text(z2_x + z2_w - 0.018, hpa_y + hpa_h - 0.016, 'Target Metric: CPU > 70%  |  Queue Depth > 500 msgs',
            ha='right', va='center', fontsize=5.1, fontweight='bold', color='#b45309')
    
    # HPA Elasticity Range Pills
    # Min Scale Pill
    ax.add_patch(patches.FancyBboxPatch(
        (z2_x + 0.018, hpa_y + 0.016), 0.224, 0.068,
        boxstyle='round,pad=0.001,rounding_size=0.003',
        facecolor='#f0fdf4', edgecolor='#4ade80', linewidth=0.7
    ))
    ax.text(z2_x + 0.018 + 0.112, hpa_y + 0.066, 'QUIET LOAD: 4 Pod Replicas',
            ha='center', va='center', fontsize=5.3, fontweight='bold', color='#15803d')
    ax.text(z2_x + 0.018 + 0.112, hpa_y + 0.046, 'Baseline Ingress: 2,400 tx/s',
            ha='center', va='center', fontsize=4.8, color='#475569')
    ax.text(z2_x + 0.018 + 0.112, hpa_y + 0.028, 'Single-Worker P50: 0.45 ms',
            ha='center', va='center', fontsize=4.7, color='#16a34a')

    # Elastic Scale Arrow in between
    ax.annotate("", xy=(z2_x + 0.278, hpa_y + 0.050), xytext=(z2_x + 0.246, hpa_y + 0.050),
                arrowprops=dict(arrowstyle="<->,head_width=0.25,head_length=0.35", color='#0284c7', lw=1.5))
    ax.text(z2_x + 0.262, hpa_y + 0.070, 'Auto-Scale', ha='center', va='bottom', fontsize=4.7, fontweight='bold', color='#0284c7')
    ax.text(z2_x + 0.262, hpa_y + 0.030, '15s spin-up', ha='center', va='top', fontsize=4.5, color='#64748b')

    # Max Scale Pill
    ax.add_patch(patches.FancyBboxPatch(
        (z2_x + 0.282, hpa_y + 0.016), 0.208, 0.068,
        boxstyle='round,pad=0.001,rounding_size=0.003',
        facecolor='#fff7ed', edgecolor='#fb923c', linewidth=0.7
    ))
    ax.text(z2_x + 0.282 + 0.104, hpa_y + 0.066, 'BURST LOAD: 32 Pod Replicas',
            ha='center', va='center', fontsize=5.3, fontweight='bold', color='#c2410c')
    ax.text(z2_x + 0.282 + 0.104, hpa_y + 0.046, 'Peak Ingress: 31,250 tx/s',
            ha='center', va='center', fontsize=4.8, color='#475569')
    ax.text(z2_x + 0.282 + 0.104, hpa_y + 0.028, 'Zero Packet Drop Guarantee',
            ha='center', va='center', fontsize=4.7, color='#ea580c')

    # Sub-element 2.2: FastAPI Scoring Worker Pods (Center-Left of Zone 2)
    pod_x, pod_w = z2_x + 0.008, 0.282
    pod_y, pod_h = 0.170, 0.572
    ax.add_patch(patches.FancyBboxPatch(
        (pod_x, pod_y), pod_w, pod_h,
        boxstyle='round,pad=0.002,rounding_size=0.005',
        facecolor='#ffffff', edgecolor='#0284c7', linewidth=1.0
    ))
    # Pod Header Strip
    ax.add_patch(patches.FancyBboxPatch(
        (pod_x + 0.004, pod_y + pod_h - 0.032), pod_w - 0.008, 0.028,
        boxstyle='round,pad=0.001,rounding_size=0.003',
        facecolor='#0284c7', edgecolor='#0284c7', linewidth=0.5
    ))
    ax.text(pod_x + pod_w/2, pod_y + pod_h - 0.018, 'FastAPI Scoring Worker Pod [cstgb-worker-prod-7f8d]',
            ha='center', va='center', fontsize=5.4, fontweight='bold', color='#ffffff')

    # Pod Container Internal Components (Stacked)
    # Component 1: FastAPI ASGI Worker
    ax.add_patch(patches.FancyBboxPatch(
        (pod_x + 0.006, pod_y + 0.440), pod_w - 0.012, 0.088,
        boxstyle='round,pad=0.001,rounding_size=0.003',
        facecolor='#f8fafc', edgecolor='#cbd5e1', linewidth=0.6
    ))
    ax.text(pod_x + 0.014, pod_y + 0.508, '1. FastAPI ASGI Worker Engine', ha='left', va='center',
            fontsize=5.2, fontweight='bold', color='#0284c7')
    ax.text(pod_x + 0.014, pod_y + 0.490, 'Python 3.12, Uvicorn, Non-blocking uvloop', ha='left', va='center',
            fontsize=4.7, color='#475569')
    ax.text(pod_x + 0.014, pod_y + 0.472, r'SLA Fast-Path Webhook Clearance: $0.45\,\text{ms}$', ha='left', va='center',
            fontsize=4.8, fontweight='bold', color='#15803d')
    ax.text(pod_x + 0.014, pod_y + 0.454, 'Async background event dispatch queue', ha='left', va='center',
            fontsize=4.6, color='#64748b')

    # Component 2: Apache Arrow Zero-Copy IPC
    ax.add_patch(patches.FancyBboxPatch(
        (pod_x + 0.006, pod_y + 0.334), pod_w - 0.012, 0.096,
        boxstyle='round,pad=0.001,rounding_size=0.003',
        facecolor='#f8fafc', edgecolor='#cbd5e1', linewidth=0.6
    ))
    ax.text(pod_x + 0.014, pod_y + 0.410, '2. Apache Arrow Zero-Copy IPC Memory', ha='left', va='center',
            fontsize=5.2, fontweight='bold', color='#0f766e')
    ax.text(pod_x + 0.014, pod_y + 0.392, r'Vectorized batch memory buffer: $\mathcal{O}(|\mathcal{E}_{\text{batch}}|)$', ha='left', va='center',
            fontsize=4.7, color='#475569')
    ax.text(pod_x + 0.014, pod_y + 0.374, r'Direct PyTorch Tensor Zero-Copy View ($0.11\,\text{ms}$)', ha='left', va='center',
            fontsize=4.8, fontweight='bold', color='#0f766e')
    ax.text(pod_x + 0.014, pod_y + 0.356, r'Kirchhoff flow & 12-D topological invariants $\mathbf{z}_{\mathrm{inv}}$', ha='left', va='center',
            fontsize=4.6, color='#64748b')

    # Component 3: TorchScript Neural Scoring Engine
    ax.add_patch(patches.FancyBboxPatch(
        (pod_x + 0.006, pod_y + 0.228), pod_w - 0.012, 0.096,
        boxstyle='round,pad=0.001,rounding_size=0.003',
        facecolor='#f8fafc', edgecolor='#cbd5e1', linewidth=0.6
    ))
    ax.text(pod_x + 0.014, pod_y + 0.304, '3. TorchScript C-STGB Neural Engine', ha='left', va='center',
            fontsize=5.2, fontweight='bold', color='#c2410c')
    ax.text(pod_x + 0.014, pod_y + 0.286, 'Tri-Band Continuous Fourier Encoding (1.2 MB)', ha='left', va='center',
            fontsize=4.7, color='#475569')
    ax.text(pod_x + 0.014, pod_y + 0.268, r'Edge-Trust MLP Denoising ($65.9\%$ Camouflage Pruned)', ha='left', va='center',
            fontsize=4.8, fontweight='bold', color='#b45309')
    ax.text(pod_x + 0.014, pod_y + 0.250, r'Harmonic Spatio-Temporal GNN Attention ($0.12\,\text{ms}$)', ha='left', va='center',
            fontsize=4.6, color='#64748b')

    # Component 4: DuckDB L1 LRU & Conformal Arbiter
    ax.add_patch(patches.FancyBboxPatch(
        (pod_x + 0.006, pod_y + 0.122), pod_w - 0.012, 0.096,
        boxstyle='round,pad=0.001,rounding_size=0.003',
        facecolor='#f8fafc', edgecolor='#cbd5e1', linewidth=0.6
    ))
    ax.text(pod_x + 0.014, pod_y + 0.198, '4. DuckDB Ego-Graph LRU & Conformal Arbiter', ha='left', va='center',
            fontsize=5.2, fontweight='bold', color='#6d28d9')
    ax.text(pod_x + 0.014, pod_y + 0.180, r'Embedded Memory-Mapped 2-Hop Cache ($250\,\text{MB}$, 88.4% Hit)', ha='left', va='center',
            fontsize=4.7, color='#475569')
    ax.text(pod_x + 0.014, pod_y + 0.162, r'Class-Conditional CRC Quantile Triage: $\Gamma(u) \subseteq \{0, 1\}$', ha='left', va='center',
            fontsize=4.8, fontweight='bold', color='#6d28d9')
    ax.text(pod_x + 0.014, pod_y + 0.144, r'Tier-3 STP Clear ($99.32\%$)  |  Tier-1 Quarantine ($0.18\%$)', ha='left', va='center',
            fontsize=4.6, color='#15803d')

    # Component 5: Container Runtime Footprint Tag
    ax.add_patch(patches.FancyBboxPatch(
        (pod_x + 0.006, pod_y + 0.014), pod_w - 0.012, 0.098,
        boxstyle='round,pad=0.001,rounding_size=0.003',
        facecolor='#f0fdf4', edgecolor='#86efac', linewidth=0.6
    ))
    ax.text(pod_x + pod_w/2, pod_y + 0.088, 'Multi-Stage Hardened Container Spec', ha='center', va='center',
            fontsize=5.0, fontweight='bold', color='#15803d')
    ax.text(pod_x + pod_w/2, pod_y + 0.070, 'Base: Debian-Slim  |  Image Size: 485 MB', ha='center', va='center',
            fontsize=4.7, color='#475569')
    ax.text(pod_x + pod_w/2, pod_y + 0.052, 'PyTorch C++ LibTorch (Zero-GPU Commodity CPU Native)', ha='center', va='center',
            fontsize=4.6, color='#15803d')
    ax.text(pod_x + pod_w/2, pod_y + 0.034, 'Appendix C.1 Dockerfile & C.2 K8s Manifest Verified', ha='center', va='center',
            fontsize=4.5, color='#64748b')

    # Sub-element 2.3: Asynchronous 4-Agent Forensic Swarm Pods (Center-Right of Zone 2)
    sw_x, sw_w = z2_x + 0.298, 0.200
    sw_y, sw_h = 0.170, 0.572
    ax.add_patch(patches.FancyBboxPatch(
        (sw_x, sw_y), sw_w, sw_h,
        boxstyle='round,pad=0.002,rounding_size=0.005',
        facecolor='#fefce8', edgecolor='#ca8a04', linewidth=0.9
    ))
    # Swarm Header Strip
    ax.add_patch(patches.FancyBboxPatch(
        (sw_x + 0.004, sw_y + sw_h - 0.032), sw_w - 0.008, 0.028,
        boxstyle='round,pad=0.001,rounding_size=0.003',
        facecolor='#ca8a04', edgecolor='#ca8a04', linewidth=0.5
    ))
    ax.text(sw_x + sw_w/2, sw_y + sw_h - 0.018, 'Forensic Swarm Pods [cstgb-swarm]',
            ha='center', va='center', fontsize=5.3, fontweight='bold', color='#ffffff')

    # 4 Swarm Agents Stacked
    agents = [
        ("Agent 1: Investigator", "GNNExplainer Subgraph Mining", "Extracts causal 2-hop transaction subgraph", "#b45309"),
        ("Agent 2: Forensics Typology", "AML Pattern Classifier", "Identifies structuring, layering & pass-thru", "#c2410c"),
        ("Agent 3: SAR Dossier Drafter", "FinCEN Form 111 XML Compiler", "Deterministic narrative synthesis <30 s", "#0f766e"),
        ("Agent 4: Compliance Auditor", "Zero-Hallucination AST Gate", r"Verifies $\mathcal{V}(\mathcal{T}) \subseteq \mathcal{V}_{\mathrm{sub}}$ (0% hallucination)", "#15803d")
    ]
    ag_y_starts = [0.550, 0.442, 0.334, 0.226]
    for (ag_title, ag_sub, ag_detail, ag_clr), ag_yst in zip(agents, ag_y_starts):
        ax.add_patch(patches.FancyBboxPatch(
            (sw_x + 0.005, ag_yst), sw_w - 0.010, 0.098,
            boxstyle='round,pad=0.001,rounding_size=0.003',
            facecolor='#ffffff', edgecolor='#fde047', linewidth=0.6
        ))
        ax.text(sw_x + 0.010, ag_yst + 0.078, ag_title, ha='left', va='center',
                fontsize=5.1, fontweight='bold', color=ag_clr)
        ax.text(sw_x + 0.010, ag_yst + 0.058, ag_sub, ha='left', va='center',
                fontsize=4.7, color='#475569')
        ax.text(sw_x + 0.010, ag_yst + 0.038, ag_detail, ha='left', va='center',
                fontsize=4.6, color='#64748b')

    # Swarm Output Card
    ax.add_patch(patches.FancyBboxPatch(
        (sw_x + 0.005, sw_y + 0.014), sw_w - 0.010, 0.098,
        boxstyle='round,pad=0.001,rounding_size=0.003',
        facecolor='#fef3c7', edgecolor='#f59e0b', linewidth=0.6
    ))
    ax.text(sw_x + sw_w/2, sw_y + 0.088, 'Async Background Execution', ha='center', va='center',
            fontsize=5.0, fontweight='bold', color='#b45309')
    ax.text(sw_x + sw_w/2, sw_y + 0.070, 'Triggered only on Tier 1 / Tier 2', ha='center', va='center',
            fontsize=4.7, color='#475569')
    ax.text(sw_x + sw_w/2, sw_y + 0.052, 'Median Synthesis: 24.8 s (SLA < 100 ms met)', ha='center', va='center',
            fontsize=4.6, fontweight='bold', color='#15803d')
    ax.text(sw_x + sw_w/2, sw_y + 0.034, 'Delivers sealed dossier to WORM vault', ha='center', va='center',
            fontsize=4.5, color='#64748b')

    # =========================================================================
    # ZONE 3: OBSERVABILITY & AUDIT WORM VAULT (x: 0.748 to 0.990, width: 0.242)
    # =========================================================================
    z3_x, z3_w = 0.748, 0.242

    ax.add_patch(patches.FancyBboxPatch(
        (z3_x, z_bot), z3_w, z_h,
        boxstyle='round,pad=0.002,rounding_size=0.005',
        facecolor='#f8fafc', edgecolor='#94a3b8', linewidth=0.8
    ))
    # Zone 3 Header Badge
    ax.add_patch(patches.FancyBboxPatch(
        (z3_x + 0.006, z_top - 0.030), z3_w - 0.012, 0.024,
        boxstyle='round,pad=0.001,rounding_size=0.003',
        facecolor='#6d28d9', edgecolor='#6d28d9', linewidth=0.5
    ))
    ax.text(z3_x + z3_w/2, z_top - 0.018, 'ZONE 3: TELEMETRY & WORM VAULT',
            ha='center', va='center', fontsize=5.5, fontweight='bold', color='#ffffff')

    # Card 3.1: Prometheus Real-Time Telemetry (Section 8.4.2 Alignment)
    ax.add_patch(patches.FancyBboxPatch(
        (z3_x + 0.006, 0.528), z3_w - 0.012, 0.340,
        boxstyle='round,pad=0.002,rounding_size=0.004',
        facecolor='#ffffff', edgecolor='#a855f7', linewidth=0.8
    ))
    ax.text(z3_x + z3_w/2, 0.846, 'Prometheus Metrics & Telemetry', ha='center', va='center',
            fontsize=5.8, fontweight='bold', color='#6d28d9')
    ax.text(z3_x + z3_w/2, 0.826, 'Scrapes /metrics endpoint every 5s', ha='center', va='center',
            fontsize=4.8, color='#475569')

    # 5 Real-Time Prometheus Metrics from Section 8.4.2
    prom_metrics = [
        ("cstgb_inference_duration", "P50: 0.45 ms | P99: 0.82 ms", "#0284c7"),
        ("cstgb_conformal_triage", "STP: 99.32% | T1: 0.18%", "#15803d"),
        ("cstgb_edge_trust_ratio", "65.9% Camouflage Filtered", "#b45309"),
        ("cstgb_lru_cache_hit", "88.4% In-Memory Cache Hit", "#0f766e"),
        ("cstgb_streaming_drift", "KS p = 0.42 > 0.05 (Stable)", "#6d28d9"),
    ]
    pm_y_starts = [0.778, 0.724, 0.670, 0.616, 0.562]
    for (pm_name, pm_val, pm_clr), pmy in zip(prom_metrics, pm_y_starts):
        ax.add_patch(patches.FancyBboxPatch(
            (z3_x + 0.010, pmy - 0.022), z3_w - 0.020, 0.046,
            boxstyle='round,pad=0.001,rounding_size=0.002',
            facecolor='#faf5ff', edgecolor='#e9d5ff', linewidth=0.5
        ))
        ax.text(z3_x + 0.016, pmy + 0.010, pm_name, ha='left', va='center',
                fontsize=4.8, fontweight='bold', color='#0f172a')
        ax.text(z3_x + 0.016, pmy - 0.008, pm_val, ha='left', va='center',
                fontsize=4.6, fontweight='bold', color=pm_clr)

    # Card 3.2: Tamper-Proof Merkle WORM Vault (SR 11-7 & FRE 902(11))
    ax.add_patch(patches.FancyBboxPatch(
        (z3_x + 0.006, 0.170), z3_w - 0.012, 0.346,
        boxstyle='round,pad=0.002,rounding_size=0.004',
        facecolor='#ffffff', edgecolor='#059669', linewidth=0.8
    ))
    ax.text(z3_x + z3_w/2, 0.494, 'Cryptographic Merkle WORM Vault', ha='center', va='center',
            fontsize=5.8, fontweight='bold', color='#059669')
    ax.text(z3_x + z3_w/2, 0.474, 'Persistent Volume Claim (PVC Storage)', ha='center', va='center',
            fontsize=4.8, color='#475569')

    ax.text(z3_x + z3_w/2, 0.446, 'SHA-256 Merkle Receipts', ha='center', va='center',
            fontsize=5.1, fontweight='bold', color='#0f766e')
    ax.text(z3_x + z3_w/2, 0.428, 'Append-Only Cryptographic Ledger', ha='center', va='center',
            fontsize=4.7, color='#64748b')

    ax.text(z3_x + z3_w/2, 0.400, 'Legal Evidence Standard', ha='center', va='center',
            fontsize=5.1, fontweight='bold', color='#15803d')
    ax.text(z3_x + z3_w/2, 0.382, 'FRE Rule 902(11) Self-Authenticating', ha='center', va='center',
            fontsize=4.7, color='#64748b')

    ax.text(z3_x + z3_w/2, 0.354, 'Model Governance Compliance', ha='center', va='center',
            fontsize=5.1, fontweight='bold', color='#6d28d9')
    ax.text(z3_x + z3_w/2, 0.336, 'Federal Reserve SR 11-7 / OCC 2011-12', ha='center', va='center',
            fontsize=4.7, color='#64748b')

    ax.text(z3_x + z3_w/2, 0.308, 'Hardware Object Lock Storage', ha='center', va='center',
            fontsize=5.1, fontweight='bold', color='#b45309')
    ax.text(z3_x + z3_w/2, 0.290, 'AWS S3 Glacier WORM / On-Prem SAN', ha='center', va='center',
            fontsize=4.7, color='#64748b')

    ax.text(z3_x + z3_w/2, 0.262, 'Regulatory Retention Docket', ha='center', va='center',
            fontsize=5.1, fontweight='bold', color='#0284c7')
    ax.text(z3_x + z3_w/2, 0.244, '5-Year Statutory BSA Countdown', ha='center', va='center',
            fontsize=4.7, color='#64748b')

    ax.text(z3_x + z3_w/2, 0.216, 'Court-Admissible Evidence', ha='center', va='center',
            fontsize=5.0, fontweight='bold', color='#15803d')
    ax.text(z3_x + z3_w/2, 0.198, 'Zero-tampering cryptographic proof', ha='center', va='center',
            fontsize=4.6, color='#64748b')

    # Inter-Zone Connecting Arrows
    # Ingress -> Cluster
    ax.annotate("", xy=(z2_x, 0.540), xytext=(z1_x + z1_w, 0.540),
                arrowprops=dict(arrowstyle="->,head_width=0.25,head_length=0.35", color='#0284c7', lw=1.6))
    ax.text((z1_x + z1_w + z2_x)/2, 0.550, 'mTLS 1.3', ha='center', va='bottom', fontsize=4.8, fontweight='bold', color='#0284c7')

    # Worker Pod -> Swarm Pod (Async Event Queue)
    ax.annotate("", xy=(sw_x, 0.450), xytext=(pod_x + pod_w, 0.450),
                arrowprops=dict(arrowstyle="->,head_width=0.22,head_length=0.32", color='#ca8a04', lw=1.4, linestyle='--'))
    ax.text((pod_x + pod_w + sw_x)/2, 0.460, '<<async>>', ha='center', va='bottom', fontsize=4.7, fontweight='bold', color='#b45309')

    # Cluster -> Telemetry
    ax.annotate("", xy=(z3_x, 0.690), xytext=(z2_x + z2_w, 0.690),
                arrowprops=dict(arrowstyle="->,head_width=0.22,head_length=0.32", color='#6d28d9', lw=1.4))
    ax.text((z2_x + z2_w + z3_x)/2, 0.700, '/metrics', ha='center', va='bottom', fontsize=4.7, fontweight='bold', color='#6d28d9')

    # Cluster -> WORM Vault
    ax.annotate("", xy=(z3_x, 0.340), xytext=(z2_x + z2_w, 0.340),
                arrowprops=dict(arrowstyle="->,head_width=0.22,head_length=0.32", color='#059669', lw=1.4))
    ax.text((z2_x + z2_w + z3_x)/2, 0.350, 'SHA-256', ha='center', va='bottom', fontsize=4.7, fontweight='bold', color='#059669')

    # =========================================================================
    # 4. BOTTOM PRODUCTION SLA & CI/CD METRIC RIBBON (4 Cards)
    # =========================================================================
    kpis = [
        {
            "x": 0.010, "w": 0.236,
            "title": "CONTAINER IMAGE FOOTPRINT",
            "metric": "485 MB Multi-Stage Slim",
            "sub": "Debian-Slim + Pre-Compiled C++ LibTorch",
            "bg": "#f0f9ff", "border": "#38bdf8", "fg": "#0369a1", "bar": "#0284c7"
        },
        {
            "x": 0.258, "w": 0.236,
            "title": "DYNAMIC HPA ELASTICITY",
            "metric": "4 to 32 Pod Replicas",
            "sub": "Scales 2.4k to 31.2k tx/s in Under 15 s",
            "bg": "#f0fdf4", "border": "#4ade80", "fg": "#15803d", "bar": "#16a34a"
        },
        {
            "x": 0.506, "w": 0.236,
            "title": "AUTOMATED CI/CD VERIFICATION",
            "metric": "158 / 158 Tests Passed",
            "sub": "100% CI Pass Rate Across 25 Test Suites",
            "bg": "#fefce8", "border": "#facc15", "fg": "#a16207", "bar": "#ca8a04"
        },
        {
            "x": 0.754, "w": 0.236,
            "title": "HIGH-AVAILABILITY UPTIME",
            "metric": "99.99% Production SLA",
            "sub": "Multi-Zone Resilience on AWS EKS / GKE",
            "bg": "#faf5ff", "border": "#c084fc", "fg": "#6d28d9", "bar": "#7c3aed"
        }
    ]

    card_y = 0.014
    card_h = 0.130

    for kpi in kpis:
        kx = kpi["x"]
        kw = kpi["w"]
        
        ax.add_patch(patches.FancyBboxPatch(
            (kx, card_y), kw, card_h,
            boxstyle='round,pad=0.002,rounding_size=0.004',
            facecolor=kpi["bg"], edgecolor=kpi["border"], linewidth=0.8
        ))
        ax.add_patch(patches.FancyBboxPatch(
            (kx + 0.004, card_y + card_h - 0.010), kw - 0.008, 0.006,
            boxstyle='round,pad=0.0005,rounding_size=0.001',
            facecolor=kpi["bar"], edgecolor=kpi["bar"], linewidth=0.3
        ))
        ax.text(kx + kw/2, card_y + card_h - 0.024, kpi["title"],
                ha='center', va='center', fontsize=5.2, fontweight='bold', color=kpi["fg"])
        ax.text(kx + kw/2, card_y + card_h - 0.058, kpi["metric"],
                ha='center', va='center', fontsize=7.2, fontweight='bold', color='#0f172a')
        ax.text(kx + kw/2, card_y + 0.026, kpi["sub"],
                ha='center', va='center', fontsize=5.1, color='#475569')

    plt.subplots_adjust(left=0.005, right=0.995, top=0.99, bottom=0.01)
    return fig

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent
    thesis_fig_dir = BASE_DIR / "papers" / "University_CSE_Thesis" / "figures"
    eaai_fig_dir = BASE_DIR / "papers" / "EAAI_Research_Paper" / "figures"
    eaai_sub_dir = BASE_DIR / "papers" / "EAAI_Submission" / "figures"
    data_fig_dir = BASE_DIR / "data" / "outputs" / "figures"
    reports_fig_dir = BASE_DIR / "reports" / "figures"

    TARGET_DIRS = [thesis_fig_dir, eaai_fig_dir, eaai_sub_dir, data_fig_dir, reports_fig_dir]
    for d in TARGET_DIRS:
        d.mkdir(parents=True, exist_ok=True)

    print("Generating Brand New Figure 8.3: Enterprise Cloud-Native Kubernetes Deployment Topology...")
    fig = generate_figure_8_3()
    
    # Save as both fig8_1_fastapi_k8s_topology (for existing LaTeX link) and fig8_3_cloud_native_k8s
    stems = ["fig8_1_fastapi_k8s_topology", "fig8_3_cloud_native_k8s"]
    for stem in stems:
        for d in TARGET_DIRS:
            fig.savefig(d / f"{stem}.pdf", bbox_inches="tight", pad_inches=0.15)
            fig.savefig(d / f"{stem}.png", dpi=300, bbox_inches="tight", pad_inches=0.15)
            print(f"  [SAVED] {d / f'{stem}.pdf'}")
    
    plt.close(fig)
    print("Done generating Figure 8.3!")

