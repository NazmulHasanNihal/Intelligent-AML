import fitz

doc = fitz.open('papers/University_CSE_Thesis/figures/fig_leave_one_out_impact.pdf')
page = doc[0]
rect = page.rect
print(f"Auditing fig_leave_one_out_impact.pdf ({rect.width:.2f} x {rect.height:.2f} pt)...")

blocks = page.get_text('blocks')
for i, b in enumerate(blocks):
    clean = ''.join(c if ord(c) < 128 else '?' for c in b[4].replace('\n', ' ')[:60])
    print(f"Block {i}: ({b[0]:.1f}, {b[1]:.1f}, {b[2]:.1f}, {b[3]:.1f}) -> {clean}")

words = page.get_text('words')
overlaps = []
for i in range(len(words)):
    for j in range(i + 1, len(words)):
        w1 = words[i]
        w2 = words[j]
        if w1[5] == w2[5] and w1[6] == w2[6]:
            continue
        r1 = fitz.Rect(w1[0], w1[1], w1[2], w1[3])
        r2 = fitz.Rect(w2[0], w2[1], w2[2], w2[3])
        intersect = r1.intersect(r2)
        if not intersect.is_empty:
            area = intersect.width * intersect.height
            min_area = min(r1.width * r1.height, r2.width * r2.height)
            if min_area > 0 and (area / min_area) > 0.08:
                overlaps.append((w1[4], w2[4], area, w1, w2))

print(f"\nTotal collisions: {len(overlaps)}")
by_block = {}
for ov in overlaps:
    key = (ov[3][5], ov[4][5])
    by_block.setdefault(key, []).append(ov)

for k, v in by_block.items():
    clean_0 = ''.join(c if ord(c) < 128 else '?' for c in v[0][0])
    clean_1 = ''.join(c if ord(c) < 128 else '?' for c in v[0][1])
    print(f"Block pair {k} ({len(v)} collisions): e.g. '{clean_0}' overlaps '{clean_1}' (area {v[0][2]:.2f})")
