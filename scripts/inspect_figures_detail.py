import re
import os

with open("scripts/generate_all_publication_figures.py", encoding="utf-8") as f:
    text = f.read()

funcs = [m.start() for m in re.finditer(r"def (plot_[a-zA-Z0-9_]+)", text)]
for idx in funcs:
    line = text[idx:idx+100].splitlines()[0]
    print(line)

