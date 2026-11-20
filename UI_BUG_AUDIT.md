# UI/UX Bug Hunt & Alignment Audit Report (Intelligent-AML v3.0)

**Date:** November 20, 2026  
**Auditor:** Staff Frontend Engineer & Enterprise UI/UX Systems Specialist  
**Target Viewports Audited:**
- `1920x1080` (Standard Compliance Monitor)
- `1440x900` (14"–15" Laptop)
- `1280x720` (Compact Enterprise Laptop)
- `390x844` (Mobile / Narrow Split-Screen)

---

## 1. Summary of Automated DOM & Alignment Findings

| ID | Category | Viewports Affected | File Path & Lines | Severity | Issue Description |
|:---|:---|:---|:---|:---|:---|
| **BUG-01** | Horizontal Page Overflow | `390x844` | `frontend/src/components/shell/CommandHeader.tsx:42-155` | **Critical** | Top command header contains unshrinkable flex row items (Fast-Path telemetry pill, stream status, banker profile, hotkey badges) forcing minimum width of 494px against a 390px viewport, causing horizontal scrollbars. |
| **BUG-02** | Sidebar Collision on Mobile | `390x844` | `frontend/src/components/shell/NavigationRail.tsx:42-51` | **Major** | Left navigation rail renders inline taking 64px width on narrow mobile viewports, constraining main viewport width to 326px and causing internal card overflow. |
| **BUG-03** | Console 404 Asset Failure | All Viewports | `frontend/public/favicon.ico` | **Minor** | Missing `favicon.ico` causing browser to throw `404 (Not Found)` on every page load. |
| **BUG-04** | CSP Dev-Mode Eval Warning | All Viewports | `frontend/src/middleware.ts:9-21` | **Medium** | Strict CSP lacks `'unsafe-eval'` in development mode, causing React/Next.js HMR and error overlay to throw console security exceptions. |
| **BUG-05** | Numeric Column Jitter | All Viewports | `frontend/src/app/page.tsx:145-233`, `frontend/src/app/triage/page.tsx:210-310` | **Medium** | Financial figures, latency timers, and risk probabilities lack `font-variant-numeric: tabular-nums` (`tabular-nums`), causing jitter during live stream updates. |
| **BUG-06** | Dual Y-Axis Recharts Tick Clipping | `1280x720`, `1440x900` | `frontend/src/app/governance/page.tsx:142-156` | **Major** | Recharts dual Y-axis chart right-margin (`right: 30`) is too narrow; percentage ticks (`0.980`, `0.990`, `1.000`) collide with right container boundary. |
| **BUG-07** | Uneven KPI Card Alignment | `1440x900`, `1920x1080` | `frontend/src/app/page.tsx:143-234` | **Medium** | KPI cards in the 4-card ribbon lack `h-full flex flex-col justify-between`, causing bottom metric rows to misalign when title text wraps. |
| **BUG-08** | Tier-2 Officer Review Queue Visibility | All Viewports | `frontend/src/app/page.tsx:188-210` | **Minor** | Tier-2 Review Queue card has passive styling without prominent left-border accent, blending in with informational metrics despite representing immediate human workload. |
| **BUG-09** | Forensic Network Graph Controls & Overlap | All Viewports | `frontend/src/app/graph/page.tsx:90-120` | **Major** | Graph canvas has fixed container height without fullscreen toggle, missing minimap, edge labels lack background pills causing text collision with overlapping edges, and neighborhood lacks 1/2/3-hop expansion limiters. |
| **BUG-10** | Alert Triage Row Density & Action Shift | All Viewports | `frontend/src/app/triage/page.tsx:95-108`, `200-280` | **Medium** | Alert triage table lacks density mode coupling (`py-1.5` compact vs `py-3` comfortable), action buttons cause column width shifts on hover, and bulk selection floating bar is missing. |
| **BUG-11** | Case Dossier Workspace Scalability | All Viewports | `frontend/src/app/cases/page.tsx:92-175` | **Medium** | Only displays 3-column card grid with no dense table view option for high-volume compliance dockets. |
| **BUG-12** | SAR Workbench Asymmetric Scrolling | All Viewports | `frontend/src/app/sar/page.tsx:75-285` | **Major** | SAR drafting interface lacks responsive two-column split with synchronized independent scroll panes, forcing long page scroll down to evidence and verification cards. |

---

## 2. Immediate Remediation Action Plan
1. **Shell & Navigation Hardening:**
   - Add responsive hiding (`hidden sm:flex`, `hidden md:flex`, `hidden lg:flex`) to header telemetry and controls.
   - On mobile (`< 768px`), hide the fixed left rail or make it an off-canvas drawer.
   - Add `favicon.ico` in `frontend/public/` to eliminate 404 asset failures.
   - Fix `frontend/src/middleware.ts` to allow `'unsafe-eval'` in development mode while enforcing strict air-gap nonces in production.
2. **Typography & Tabular Alignment:**
   - Add `tabular-nums` class to all currency displays, probabilities, latency badges, and table figures.
3. **KPI & Card Alignment:**
   - Refactor 4-card KPI ribbon to `h-full flex flex-col justify-between` with prominent amber/crimson left-border accent on Tier-2 card.
