# C-STGB Complete Parameter Directory & Sensitivity Reaction Guide
### **Comprehensive Breakdown of All Parameters, Hyperparameters, and Their Algorithmic Reactions**
**Author:** Nazmul Hasan Nihal (Lead AI / AML Systems Architect)

---

## 1. Executive Summary & Parameter Inventory

The **`C-STGB`** architecture contains:
1. **206,030 Trainable Neural Weights** in the `BurstAwareHGT` spatiotemporal backbone (on standard benchmark topologies like `elliptic_v1`), occupying only **~0.82 MB of RAM**.
2. **6 Learnable Domain-Specific Physicochemical Parameters** ($\lambda_r, \beta_r, \gamma_{\text{cam}}$ across 2 convolution layers).
3. **28 Core Architectural Hyperparameters** controlling data ingestion, wavelet frequency extraction, self-supervised InfoNCE pretraining, GraphSMOTE augmentation, multi-moment pooling, Tri-Model decision stacking, and Mondrian conformal risk bounds.

---

## 2. Complete Parameter Catalog by Pipeline Layer

### Layer 1: Temporal Feature Engineering & Wavelet Decomposition
| Parameter | Default Value | Code Location | Description |
| :--- | :---: | :--- | :--- |
| `window_size` | `10` | `htgnn.py:114` | Rolling transaction window size for burst frequency calculation. |
| `dwt_scaling` | `1.4142` ($\sqrt{2}$) | `htgnn.py:121` | Haar Wavelet normalization constant separating approximation ($c_A$) and detail ($c_D$). |
| `flow_invariants_dim` | `8` | `htgnn.py:242` | Dimension of mass flow & velocity vector ($[d_{\text{in}}, d_{\text{out}}, \text{asym}, f_{\text{in}}, f_{\text{out}}, \text{pass\_through}, c_A, c_D]$). |

---

### Layer 2: Topological Augmentation & Self-Supervised Pretraining
| Parameter | Default Value | Code Location | Description |
| :--- | :---: | :--- | :--- |
| `smote_k_neighbors` | `5` | `htgnn.py:598` | Number of nearest minority neighbors for Cosine-Directed GraphSMOTE interpolation. |
| `smote_ratio` | Dynamic | `htgnn.py:603` | Minority synthetic oversampling factor. |
| `infonce_epochs` | `4` | `htgnn.py:628` | Number of self-supervised contrastive pretraining epochs on unlabeled graph nodes. |
| `infonce_temperature` ($\tau$) | `0.1` | `htgnn.py:628` | Softmax temperature for InfoNCE contrastive cosine similarity scaling. |
| `infonce_jitter_ratio` | `0.05` ($\pm 5\%$) | `htgnn.py:642` | Temporal jitter injected into $\Delta t$ to generate positive contrastive views. |
| `infonce_dropout` | `0.10` (10%) | `htgnn.py:643` | Node feature masking rate for contrastive view generation. |

---

### Layer 3: Spatio-Temporal Neural Backbone (`BurstAwareHGT`)
| Parameter / Weight Tensor | Shape / Value | Trainable? | Code Location | Description |
| :--- | :---: | :---: | :--- | :--- |
| `node_proj.<type>.weight` | `[128, in_dim]` | Yes | `htgnn.py:348` | Heterogeneous linear projection mapping raw features to hidden dimension ($128$). |
| `node_proj.<type>.bias` | `[128]` | Yes | `htgnn.py:348` | Node projection bias vector. |
| `raw_lambda` ($\lambda_r$) | Scalar (`0.10`) | **Yes (Learnable)** | `burst_aware_hgt_conv.py:27` | **Temporal Velocity Decay Prior:** Exponential penalty on dormant inter-transaction delays. |
| `raw_beta` ($\beta_r$) | Scalar (`0.05`) | **Yes (Learnable)** | `burst_aware_hgt_conv.py:28` | **Burst Activity Multiplier:** Attention booster during high-frequency smurfing bursts. |
| `cam_gamma` ($\gamma_{\text{cam}}$) | Scalar (`1.00`) | **Yes (Learnable)** | `burst_aware_hgt_conv.py:30` | **Anti-Camouflage Softness:** Sigmoid cosine gating factor penalizing deceptive edges. |
| `time_proj.weight / bias` | `[32, 16]` / `[32]` | Yes | `burst_aware_hgt_conv.py:35` | Linear projection mapping Sinusoidal LUT time encoding to attention space. |
| `q_linear, k_linear, v_linear` | `[128, 128]` | Yes | `burst_aware_hgt_conv.py:38` | Query, Key, and Value attention transformation matrices. |
| `out_linear.weight / bias` | `[128, 128]` / `[128]` | Yes | `burst_aware_hgt_conv.py:44` | Post-aggregation linear transformation layer. |
| `hidden_channels` | `128` | No (Hyperparam) | `htgnn.py:31` | Latent embedding dimensionality across all GNN layers. |
| `num_layers` | `2` | No (Hyperparam) | `htgnn.py:32` | Number of spatiotemporal message-passing hops. |
| `dropout` | `0.20` | No (Hyperparam) | `htgnn.py:35` | GNN layer dropout probability preventing over-smoothing. |
| `focal_gamma` ($\gamma$) | `2.0` | No (Hyperparam) | `htgnn.py:696` | Focusing parameter in Focal Loss downweighting easy licit examples. |
| `focal_alpha` ($\alpha$) | Dynamic Inverse | No (Hyperparam) | `htgnn.py:681` | Class balance weighting vector in Focal Loss. |
| `ewc_lambda` | `100.0` | No (Hyperparam) | `htgnn.py:645` | Elastic Weight Consolidation penalty preventing catastrophic forgetting. |

