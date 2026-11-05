from pathlib import Path

# Fix sys.path in generate_final_10_of_10_figures.py
p1 = Path("scripts/generate_final_10_of_10_figures.py")
c1 = p1.read_text(encoding="utf-8")
c1 = c1.replace(
    'BASE_DIR = Path(__file__).resolve().parent.parent',
    'BASE_DIR = Path(__file__).resolve().parent.parent\nimport sys\nif str(BASE_DIR) not in sys.path:\n    sys.path.insert(0, str(BASE_DIR))'
)
p1.write_text(c1, encoding="utf-8")

# Fix sys.path in generate_all_publication_figures.py
p2 = Path("scripts/generate_all_publication_figures.py")
c2 = p2.read_text(encoding="utf-8")
c2 = c2.replace(
    'BASE_DIR = Path(__file__).resolve().parent.parent',
    'BASE_DIR = Path(__file__).resolve().parent.parent\nimport sys\nif str(BASE_DIR) not in sys.path:\n    sys.path.insert(0, str(BASE_DIR))'
)
p2.write_text(c2, encoding="utf-8")

print("Added sys.path to both generators")

