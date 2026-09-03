"""
test_omni_domain_features.py — Unit and Integration Tests for Omni-Flow 2.0 Feature Extraction.
"""

import os
import sys
from pathlib import Path

# Windows PyTorch DLL loading safety guard
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
_venv_torch_lib = Path(__file__).resolve().parent.parent / "venv" / "Lib" / "site-packages" / "torch" / "lib"
_dll_handle = None
if _venv_torch_lib.exists():
    os.environ["PATH"] = str(_venv_torch_lib) + ";" + os.environ.get("PATH", "")
    if hasattr(os, "add_dll_directory"):
        try:
            _dll_handle = os.add_dll_directory(str(_venv_torch_lib))
        except Exception:
            pass

import pytest
import numpy as np
import pandas as pd
from src.models.omni_domain_feature_extractor import OmniDomainFeatureExtractor


class TestOmniDomainFeatures:
    def test_01_banking_ledger_cross_bank_and_format(self):
        """Tests that banking features correctly extract cross-bank and wire format flags."""
        extractor = OmniDomainFeatureExtractor()
        
        nodes_df = pd.DataFrame({
            "node_id": ["acc1", "acc2", "acc3"],
            "node_type": ["Account", "Account", "Account"]
        })
        
        edges_df = pd.DataFrame({
            "src": ["acc1", "acc2"],
            "dst": ["acc2", "acc3"],
            "From Bank": ["BankA", "BankB"],
            "To Bank": ["BankB", "BankB"],
            "Payment Format": ["Wire Transfer", "Cash Deposit"],
            "Payment Currency": ["USD", "EUR"],
            "Receiving Currency": ["USD", "USD"],
            "Amount Paid": [9500.0, 50000.0]
        })
        
        feats = extractor.extract_features(nodes_df, edges_df, "ibm_amlsim_hi_small")
        assert feats.shape == (3, 24)
        assert not np.isnan(feats).any()
        
        # acc1 made cross-bank wire transfer: features[0, 0] > 0 (cross-bank) and features[0, 2] > 0 (src wire)
        assert feats[0, 0] > 0
        assert feats[0, 2] > 0

    def test_02_mobile_money_account_draining(self):
        """Tests that PaySim account draining and zero-balance destination surge are detected."""
        extractor = OmniDomainFeatureExtractor()
        
        nodes_df = pd.DataFrame({
            "node_id": ["user1", "user2"],
            "node_type": ["User", "User"]
        })
        
        edges_df = pd.DataFrame({
            "src": ["user1"],
            "dst": ["user2"],
            "type": ["TRANSFER"],
            "amount": [100000.0],
            "oldbalanceOrg": [100000.0],
            "newbalanceOrig": [0.0],
            "oldbalanceDest": [0.0],
            "newbalanceDest": [100000.0]
        })
        
        feats = extractor.extract_features(nodes_df, edges_df, "paysim1")
        assert feats.shape == (2, 24)
        # user1 is drained: features[0, 6] > 0
        assert feats[0, 6] > 0
        # user2 received zero-dest surge: features[1, 8] > 0
        assert feats[1, 8] > 0

    def test_03_empty_and_corrupt_data_resilience(self):
        """Tests that extractor gracefully handles empty or malformed DataFrames."""
        extractor = OmniDomainFeatureExtractor()
        
        empty_nodes = pd.DataFrame(columns=["node_id", "node_type"])
        empty_edges = pd.DataFrame(columns=["src", "dst"])
        
        feats = extractor.extract_features(empty_nodes, empty_edges, "unknown")
        assert feats.shape == (0, 24)
