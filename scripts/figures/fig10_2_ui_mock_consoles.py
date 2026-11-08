"""
Figure 10.2: Verification and Synchronization of UI Mock Consoles
Standalone publication script for C-STGB monograph.
Synchronizes and verifies all 6 UI console PNG files across all 5 directories:
1. 01_surveillance_desk.png
2. 02_network_topology.png
3. 03_case_management.png
4. 04_case_detail_four_eyes.png
5. 05_multi_agent_sar.png
6. 06_model_governance_drift.png
"""
import sys
import shutil
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import TARGET_DIRS

UI_FILES = [
    "01_surveillance_desk.png",
    "02_network_topology.png",
    "03_case_management.png",
    "04_case_detail_four_eyes.png",
    "05_multi_agent_sar.png",
    "06_model_governance_drift.png"
]

def generate():
    # Source is papers/University_CSE_Thesis/figures
    src_dir = TARGET_DIRS[0]
    print(f"Checking and synchronizing {len(UI_FILES)} UI console screenshots...")
    
    for f in UI_FILES:
        src = src_dir / f
        if not src.exists():
            print(f"  [WARN] Source file missing: {src}")
            continue
        for d in TARGET_DIRS[1:]:
            d.mkdir(parents=True, exist_ok=True)
            dst = d / f
            if not dst.exists() or src.stat().st_size != dst.stat().st_size:
                shutil.copyfile(src, dst)
        print(f"  [OK] Synchronized {f} across all 5 directories.")

if __name__ == "__main__":
    generate()
