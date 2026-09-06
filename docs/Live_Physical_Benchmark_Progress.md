# 🚀 Live Physical Benchmark Execution Progress

**Last Updated:** `2026-09-04 08:31:34 UTC`  
**Overall Completion:** `143/182 Model Runs` (**78.6%**)  
**Resumption Guard:** Atomic per-model JSON checkpoints active (safe against crashes/power loss)

---

## Benchmark Execution Matrix (Real Empirical Results)

| Dataset Identifier | Completed Models | Execution Status | C-STGB F1 | C-STGB PR-AUC |
| :--- | :---: | :---: | :---: | :---: |
| `elliptic_v1` | 13/13 | **COMPLETED** | 99.44% | 1.0000 |
| `elliptic_v2` | 13/13 | **COMPLETED** | 100.00% | 1.0000 |
| `ibm_amlsim_hi_small` | 13/13 | **COMPLETED** | 37.70% | 0.3550 |
| `ibm_amlsim_li_small` | 13/13 | **COMPLETED** | 15.76% | 0.1485 |
| `mtgox_leaked` | 13/13 | **COMPLETED** | 72.21% | 0.8306 |
| `saml_d` | 13/13 | **COMPLETED** | 93.68% | 0.9574 |
| `paysim1` | 13/13 | **COMPLETED** | 10.68% | 0.1173 |
| `eth_phishing` | 0/13 | **PENDING** | - | - |
| `xblock_eth` | 13/13 | **COMPLETED** | 96.94% | 0.9915 |
| `cc_transactions` | 13/13 | **COMPLETED** | 51.40% | 0.5213 |
| `data_generator` | 13/13 | **COMPLETED** | 99.93% | 1.0000 |
| `dgraphfin` | 13/13 | **COMPLETED** | 97.91% | 0.9979 |
| `smart_ponzi` | 0/13 | **PENDING** | - | - |
| `synthaml` | 0/13 | **PENDING** | - | - |

---

## Instructions for Resumption
If the machine is turned off, restarted, or interrupted:
```bash
python scripts/master_physical_benchmark_runner.py
```
The script will automatically detect all existing checkpoints and resume instantly from where it stopped.
