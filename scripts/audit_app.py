import os, re

app_dir = 'frontend/src/app'
imports = set()
for root, dirs, files in os.walk(app_dir):
    for f in files:
        if f.endswith(('.ts', '.tsx')):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fp:
                for line in fp:
                    m = re.search(r'from\s+[\'"]([^\'"]+)[\'"]', line)
                    if m:
                        imports.add(m.group(1))

print("=== ALL IMPORTS IN frontend/src/app ===")
for imp in sorted(imports):
    print(" ", imp)
