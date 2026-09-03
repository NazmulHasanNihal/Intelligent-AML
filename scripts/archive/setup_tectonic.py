import os
import sys
import zipfile
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TOOLS_DIR = BASE_DIR / "tools" / "tectonic"
ZIP_PATH = BASE_DIR / "tools" / "tectonic.zip"
EXE_PATH = TOOLS_DIR / "tectonic.exe"

TECTONIC_URL = "https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic@0.17.0/tectonic-0.17.0-x86_64-pc-windows-msvc.zip"

def setup_tectonic():
    TOOLS_DIR.mkdir(parents=True, exist_ok=True)
    if not EXE_PATH.exists():
        print(f"Downloading Tectonic compiler from {TECTONIC_URL}...")
        headers = {"User-Agent": "Mozilla/5.0"}
        req = urllib.request.Request(TECTONIC_URL, headers=headers)
        with urllib.request.urlopen(req) as response, open(ZIP_PATH, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        print("Extracting Tectonic...")
        with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
            zip_ref.extractall(TOOLS_DIR)
        if ZIP_PATH.exists():
            ZIP_PATH.unlink()
        print(f"Tectonic installed successfully at {EXE_PATH}")
    else:
        print(f"Tectonic already installed at {EXE_PATH}")

    # Test execution
    import subprocess
    res = subprocess.run([str(EXE_PATH), "--version"], capture_output=True, text=True)
    print(f"Version output: {res.stdout.strip()}")

if __name__ == "__main__":
    setup_tectonic()
