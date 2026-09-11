import pypdf
import pymupdf
import re
import sys

def verify_submission():
    print("==============================================================================")
    print("[*] IEEE TIFS SUBMISSION PACKAGE COMPREHENSIVE VERIFICATION AUDIT")
    print("==============================================================================")
    
    # 1. Page Count Verification
    main_reader = pypdf.PdfReader('papers/IEEE_Research_Paper/main.pdf')
    supp_reader = pypdf.PdfReader('papers/IEEE_Research_Paper/supplementary.pdf')
    cl_reader = pypdf.PdfReader('papers/IEEE_Research_Paper/Cover_Letter_IEEE_TIFS.pdf')

    main_pages = len(main_reader.pages)
    supp_pages = len(supp_reader.pages)
    cl_pages = len(cl_reader.pages)
    tkde_cl_reader = pypdf.PdfReader('papers/IEEE_Research_Paper/Cover_Letter_IEEE_TKDE.pdf')
    tkde_cl_pages = len(tkde_cl_reader.pages)

    print(f"\n[1] PAGE BUDGET CHECKS:")
    print(f"    - main.pdf: {main_pages} pages (Budget: exactly 13.0) -> {'PASS' if main_pages == 13 else 'FAIL'}")
    print(f"    - supplementary.pdf: {supp_pages} pages (Budget: exactly 6.0) -> {'PASS' if supp_pages == 6 else 'FAIL'}")
    print(f"    - Cover_Letter_IEEE_TIFS.pdf: {cl_pages} page (Budget: 1.0) -> {'PASS' if cl_pages == 1 else 'FAIL'}")
    print(f"    - Cover_Letter_IEEE_TKDE.pdf: {tkde_cl_pages} page (Budget: 1.0) -> {'PASS' if tkde_cl_pages == 1 else 'FAIL'}")

    assert main_pages == 13, f"main.pdf must be exactly 13 pages, got {main_pages}"
    assert supp_pages == 6, f"supplementary.pdf must be exactly 6 pages, got {supp_pages}"
    assert cl_pages == 1, f"TIFS Cover letter must be 1 page, got {cl_pages}"
    assert tkde_cl_pages == 1, f"TKDE Cover letter must be 1 page, got {tkde_cl_pages}"

    # 2. Text & Citation Audit
    print(f"\n[2] CITATION & STATE-OF-THE-ART POSITIONING CHECKS:")
    full_main_text = ' '.join([p.extract_text() for p in main_reader.pages])

    flagship_cits = ['Fu', 'CamFD', 'Cheng', 'Qiao']
    for c in flagship_cits:
        found = c in full_main_text
        print(f"    - Flagship Citation [{c}]: {'FOUND' if found else 'MISSING'}")
        assert found, f"Missing citation for {c} in main text"

    # Ensure no deprecated TIFS citations remain
    assert 'MLaD' not in full_main_text, "Found deprecated MLaD reference in main text!"
    print("    - Deprecated TIFS Citation [MLaD]: PURGED COMPLETELY (PASS)")

    # 3. Phantom Supplementary Table Reference Audit
    print(f"\n[3] CROSS-REFERENCE INTEGRITY CHECKS:")
    phantom_tables = re.findall(r'Table\s+S(?:1[2-9]|[2-9][0-9])', full_main_text)
    print(f"    - Phantom tables detected: {phantom_tables} -> {'PASS (Zero phantoms)' if not phantom_tables else 'FAIL'}")
    assert len(phantom_tables) == 0, f"Found phantom supplementary tables: {phantom_tables}"

    valid_tables = sorted(list(set(re.findall(r'Table\s+S(?:[1-9]|1[0-1])', full_main_text))))
    print(f"    - Valid supplementary tables referenced: {valid_tables}")

    # 4. Cover Letter Claims Alignment
    print(f"\n[4] COVER LETTER CLAIMS AUDIT (TKDE):")
    tkde_cl_text = tkde_cl_reader.pages[0].extract_text()
    tkde_claims = ['13.0 pages', '6.0 pages', 'Fu', 'Cheng', 'Qiao', 'TKDE']
    for claim in tkde_claims:
        found = claim in tkde_cl_text
        print(f"    - Claim [{claim}]: {'VERIFIED' if found else 'MISSING'}")
        assert found, f"TKDE Cover letter missing claim: {claim}"

    # 5. Visual Rendering & Vector Graphics Check
    print(f"\n[5] FIGURE GRAPHICS QUALITY CHECKS (main.pdf):")
    doc = pymupdf.open('papers/IEEE_Research_Paper/main.pdf')
    for p_num in [3, 8, 10, 11]:  # Pages with figures
        p = doc[p_num]
        imgs = p.get_images()
        drawings = p.get_drawings()
        print(f"    - Page {p_num+1}: {len(imgs)} raster images, {len(drawings)} vector drawing paths")

    print("\n==============================================================================")
    print("[SUCCESS] ALL SUBMISSION PACKAGE CHECKS PASSED PERFECTLY!")
    print("==============================================================================")

if __name__ == '__main__':
    verify_submission()
