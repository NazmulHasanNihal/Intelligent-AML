import re

scripts = [
    'scripts/generate_all_publication_figures.py',
    'scripts/generate_publication_figures_extra.py',
    'scripts/generate_final_10_of_10_figures.py'
]

for s in scripts:
    with open(s, 'r', encoding='utf-8') as f:
        c = f.read()
    print(f'=== {s} ===')
    matches = re.findall(r'def\s+(\w+)\s*\(', c)
    print('Functions:', matches)
    save_matches = re.findall(r'save\w*\([^,\)]+,\s*[\'"]([^\'"]+)[\'"]', c)
    print('Saves:', set(save_matches))

