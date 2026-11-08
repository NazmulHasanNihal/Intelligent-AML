import os, re

thesis_dir = 'papers/University_CSE_Thesis'
tex_files = [
    'chapters/ch1_introduction.tex',
    'chapters/ch2_literature_review.tex',
    'chapters/ch3_system_architecture.tex',
    'chapters/ch4_data_pipeline.tex',
    'chapters/ch5_conformal_ethics.tex',
    'chapters/ch6_xai_agentic_sar.tex',
    'chapters/ch7_experiments.tex',
    'chapters/ch8_software_engineering.tex',
    'chapters/ch9_conclusion.tex',
    'chapters/ch10_appendices.tex'
]

figure_inventory = []

for tf in tex_files:
    path = os.path.join(thesis_dir, tf)
    if not os.path.exists(path): continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by figure environment
    pattern = r'\\begin\{figure\}.*?\\end\{figure\}'
    fig_envs = re.findall(pattern, content, re.DOTALL)
    for env in fig_envs:
        # find \includegraphics
        img_matches = re.findall(r'\\includegraphics(?:\[.*?\])?\{([^}]+)\}', env)
        caption_m = re.search(r'\\caption(?:\[(.*?)\])?\{(.*?)\}', env, re.DOTALL)
        label_m = re.search(r'\\label\{([^}]+)\}', env)
        
        cap = caption_m.group(1) if (caption_m and caption_m.group(1)) else (caption_m.group(2) if caption_m else '')
        lbl = label_m.group(1) if label_m else ''
        for img in img_matches:
            figure_inventory.append({
                'chapter': tf,
                'img': img,
                'basename': os.path.basename(img),
                'caption': cap.strip().replace('\n', ' '),
                'label': lbl
            })

print(f'Total figures found across chapters: {len(figure_inventory)}')
for i, item in enumerate(figure_inventory, 1):
    print(f"{i:02d}. [{item['chapter'].split('/')[-1]}] {item['basename']} -> label: {item['label']} -> {item['caption'][:60]}")

