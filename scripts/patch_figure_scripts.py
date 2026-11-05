from pathlib import Path

# 1. Patch scripts/generate_all_publication_figures.py
p1 = Path("scripts/generate_all_publication_figures.py")
c1 = p1.read_text(encoding="utf-8")
c1 = c1.replace(
    'OUT_DIRS = [\n    BASE_DIR / "data" / "outputs" / "figures",\n    thesis_fig_dir,\n    eaai_fig_dir,\n]',
    'OUT_DIRS = [\n    BASE_DIR / "data" / "outputs" / "figures",\n    thesis_fig_dir,\n    eaai_fig_dir,\n    BASE_DIR / "papers" / "EAAI_Submission" / "figures",\n    BASE_DIR / "reports" / "figures",\n]'
)
c1 = c1.replace(
    'OUT_DIRS = [\r\n    BASE_DIR / "data" / "outputs" / "figures",\r\n    thesis_fig_dir,\r\n    eaai_fig_dir,\r\n]',
    'OUT_DIRS = [\r\n    BASE_DIR / "data" / "outputs" / "figures",\r\n    thesis_fig_dir,\r\n    eaai_fig_dir,\r\n    BASE_DIR / "papers" / "EAAI_Submission" / "figures",\r\n    BASE_DIR / "reports" / "figures",\r\n]'
)
c1 = c1.replace("pad_inches=0.06", "pad_inches=0.15")
p1.write_text(c1, encoding="utf-8")
print("generate_all_publication_figures.py patched")

# 2. Patch scripts/generate_final_10_of_10_figures.py
p2 = Path("scripts/generate_final_10_of_10_figures.py")
c2 = p2.read_text(encoding="utf-8")
c2 = c2.replace(
    'TARGET_DIRS = [data_fig_dir, thesis_fig_dir, eaai_fig_dir]',
    'TARGET_DIRS = [data_fig_dir, thesis_fig_dir, eaai_fig_dir, BASE_DIR / "papers" / "EAAI_Submission" / "figures", BASE_DIR / "reports" / "figures"]'
)
c2 = c2.replace("pad_inches=0.03", "pad_inches=0.15")
p2.write_text(c2, encoding="utf-8")
print("generate_final_10_of_10_figures.py patched")

# 3. Patch scripts/generate_thesis_distinct_figures.py
p3 = Path("scripts/generate_thesis_distinct_figures.py")
c3 = p3.read_text(encoding="utf-8")
c3 = c3.replace(
    'TARGET_DIRS = [thesis_fig_dir, eaai_fig_dir, data_fig_dir]',
    'TARGET_DIRS = [thesis_fig_dir, eaai_fig_dir, data_fig_dir, BASE_DIR / "papers" / "EAAI_Submission" / "figures", BASE_DIR / "reports" / "figures"]'
)
c3 = c3.replace("pad_inches=0.04", "pad_inches=0.15")
p3.write_text(c3, encoding="utf-8")
print("generate_thesis_distinct_figures.py patched")

