import fitz

doc = fitz.open('papers/University_CSE_Thesis/figures/fig_streaming_latency_waterfall.pdf')
page = doc[0]
rect = page.rect
print(f"Auditing fig_streaming_latency_waterfall.pdf ({rect.width:.2f} x {rect.height:.2f} pt)...")
print(f"Aspect ratio: {rect.width / rect.height:.3f}")
scale_to_355 = 355.0 / rect.width
print(f"Rendered height at 0.85textwidth: {rect.height * scale_to_355:.1f} pt")

words = page.get_text('words')
print(f"Total words: {len(words)}")

# Check margins
clipped = [w for w in words if w[0] < 3.0 or w[1] < 3.0 or w[2] > rect.width - 3.0 or w[3] > rect.height - 3.0]
print(f"Border clipped words (<3pt margin): {len(clipped)}")
for cw in clipped:
    print("  Clipped:", cw[:5])

# Check overlaps
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

print(f"Total collisions: {len(overlaps)}")
for ov in overlaps[:10]:
    clean_0 = ''.join(c if ord(c) < 128 else '?' for c in ov[0])
    clean_1 = ''.join(c if ord(c) < 128 else '?' for c in ov[1])
    print(f"  Collision: '{clean_0}' overlaps '{clean_1}' (area {ov[2]:.2f})")

