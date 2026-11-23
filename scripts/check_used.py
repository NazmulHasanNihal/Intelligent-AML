import os, re

def check_used():
    used_files = set()
    to_scan = []
    
    # Start with all app files
    for root, dirs, files in os.walk('frontend/src/app'):
        for f in files:
            if f.endswith(('.ts', '.tsx')):
                to_scan.append(os.path.join(root, f))
                used_files.add(os.path.abspath(os.path.join(root, f)))
    
    # Also include proxy.ts
    if os.path.exists('frontend/src/proxy.ts'):
        to_scan.append('frontend/src/proxy.ts')
        used_files.add(os.path.abspath('frontend/src/proxy.ts'))

    while to_scan:
        curr = to_scan.pop(0)
        with open(curr, 'r', encoding='utf-8') as fp:
            content = fp.read()
        
        matches = re.findall(r'from\s+[\'"]([^\'"]+)[\'"]', content)
        for m in matches:
            if m.startswith('@/'):
                target_rel = m[2:]
                target_base = os.path.join('frontend/src', target_rel)
                for ext in ['', '.ts', '.tsx', '.js', '.jsx', '/index.ts', '/index.tsx', '/index.js']:
                    candidate = target_base + ext
                    if os.path.isfile(candidate):
                        cand_abs = os.path.abspath(candidate)
                        if cand_abs not in used_files:
                            used_files.add(cand_abs)
                            to_scan.append(candidate)
                        break

    print(f"Total active files referenced by App Router: {len(used_files)}")
    
    all_src_files = []
    for root, dirs, files in os.walk('frontend/src'):
        for f in files:
            if f.endswith(('.ts', '.tsx', '.js', '.jsx')):
                all_src_files.append(os.path.abspath(os.path.join(root, f)))

    unused = [f for f in all_src_files if f not in used_files]
    print(f"Total src files: {len(all_src_files)}")
    print(f"Unused legacy files: {len(unused)}")
    print("Unused files sample:")
    for u in unused[:15]:
        print(" ", os.path.relpath(u, 'frontend/src'))

check_used()
