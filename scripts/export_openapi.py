"""
export_openapi.py — Exports typed OpenAPI schema from FastAPI backend.
"""

import sys
import os
sys.path.insert(0, os.path.abspath("."))
import json
from pathlib import Path
from src.engine.api import app

def main():
    openapi_schema = app.openapi()
    
    # Save to api/openapi.json
    api_dir = Path("api")
    api_dir.mkdir(parents=True, exist_ok=True)
    out_file = api_dir / "openapi.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=2)
    print(f"Exported OpenAPI schema to {out_file}")

    # Also save to frontend/src/lib/api/openapi.json
    frontend_api_dir = Path("frontend/src/lib/api")
    frontend_api_dir.mkdir(parents=True, exist_ok=True)
    fe_out_file = frontend_api_dir / "openapi.json"
    with open(fe_out_file, "w", encoding="utf-8") as f:
        json.dump(openapi_schema, f, indent=2)
    print(f"Exported OpenAPI schema to {fe_out_file}")

if __name__ == "__main__":
    main()