---

### Layer 4: Multi-Moment Ego-Neighborhood Subnetwork Pooling
| Parameter | Value | Code Location | Description |
| :--- | :---: | :--- | :--- |
| `num_moments` | `5` | `htgnn.py:832` | Statistical moments extracted per node: Mean ($\bar{z}$), Contrast ($\Delta z$), Std ($\sigma$), Max ($z_{\max}$), Min ($z_{\min}$). |
| `fused_dim` | $x + 6 \times z$ | `htgnn.py:934` | Dimensionality of fused vector: $173 + 128 + 5 \times 128 = 941$ continuous features. |

---

### Layer 5: Tri-Model Stacking Decision Ensemble
| Hyperparameter | Default Value | Code Location | Description |
| :--- | :---: | :--- | :--- |
| `w_xgb` | `0.40` (Tuned: `0.384`) | `htgnn.py:939` | XGBoost soft voting ensemble blend weight. |
| `w_lgb` | `0.35` (Tuned: `0.289`) | `htgnn.py:939` | LightGBM soft voting ensemble blend weight. |
| `w_cat` | `0.25` (Tuned: `0.327`) | `htgnn.py:939` | CatBoost soft voting ensemble blend weight. |
| `n_estimators` (XGB/LGB) | `120` (Tuned: `80`) | `htgnn.py:917` | Maximum boosting trees per model. |
| `max_depth` (XGB/Cat) | `6` (Tuned: `8`) | `htgnn.py:918` | Maximum tree split depth. |
| `num_leaves` (LGBM) | `31` | `htgnn.py:928` | Maximum leaf nodes per tree in LightGBM. |
| `learning_rate` | `0.08` | `htgnn.py:919` | Boosting shrinkage rate for all three tree heads. |
| `scale_pos_weight` | Dynamic ($N_{\text{neg}}/N_{\text{pos}}$) | `htgnn.py:950` | Asymmetric class weighting balancing gradient updates on rare illicit nodes. |
| `dollar_loss_weight` ($w_i$) | $1 + 0.5 \log_{10}(1 + \text{Amt})$ | `htgnn.py:1034` | Dollar-weighted exposure scaling factor for training loss. |

---

### Layer 6: Optimal Threshold & Mondrian Conformal Prediction
| Hyperparameter | Default Value | Code Location | Description |
| :--- | :---: | :--- | :--- |
| `optimal_threshold` ($\tau^*$) | `0.58` (Dynamic) | `htgnn.py:979` | Threshold maximizing F1 on validation slice (searched over $0.40 - 0.85$). |
| `conformal_alpha` ($\alpha$) | `0.10` | `htgnn.py:915` | Target marginal error rate guaranteeing $1 - \alpha = 90\%$ coverage. |
| `conformal_q` ($q$) | `0.0599` (Dynamic) | `htgnn.py:985` | Calibrated non-conformity threshold quantile for prediction sets. |
| `mondrian_strata_percentile` | `50th` (Median) | `htgnn.py:982` | Node degree split separating Central Hubs vs. Peripheral Accounts. |

---

## 3. Parameter Sensitivity & Reaction Analysis Matrix

The table below describes how changing each parameter impacts model behavior:

