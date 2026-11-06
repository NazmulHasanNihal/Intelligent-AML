"""
scripts/redesign_fig8_3_cloud_native_k8s.py
Publication-grade Kubernetes Deployment Topology & Elastic Autoscaling Architecture.

Conforms to IEEE/ACM computer systems architecture diagram standards:
- Zone 1: Banking Ingress & Edge Security Gateway (mTLS 1.3, Envoy/Nginx, RBAC)
- Zone 2: Kubernetes Production Cluster (Namespace: cstgb-production)
  * Horizontal Pod Autoscaler (HPA v2): dynamic scaling 4 <-> 32 pods (2.4k to 31.2k tx/s)
  * Containerized FastAPI Scoring Worker Pod micro-architecture
  * Quarantined Asynchronous 4-Agent Forensic Swarm
- Zone 3: Storage, Telemetry & Tamper-Proof Merkle WORM Vault (Prometheus, S3 Object Lock, FRE 902(11))
- Sharp rectangular engineering blocks, explicit bus connectors, strictly NO consumer card ribbons.
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
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
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
    # Aspect ratio ~2.08:1 (9.4 x 4.5 inches)
    fig, ax = plt.subplots(figsize=(9.4, 4.50))
    ax.axis('off')
    ax.set_xlim([-0.010, 1.010])
    ax.set_ylim([-0.015, 1.015])

    # 1. Outer Master Canvas Frame (sharp rectangle)
    ax.add_patch(patches.Rectangle(
        (0.000, 0.000), 1.000, 1.000,
        facecolor='#ffffff', edgecolor='#94a3b8', linewidth=1.0
    ))

    # 2. Master Header Banner
    ax.add_patch(patches.Rectangle(
        (0.005, 0.922), 0.990, 0.072,
        facecolor='#0f172a', edgecolor='#0f172a', linewidth=0.5
    ))
    ax.text(0.018, 0.968, 'Enterprise Cloud-Native Kubernetes Deployment Topology & Elastic Autoscaling',
            ha='left', va='center', fontsize=8.8, fontweight='bold', color='#ffffff')
    ax.text(0.018, 0.938,
            r'End-to-End Orchestration: Ingress mTLS 1.3 $\rightarrow$ HPA Elastic Scaling (4 $\rightleftharpoons$ 32 Pods) $\rightarrow$ TorchScript & Arrow IPC $\rightarrow$ Prometheus & WORM Vault',
            ha='left', va='center', fontsize=6.0, color='#94a3b8')

    # Top Right SLA Pill
    ax.add_patch(patches.Rectangle(
        (0.755, 0.932), 0.235, 0.052,
        facecolor='#0284c7', edgecolor='#38bdf8', linewidth=0.8
    ))
    ax.text(0.872, 0.958, 'HPA ELASTIC: 4 - 32 PODS (31.2k tx/s)',
            ha='center', va='center', fontsize=6.0, fontweight='bold', color='#ffffff')

    # =========================================================================
    # ZONE 1: SECURE INGRESS & API GATEWAY (x: 0.010 to 0.224, width: 0.214)
    # =========================================================================
    z1_x, z1_w = 0.010, 0.214
    z_top, z_bot = 0.918, 0.025
    z_h = z_top - z_bot

    ax.add_patch(patches.Rectangle(
        (z1_x, z_bot), z1_w, z_h,
        facecolor='#f8fafc', edgecolor='#94a3b8', linewidth=1.0
    ))
    # Zone 1 Header
    ax.add_patch(patches.Rectangle(
        (z1_x, z_top - 0.032), z1_w, 0.032,
        facecolor='#334155', edgecolor='#334155', linewidth=0.5
    ))
    ax.text(z1_x + z1_w/2, z_top - 0.016, 'ZONE 1: SECURE INGRESS & GATEWAY',
            ha='center', va='center', fontsize=5.8, fontweight='bold', color='#ffffff')

    # Block 1.1: Core Banking System (CBS)
    ax.add_patch(patches.Rectangle(
        (z1_x + 0.006, 0.615), z1_w - 0.012, 0.260,
        facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=0.8
    ))
    ax.text(z1_x + z1_w/2, 0.850, 'Core Banking Systems (CBS)', ha='center', va='center',
            fontsize=6.0, fontweight='bold', color='#0f172a')
    ax.text(z1_x + z1_w/2, 0.825, 'Temenos T24 / Finacle / Flexcube', ha='center', va='center',
            fontsize=5.1, color='#475569')
    ax.text(z1_x + z1_w/2, 0.790, 'Payment Webhook Stream', ha='center', va='center',
            fontsize=5.4, fontweight='bold', color='#0284c7')
    ax.text(z1_x + z1_w/2, 0.765, 'ISO 20022 camt.053 & pacs.008', ha='center', va='center',
            fontsize=5.0, color='#64748b')
    ax.text(z1_x + z1_w/2, 0.730, 'WebSocket Live Feeds', ha='center', va='center',
            fontsize=5.4, fontweight='bold', color='#0f766e')
    ax.text(z1_x + z1_w/2, 0.705, 'Full-Duplex Operational Triage', ha='center', va='center',
            fontsize=5.0, color='#64748b')
    ax.text(z1_x + z1_w/2, 0.665, 'Mutual TLS 1.3 Banking Rails', ha='center', va='center',
            fontsize=5.2, fontweight='bold', color='#15803d')
    ax.text(z1_x + z1_w/2, 0.640, 'Hardware Security Module (HSM)', ha='center', va='center',
            fontsize=4.8, color='#64748b')

    # Block 1.2: Envoy / Nginx Ingress Controller
    ax.add_patch(patches.Rectangle(
        (z1_x + 0.006, 0.330), z1_w - 0.012, 0.270,
        facecolor='#ffffff', edgecolor='#0284c7', linewidth=0.9
    ))
    ax.text(z1_x + z1_w/2, 0.575, 'Envoy / Nginx Ingress Gateway', ha='center', va='center',
            fontsize=6.0, fontweight='bold', color='#0369a1')
    ax.text(z1_x + z1_w/2, 0.550, 'Edge Traffic & Load Balancing', ha='center', va='center',
            fontsize=5.1, color='#475569')
    ax.text(z1_x + z1_w/2, 0.515, 'mTLS 1.3 Cryptographic Termination', ha='center', va='center',
            fontsize=5.3, fontweight='bold', color='#0284c7')
    ax.text(z1_x + z1_w/2, 0.490, 'Automated Cert-Manager Vault CA', ha='center', va='center',
            fontsize=4.9, color='#64748b')
    ax.text(z1_x + z1_w/2, 0.455, 'Token Bucket Rate Limiting', ha='center', va='center',
            fontsize=5.3, fontweight='bold', color='#b45309')
    ax.text(z1_x + z1_w/2, 0.430, 'Peak 50,000 req/s burst tolerance', ha='center', va='center',
            fontsize=4.9, color='#64748b')
    ax.text(z1_x + z1_w/2, 0.395, 'Cloud-Native WAF Defense', ha='center', va='center',
            fontsize=5.3, fontweight='bold', color='#b91c1c')
    ax.text(z1_x + z1_w/2, 0.370, 'Path sanitization & anti-CSRF filter', ha='center', va='center',
            fontsize=4.9, color='#64748b')

    # Block 1.3: Security, JWT & RBAC
    ax.add_patch(patches.Rectangle(
        (z1_x + 0.006, 0.040), z1_w - 0.012, 0.275,
        facecolor='#ffffff', edgecolor='#cbd5e1', linewidth=0.8
    ))
    ax.text(z1_x + z1_w/2, 0.290, 'OAuth2 & JWT RBAC Security', ha='center', va='center',
            fontsize=6.0, fontweight='bold', color='#0f172a')
    ax.text(z1_x + z1_w/2, 0.265, 'Zero-Trust Enterprise Perimeter', ha='center', va='center',
            fontsize=5.1, color='#475569')
    ax.text(z1_x + z1_w/2, 0.230, 'Maker-Checker Separation', ha='center', va='center',
            fontsize=5.3, fontweight='bold', color='#6d28d9')
    ax.text(z1_x + z1_w/2, 0.205, 'Four-Eyes Dual Sign-Off gate', ha='center', va='center',
            fontsize=4.9, color='#64748b')
    ax.text(z1_x + z1_w/2, 0.170, 'Role Separation Levels', ha='center', va='center',
            fontsize=5.3, fontweight='bold', color='#0f766e')
    ax.text(z1_x + z1_w/2, 0.145, 'Analyst / Investigator / Auditor', ha='center', va='center',
            fontsize=4.9, color='#64748b')
    ax.text(z1_x + z1_w/2, 0.110, 'SHA-256 PII De-Identification', ha='center', va='center',
            fontsize=5.3, fontweight='bold', color='#15803d')
    ax.text(z1_x + z1_w/2, 0.085, 'Salted key rings (GDPR / GLBA)', ha='center', va='center',
            fontsize=4.9, color='#64748b')
    ax.text(z1_x + z1_w/2, 0.055, 'AES-256-GCM Wire Encryption', ha='center', va='center',
            fontsize=5.0, fontweight='bold', color='#0284c7')

    # =========================================================================
    # ZONE 2: KUBERNETES PRODUCTION CLUSTER (x: 0.234 to 0.740, width: 0.506)
    # =========================================================================
    z2_x, z2_w = 0.234, 0.506

    ax.add_patch(patches.Rectangle(
        (z2_x, z_bot), z2_w, z_h,
        facecolor='#f0f9ff', edgecolor='#0284c7', linewidth=1.2, linestyle='--'
    ))
    # Zone 2 Header
    ax.add_patch(patches.Rectangle(
        (z2_x, z_top - 0.032), z2_w, 0.032,
        facecolor='#0284c7', edgecolor='#0284c7', linewidth=0.5
    ))
    ax.text(z2_x + z2_w/2, z_top - 0.016, 'ZONE 2: KUBERNETES PRODUCTION CLUSTER  [Namespace: cstgb-production]',
            ha='center', va='center', fontsize=6.2, fontweight='bold', color='#ffffff')

    # Sub-element 2.1: Horizontal Pod Autoscaler (HPA v2)
    hpa_y, hpa_h = 0.760, 0.118
    ax.add_patch(patches.Rectangle(
        (z2_x + 0.008, hpa_y), z2_w - 0.016, hpa_h,
        facecolor='#ffffff', edgecolor='#38bdf8', linewidth=0.9
    ))
    ax.text(z2_x + 0.018, hpa_y + hpa_h - 0.018, 'Kubernetes Horizontal Pod Autoscaler (HPA v2)',
            ha='left', va='center', fontsize=6.4, fontweight='bold', color='#0369a1')
    ax.text(z2_x + z2_w - 0.018, hpa_y + hpa_h - 0.018, 'Metrics: CPU > 70% | Queue Depth > 500 msgs',
            ha='right', va='center', fontsize=5.3, fontweight='bold', color='#b45309')
    
    # Min Scale Box
    ax.add_patch(patches.Rectangle(
        (z2_x + 0.018, hpa_y + 0.014), 0.218, 0.072,
        facecolor='#f0fdf4', edgecolor='#4ade80', linewidth=0.8
    ))
    ax.text(z2_x + 0.018 + 0.109, hpa_y + 0.068, 'BASELINE: 4 Pod Replicas',
            ha='center', va='center', fontsize=5.5, fontweight='bold', color='#15803d')
    ax.text(z2_x + 0.018 + 0.109, hpa_y + 0.048, 'Sustained Ingress: 2,400 tx/s',
            ha='center', va='center', fontsize=5.0, color='#475569')
    ax.text(z2_x + 0.018 + 0.109, hpa_y + 0.028, 'Single-Worker P50: 0.45 ms',
            ha='center', va='center', fontsize=4.8, color='#16a34a')

    # Elastic Scale Arrow
    ax.annotate("", xy=(z2_x + 0.278, hpa_y + 0.050), xytext=(z2_x + 0.246, hpa_y + 0.050),
                arrowprops=dict(arrowstyle="<->,head_width=0.25,head_length=0.35", color='#0284c7', lw=1.5))
    ax.text(z2_x + 0.262, hpa_y + 0.070, 'Auto-Scale', ha='center', va='bottom', fontsize=5.0, fontweight='bold', color='#0284c7')
    ax.text(z2_x + 0.262, hpa_y + 0.028, '<15s spin-up', ha='center', va='top', fontsize=4.7, color='#64748b')

    # Max Scale Box
    ax.add_patch(patches.Rectangle(
        (z2_x + 0.282, hpa_y + 0.014), 0.210, 0.072,
        facecolor='#fff7ed', edgecolor='#fb923c', linewidth=0.8
    ))
    ax.text(z2_x + 0.282 + 0.105, hpa_y + 0.068, 'BURST PEAK: 32 Pod Replicas',
            ha='center', va='center', fontsize=5.5, fontweight='bold', color='#c2410c')
    ax.text(z2_x + 0.282 + 0.105, hpa_y + 0.048, 'Peak Ingress: 31,250 tx/s',
            ha='center', va='center', fontsize=5.0, color='#475569')
    ax.text(z2_x + 0.282 + 0.105, hpa_y + 0.028, 'Zero Packet Drop Guarantee',
            ha='center', va='center', fontsize=4.8, color='#ea580c')

    # Sub-element 2.2: FastAPI Scoring Worker Pods
    pod_x, pod_w = z2_x + 0.008, 0.282
    pod_y, pod_h = 0.040, 0.705
    ax.add_patch(patches.Rectangle(
        (pod_x, pod_y), pod_w, pod_h,
        facecolor='#ffffff', edgecolor='#0284c7', linewidth=1.1
    ))
    # Pod Header
    ax.add_patch(patches.Rectangle(
        (pod_x, pod_y + pod_h - 0.034), pod_w, 0.034,
        facecolor='#0284c7', edgecolor='#0284c7', linewidth=0.5
    ))
    ax.text(pod_x + pod_w/2, pod_y + pod_h - 0.017, 'FastAPI Scoring Worker Pod [cstgb-worker-prod]',
            ha='center', va='center', fontsize=5.6, fontweight='bold', color='#ffffff')

    # Pod Internal Sub-components
    # Component 1: FastAPI ASGI
    ax.add_patch(patches.Rectangle(
        (pod_x + 0.006, pod_y + 0.540), pod_w - 0.012, 0.120,
        facecolor='#f8fafc', edgecolor='#cbd5e1', linewidth=0.7
    ))
    ax.text(pod_x + 0.012, pod_y + 0.640, '1. FastAPI ASGI Worker Engine', ha='left', va='center',
            fontsize=5.5, fontweight='bold', color='#0284c7')
    ax.text(pod_x + 0.012, pod_y + 0.615, 'Python 3.12, Uvicorn, Non-blocking uvloop', ha='left', va='center',
            fontsize=5.0, color='#475569')
    ax.text(pod_x + 0.012, pod_y + 0.590, r'SLA Fast-Path Webhook Clearance: $0.45\,\text{ms}$', ha='left', va='center',
            fontsize=5.1, fontweight='bold', color='#15803d')
    ax.text(pod_x + 0.012, pod_y + 0.565, 'Async background event dispatch queue', ha='left', va='center',
            fontsize=4.8, color='#64748b')

    # Component 2: Apache Arrow Zero-Copy IPC
    ax.add_patch(patches.Rectangle(
        (pod_x + 0.006, pod_y + 0.405), pod_w - 0.012, 0.125,
        facecolor='#f8fafc', edgecolor='#cbd5e1', linewidth=0.7
    ))
    ax.text(pod_x + 0.012, pod_y + 0.516, '2. Apache Arrow IPC Shared Memory', ha='left', va='center',
            fontsize=5.5, fontweight='bold', color='#0f766e')
    ax.text(pod_x + 0.012, pod_y + 0.482, r'Vectorized batch buffer: $\mathcal{O}(|\mathcal{E}|)$', ha='left', va='center',
            fontsize=5.0, color='#475569')
    ax.text(pod_x + 0.012, pod_y + 0.456, r'Direct PyTorch Tensor View ($0.11\,\text{ms}$)', ha='left', va='center',
            fontsize=5.1, fontweight='bold', color='#0f766e')
    ax.text(pod_x + 0.012, pod_y + 0.430, r'Kirchhoff flow & 12-D invariants $\mathbf{z}_{\mathrm{inv}}$', ha='left', va='center',
            fontsize=4.8, color='#64748b')

    # Component 3: TorchScript Neural Scoring Engine
    ax.add_patch(patches.Rectangle(
        (pod_x + 0.006, pod_y + 0.270), pod_w - 0.012, 0.125,
        facecolor='#f8fafc', edgecolor='#cbd5e1', linewidth=0.7
    ))
    ax.text(pod_x + 0.012, pod_y + 0.375, '3. TorchScript C-STGB Neural Engine', ha='left', va='center',
            fontsize=5.5, fontweight='bold', color='#c2410c')
    ax.text(pod_x + 0.012, pod_y + 0.350, 'Tri-Band Continuous Fourier Encoding (1.2 MB)', ha='left', va='center',
            fontsize=5.0, color='#475569')
    ax.text(pod_x + 0.012, pod_y + 0.325, r'Edge-Trust MLP Denoising ($65.9\%$ Camouflage Pruned)', ha='left', va='center',
            fontsize=5.1, fontweight='bold', color='#b45309')
    ax.text(pod_x + 0.012, pod_y + 0.300, r'Harmonic Spatio-Temporal GNN Attention ($0.12\,\text{ms}$)', ha='left', va='center',
            fontsize=4.8, color='#64748b')

    # Component 4: DuckDB L1 LRU & Conformal Arbiter
    ax.add_patch(patches.Rectangle(
        (pod_x + 0.006, pod_y + 0.135), pod_w - 0.012, 0.125,
        facecolor='#f8fafc', edgecolor='#cbd5e1', linewidth=0.7
    ))
    ax.text(pod_x + 0.012, pod_y + 0.240, '4. DuckDB Ego-Graph LRU & Conformal Arbiter', ha='left', va='center',
            fontsize=5.5, fontweight='bold', color='#6d28d9')
    ax.text(pod_x + 0.012, pod_y + 0.215, r'Embedded Memory-Mapped 2-Hop Cache ($250\,\text{MB}$, 88.4% Hit)', ha='left', va='center',
            fontsize=5.0, color='#475569')
    ax.text(pod_x + 0.012, pod_y + 0.190, r'Class-Conditional CRC Quantile Triage: $\Gamma(u) \in \{\{0\}, \{1\}, \{0,1\}\}$', ha='left', va='center',
            fontsize=5.1, fontweight='bold', color='#6d28d9')
    ax.text(pod_x + 0.012, pod_y + 0.165, r'Tier-3 STP Clear ($99.33\%$) | Tier-1 Quarantine ($0.18\%$)', ha='left', va='center',
            fontsize=4.8, color='#15803d')

    # Component 5: Hardened Container Spec
    ax.add_patch(patches.Rectangle(
        (pod_x + 0.006, pod_y + 0.010), pod_w - 0.012, 0.115,
        facecolor='#f0fdf4', edgecolor='#86efac', linewidth=0.7
    ))
    ax.text(pod_x + pod_w/2, pod_y + 0.102, 'Multi-Stage Hardened Container Spec', ha='center', va='center',
            fontsize=5.3, fontweight='bold', color='#15803d')
    ax.text(pod_x + pod_w/2, pod_y + 0.080, 'Base: Debian-Slim | Image Size: 485 MB', ha='center', va='center',
            fontsize=4.9, color='#475569')
    ax.text(pod_x + pod_w/2, pod_y + 0.058, 'PyTorch C++ LibTorch (Zero-GPU Commodity CPU Native)', ha='center', va='center',
            fontsize=4.8, color='#15803d')
    ax.text(pod_x + pod_w/2, pod_y + 0.035, 'Appendix C.1 Dockerfile & C.2 K8s Manifest Verified', ha='center', va='center',
            fontsize=4.7, color='#64748b')

    # Sub-element 2.3: Asynchronous 4-Agent Forensic Swarm Pods
    sw_x, sw_w = z2_x + 0.298, 0.200
    sw_y, sw_h = 0.040, 0.705
    ax.add_patch(patches.Rectangle(
        (sw_x, sw_y), sw_w, sw_h,
        facecolor='#fefce8', edgecolor='#ca8a04', linewidth=1.0
    ))
    # Swarm Header
    ax.add_patch(patches.Rectangle(
        (sw_x, sw_y + sw_h - 0.034), sw_w, 0.034,
        facecolor='#ca8a04', edgecolor='#ca8a04', linewidth=0.5
    ))
    ax.text(sw_x + sw_w/2, sw_y + sw_h - 0.017, 'Forensic Swarm Pods [cstgb-swarm]',
            ha='center', va='center', fontsize=5.5, fontweight='bold', color='#ffffff')

    # 4 Swarm Agents Stacked
    agents = [
        ("Agent 1: Lead Coordinator", "GNNExplainer Subgraph Mining", "Extracts causal 2-hop transaction subgraph", "#b45309"),
        ("Agent 2: Topology Specialist", "AML Typology Classifier", "Identifies structuring, layering & pass-thru", "#c2410c"),
        ("Agent 3: Legal SAR Drafter", "FinCEN Form 111 XML Compiler", "Deterministic narrative synthesis <30 s", "#0f766e"),
        ("Agent 4: Compliance Rule Verifier", "Context-Free AST Gate", "Deterministic grammar (0% hallucination)", "#15803d")
    ]
    ag_y_starts = [0.550, 0.420, 0.290, 0.160]
    for (ag_title, ag_sub, ag_detail, ag_clr), ag_yst in zip(agents, ag_y_starts):
        ax.add_patch(patches.Rectangle(
            (sw_x + 0.005, ag_yst), sw_w - 0.010, 0.118,
            facecolor='#ffffff', edgecolor='#fde047', linewidth=0.7
        ))
        ax.text(sw_x + 0.010, ag_yst + 0.095, ag_title, ha='left', va='center',
                fontsize=5.4, fontweight='bold', color=ag_clr)
        ax.text(sw_x + 0.010, ag_yst + 0.068, ag_sub, ha='left', va='center',
                fontsize=4.9, color='#475569')
        ax.text(sw_x + 0.010, ag_yst + 0.042, ag_detail, ha='left', va='center',
                fontsize=4.8, color='#64748b')

    # Swarm Output Box
    ax.add_patch(patches.Rectangle(
        (sw_x + 0.005, sw_y + 0.010), sw_w - 0.010, 0.140,
        facecolor='#fef3c7', edgecolor='#f59e0b', linewidth=0.7
    ))
    ax.text(sw_x + sw_w/2, sw_y + 0.120, 'Async Background Execution', ha='center', va='center',
            fontsize=5.3, fontweight='bold', color='#b45309')
    ax.text(sw_x + sw_w/2, sw_y + 0.095, 'Triggered on Tier 1 / Tier 2 alerts', ha='center', va='center',
            fontsize=4.9, color='#475569')
    ax.text(sw_x + sw_w/2, sw_y + 0.070, 'Median Synthesis: 24.8 s (SLA < 100 ms met)', ha='center', va='center',
            fontsize=4.9, fontweight='bold', color='#15803d')
    ax.text(sw_x + sw_w/2, sw_y + 0.045, 'Delivers sealed dossier to WORM vault', ha='center', va='center',
            fontsize=4.7, color='#64748b')
    ax.text(sw_x + sw_w/2, sw_y + 0.022, 'FRE Rule 902(11) Self-Authenticating', ha='center', va='center',
            fontsize=4.7, fontweight='bold', color='#0f766e')

    # =========================================================================
    # ZONE 3: OBSERVABILITY & AUDIT WORM VAULT (x: 0.748 to 0.990, width: 0.242)
    # =========================================================================
    z3_x, z3_w = 0.748, 0.242

    ax.add_patch(patches.Rectangle(
        (z3_x, z_bot), z3_w, z_h,
        facecolor='#f8fafc', edgecolor='#94a3b8', linewidth=1.0
    ))
    # Zone 3 Header
    ax.add_patch(patches.Rectangle(
        (z3_x, z_top - 0.032), z3_w, 0.032,
        facecolor='#6d28d9', edgecolor='#6d28d9', linewidth=0.5
    ))
    ax.text(z3_x + z3_w/2, z_top - 0.016, 'ZONE 3: TELEMETRY & WORM VAULT',
            ha='center', va='center', fontsize=5.8, fontweight='bold', color='#ffffff')

    # Block 3.1: Prometheus Real-Time Telemetry
    ax.add_patch(patches.Rectangle(
        (z3_x + 0.006, 0.465), z3_w - 0.012, 0.410,
        facecolor='#ffffff', edgecolor='#a855f7', linewidth=0.9
    ))
    ax.text(z3_x + z3_w/2, 0.852, 'Prometheus Metrics & Telemetry', ha='center', va='center',
            fontsize=6.0, fontweight='bold', color='#6d28d9')
    ax.text(z3_x + z3_w/2, 0.828, 'Scrapes /metrics endpoint every 5s', ha='center', va='center',
            fontsize=5.0, color='#475569')

    # 5 Real-Time Prometheus Metrics
    prom_metrics = [
        ("cstgb_inference_duration", "P50: 0.45 ms | P99: 0.82 ms", "#0284c7"),
        ("cstgb_conformal_triage", "STP: 99.33% | T1: 0.18%", "#15803d"),
        ("cstgb_edge_trust_ratio", "65.9% Camouflage Filtered", "#b45309"),
        ("cstgb_lru_cache_hit", "88.4% In-Memory Cache Hit", "#0f766e"),
        ("cstgb_streaming_drift", "KS p = 0.42 > 0.05 (Stable)", "#6d28d9"),
    ]
    pm_y_starts = [0.775, 0.710, 0.645, 0.580, 0.515]
    for (pm_name, pm_val, pm_clr), pmy in zip(prom_metrics, pm_y_starts):
        ax.add_patch(patches.Rectangle(
            (z3_x + 0.010, pmy - 0.025), z3_w - 0.020, 0.054,
            facecolor='#faf5ff', edgecolor='#e9d5ff', linewidth=0.6
        ))
        ax.text(z3_x + 0.016, pmy + 0.012, pm_name, ha='left', va='center',
                fontsize=5.1, fontweight='bold', color='#0f172a')
        ax.text(z3_x + 0.016, pmy - 0.010, pm_val, ha='left', va='center',
                fontsize=4.9, fontweight='bold', color=pm_clr)

    # Block 3.2: Tamper-Proof Merkle WORM Vault
    ax.add_patch(patches.Rectangle(
        (z3_x + 0.006, 0.040), z3_w - 0.012, 0.415,
        facecolor='#ffffff', edgecolor='#059669', linewidth=0.9
    ))
    ax.text(z3_x + z3_w/2, 0.432, 'Cryptographic Merkle WORM Vault', ha='center', va='center',
            fontsize=6.0, fontweight='bold', color='#059669')
    ax.text(z3_x + z3_w/2, 0.408, 'Persistent Volume Claim (PVC Storage)', ha='center', va='center',
            fontsize=5.0, color='#475569')

    ax.text(z3_x + z3_w/2, 0.375, 'SHA-256 Merkle Receipts', ha='center', va='center',
            fontsize=5.3, fontweight='bold', color='#0f766e')
    ax.text(z3_x + z3_w/2, 0.352, 'Append-Only Cryptographic Ledger', ha='center', va='center',
            fontsize=4.9, color='#64748b')

    ax.text(z3_x + z3_w/2, 0.320, 'Legal Evidence Standard', ha='center', va='center',
            fontsize=5.3, fontweight='bold', color='#15803d')
    ax.text(z3_x + z3_w/2, 0.297, 'FRE Rule 902(11) Self-Authenticating', ha='center', va='center',
            fontsize=4.9, color='#64748b')

    ax.text(z3_x + z3_w/2, 0.265, 'Model Governance Compliance', ha='center', va='center',
            fontsize=5.3, fontweight='bold', color='#6d28d9')
    ax.text(z3_x + z3_w/2, 0.242, 'Federal Reserve SR 11-7 / OCC 2011-12', ha='center', va='center',
            fontsize=4.9, color='#64748b')

    ax.text(z3_x + z3_w/2, 0.210, 'Hardware Object Lock Storage', ha='center', va='center',
            fontsize=5.3, fontweight='bold', color='#b45309')
    ax.text(z3_x + z3_w/2, 0.187, 'AWS S3 Glacier WORM / On-Prem SAN', ha='center', va='center',
            fontsize=4.9, color='#64748b')

    ax.text(z3_x + z3_w/2, 0.155, 'Regulatory Retention Docket', ha='center', va='center',
            fontsize=5.3, fontweight='bold', color='#0284c7')
    ax.text(z3_x + z3_w/2, 0.132, '5-Year Statutory BSA Countdown', ha='center', va='center',
            fontsize=4.9, color='#64748b')

    ax.text(z3_x + z3_w/2, 0.100, 'Court-Admissible Evidence', ha='center', va='center',
            fontsize=5.2, fontweight='bold', color='#15803d')
    ax.text(z3_x + z3_w/2, 0.077, 'Zero-tampering cryptographic proof', ha='center', va='center',
            fontsize=4.8, color='#64748b')
    ax.text(z3_x + z3_w/2, 0.054, 'Immutable SHA-256 Digest', ha='center', va='center',
            fontsize=4.8, fontweight='bold', color='#059669')

    # Inter-Zone Connecting Arrows
    # Ingress -> Cluster
    ax.annotate("", xy=(z2_x, 0.540), xytext=(z1_x + z1_w, 0.540),
                arrowprops=dict(arrowstyle="->,head_width=0.25,head_length=0.35", color='#0284c7', lw=1.6))
    ax.text((z1_x + z1_w + z2_x)/2, 0.550, 'mTLS 1.3', ha='center', va='bottom', fontsize=5.0, fontweight='bold', color='#0284c7')

    # Worker Pod -> Swarm Pod (Async Event Queue)
    ax.annotate("", xy=(sw_x, 0.450), xytext=(pod_x + pod_w, 0.450),
                arrowprops=dict(arrowstyle="->,head_width=0.22,head_length=0.32", color='#ca8a04', lw=1.4, linestyle='--'))
    ax.text((pod_x + pod_w + sw_x)/2, 0.454, '«async»', ha='center', va='bottom', fontsize=4.8, fontweight='bold', color='#b45309')

    # Cluster -> Telemetry
    ax.annotate("", xy=(z3_x, 0.690), xytext=(z2_x + z2_w, 0.690),
                arrowprops=dict(arrowstyle="->,head_width=0.22,head_length=0.32", color='#6d28d9', lw=1.4))
    ax.text((z2_x + z2_w + z3_x)/2, 0.700, '/metrics', ha='center', va='bottom', fontsize=4.8, fontweight='bold', color='#6d28d9')

    # Cluster -> WORM Vault
    ax.annotate("", xy=(z3_x, 0.280), xytext=(z2_x + z2_w, 0.280),
                arrowprops=dict(arrowstyle="->,head_width=0.22,head_length=0.32", color='#059669', lw=1.4))
    ax.text((z2_x + z2_w + z3_x)/2, 0.290, 'SHA-256', ha='center', va='bottom', fontsize=4.8, fontweight='bold', color='#059669')

    plt.subplots_adjust(left=0.005, right=0.995, top=0.99, bottom=0.01)
    return fig

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent
    TARGET_DIRS = [
        BASE_DIR / "papers" / "University_CSE_Thesis" / "figures",
        BASE_DIR / "papers" / "EAAI_Research_Paper" / "figures",
        BASE_DIR / "papers" / "EAAI_Submission" / "figures",
        BASE_DIR / "data" / "outputs" / "figures",
        BASE_DIR / "reports" / "figures",
    ]
    for d in TARGET_DIRS:
        d.mkdir(parents=True, exist_ok=True)

    print("Generating Clean Kubernetes Deployment Topology (NO Cards)...")
    fig = generate_figure_8_3()
    
    stems = ["fig8_1_fastapi_k8s_topology", "fig8_3_cloud_native_k8s"]
    for stem in stems:
        for d in TARGET_DIRS:
            fig.savefig(d / f"{stem}.pdf", bbox_inches="tight", pad_inches=0.10)
            fig.savefig(d / f"{stem}.png", dpi=300, bbox_inches="tight", pad_inches=0.10)
            print(f"  [SAVED] {d / f'{stem}.pdf'}")
    
    plt.close(fig)
    print("Done generating Figure 8.3!")
