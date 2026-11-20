"""
scripts/diagnose_ui_layout.py
Automated headless DOM, layout, overflow, and console error auditor for Intelligent-AML.
Audits 4 viewports across all 8 institutional routes:
- 1920x1080 (Standard Compliance Monitor)
- 1440x900 (14"–15" Laptop)
- 1280x720 (Compact Enterprise Laptop)
- 390x844 (Mobile / Narrow Split-Screen)
"""
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

VIEWPORTS = [
    ("1920x1080", 1920, 1080, False),
    ("1440x900", 1440, 900, False),
    ("1280x720", 1280, 720, False),
    ("390x844", 390, 844, True)
]

ROUTES = [
    "/",
    "/triage",
    "/cases",
    "/graph",
    "/sar",
    "/rfi",
    "/recourse",
    "/governance"
]

def create_driver(is_mobile=False, width=1920, height=1080):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.set_capability("goog:loggingPrefs", {"browser": "ALL"})

    if is_mobile:
        chrome_options.add_experimental_option("mobileEmulation", {
            "deviceMetrics": {"width": width, "height": height, "pixelRatio": 3.0}
        })
    else:
        chrome_options.add_argument(f"--window-size={width},{height}")

    driver = webdriver.Chrome(options=chrome_options)
    if not is_mobile:
        driver.set_window_size(width, height)
    return driver

def run_audit():
    audit_results = []
    total_checks = len(VIEWPORTS) * len(ROUTES)
    passed_checks = 0

    for vp_name, width, height, is_mobile in VIEWPORTS:
        print(f"\n=======================================================")
        print(f"Auditing Viewport: {vp_name} ({width}x{height}, mobile={is_mobile})")
        print(f"=======================================================")

        driver = create_driver(is_mobile=is_mobile, width=width, height=height)

        try:
            for route in ROUTES:
                url = f"http://localhost:3000{route}"
                driver.get(url)
                time.sleep(1.8) # Allow hydration and client effects

                # 1. Console Logs
                logs = driver.get_log("browser")
                severe_logs = [l for l in logs if l.get("level") in ("SEVERE", "WARNING")]

                # 2. Check Document Horizontal Overflow
                overflow_info = driver.execute_script("""
                    const docEl = document.documentElement;
                    const body = document.body;
                    const winWidth = window.innerWidth;
                    const docScrollWidth = docEl.scrollWidth;
                    const bodyScrollWidth = body.scrollWidth;

                    const maxScrollWidth = Math.max(docScrollWidth, bodyScrollWidth);
                    const hasDocOverflow = maxScrollWidth > winWidth + 1;

                    // Find any overflowing elements
                    const overflowingElements = [];
                    const allEls = document.querySelectorAll('*');
                    for (const el of allEls) {
                        const style = window.getComputedStyle(el);
                        if (style.overflowX === 'hidden' || style.overflowX === 'scroll' || style.overflowX === 'auto') {
                            continue;
                        }
                        const rect = el.getBoundingClientRect();
                        if (rect.right > winWidth + 2 && rect.width > 0) {
                            overflowingElements.push({
                                tag: el.tagName.toLowerCase(),
                                id: el.id,
                                className: (el.className || '').toString().slice(0, 60),
                                right: Math.round(rect.right),
                                winWidth: winWidth
                            });
                        }
                    }

                    return {
                        hasDocOverflow,
                        docScrollWidth: maxScrollWidth,
                        winWidth,
                        overflowingElements: overflowingElements.slice(0, 5)
                    };
                """)

                # 3. Check Header Height and Alignment
                header_info = driver.execute_script("""
                    const header = document.querySelector('header');
                    if (!header) return null;
                    const rect = header.getBoundingClientRect();
                    return {
                        height: Math.round(rect.height),
                        width: Math.round(rect.width)
                    };
                """)

                # 4. Check for clipped text or clipped SVG chart elements
                svg_issues = driver.execute_script("""
                    const issues = [];
                    const svgs = document.querySelectorAll('svg');
                    for (const svg of svgs) {
                        const texts = svg.querySelectorAll('text');
                        const svgRect = svg.getBoundingClientRect();
                        for (const t of texts) {
                            const tRect = t.getBoundingClientRect();
                            if (tRect.width > 0 && tRect.height > 0) {
                                if (tRect.left < svgRect.left - 5 || tRect.right > svgRect.right + 5) {
                                    issues.push({
                                        text: t.textContent.trim().slice(0, 40),
                                        tLeft: Math.round(tRect.left),
                                        svgLeft: Math.round(svgRect.left),
                                        tRight: Math.round(tRect.right),
                                        svgRight: Math.round(svgRect.right)
                                    });
                                }
                            }
                        }
                    }
                    return issues.slice(0, 5);
                """)

                result = {
                    "viewport": vp_name,
                    "route": route,
                    "overflow": overflow_info,
                    "header": header_info,
                    "svg_issues": svg_issues,
                    "console_errors": [l["message"] for l in severe_logs if l.get("level") == "SEVERE"],
                    "console_warnings": [l["message"] for l in severe_logs if l.get("level") == "WARNING"]
                }
                audit_results.append(result)

                is_pass = not overflow_info["hasDocOverflow"] and len(result["console_errors"]) == 0
                if is_pass:
                    passed_checks += 1
                status_str = "PASS" if is_pass else "FAIL"

                print(f"[{status_str}] {route}: docW={overflow_info['docScrollWidth']} vs win={overflow_info['winWidth']} | "
                      f"HeaderH={header_info['height'] if header_info else 'N/A'} | "
                      f"Err={len(result['console_errors'])}, Warn={len(result['console_warnings'])} | "
                      f"SVGIssues={len(svg_issues)}")
                if overflow_info["hasDocOverflow"]:
                    print(f"   -> Overflow: {overflow_info['overflowingElements']}")
                if result["console_errors"]:
                    print(f"   -> Errors: {result['console_errors']}")

        finally:
            driver.quit()

    print(f"\n=======================================================")
    print(f"FINAL AUDIT RESULT: {passed_checks} / {total_checks} PASSED")
    print(f"=======================================================")

    with open("UI_AUDIT_FINAL.json", "w", encoding="utf-8") as f:
        json.dump(audit_results, f, indent=2)

if __name__ == "__main__":
    run_audit()
