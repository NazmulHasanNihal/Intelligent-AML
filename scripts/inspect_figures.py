import pymupdf

def inspect():
    doc1 = pymupdf.open('papers/IEEE_Research_Paper/figures/fig6_system_architecture.pdf')
    page1 = doc1[0]
    print('=== FIG 1 TEXT BLOCKS ===')
    for b in page1.get_text('blocks'):
        txt = b[4].strip().replace('\n', ' ')
        safe = txt.encode('ascii', errors='replace').decode('ascii')
        print(f"y={b[1]:.1f}..{b[3]:.1f}, x={b[0]:.1f}..{b[2]:.1f}: {safe}")

    doc2 = pymupdf.open('papers/IEEE_Research_Paper/figures/fig2_tsne_manifold_separation.pdf')
    page2 = doc2[0]
    print('\n=== FIG 2 TEXT BLOCKS ===')
    for b in page2.get_text('blocks'):
        txt = b[4].strip().replace('\n', ' ')
        safe = txt.encode('ascii', errors='replace').decode('ascii')
        print(f"y={b[1]:.1f}..{b[3]:.1f}, x={b[0]:.1f}..{b[2]:.1f}: {safe}")

if __name__ == '__main__':
    inspect()
