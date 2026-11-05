from pathlib import Path

p = Path("scripts/generate_publication_figures_extra.py")
content = p.read_text(encoding="utf-8")

content = content.replace(
    'OUT_DIRS = [out_fig_dir, thesis_fig_dir, eaai_fig_dir]',
    'OUT_DIRS = [out_fig_dir, thesis_fig_dir, eaai_fig_dir, BASE_DIR / "papers" / "EAAI_Submission" / "figures", BASE_DIR / "reports" / "figures"]'
)
content = content.replace("pad_inches=0.05", "pad_inches=0.15")
content = content.replace("pad_inches=0.04", "pad_inches=0.15")

p.write_text(content, encoding="utf-8")
print("Patched generate_publication_figures_extra.py with pad_inches=0.15 and all directories")

