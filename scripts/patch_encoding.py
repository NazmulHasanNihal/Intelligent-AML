import json

nb_path = 'notebooks/Layer1_Ingestion/01_Layer1_Data_Ingestion_v4_COMPLETE.ipynb'
script_path = 'scripts/layer_1_graph_builder.py'

fix_code = "import sys; hasattr(sys.stdout, 'reconfigure') and sys.stdout.reconfigure(encoding='utf-8')\n"

with open(script_path, 'r', encoding='utf-8') as f:
    content = f.read()

if 'sys.stdout.reconfigure' not in content:
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(fix_code + content)

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

patched = False
for c in nb['cells']:
    if c['cell_type'] == 'code':
        source = c['source']
        if len(source) > 0:
            if 'sys.stdout.reconfigure' not in ''.join(source):
                source.insert(0, fix_code)
            patched = True
            break

if patched:
    with open(nb_path, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)

print('Patched stdout encoding!')
