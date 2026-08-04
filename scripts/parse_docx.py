import zipfile
import xml.etree.ElementTree as ET
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

docx_path = r'c:\Research and Business Project\Intelligent AML\planning_document\Intelligent_AML_75Papers_FINAL_10of10.docx'
with zipfile.ZipFile(docx_path) as z:
    xml_content = z.read('word/document.xml')

tree = ET.fromstring(xml_content)
ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

tables = tree.findall('.//w:tbl', ns)
print(f'Total tables found: {len(tables)}')

all_rows = []
for tbl_idx, tbl in enumerate(tables):
    rows = tbl.findall('.//w:tr', ns)
    print(f'\n--- Table {tbl_idx+1}: {len(rows)} rows ---')
    for r_idx, r in enumerate(rows):
        cells = r.findall('.//w:tc', ns)
        cell_texts = []
        for c in cells:
            t = ' '.join([node.text for node in c.findall('.//w:t', ns) if node.text])
            cell_texts.append(t.strip())
        sep = " | "
        row_str = sep.join(cell_texts)
        all_rows.append(row_str)
        if r_idx < 10:
            print(f'Row {r_idx+1}: {row_str[:150]}')

with open('all_docx_rows.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(all_rows))
print('\nSaved all_docx_rows.txt')
