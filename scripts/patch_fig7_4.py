import sys

with open('scripts/generate_final_10_of_10_figures.py', 'r', encoding='utf-8') as f:
    txt = f.read()

target = '11. CRITICAL DIFFERENCE'

if target in txt:
    start_idx = txt.find(target) - 72 # line before header
    end_str = 'save_fig(fig, ["fig_critical_difference_lollipop", "fig7_3_critical_difference_lollipop"])'
    end_idx = txt.find(end_str, start_idx) + len(end_str)
    
    new_section = '''print("======================================================================")
print("11. CRITICAL DIFFERENCE (CD) & DOMAIN SYNTHESIS CHART (Fig 7.4)")
print("======================================================================")
from scripts.redesign_fig7_4_critical_difference import generate_figure_7_4
fig = generate_figure_7_4()
save_fig(fig, ["fig_critical_difference_lollipop", "fig7_3_critical_difference_lollipop"])'''
    
    txt = txt[:start_idx] + new_section + txt[end_idx:]
    with open('scripts/generate_final_10_of_10_figures.py', 'w', encoding='utf-8') as f:
        f.write(txt)
    print('Successfully patched generate_final_10_of_10_figures.py!')
else:
    print('Target not found')

