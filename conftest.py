import os
import sys
from pathlib import Path

# Add PyTorch safety guards on Windows
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
_repo_root = Path(__file__).resolve().parent
_torch_candidates = [
    Path(sys.prefix) / "Lib" / "site-packages" / "torch" / "lib",
    _repo_root / ".venv" / "Lib" / "site-packages" / "torch" / "lib",
    _repo_root / "venv" / "Lib" / "site-packages" / "torch" / "lib",
]
_dll_handles = []
for _torch_lib in _torch_candidates:
    if _torch_lib.exists():
        os.environ["PATH"] = str(_torch_lib) + ";" + os.environ.get("PATH", "")
        if hasattr(os, "add_dll_directory"):
            try:
                _dll_handles.append(os.add_dll_directory(str(_torch_lib)))
            except Exception:
                pass
        break

# Pre-initialize torch before numpy/pandas to prevent Windows DLL conflicts
try:
    import torch
except Exception:
    pass
