import os
import sys
from pathlib import Path

# Add PyTorch safety guards on Windows
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
_venv_torch_lib = Path(__file__).resolve().parent / "venv" / "Lib" / "site-packages" / "torch" / "lib"
_dll_handles = []
if _venv_torch_lib.exists():
    os.environ["PATH"] = str(_venv_torch_lib) + ";" + os.environ.get("PATH", "")
    if hasattr(os, "add_dll_directory"):
        try:
            _dll_handles.append(os.add_dll_directory(str(_venv_torch_lib)))
        except Exception:
            pass

# Pre-initialize torch before numpy/pandas to prevent Windows DLL conflicts
try:
    import torch
except Exception:
    pass
