"""Master execution script: Discovers and runs all standalone figure scripts in scripts/figures/.
Asserts 100% success rate with zero failures.
"""

import sys
import subprocess
import glob
from pathlib import Path

def main():
    root = Path(__file__).resolve().parent
    # Find all fig*.py files
    scripts = sorted(root.glob("fig*.py"))
    
    print(f"==================================================")
    print(f"DISCOVERED {len(scripts)} STANDALONE FIGURE SCRIPTS")
    print(f"==================================================")
    
    failed = []
    passed = []
    
    for i, s in enumerate(scripts, 1):
        print(f"[{i:02d}/{len(scripts):02d}] Running {s.name}...", end=" ", flush=True)
        res = subprocess.run([sys.executable, str(s)], capture_output=True, text=True)
        if res.returncode == 0:
            print("OK")
            passed.append(s.name)
        else:
            print("FAILED")
            print(f"--- STDERR for {s.name} ---")
            print(res.stderr)
            print(f"--- STDOUT for {s.name} ---")
            print(res.stdout)
            failed.append((s.name, res.stderr))
            
    print("\n" + "="*50)
    print(f"SUMMARY: {len(passed)} PASSED, {len(failed)} FAILED out of {len(scripts)}")
    print("="*50)
    
    if failed:
        print("\nFailed scripts:")
        for name, err in failed:
            print(f"- {name}: {err.strip().splitlines()[-1] if err.strip() else 'Unknown error'}")
        sys.exit(1)
    else:
        print("\nALL FIGURE SCRIPTS EXECUTED SUCCESSFULLY (EXIT CODE 0)!")
        sys.exit(0)

if __name__ == "__main__":
    main()

