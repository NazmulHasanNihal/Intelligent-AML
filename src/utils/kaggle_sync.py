import os
import subprocess
from pathlib import Path

# Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
OUTPUT_DIR = BASE_DIR / "data" / "outputs"

def pull_kaggle_outputs(kernel_slug: str):
    """
    Pulls the output artifacts (models, heatmaps, parquets) from a finished Kaggle notebook
    down to the local data/outputs/ directory.
    
    Args:
        kernel_slug (str): The Kaggle username/notebook-name (e.g., 'johndoe/htgnn-training')
    """
    print(f"Syncing outputs from Kaggle Execution Plane: {kernel_slug}")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Run the kaggle kernels output command
    cmd = [
        "kaggle", "kernels", "output",
        kernel_slug,
        "-p", str(OUTPUT_DIR)
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print(f"Successfully synced artifacts to {OUTPUT_DIR}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to sync outputs. Ensure you have run 'kaggle kernels push' and the notebook has finished executing.")
        print(f"Error: {e}")

if __name__ == "__main__":
    # Example usage: Replace with your actual Kaggle notebook slug
    # pull_kaggle_outputs("your-kaggle-username/01-data-ingestion-and-graph")
    print("Kaggle Sync Utility initialized. Waiting for execution instructions.")
