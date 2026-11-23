import os
import re
import json

findings = {
    'metrics': [],
    'personas': [],
    'claims': [],
    'timestamps': []
}

app_dir = 'frontend/src'

for root, _, files in os.walk(app_dir):
    for f in files:
        if f.endswith(('.tsx', '.ts', '.jsx', '.js')):
            path = os.path.join(root, f).replace('\\', '/')
            with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
                lines = fp.readlines()
                for line_idx, line in enumerate(lines):
                    # Check metrics
                    for m in re.finditer(r'(\d+(?:\.\d+)?%|\d+(?:\.\d+)?\s*ms|2,028|2,029|1,280|748)', line):
                        val = m.group(1)
                        if val not in ['100%', '0%', '50%']:
                            findings['metrics'].append({
                                'file': path,
                                'line': line_idx + 1,
                                'value': val,
                                'text': line.strip()
                            })
                    # Check personas
                    for p in ['Sarah L. Jenkins', 'Sarah Jenkins', 'Nazmul Hasan', 'Kazi Farhan', 'Musrat Jahan', 'Tanvir Mahmud']:
                        if p in line:
                            findings['personas'].append({
                                'file': path,
                                'line': line_idx + 1,
                                'persona': p,
                                'text': line.strip()
                            })
                    # Check claims
                    for c in ['Air-Gap', 'EXTERNAL EGRESS', '00:04:12', 'LIVE']:
                        if c in line and not line.strip().startswith('//'):
                            findings['claims'].append({
                                'file': path,
                                'line': line_idx + 1,
                                'claim': c,
                                'text': line.strip()
                            })
                    # Check timestamps
                    if '2026-09-02' in line:
                        findings['timestamps'].append({
                            'file': path,
                            'line': line_idx + 1,
                            'timestamp': '2026-09-02',
                            'text': line.strip()
                        })

print('Metrics count:', len(findings['metrics']))
print('Personas count:', len(findings['personas']))
print('Claims count:', len(findings['claims']))
print('Timestamps count:', len(findings['timestamps']))

with open('audit_findings.json', 'w', encoding='utf-8') as out:
    json.dump(findings, out, indent=2)
