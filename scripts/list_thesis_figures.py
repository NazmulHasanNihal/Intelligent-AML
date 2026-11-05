import os
import re
from pathlib import Path

thesis_dir = Path("papers/University_CSE_Thesis")
tex_files = sorted(thesis_dir.rglob("*.tex"))

figs = []
for tf in tex_files:
    content = tf.read_text(encoding="utf-8", errors="ignore")
    pattern = re.compile(r"\\begin\{figure\}(?:\[.*?\])?(.*?)\\end\{figure\}", re.DOTALL)
    for match in pattern.finditer(content):
        ftext = match.group(1)
        graphics = re.findall(r"\\includegraphics(?:\[.*?\])?\{([^}]+)\}", ftext)
        captions = re.findall(r"\\caption(?:\[.*?\])?\{([^}]+)\}", ftext)
        labels = re.findall(r"\\label\{([^}]+)\}", ftext)
        figs.append({
            "file": tf.relative_to(thesis_dir).as_posix(),
            "label": labels[0] if labels else "N/A",
            "graphics": ", ".join(graphics),
            "caption": captions[0][:75] if captions else "No caption"
        })

print(f"Total figures found: {len(figs)}")
for i, f in enumerate(figs, 1):
    print(f"{i:2d}. [{f['file']}] {f['label']} -> {f['graphics']} | {f['caption']}")
