with open('scripts/generate_final_10_of_10_figures.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for l in lines:
    if 'print("14. COMPLIANCE ALERT-VOLUME FUNNEL CHART (Ch 5) (Upgraded)' in l:
        new_lines.append('print("14. COMPLIANCE ALERT-VOLUME FUNNEL CHART (Ch 5) (Upgraded)")\n')
    elif 'print("14. COMPLIANCE ALERT-VOLUME FUNNEL CHART (Ch 5)...")' in l:
        continue
    else:
        new_lines.append(l)

with open('scripts/generate_final_10_of_10_figures.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Fixed line 1215 in generate_final_10_of_10_figures.py")