4. **Graph Studio Upgrades:**
   - Make canvas height viewport-aware (`min-h-[520px] h-[calc(100vh-240px)]`), add Fullscreen toggle, Zoom-to-fit button, Minimap, 1/2/3-hop perimeter controls, and edge label background pills.
5. **Alert Triage & Cases Docket:**
   - Link density mode to table padding, add hover action buttons without shift, add floating bulk action bar, and add Card/Table view switcher for cases.
6. **Charts & SAR Workbench:**
   - Fix dual Y-axis margins (`margin={{ top: 16, right: 56, left: 16, bottom: 16 }}`) and add `width={48}` to right `<YAxis>`.
   - Refactor SAR Workbench into a clean 2-column split-screen with independent scroll panes.


---

## 3. Post-Remediation Automated Verification Matrix

Automated headless Chrome diagnostic executed across all 32 viewport-route combinations (`py scripts/diagnose_ui_layout.py`):

| Viewport | Route | Document Width vs Viewport | Header Height | Console Errors | SVG / Label Clipping | Gate Result |
|:---|:---|:---|:---|:---|:---|:---|
| **1920x1080** | `/` (Overview) | 1898px &le; 1904px | 56px | 0 | 0 | **PASS** |
| **1920x1080** | `/triage` (Alert Triage) | 1904px &le; 1904px | 56px | 0 | 0 | **PASS** |
| **1920x1080** | `/cases` (Case Docket) | 1904px &le; 1904px | 56px | 0 | 0 | **PASS** |
| **1920x1080** | `/graph` (Topology Graph) | 1904px &le; 1904px | 56px | 0 | 0 | **PASS** |
| **1920x1080** | `/sar` (SAR Workbench) | 1904px &le; 1904px | 56px | 0 | 0 | **PASS** |
| **1920x1080** | `/rfi` (Compliance RFI) | 1904px &le; 1904px | 56px | 0 | 0 | **PASS** |
| **1920x1080** | `/recourse` (Recourse Sandbox) | 1904px &le; 1904px | 56px | 0 | 0 | **PASS** |
| **1920x1080** | `/governance` (Model WORM) | 1898px &le; 1904px | 56px | 0 | 0 | **PASS** |
| **1440x900** | `/` (Overview) | 1418px &le; 1424px | 56px | 0 | 0 | **PASS** |
| **1440x900** | `/triage` (Alert Triage) | 1424px &le; 1424px | 56px | 0 | 0 | **PASS** |
| **1440x900** | `/cases` (Case Docket) | 1424px &le; 1424px | 56px | 0 | 0 | **PASS** |
| **1440x900** | `/graph` (Topology Graph) | 1424px &le; 1424px | 56px | 0 | 0 | **PASS** |
| **1440x900** | `/sar` (SAR Workbench) | 1424px &le; 1424px | 56px | 0 | 0 | **PASS** |
| **1440x900** | `/rfi` (Compliance RFI) | 1418px &le; 1424px | 56px | 0 | 0 | **PASS** |
| **1440x900** | `/recourse` (Recourse Sandbox) | 1424px &le; 1424px | 56px | 0 | 0 | **PASS** |
| **1440x900** | `/governance` (Model WORM) | 1418px &le; 1424px | 56px | 0 | 0 | **PASS** |
| **1280x720** | `/` (Overview) | 1258px &le; 1264px | 56px | 0 | 0 | **PASS** |
| **1280x720** | `/triage` (Alert Triage) | 1264px &le; 1264px | 56px | 0 | 0 | **PASS** |
| **1280x720** | `/cases` (Case Docket) | 1264px &le; 1264px | 56px | 0 | 0 | **PASS** |
| **1280x720** | `/graph` (Topology Graph) | 1258px &le; 1264px | 56px | 0 | 0 | **PASS** |
| **1280x720** | `/sar` (SAR Workbench) | 1258px &le; 1264px | 56px | 0 | 0 | **PASS** |
| **1280x720** | `/rfi` (Compliance RFI) | 1258px &le; 1264px | 56px | 0 | 0 | **PASS** |
| **1280x720** | `/recourse` (Recourse Sandbox) | 1258px &le; 1264px | 56px | 0 | 0 | **PASS** |
| **1280x720** | `/governance` (Model WORM) | 1258px &le; 1264px | 56px | 0 | 0 | **PASS** |
| **390x844** | `/` (Overview) | 390px = 390px | 56px | 0 | 0 | **PASS** |
| **390x844** | `/triage` (Alert Triage) | 390px = 390px | 56px | 0 | 0 | **PASS** |
| **390x844** | `/cases` (Case Docket) | 390px = 390px | 56px | 0 | 0 | **PASS** |
| **390x844** | `/graph` (Topology Graph) | 390px = 390px | 56px | 0 | 0 | **PASS** |
| **390x844** | `/sar` (SAR Workbench) | 390px = 390px | 56px | 0 | 0 | **PASS** |
| **390x844** | `/rfi` (Compliance RFI) | 390px = 390px | 56px | 0 | 0 | **PASS** |
| **390x844** | `/recourse` (Recourse Sandbox) | 390px = 390px | 56px | 0 | 0 | **PASS** |
| **390x844** | `/governance` (Model WORM) | 390px = 390px | 56px | 0 | 0 | **PASS** |

**Summary Result:** **32 / 32 Passed** (100% compliance with zero horizontal overflows, zero console exceptions, and zero label clipping).
