"""
Intelligent AML — Neuro-Symbolic Framework
for Omni-Channel Financial Fraud Detection

Root package initializer.
"""

import os
import sys

# Critical Windows OpenMP & PyTorch DLL conflict fix
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["OMP_NUM_THREADS"] = "1"

# Windows PyTorch DLL auto-resolver
if sys.platform == "win32":
    for p in list(sys.path):
        if not p or not os.path.exists(p):
            continue
        torch_lib = os.path.join(p, "torch", "lib")
        if os.path.isdir(torch_lib):
            if hasattr(os, "add_dll_directory"):
                try:
                    os.add_dll_directory(torch_lib)
                except Exception:
                    pass
            if torch_lib not in os.environ.get("PATH", ""):
                os.environ["PATH"] = torch_lib + os.pathsep + os.environ.get("PATH", "")
    try:
        import torch
    except Exception:
        pass

__version__ = "1.0.0"
__author__ = "Md. Nazmul"