| Parameter | If You INCREASE It ($\uparrow$) | If You DECREASE It ($\downarrow$) | Recommended Best Practice |
| :--- | :--- | :--- | :--- |
| **`optimal_threshold` ($\tau^*$)** | 🟢 **Higher Precision** (fewer false positives).<br>🔴 **Lower Recall** (misses edge-case mules). | 🟢 **Higher Recall** (catches more laundering).<br>🔴 **Lower Precision** (more false alarms). | Set to **`0.55 - 0.65`** for balanced F1, or **`0.75+`** if analyst capacity is constrained. |
| **`cam_gamma` ($\gamma_{\text{cam}}$)** | 🟢 **Stricter Anti-Camouflage** (isolates clusters aggressively).<br>🔴 Can fragment legitimate subnets if too high. | 🟢 **Smoother Neighborhoods**.<br>🔴 Vulnerable to adversarial camouflage links. | Keep learnable via gradient descent (converges naturally around **`1.2 - 1.8`**). |
| **`raw_lambda` ($\lambda_r$)** | 🟢 **Stronger Time Decay** (old transactions rapidly forgotten).<br>🔴 May miss slow multi-month layering. | 🟢 **Longer Memory**.<br>🔴 Vulnerable to stale network history. | Keep learnable with initial prior $\lambda_0 = 0.10$. |
| **`raw_beta` ($\beta_r$)** | 🟢 **Hyper-Sensitive to Bursts** (amplifies smurfing detection).<br>🔴 Risk of false alerts on regular payroll spikes. | 🟢 **More Stable on High Volumes**.<br>🔴 Slower reaction to rapid mixer bursts. | Keep learnable with initial prior $\beta_0 = 0.05$. |
| **`scale_pos_weight`** | 🟢 **Massive Boost in Recall** (forces trees to focus on rare illicit cases).<br>🔴 Decreases Precision slightly. | 🟢 **Higher Precision**.<br>🔴 Severe collapse in Recall on 99:1 imbalance. | Set to auto-ratio: $\max(1.0, N_{\text{neg}} / N_{\text{pos}})$. |
| **`dollar_loss_weight`** | 🟢 **Zero Misses on High-Value Syndicates** (\$1M+ rings caught).<br>🔴 Small \$10 smurfing rings get less weight. | 🟢 **Equal Treatment across All Amounts**.<br>🔴 High-dollar risk not prioritized. | Keep logarithmic formula: $1.0 + 0.5 \log_{10}(1 + \text{Amount})$. |
| **`hidden_channels`** | 🟢 **Higher Model Capacity & Expressivity**.<br>🔴 Slightly higher RAM and latency (>25 ms if 256). | 🟢 **Ultra-Fast Sub-10ms Inference**.<br>🔴 Slight under-fitting on complex graphs. | Set to **`128`** for optimal latency/accuracy sweet spot. |
| **`num_layers`** | 🟢 **Captures 3-Hop / 4-Hop Transitive Laundering**.<br>🔴 Risk of over-smoothing; higher latency. | 🟢 **Fast & Localized 1-Hop Analysis**.<br>🔴 Misses intermediaries in peeling chains. | Set to **`2`** (optimal for AML 2-hop ego-networks). |
| **`conformal_alpha` ($\alpha$)** | 🟢 **Smaller, Tighter Prediction Sets**.<br>🔴 Higher nominal error rate ($1 - \alpha$). | 🟢 **Guaranteed 99% Coverage** ($\alpha=0.01$).<br>🔴 More accounts routed to Review Queue. | Set to **`0.10`** for retail AML, **`0.01 - 0.05`** for high-risk wire transfers. |
| **`w_xgb / w_lgb / w_cat`** | Adjusts bias toward exact splits (XGB), histogram speed (LGB), or symmetric trees (Cat). | Shifting weight to CatBoost improves stability on extreme 99.9% imbalance. | Use Bayesian tuned blend: **`0.38 XGB + 0.29 LGB + 0.33 Cat`**. |

---

## 4. Parameter Tuning Recipes for Specific Operational Goals

### 🎯 Recipe A: "Max Catch Rate / Ultra-High Recall" (Regulator Strict Audit)
* **Goal:** Catch 80%+ of all money laundering; prioritize zero missed illicit rings.
* **Tuning Adjustments:**
  1. `optimal_threshold` $\tau^* \to \mathbf{0.45}$ (lower decision hurdle).
  2. `scale_pos_weight` multiplier $\to \mathbf{1.5 \times (N_{\text{neg}}/N_{\text{pos}})}$.
  3. `raw_beta` ($\beta_r$) initialization $\to \mathbf{0.15}$ (boost sensitivity to smurfing bursts).
  4. `conformal_alpha` $\alpha \to \mathbf{0.05}$ (95% coverage guarantee).

### 🎯 Recipe B: "Zero False Alarms / Analyst Capacity Constrained"
* **Goal:** Minimize manual alert reviews; only trigger alarms on near-certain illicit syndicates.
* **Tuning Adjustments:**
  1. `optimal_threshold` $\tau^* \to \mathbf{0.75 - 0.80}$.
  2. `cam_gamma` ($\gamma_{\text{cam}}$) $\to \mathbf{2.5}$ (very strict camouflage penalty).
  3. `max_depth` in trees $\to \mathbf{4}$ (prevent overfitting to fringe noise).
  4. Blend weights $\to \mathbf{0.60 \text{ XGB} + 0.20 \text{ LGB} + 0.20 \text{ Cat}}$.

### 🎯 Recipe C: "Sub-10ms Ultra-Low Latency Gateway" (Instant Cards/Payments)
* **Goal:** Maximize transaction throughput (10,000+ TPS) with minimal CPU/GPU overhead.
* **Tuning Adjustments:**
  1. `hidden_channels` $\to \mathbf{64}$.
  2. `n_estimators` in tree ensemble $\to \mathbf{60}$.
  3. GNN `num_layers` $\to \mathbf{1}$.
  4. Batch Latency Drops to **~7.5 ms**.
