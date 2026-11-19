"""
Builds the official 20-Slide B.Sc. Thesis Defense & FinTech Venture Pitch Presentation:
C-STGB: Conformal Spatio-Temporal GraphBoost for High-Velocity Financial Forensics and Compliance Automation
Follows the strict Two-Zone Design Pattern:
  - Zone 1 (Top 80%): Plain-English Visuals, KPI Cards, Process Chevrons, Architecture Flowcharts, Benchmark Tables
  - Zone 2 (Bottom 20%): Dedicated Mathematical & Engineering Reference Strip for CSE Examiners
  - Speaker Pitch Scripts embedded directly into PPTX Speaker Notes on every slide.
"""
import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# Color Palette Constants
BG_LIGHT    = RGBColor(255, 255, 255)
BG_CARD     = RGBColor(248, 250, 252)  # #f8fafc
BORDER_CARD = RGBColor(226, 232, 240)  # #e2e8f0
DARK_NAVY   = RGBColor(15, 23, 42)     # #0f172a
SLATE_MUTED = RGBColor(100, 116, 139)  # #64748b
COLOR_MUTED = SLATE_MUTED
TEXT_DARK   = RGBColor(15, 23, 42)     # #0f172a
WHITE       = RGBColor(255, 255, 255)

COLOR_BLUE     = RGBColor(37, 99, 235)   # #2563eb
COLOR_BLUE_BG  = RGBColor(239, 246, 255) # #eff6ff
COLOR_GREEN    = RGBColor(16, 185, 129)  # #10b981
COLOR_GREEN_BG = RGBColor(236, 253, 245) # #ecfdf5
COLOR_AMBER    = RGBColor(245, 158, 11)  # #f59e0b
COLOR_AMBER_BG = RGBColor(254, 243, 199) # #fef3c7
COLOR_RED      = RGBColor(239, 68, 68)   # #ef4444
COLOR_RED_BG   = RGBColor(254, 226, 226) # #fee2e2
COLOR_PURPLE   = RGBColor(124, 58, 237)  # #7c3aed
COLOR_PURPLE_BG= RGBColor(250, 245, 255) # #faf5ff

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Helper functions
    def add_header(slide, phase_badge, title_text, subtitle_text=""):
        # Header Box
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.733), Inches(0.85))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        # Phase badge
        p0 = tf.paragraphs[0]
        p0.text = phase_badge.upper()
        p0.font.size = Pt(8.5)
        p0.font.bold = True
        p0.font.color.rgb = COLOR_BLUE
        p0.font.name = "Arial"
        
        # Title
        p1 = tf.add_paragraph()
        p1.text = title_text
        p1.font.size = Pt(18)
        p1.font.bold = True
        p1.font.color.rgb = DARK_NAVY
        p1.font.name = "Arial"
        
        if subtitle_text:
            p2 = tf.add_paragraph()
            p2.text = subtitle_text
            p2.font.size = Pt(9.5)
            p2.font.color.rgb = SLATE_MUTED
            p2.font.name = "Arial"

    def add_examiner_strip(slide, math_bullets):
        """Adds Zone 2: Dedicated Mathematical & Engineering Reference Strip for CSE examiners."""
        x = Inches(0.8)
        y = Inches(5.95)
        w = Inches(11.733)
        h = Inches(1.18)

        # Background card
        rect = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
        rect.fill.solid()
        rect.fill.fore_color.rgb = RGBColor(241, 245, 249) # #f1f5f9
        rect.line.color.rgb = COLOR_BLUE
        rect.line.width = Pt(1.2)

        # Header Pill
        pill = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, Inches(4.2), Inches(0.24))
        pill.fill.solid()
        pill.fill.fore_color.rgb = DARK_NAVY
        pill.line.fill.background()
        tf_pill = pill.text_frame
        tf_pill.margin_left = Inches(0.1)
        tf_pill.margin_top = Inches(0.02)
        p = tf_pill.paragraphs[0]
        p.text = "ZONE 2: CSE EXAMINER MATHEMATICAL & ENGINEERING SPECIFICATION"
        p.font.size = Pt(7.0)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.font.name = "Arial"

        # Math / Engineering text
        tb = slide.shapes.add_textbox(x + Inches(0.15), y + Inches(0.28), w - Inches(0.3), h - Inches(0.32))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        for idx, bullet in enumerate(math_bullets):
            p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
            p.text = f"• {bullet}"
            p.font.size = Pt(7.8)
            p.font.color.rgb = DARK_NAVY
            p.font.name = "Arial"
            p.space_after = Pt(2)

    def set_speaker_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    # =========================================================================
    # SLIDE 1: Title & Executive Positioning
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    
    # Hero Card
    hero = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.6), Inches(11.733), Inches(4.2))
    hero.fill.solid()
    hero.fill.fore_color.rgb = DARK_NAVY
    hero.line.color.rgb = COLOR_BLUE
    hero.line.width = Pt(1.5)

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(0.8), Inches(10.933), Inches(3.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "NATIONAL UNIVERSITY & COLLEGE OF TECHNOLOGY"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE
    p.alignment = PP_ALIGN.CENTER

    p = tf1.add_paragraph()
    p.text = "Department of Computer Science and Engineering | B.Sc. (Honours) Thesis Defense & FinTech Venture Pitch"
    p.font.size = Pt(9.5)
    p.font.color.rgb = RGBColor(148, 163, 184)
    p.alignment = PP_ALIGN.CENTER
    p.space_after = Pt(14)

    p = tf1.add_paragraph()
    p.text = "C-STGB: Conformal Spatio-Temporal GraphBoost for High-Velocity Financial Forensics and Compliance Automation"
    p.font.size = Pt(22)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER
    p.space_after = Pt(12)

    p = tf1.add_paragraph()
    p.text = "A Physics-Guided, Non-Stationary Relational Deep Learning Architecture with Sub-Millisecond Conformal Triage and Zero-Hallucination Agentic Regulatory SAR Compilation"
    p.font.size = Pt(10.5)
    p.font.color.rgb = RGBColor(226, 232, 240)
    p.alignment = PP_ALIGN.CENTER

    # Presenters & Supervisor Cards Below Hero
    pres_card = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(5.0), Inches(6.8), Inches(1.9))
    pres_card.fill.solid()
    pres_card.fill.fore_color.rgb = BG_CARD
    pres_card.line.color.rgb = BORDER_CARD
    pres_tf = pres_card.text_frame
    pres_tf.word_wrap = True
    pres_tf.margin_left = Inches(0.2)
    pres_tf.margin_top = Inches(0.12)
    p = pres_tf.paragraphs[0]
    p.text = "PRESENTED BY (DEFENSE CANDIDATES):"
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE
    
    candidates = [
        "1. Md. Nazmul Hasan Nihal — Roll: 20502002281 | Reg: 20502002281",
        "2. Musrat Jahan Gungun — Roll: 20502002262 | Reg: 20502002262",
        "3. Sagor Chandra — Roll: 20502002264 | Reg: 20502002264"
    ]
    for c in candidates:
        p = pres_tf.add_paragraph()
        p.text = c
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = DARK_NAVY

    sup_card = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.8), Inches(5.0), Inches(4.733), Inches(1.9))
    sup_card.fill.solid()
    sup_card.fill.fore_color.rgb = BG_CARD
    sup_card.line.color.rgb = BORDER_CARD
    sup_tf = sup_card.text_frame
    sup_tf.word_wrap = True
    sup_tf.margin_left = Inches(0.2)
    sup_tf.margin_top = Inches(0.12)
    p = sup_tf.paragraphs[0]
    p.text = "UNDER THE SUPERVISION OF:"
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE
    
    p = sup_tf.add_paragraph()
    p.text = "Maheli Ahmed"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY
    p = sup_tf.add_paragraph()
    p.text = "Lecturer, Department of Computer Science & Engineering\nCollege of Technology, National University of Bangladesh"
    p.font.size = Pt(8.5)
    p.font.color.rgb = SLATE_MUTED

    set_speaker_notes(s1, "Introduce C-STGB not merely as an academic algorithm, but as a production-ready financial surveillance engine built to detect high-velocity money laundering in under half a millisecond while automating regulatory reporting.")

    # =========================================================================
    # SLIDE 2: Presentation Roadmap & Structural Flow
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "Executive Agenda & Roadmap", "Presentation Roadmap & Structural Flow",
               "Five Sequential Phases Mapping Departmental CSE Requirements to High-Impact Enterprise FinTech Architecture")

    phases = [
        ("PHASE 1", "Crisis & Objectives", "Slides 3–6", "The $2T AML Crisis, Problem Statement, 3 Falsifiable Hypotheses & Core Contributions.", COLOR_BLUE, COLOR_BLUE_BG),
        ("PHASE 2", "Literature & SOTA Gap", "Slides 7–9", "Laundering Typologies, Forensic Evolution & 25-Paper State-of-the-Art Gap Matrix.", COLOR_AMBER, COLOR_AMBER_BG),
        ("PHASE 3", "Proposed C-STGB Core", "Slides 10–16", "6-Layer Pipeline, 12-D Flow Invariants, Tri-Band GNN, Latent SMOTE, CRC & Agentic SAR.", COLOR_PURPLE, COLOR_PURPLE_BG),
        ("PHASE 4", "Empirical Proof", "Slides 17–18", "14-Dataset Benchmark, Calibration Reliability & Stepwise Ablation Waterfall Proof.", COLOR_GREEN, COLOR_GREEN_BG),
        ("PHASE 5", "Venture Pitch & Impact", "Slides 19–20", "Live ACC_9941 Case Study, B2B SaaS Commercial Economics & 3-Horizon Financial Roadmap.", DARK_NAVY, BG_CARD),
    ]

    card_w = Inches(2.22)
    card_gap = Inches(0.15)
    start_x = Inches(0.8)

    for i, (p_num, p_title, p_slides, p_desc, col, bg_col) in enumerate(phases):
        cx = start_x + i * (card_w + card_gap)
        c_shape = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, cx, Inches(1.4), card_w, Inches(4.3))
        c_shape.fill.solid()
        c_shape.fill.fore_color.rgb = bg_col
        c_shape.line.color.rgb = col
        c_shape.line.width = Pt(1.4)
        
        tf = c_shape.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.15)
        tf.margin_top = Inches(0.2)
        
        p = tf.paragraphs[0]
        p.text = p_num
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = col
        
        p = tf.add_paragraph()
        p.text = p_title
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = DARK_NAVY
        p.space_after = Pt(4)

        p = tf.add_paragraph()
        p.text = p_slides
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(12)

        p = tf.add_paragraph()
        p.text = p_desc
        p.font.size = Pt(8.5)
        p.font.color.rgb = SLATE_MUTED

    add_examiner_strip(s2, [
        "Curriculum Mapping: Fully satisfies National University B.Sc. in CSE graduation criteria (Problem Formulation, SOTA Literature Gap, Mathematical Novelty, Experimental Proof, Practical Deployment).",
        "Verification Rigor: Evaluated across 14 financial transaction networks totaling 125GB+ data with zero temporal lookahead leakage (Lemma S1)."
    ])
    set_speaker_notes(s2, "Walk the committee through the five-stage narrative, noting that every academic requirement from the departmental template is preserved and paired with real-world banking economics.")

    # =========================================================================
    # SLIDE 3: Executive Abstract & The $2 Trillion Crisis
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "Phase 1: Executive Hook", "Executive Abstract & The $2 Trillion Global AML Crisis",
               "Traditional Anti-Money Laundering Architecture is Structurally Broken — C-STGB Delivers a Mathematically Bounded Solution")

    # 3 Large Metric Cards
    kpis = [
        ("$2.0T+ Annually", "The Global Crime Scale", "2% to 5% of global GDP laundered each year; less than 1.0% is ever intercepted by existing banking systems.", COLOR_RED, COLOR_RED_BG),
        ("> 95.0% False Alarms", "The Operational Bottleneck", "Legacy rule engines generate massive alert fatigue, costing Tier-1 banks $3.2B+ annually in wasted manual analyst reviews.", COLOR_AMBER, COLOR_AMBER_BG),
        ("0.45 ms & 99.5% Cut", "The C-STGB Solution", "Delivers rank #1 F1 across 14 benchmarks, guarantees 99.12% illicit coverage, and slashes manual triage volume by 99.50%+.", COLOR_GREEN, COLOR_GREEN_BG)
    ]
    kw = Inches(3.77)
    kgap = Inches(0.2)
    for i, (val, title, desc, col, bg) in enumerate(kpis):
        kx = Inches(0.8) + i * (kw + kgap)
        card = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, kx, Inches(1.35), kw, Inches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = bg
        card.line.color.rgb = col
        card.line.width = Pt(1.5)
        
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.18)
        
        p = tf.paragraphs[0]
        p.text = val
        p.font.size = Pt(20)
        p.font.bold = True
        p.font.color.rgb = col
        
        p = tf.add_paragraph()
        p.text = title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = DARK_NAVY
        p.space_after = Pt(4)

        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(8.5)
        p.font.color.rgb = DARK_NAVY

    # 3-Stage Process Strip: Problem -> Innovation -> Verified Impact
    p_card = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.75), Inches(11.733), Inches(2.0))
    p_card.fill.solid()
    p_card.fill.fore_color.rgb = BG_CARD
    p_card.line.color.rgb = BORDER_CARD
    p_card.line.width = Pt(1.2)
    
    tf = p_card.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.15)
    
    p = tf.paragraphs[0]
    p.text = "THE C-STGB UNIFIED ENTERPRISE VALUE CHAIN: PROBLEM -> INNOVATION -> IMPACT"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE
    p.space_after = Pt(6)

    chain_text = [
        "1. Problem: Syndicates evade tabular SQL filters via multi-hop peel chains, millisecond MFS bursts, and 90-day dormant sleeper accounts.",
        "2. Innovation: C-STGB unifies 12-D physics flow invariants, Tri-Band continuous harmonic attention, Latent GraphSMOTE, and Conformal Risk Control.",
        "3. Verified Impact: Rank #1 on 14 production networks (+24.6 pp F1 lead over SOTA), 0.45 ms fast-path SLA, and zero-hallucination agentic SAR generation."
    ]
    for ct in chain_text:
        p = tf.add_paragraph()
        p.text = ct
        p.font.size = Pt(8.5)
        p.font.color.rgb = DARK_NAVY
        p.space_after = Pt(2)

    add_examiner_strip(s3, [
        "Mathematical Guarantees: Class-conditional dual quantiles enforce P(Y ∈ Γ(X) | Y=1) ≥ 1 - α (finite-sample coverage under non-exchangeable drift).",
        "Algorithmic Core: Zero-copy Apache Arrow ingestion + TorchScript GNN forward pass meets sub-millisecond banking core SLAs (<0.45 ms)."
    ])
    set_speaker_notes(s3, "Contrast the massive global scale of financial crime with the failure of current compliance tools, positioning C-STGB as an end-to-end mathematical and operational fix.")

    # =========================================================================
    # SLIDE 4: Problem Statement — Three Structural Failure Modes
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "Phase 1: Problem Statement", "Problem Statement — Three Structural Failure Modes",
               "Why Conventional SQL Rules, Tabular Ensembles, and Standard Graph Neural Networks Collapse in High-Velocity Banking")

    # Embed Figure 1.3 (5 Failure Modes) at top of Slide 4
    fig_path = "papers/University_CSE_Thesis/figures/fig_1_3_failure_modes.png"
    if os.path.exists(fig_path):
        s4.shapes.add_picture(fig_path, Inches(0.8), Inches(1.35), Inches(11.733), Inches(2.1))

    failures = [
        ("Failure 1: Relational Blindness", "Legacy SQL Rules & Tabular ML (XGBoost)",
         "SQL thresholds evaluate transactions as isolated rows (i.i.d. assumption). They are structurally blind to multi-hop topology, missing smurfing fan-ins, wash rings, and peel chains.",
         "Banking Penalty: $35M+ annual fines.", COLOR_RED),
        ("Failure 2: Velocity & Camouflage", "Standard GNNs (GCN / GAT / EvolveGCN)",
         "Laundering rings exploit millisecond bursts or 90-day dormant delays while hiding behind merchant hubs. Exponential temporal kernels vanish, and message-passing over-smooths.",
         "Banking Penalty: Blind to sleeper accounts.", COLOR_AMBER),
        ("Failure 3: Extreme Class Skew", "Bayes Risk Collapse (π < 0.05%)",
         "Illicit transactions represent <1 in 2,000 events. Standard cross-entropy loss outputs conservative risk scores, causing an 88% recall collapse under default τ = 0.50.",
         "Banking Penalty: Over 90% false negatives.", COLOR_PURPLE)
    ]
    col_w = Inches(3.77)
    for i, (ftitle, fsub, fdesc, fpen, col) in enumerate(failures):
        fx = Inches(0.8) + i * (col_w + Inches(0.2))
        card = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, fx, Inches(3.55), col_w, Inches(2.25))
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = col
        card.line.width = Pt(1.3)
        
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.15)
        tf.margin_top = Inches(0.1)
        
        p = tf.paragraphs[0]
        p.text = ftitle
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = col
        
        p = tf.add_paragraph()
        p.text = fsub
        p.font.size = Pt(7.8)
        p.font.bold = True
        p.font.color.rgb = DARK_NAVY
        p.space_after = Pt(2)

        p = tf.add_paragraph()
        p.text = fdesc
        p.font.size = Pt(7.4)
        p.font.color.rgb = SLATE_MUTED
        p.space_after = Pt(3)

        p = tf.add_paragraph()
        p.text = fpen
        p.font.size = Pt(7.6)
        p.font.bold = True
        p.font.color.rgb = col

    add_examiner_strip(s4, [
        "Temporal Decay Vanishing: Conventional single-rate decay w(Δt) = exp(-λ Δt) vanishes for Δt > 20 days; gradients ∂L/∂w → 0, erasing 90-day dormant chains.",
        "Over-Smoothing & 1-WL Limit: High-degree merchant hubs cause Dirichlet energy collapse E(H) → 0; standard 1-WL GNNs treat degree-4 merchants and degree-4 mules as isomorphic."
    ])
    set_speaker_notes(s4, "Emphasize that banks face a dual crisis: tabular models cannot see network shapes, while standard graph neural networks get blinded by legitimate commercial hubs and extreme data imbalance.")

    # =========================================================================
    # SLIDE 5: Research Objectives & Falsifiable Hypotheses
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "Phase 1: Research Objectives", "Research Objectives & Falsifiable Hypotheses",
               "Framing Scientific Inquiry as Measurable, Falsifiable Computer Science Hypotheses Evaluated with Rigorous Statistical Testing")

    objectives = [
        ("Hypothesis H1 (Velocity & Camouflage Robustness)",
         "Formulate Continuous Tri-Band Harmonic Temporal Attention combined with localized Hawkes point processes and a learnable Edge-Trust Gating mechanism.",
         "Falsifiable Target: Capture both <1-minute bursts and 90-day dormant hops; prune ≥ 60.0% of adversarial camouflage chaff while outperforming static GNNs by ≥ +35.0 pp F1.",
         COLOR_BLUE),
        ("Hypothesis H2 (Extreme Skew & Minority Recall Recovery)",
         "Formulate Typology-Clustered Latent GraphSMOTE and Asymmetric Cost-Sensitive Focal Tversky Loss to synthesize minority laundering nodes within latent manifolds.",
         "Falsifiable Target: Recover minority recall from 10.33% to ≥ 85.00% under extreme <0.05% skew without temporal lookahead leakage or Kirchhoff flow violations.",
         COLOR_PURPLE),
        ("Hypothesis H3 (Bounded Conformal Triage & Regulatory Audit)",
         "Establish Class-Conditional Conformal Risk Control (CRC) with dual calibration quantiles and integrate an Assisted 4-Agent AST-validated SAR compiler.",
         "Falsifiable Target: Prove finite-sample recall coverage ≥ 99.0%, reduce human compliance review volume by ≥ 99.0%, and generate factual SAR dossiers in <60 seconds.",
         COLOR_GREEN)
    ]
    row_h = Inches(1.35)
    row_gap = Inches(0.12)
    for i, (htitle, hmech, htarget, col) in enumerate(objectives):
        ry = Inches(1.35) + i * (row_h + row_gap)
        card = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), ry, Inches(11.733), row_h)
        card.fill.solid()
        card.fill.fore_color.rgb = BG_CARD
        card.line.color.rgb = col
        card.line.width = Pt(1.3)
        
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.12)
        
        p = tf.paragraphs[0]
        p.text = htitle
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col
        
        p = tf.add_paragraph()
        p.text = f"Engineering Formulation: {hmech}"
        p.font.size = Pt(8.5)
        p.font.color.rgb = DARK_NAVY
        p.space_after = Pt(2)

        p = tf.add_paragraph()
        p.text = htarget
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = DARK_NAVY

    add_examiner_strip(s5, [
        "Statistical Validation Framework: Non-parametric paired Wilcoxon signed-rank tests (α = 0.001) across 14 networks assert stochastic dominance over all baselines.",
        "Non-Stationary Safety: Dvoretzky-Kiefer-Wolfowitz (DKW) inequality provides uniform empirical CDF confidence bands, bounding non-stationary distribution drift."
    ])
    set_speaker_notes(s5, "Explain to the CSE head that framing objectives as falsifiable mathematical hypotheses transforms the project from software development into verifiable computer science research.")

    # =========================================================================
    # SLIDE 6: Core Contributions — The Main Power of C-STGB
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "Phase 1: Core Contributions", "Core Contributions — The Four Pillars of C-STGB",
               "Four Standalone Scientific and Architectural Innovations Unifying Geometric Deep Learning, Conformal Prediction, and Agentic Law")

    pillars = [
        ("Pillar 1: 12-D Flow Invariants & Cold-Start Gate",
         "Kirchhoff conservation and Hawkes point process arrival kinetics capture physical mass balances. Evidence-adaptive gate balances tabular vs graph embeddings, achieving 89.60% F1 on zero-history accounts (+71.20 pp lead).",
         "Enterprise Value: Closes the zero-day account evasion loophole.", COLOR_BLUE, COLOR_BLUE_BG),
        ("Pillar 2: Tri-Band Attention & Anti-Camouflage Gate",
         "Multi-scale continuous-time harmonic attention bridges sub-minute bursts and 90-day hibernation. Learnable edge-trust gating filters 65.9% of noisy commercial chaff, preserving Dirichlet energy.",
         "Enterprise Value: Prevents criminals from hiding behind legitimate merchant hubs.", COLOR_PURPLE, COLOR_PURPLE_BG),
        ("Pillar 3: Class-Conditional Conformal Triage",
         "Solves marginal conformal coverage collapse under extreme skew via class-split non-conformity quantiles. Guarantees 99.12% illicit recall while auto-clearing 99.32% of benign flow without human intervention.",
         "Enterprise Value: 99.50%+ reduction in analyst investigation queues.", COLOR_GREEN, COLOR_GREEN_BG),
        ("Pillar 4: Zero-Hallucination 4-Agent SAR Compiler",
         "Multi-agent forensic swarm coupled with an Abstract Syntax Tree (AST) grammar verifier. Synthesizes court-admissible FinCEN Form 111 / BFIU dossiers with 0.00% factual error in under 60 seconds.",
         "Enterprise Value: Cuts SAR preparation time from 4 hours to <60 seconds.", COLOR_AMBER, COLOR_AMBER_BG)
    ]
    bw = Inches(5.75)
    bh = Inches(2.1)
    for i, (ptitle, pmech, pval, col, bg) in enumerate(pillars):
        bx = Inches(0.8) + (i % 2) * (bw + Inches(0.233))
        by = Inches(1.35) + (i // 2) * (bh + Inches(0.18))
        card = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, bx, by, bw, bh)
        card.fill.solid()
        card.fill.fore_color.rgb = bg
        card.line.color.rgb = col
        card.line.width = Pt(1.4)
        
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.15)
        
        p = tf.paragraphs[0]
        p.text = ptitle
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(4)

        p = tf.add_paragraph()
        p.text = pmech
        p.font.size = Pt(8.2)
        p.font.color.rgb = DARK_NAVY
        p.space_after = Pt(4)

        p = tf.add_paragraph()
        p.text = pval
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = col

    add_examiner_strip(s6, [
        "Theoretical Novelty: Proves Proposition S1 (12-D Invariant Disambiguation breaks 1-WL isomorphism) and Proposition S2 (Latent SMOTE preserves Kirchhoff bounds).",
        "Algorithmic Independence: All 4 pillars are modularly decoupled, allowing selective production deployment in existing Tier-1 bank tech stacks."
    ])
    set_speaker_notes(s6, "Highlight that these four pillars represent both your academic novelty for Q1 journal publication and your defensible intellectual property for a FinTech startup.")

    # =========================================================================
    # SLIDE 7: Literature Study I — Money Laundering Typologies
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "Phase 2: Literature Study I", "Literature Study I — Money Laundering Typologies & Attack Mechanics",
               "Comparing Benign Commercial Merchant Star Topologies Against Structured Multi-Hop Laundering Chains")

    # Embed Figure 1.1 if available
    fig_path = "papers/University_CSE_Thesis/figures/fig_benign_vs_smurfing_topology.png"
    if os.path.exists(fig_path):
        s7.shapes.add_picture(fig_path, Inches(0.8), Inches(1.35), Inches(5.8), Inches(4.35))
    else:
        # Placeholder card
        c_left = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(5.8), Inches(4.35))
        c_left.fill.solid()
        c_left.fill.fore_color.rgb = BG_CARD
        c_left.line.color.rgb = BORDER_CARD

    # Text Explanation Card on Right
    c_right = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(1.35), Inches(5.733), Inches(4.35))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = BG_CARD
    c_right.line.color.rgb = BORDER_CARD
    c_right.line.width = Pt(1.2)
    
    tf = c_right.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.18)
    
    p = tf.paragraphs[0]
    p.text = "THE THREE CANONICAL PHASES OF ADVERSARIAL LAUNDERING"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY
    p.space_after = Pt(8)

    stages = [
        ("1. Placement (Smurfing / Fan-In):",
         "Criminal syndicates fragment BDT 5,000,000 illicit funds into 100 sub-threshold BDT 49,000 deposits across bKash/Nagad accounts, evading BDT 100,000 static CTR alarms."),
        ("2. Layering (Peel Chains & Wash Loops):",
         "Funds bounce rapidly across pass-through mule conduits. Inflow volume closely matches outflow volume (Kirchhoff ratio Φ_peel ≈ 1.0) with rapid dwell velocity (<3.8 minutes)."),
        ("3. Integration (Cash-Out Offshore Sink):",
         "Layered flows converge into offshore shell trade entities (Singapore/UAE) or crypto OTC desks. The criminal syndicate extracts clean commercial capital.")
    ]
    for stitle, sdesc in stages:
        p = tf.add_paragraph()
        p.text = stitle
        p.font.size = Pt(9)
        p.font.bold = True
        p.font.color.rgb = COLOR_RED
        
        p = tf.add_paragraph()
        p.text = sdesc
        p.font.size = Pt(8.2)
        p.font.color.rgb = DARK_NAVY
        p.space_after = Pt(6)

    add_examiner_strip(s7, [
        "Kirchhoff Peeling Ratio Metric: Φ_peel(u) = min(Inflow_u, Outflow_u) / [max(Inflow_u, Outflow_u) + ε] → 1.0 for pass-through mule accounts vs 0.02 for legitimate retail merchants.",
        "Hawkes Self-Exciting Process: λ_u(t) = μ_u + Σ_{t_i < t} α_H exp(-β_H(t - t_i)) quantifies explosive transaction burst cascades across smurfing nodes."
    ])
    set_speaker_notes(s7, "Just as the template illustrated normal versus malicious SQL queries, use this visual to show how a 5M BDT smurfing attack looks identical to normal traffic in a spreadsheet but stands out immediately as a directed graph motif.")

    # =========================================================================
    # SLIDE 8: Literature Study II — Evolution of Financial Forensics
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "Phase 2: Literature Study II", "Literature Study II — Evolution of Financial Crime Surveillance",
               "A Three-Generation Evolutionary Staircase: Moving from Tabular Heuristics to Continuous-Time Conformal Graph Learning")

    gens = [
        ("Generation 1: Static Rules & Tabular Ensembles", "1990s – 2017: SQL Rules, Random Forest, XGBoost",
         "Fast and scalable on flat customer feature vectors. However, they operate on the flawed i.i.d. assumption with 0% multi-hop relational awareness. Over 95% false positives and completely blind to peel chains.",
         COLOR_MUTED, BG_CARD),
        ("Generation 2: Discrete Homogeneous GNNs", "2017 – 2022: GCN, GAT, EvolveGCN, TGAT",
         "Captured basic graph connectivity through recursive neighborhood aggregation. However, discrete snapshotting erased burst timing; message passing over-smoothed in high-degree hubs; and 0.05% skew collapsed recall.",
         COLOR_AMBER, COLOR_AMBER_BG),
        ("Generation 3: Proposed C-STGB Neuro-Symbolic Paradigm", "2024 – Present: C-STGB (Proposed Framework)",
         "Unifies 12-D mass-flow invariants, continuous Tri-Band temporal attention, learnable edge-trust gating, Latent GraphSMOTE, and Class-Conditional Conformal Risk Control. Delivers 91.42% F1 (+24.6 pp lead) with 0.45 ms SLA.",
         COLOR_GREEN, COLOR_GREEN_BG)
    ]
    gh = Inches(1.35)
    for i, (gtitle, gera, gdesc, col, bg) in enumerate(gens):
        gy = Inches(1.35) + i * (gh + Inches(0.12))
        card = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), gy, Inches(11.733), gh)
        card.fill.solid()
        card.fill.fore_color.rgb = bg
        card.line.color.rgb = col
        card.line.width = Pt(1.4)
        
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.12)
        
        p = tf.paragraphs[0]
        p.text = gtitle
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col
        
        p = tf.add_paragraph()
        p.text = gera
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = DARK_NAVY
        p.space_after = Pt(3)

        p = tf.add_paragraph()
        p.text = gdesc
        p.font.size = Pt(8.2)
        p.font.color.rgb = DARK_NAVY

    add_examiner_strip(s8, [
        "1-WL Graph Isomorphism Expressive Limit: Morris et al. (2019) proved standard message passing cannot distinguish graphs with identical degree profiles; C-STGB breaks 1-WL symmetry via 12-D flow invariants.",
        "Continuous-Time Dynamical Stability: Dirichlet Energy E(H) = Tr(H^T L H) is strictly bounded away from 0 via edge-trust gating, preventing feature over-smoothing across deep layers."
    ])
    set_speaker_notes(s8, "Explain that while tree ensembles like Random Forest and XGBoost are strong on static tabular attributes, they cannot trace multi-hop peel chains without C-STGB's topological message passing.")

    # =========================================================================
    # SLIDE 9: Related Works & State-of-the-Art Gap Matrix
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "Phase 2: Related Works & Gap Matrix", "Related Works & State-of-the-Art Gap Matrix",
               "Critical Synthesis of Five Foundational Literature Paradigms Establishing the Theoretical and Practical Necessity of C-STGB")

    # Table comparing 5 papers vs C-STGB
    tbl_shape = s9.shapes.add_table(6, 5, Inches(0.8), Inches(1.35), Inches(11.733), Inches(2.7))
    tbl = tbl_shape.table
    tbl.columns[0].width = Inches(2.4)
    tbl.columns[1].width = Inches(2.7)
    tbl.columns[2].width = Inches(1.8)
    tbl.columns[3].width = Inches(2.2)
    tbl.columns[4].width = Inches(2.633)

    headers = ["Research Work", "Core Architecture", "Velocity Aware", "Skew & Camouflage", "Guaranteed Triage & SAR"]
    for ci, h in enumerate(headers):
        cell = tbl.cell(0, ci)
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    rows_data = [
        ("Weber et al. (2019)", "GCN + Random Forest", "No (Static Snapshots)", "No (Fails on 0.05% Skew)", "No (Point Softmax Only)"),
        ("Pareja et al. (2020)", "EvolveGCN (Discrete RNN)", "Partial (1-day windows)", "No (Over-smoothed Hubs)", "No (Manual Heuristics)"),
        ("Eddin et al. (2022)", "Subgraph Alert GNN", "Partial (Discrete Graphs)", "No (Hub Camouflage Blind)", "No (No Confidence Bounds)"),
        ("Egressy et al. (2024)", "Directed Multigraph GNN", "Yes (Directional GNN)", "Partial (No Invariant Gating)", "No (No Legal SAR Output)"),
        ("Proposed C-STGB", "Tri-Band GNN + CRC + Agents", "Yes (Continuous 3-Band)", "Yes (65.9% Chaff Pruned)", "Yes (99.12% Cov + AST SAR)")
    ]
    for ri, r in enumerate(rows_data):
        is_cstgb = (ri == 4)
        bg_col = COLOR_GREEN_BG if is_cstgb else (BG_CARD if ri % 2 == 0 else WHITE)
        for ci, val in enumerate(r):
            cell = tbl.cell(ri + 1, ci)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_col
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(8.0)
            p.font.bold = is_cstgb
            p.font.color.rgb = COLOR_GREEN if is_cstgb else DARK_NAVY
            if ci > 0:
                p.alignment = PP_ALIGN.CENTER

    # Summary box below table
    sbox = s9.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.2), Inches(11.733), Inches(1.5))
    sbox.fill.solid()
    sbox.fill.fore_color.rgb = BG_CARD
    sbox.line.color.rgb = BORDER_CARD
    tf = sbox.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.12)
    p = tf.paragraphs[0]
    p.text = "CORE RESEARCH GAPS SOLVED BY C-STGB:"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE
    p.space_after = Pt(4)
    gaps = [
        "1. Velocity Erasure: Existing models use coarse discrete time slices (e.g. 1-day or 2-week) that completely erase sub-second mobile money smurfing bursts.",
        "2. Absence of Finite-Sample Risk Guarantees: All prior GNN models rely on arbitrary softmax thresholds (τ = 0.50), resulting in uncontrolled false negatives.",
        "3. Lack of Operational Compliance Tooling: Not a single prior academic paper bridges the gap between GNN inference and automated, court-admissible SAR filings."
    ]
    for g in gaps:
        p = tf.add_paragraph()
        p.text = g
        p.font.size = Pt(8.0)
        p.font.color.rgb = DARK_NAVY
        p.space_after = Pt(1)

    add_examiner_strip(s9, [
        "SOTA Gap Quantification: 25-paper survey across KDD, AAAI, NeurIPS, and IEEE S&P confirms C-STGB is the first framework providing distribution-free finite-sample guarantees in financial graphs.",
        "Computational SLA Gap: While existing dynamic GNNs require 40–180 ms per inference, C-STGB executes in 0.45 ms via out-of-core DuckDB caching."
    ])
    set_speaker_notes(s9, "Highlight that none of the existing models solve the complete problem: some capture static topology, some capture discrete time, but none handle extreme skew, camouflage pruning, and automated legal compliance together.")

    # =========================================================================
    # SLIDE 10: Proposed Method — End-to-End 6-Layer System Overview
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "Phase 3: Proposed Architecture", "Proposed Method — End-to-End 6-Layer Operational Architecture",
               "From ISO 20022 Stream Ingestion to Sub-Millisecond Conformal Triage and Merkle-Sealed Regulatory Reporting")

    # Embed Figure 1.3 / 1.2
    fig_path = "papers/University_CSE_Thesis/figures/fig1_operational_architecture_flowchart.png"
    if os.path.exists(fig_path):
        s10.shapes.add_picture(fig_path, Inches(0.8), Inches(1.35), Inches(11.733), Inches(4.35))
    else:
        # Fallback card
        c = s10.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(11.733), Inches(4.35))
        c.fill.solid()
        c.fill.fore_color.rgb = BG_CARD
        c.line.color.rgb = BORDER_CARD

    add_examiner_strip(s10, [
        "Sub-Millisecond Fast-Path SLA: Total end-to-end inference latency = 0.45 ms (Ingestion: 0.11 ms, Invariants: 0.08 ms, GNN: 0.16 ms, CRC: 0.04 ms, Response: 0.06 ms).",
        "Deterministic Risk Triage: Tier 1 Quarantined (0.18%), Tier 2 Human Review (0.49% — 49 / 10k wires), Tier 3 Straight-Through Cleared (99.33% — 9,933 / 10k wires automated STP)."
    ])
    set_speaker_notes(s10, "Walk across the flowchart from left to right, pointing out how the 6 layers process a payment in 0.45 ms on the fast path while guaranteeing human-in-the-loop regulatory compliance.")

    # =========================================================================
    # SLIDE 11: Proposed Method (Parts 1 & 2) — 14-Dataset Portfolio & Ingestion
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "Phase 3: Data Ingestion & Partitions", "14-Dataset Cross-Domain Portfolio & Zero-Lookahead Ingestion",
               "Evaluating Across 4 Financial Sectors with Strict Forward-in-Time Temporal Partitions (Lemma S1) and 16GB RAM Out-of-Core Execution")

    # Left: 14 Dataset Portfolio Card
    c_left = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(5.6), Inches(4.35))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = BG_CARD
    c_left.line.color.rgb = BORDER_CARD
    c_left.line.width = Pt(1.2)
    tf = c_left.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.18)
    p = tf.paragraphs[0]
    p.text = "14 CROSS-DOMAIN FINANCIAL BENCHMARKS"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE
    p.space_after = Pt(6)

    datasets_summary = [
        ("Public Cryptographic Ledgers (5 Networks):",
         "elliptic_v1 (203k tx), elliptic_v2 (122k tx), eth_phishing (2.9M tx), xblock_eth (1.1M tx), mtgox_leaked (140k tx). Captures UTXO and EVM smart contract laundering."),
        ("Multi-Bank & Inter-Bank Clearing (5 Networks):",
         "saml_d (9.2M tx across 15 banks), dgraphfin (4.3M dynamic credit nodes), ibm_amlsim_hi/li variants (synthetic wire rails)."),
        ("Mobile Money & Card Payment Streams (4 Networks):",
         "paysim_extended (1.04M m-wallet hops), cc_transactions (284k credit card streams), paysim1 (6.3M mobile payments).")
    ]
    for dtitle, ddesc in datasets_summary:
        p = tf.add_paragraph()
        p.text = dtitle
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = DARK_NAVY
        p = tf.add_paragraph()
        p.text = ddesc
        p.font.size = Pt(7.8)
        p.font.color.rgb = SLATE_MUTED
        p.space_after = Pt(4)

    # Right: Embed ERD or Causal Slicing Figure
    fig_path = "papers/University_CSE_Thesis/figures/fig4_2_database_erd.png"
    if os.path.exists(fig_path):
        s11.shapes.add_picture(fig_path, Inches(6.6), Inches(1.35), Inches(5.933), Inches(4.35))
    else:
        c_right = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.6), Inches(1.35), Inches(5.933), Inches(4.35))
        c_right.fill.solid()
        c_right.fill.fore_color.rgb = BG_CARD
        c_right.line.color.rgb = BORDER_CARD

    add_examiner_strip(s11, [
        "Lemma S1 (Zero-Lookahead Chronological Partitioning): I(G_train; D_test | D_train) = 0; strict chronological splitting guarantees zero evaluation contamination.",
        "Out-of-Core Memory Footprint: DuckDB composite B-tree indexes + Arrow zero-copy memory buffers stream 125GB+ transaction ledgers in under 250 MB RAM."
    ])
    set_speaker_notes(s11, "Contrast the template's single static CSV split with your 14-dataset cross-domain benchmark and out-of-core DuckDB streaming engine that prevents RAM crashes on standard bank hardware.")

    # =========================================================================
    # SLIDE 12: Proposed Method (Part 3) — 12-D Canonical Invariants & Cold-Start
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "Phase 3: Domain Invariants", "12-D Canonical Flow Invariants & Cold-Start Fusion Gate",
               "Overcoming 1-WL Graph Isomorphism and Resolving the Zero-History Mule Cold-Start Problem (+71.20 pp F1 Gain)")

    # Left: 5 Invariant Groups
    c_left = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(5.5), Inches(4.35))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = BG_CARD
    c_left.line.color.rgb = BORDER_CARD
    c_left.line.width = Pt(1.2)
    tf = c_left.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.18)
    p = tf.paragraphs[0]
    p.text = "5 PHYSICS-GUIDED INVARIANT GROUPS (12-D VECTOR)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE
    p.space_after = Pt(6)

    inv_groups = [
        ("1. Kirchhoff Conservation:", "Flow ratio Φ_flow and net balance asymmetry Ψ_asym track pass-through vs absorbing accounts."),
        ("2. Hawkes Point Process:", "Instantaneous arrival velocity λ_u(t) and excitation parameter capture smurfing bursts."),
        ("3. Directed 2-Hop Kinetics:", "Forward velocity s_fwd and backward velocity s_bwd quantify funnel-in vs peel-out dynamics."),
        ("4. Structural Topological Cycles:", "Detects circular wash loops and multi-entity laundering rings."),
        ("5. 7-Moment Statistical Profile:", "Transaction amount variance v_A, inter-arrival variance σ_Δt, and KYC risk score.")
    ]
    for ititle, idesc in inv_groups:
        p = tf.add_paragraph()
        p.text = ititle
        p.font.size = Pt(8.5)
        p.font.bold = True
        p.font.color.rgb = DARK_NAVY
        p = tf.add_paragraph()
        p.text = idesc
        p.font.size = Pt(7.8)
        p.font.color.rgb = SLATE_MUTED
        p.space_after = Pt(3)

    # Right: Embed Canonical Invariants Empirical plot
    fig_path = "papers/University_CSE_Thesis/figures/fig_canonical_invariants_empirical.png"
    if os.path.exists(fig_path):
        s12.shapes.add_picture(fig_path, Inches(6.5), Inches(1.35), Inches(6.033), Inches(4.35))
    else:
        c_right = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.5), Inches(1.35), Inches(6.033), Inches(4.35))
        c_right.fill.solid()
        c_right.fill.fore_color.rgb = BG_CARD
        c_right.line.color.rgb = BORDER_CARD

    add_examiner_strip(s12, [
        "Cold-Start Evidence-Adaptive Fusion: h_u* = α_u h_u^(L) + (1 - α_u) W_inv z_inv(u,t), where α_u = σ(w_α^T [deg(u), Δt_u, Vol_u]).",
        "Empirical Cold-Start Breakthrough: At degree 0, standalone GNN achieves only 18.40% F1; C-STGB fusion achieves 89.60% F1 (+71.20 pp gain)."
    ])
    set_speaker_notes(s12, "Explain that criminals constantly open fresh accounts with no graph history; your 12-D physics-inspired invariants catch them on their very first burst transfer.")

    # =========================================================================
    # SLIDE 13: Proposed Method (Part 4) — C-STGB Neural Core
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "Phase 3: Neural Core", "C-STGB Neural Core — Tri-Band Harmonic Attention & Edge Gate",
               "Continuous Multi-Scale Temporal Attention Bridges Sub-Minute Bursts and 90-Day Dormancy while Pruning Camouflage Chaff")

    # Embed Slide 13 Neural Core (Tri-Band Continuous Harmonic Attention & Edge-Trust Gating)
    fig_path = "papers/University_CSE_Thesis/figures/fig_slide13_neural_core.png"
    if os.path.exists(fig_path):
        s13.shapes.add_picture(fig_path, Inches(0.8), Inches(1.35), Inches(11.733), Inches(4.35))
    else:
        c = s13.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(11.733), Inches(4.35))
        c.fill.solid()
        c.fill.fore_color.rgb = BG_CARD
        c.line.color.rgb = BORDER_CARD

    add_examiner_strip(s13, [
        "Continuous Tri-Band Kernel: w(Δt) = Σ_b π_b [w_min + (1 - w_min) exp(-λ_b Δt)](1 + β_b tanh(burst_ij)); w_min = 0.05 prevents gradient vanishing.",
        "Learnable Edge-Trust Gating: g^_ij = σ(w_g^T [h_i || h_j || e_ij]) ∈ [0.10, 1.0]; prunes 65.9% of merchant hub camouflage chaff."
    ])
    set_speaker_notes(s13, "Point to the two mechanisms that defeat adversarial evasion: Tri-Band decay catches both 5-second mobile bursts and 90-day sleeper accounts, while the Edge Gate cuts off commercial hub camouflage.")

    # =========================================================================
    # SLIDE 14: Proposed Method (Part 5) — Latent SMOTE & Focal Tversky Loss
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "Phase 3: Imbalance Rectification", "Latent GraphSMOTE & Asymmetric Focal Tversky Loss",
               "Eliminating Minority Recall Collapse Under Extreme Skew (π < 0.05%) while Preserving Kirchhoff Monetary Flow Bounds")

    # Embed Figure 18 GraphSMOTE
    fig_path = "papers/University_CSE_Thesis/figures/fig18_graphsmote_synthesis_pipeline.png"
    if os.path.exists(fig_path):
        s14.shapes.add_picture(fig_path, Inches(0.8), Inches(1.35), Inches(5.8), Inches(4.35))
    else:
        c_left = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(5.8), Inches(4.35))
        c_left.fill.solid()
        c_left.fill.fore_color.rgb = BG_CARD
        c_left.line.color.rgb = BORDER_CARD

    # Embed Figure 3.10 Gradient Dynamics on right
    fig_path2 = "papers/University_CSE_Thesis/figures/fig_3_10_gradient_dynamics.png"
    if os.path.exists(fig_path2):
        s14.shapes.add_picture(fig_path2, Inches(6.8), Inches(1.35), Inches(5.733), Inches(4.35))
    else:
        c_right = s14.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(1.35), Inches(5.733), Inches(4.35))
        c_right.fill.solid()
        c_right.fill.fore_color.rgb = BG_CARD
        c_right.line.color.rgb = BORDER_CARD

    add_examiner_strip(s14, [
        "Proposition S2 (Kirchhoff Flow Preservation): min(Φ_u, Φ_v) ≤ Φ_flow(h_syn) ≤ max(Φ_u, Φ_v); latent interpolation strictly preserves monetary mass conservation.",
        "Asymmetric Loss: L_AFT = (1 - TI_c)^γ; with β_FN = 0.85 and β_FP = 0.15, false-negative gradients receive a 5.67x amplification over false positives."
    ])
    set_speaker_notes(s14, "Directly address your supervisor's template focus on overfitting and underfitting: Latent GraphSMOTE prevents overfitting on rare fraud motifs, while Asymmetric Focal Tversky Loss prevents underfitting on the minority class.")

    # =========================================================================
    # SLIDE 15: Proposed Method (Part 6) — Conformal Risk Control (CRC)
    # =========================================================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "Phase 3: Conformal Triage", "Class-Conditional Conformal Risk Control (CRC)",
               "Finite-Sample Statistical Coverage Guarantees Overcoming Marginal Collapse and Enabling 99.33% Automated Straight-Through Clearing")

    # Embed Conformal Conveyor Funnel
    fig_path = "papers/University_CSE_Thesis/figures/fig_conformal_conveyor_funnel.png"
    if os.path.exists(fig_path):
        s15.shapes.add_picture(fig_path, Inches(0.8), Inches(1.35), Inches(11.733), Inches(4.35))
    else:
        c = s15.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(11.733), Inches(4.35))
        c.fill.solid()
        c.fill.fore_color.rgb = BG_CARD
        c.line.color.rgb = BORDER_CARD

    add_examiner_strip(s15, [
        "Finite-Sample Recall Coverage: P(Y_{n+1} ∈ Γ(X_{n+1}) | Y = 1) ≥ 1 - α_1; calibrated across disjoint calibration split D_cal.",
        "Operational Workload Routing: Tier 1 Auto-Hold (0.18% vol), Tier 2 Human + Swarm Review (0.49% vol — 49 / 10k wires), Tier 3 Instant Auto-Clear (99.33% vol — 9,933 / 10k wires)."
    ])
    set_speaker_notes(s15, "Explain the business breakthrough here: instead of drowning compliance officers in 95% false alarms, Conformal Risk Control mathematically proves which 99.33% of transactions can be safely cleared without human touch.")

    # =========================================================================
    # SLIDE 16: Proposed Method (Part 7) — Causal XAI & 4-Agent SAR Desk
    # =========================================================================
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "Phase 3: Agentic SAR Desk", "Causal XAI & Assisted 4-Agent SAR Compliance Desk",
               "GNNExplainer Subgraph Hydration, Abstract Syntax Tree Grammar Validation, and SHA-256 Merkle WORM Regulatory Archival")

    # Embed Figure 6.1 (Forensic Swarm) or Fig 6.5 (Merkle Tree)
    fig_path = "papers/University_CSE_Thesis/figures/fig_forensic_swarm.png"
    if os.path.exists(fig_path):
        s16.shapes.add_picture(fig_path, Inches(0.8), Inches(1.35), Inches(11.733), Inches(4.35))
    else:
        c = s16.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(11.733), Inches(4.35))
        c.fill.solid()
        c.fill.fore_color.rgb = BG_CARD
        c.line.color.rgb = BORDER_CARD

    add_examiner_strip(s16, [
        "AST Grammar Verification: Every entity ID, timestamp, and BDT/USD amount is verified against DuckDB transactional facts (0.00% hallucination rate).",
        "FRE Rule 902(11) Self-Authenticating Legal Admissibility: Modifying even one byte in a filed SAR breaks the SHA-256 Merkle tree root."
    ])
    set_speaker_notes(s16, "Emphasize that banks cannot use standard ChatGPT because LLMs hallucinate numbers and autonomous filing is illegal; your AST compiler guarantees zero hallucinations and keeps a human officer in final control.")

    # =========================================================================
    # SLIDE 17: Empirical Evaluation & Calibration Proof
    # =========================================================================
    s17 = prs.slides.add_slide(blank_layout)
    add_header(s17, "Phase 4: Empirical Evaluation", "Performance Evaluation Metrics & Conformal Calibration Proof",
               "Rigorous Evaluation on Imbalanced PR-AUC and Empirical Verification of Finite-Sample Coverage Under Adversarial Drift")

    # Left: Calibration Scorecard Table
    tbl_shape = s17.shapes.add_table(6, 5, Inches(0.8), Inches(1.35), Inches(5.8), Inches(2.6))
    tbl = tbl_shape.table
    tbl.columns[0].width = Inches(1.8)
    tbl.columns[1].width = Inches(1.0)
    tbl.columns[2].width = Inches(1.0)
    tbl.columns[3].width = Inches(1.0)
    tbl.columns[4].width = Inches(1.0)

    headers = ["Calibration Method", "Benign Cov", "Illicit Cov", "Target Gap", "Queue Size"]
    for ci, h in enumerate(headers):
        cell = tbl.cell(0, ci)
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(7.5)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    cal_data = [
        ("Uncalibrated Softmax", "99.94%", "71.20%", "-27.80 pp", "0.12%"),
        ("Temperature Scaling", "99.89%", "92.80%", "-6.20 pp", "0.31%"),
        ("Isotonic Regression", "99.85%", "94.50%", "-4.50 pp", "0.38%"),
        ("Marginal Conformal", "99.91%", "82.40%", "-16.60 pp", "18.40%"),
        ("C-STGB Class-Cond. CRC", "99.33%", "99.12%", "+0.12 pp", "0.49%")
    ]
    for ri, r in enumerate(cal_data):
        is_cstgb = (ri == 4)
        bg_col = COLOR_GREEN_BG if is_cstgb else (BG_CARD if ri % 2 == 0 else WHITE)
        for ci, val in enumerate(r):
            cell = tbl.cell(ri + 1, ci)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg_col
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(7.5)
            p.font.bold = is_cstgb
            p.font.color.rgb = COLOR_GREEN if is_cstgb else DARK_NAVY
            if ci > 0:
                p.alignment = PP_ALIGN.CENTER

    # Discussion Box below Table
    box_cal = s17.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(4.1), Inches(5.8), Inches(1.6))
    box_cal.fill.solid()
    box_cal.fill.fore_color.rgb = BG_CARD
    box_cal.line.color.rgb = BORDER_CARD
    tf = box_cal.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.15)
    tf.margin_top = Inches(0.1)
    p = tf.paragraphs[0]
    p.text = "WHY PR-AUC TRUMPS ACCURACY IN AML:"
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE
    p.space_after = Pt(2)
    p = tf.add_paragraph()
    p.text = "Under <0.05% skew, a trivial model predicting all-benign achieves 99.95% accuracy while missing 100% of money laundering. PR-AUC and minority recall are the true forensic measures of model efficacy."
    p.font.size = Pt(7.8)
    p.font.color.rgb = DARK_NAVY

    # Right: Embed PR Curves plot
    fig_path = "papers/University_CSE_Thesis/figures/fig_all_datasets_pr_curves.png"
    if os.path.exists(fig_path):
        s17.shapes.add_picture(fig_path, Inches(6.8), Inches(1.35), Inches(5.733), Inches(4.35))
    else:
        c_right = s17.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(1.35), Inches(5.733), Inches(4.35))
        c_right.fill.solid()
        c_right.fill.fore_color.rgb = BG_CARD
        c_right.line.color.rgb = BORDER_CARD

    add_examiner_strip(s17, [
        "Adaptive Conformal Inference (ACI): α_{t+1} = α_t + γ(α - err_t) dynamically shifts non-conformity quantiles to guarantee ≥99.0% empirical coverage under drift.",
        "DKW Uniform Risk Bound: P(sup_s |F_n(s) - F(s)| > ε) ≤ 2 exp(-2n ε^2) guarantees calibration bounds hold across all 14 evaluated datasets."
    ])
    set_speaker_notes(s17, "Walk through the calibration scorecard, emphasizing that C-STGB is the only model that achieves the statutory 99.0% coverage requirement while keeping the human review queue under 0.50%.")

    # =========================================================================
    # SLIDE 18: Performance Comparison & Stepwise Ablation Study
    # =========================================================================
    s18 = prs.slides.add_slide(blank_layout)
    add_header(s18, "Phase 4: Benchmarks & Ablation", "Master Cross-Domain Benchmarks & Stepwise Ablation Study",
               "Empirical Superiority Across 14 Networks and Stepwise Component Attribution Proving Each Innovation's Contribution")

    # Left: Master Benchmark Table
    tbl_shape = s18.shapes.add_table(7, 5, Inches(0.8), Inches(1.35), Inches(5.8), Inches(4.35))
    tbl = tbl_shape.table
    tbl.columns[0].width = Inches(1.6)
    tbl.columns[1].width = Inches(1.3)
    tbl.columns[2].width = Inches(0.9)
    tbl.columns[3].width = Inches(1.0)
    tbl.columns[4].width = Inches(1.0)

    headers = ["Benchmark Dataset", "Domain", "GCN F1", "XGBoost F1", "C-STGB F1"]
    for ci, h in enumerate(headers):
        cell = tbl.cell(0, ci)
        cell.fill.solid()
        cell.fill.fore_color.rgb = DARK_NAVY
        p = cell.text_frame.paragraphs[0]
        p.text = h
        p.font.size = Pt(7.5)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

    bench_data = [
        ("elliptic_v1", "Bitcoin UTXO", "68.40%", "88.35%", "91.42%"),
        ("elliptic_v2", "Multi-Asset Crypto", "71.20%", "91.10%", "99.10%"),
        ("paysim_extended", "Mobile Money", "64.50%", "96.40%", "99.80%"),
        ("saml_d", "15-Bank Wire", "58.90%", "84.20%", "93.68%"),
        ("eth_phishing", "Ethereum DeFi", "79.40%", "94.80%", "99.75%"),
        ("ibm_amlsim_hi", "Multi-Tier Wire", "19.80%", "38.90%", "46.85%")
    ]
    for ri, r in enumerate(bench_data):
        for ci, val in enumerate(r):
            cell = tbl.cell(ri + 1, ci)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLOR_GREEN_BG if ci == 4 else (BG_CARD if ri % 2 == 0 else WHITE)
            p = cell.text_frame.paragraphs[0]
            p.text = val
            p.font.size = Pt(7.5)
            p.font.bold = (ci == 4)
            p.font.color.rgb = COLOR_GREEN if ci == 4 else DARK_NAVY
            if ci > 1:
                p.alignment = PP_ALIGN.CENTER

    # Right: Embed Champion Delta / Leave-One-Out plot
    fig_path = "papers/University_CSE_Thesis/figures/fig_champion_vs_runnerup_delta.png"
    if os.path.exists(fig_path):
        s18.shapes.add_picture(fig_path, Inches(6.8), Inches(1.35), Inches(5.733), Inches(4.35))
    else:
        c_right = s18.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(1.35), Inches(5.733), Inches(4.35))
        c_right.fill.solid()
        c_right.fill.fore_color.rgb = BG_CARD
        c_right.line.color.rgb = BORDER_CARD

    add_examiner_strip(s18, [
        "Ablation Climb on Elliptic-v1: GCN (26.4%) → +Invariants (54.8%) → +Tri-Band (68.5%) → +Edge Gate (76.2%) → +SMOTE (86.1%) → +Focal Tversky (91.42%).",
        "Statistical Significance: Global Rank #1 across all 14 networks confirmed via Paired Wilcoxon Signed-Rank Test (W = 105.0, p = 0.000122)."
    ])
    set_speaker_notes(s18, "Point to the ablation progression to show examiners that our performance does not come from a single trick, but from a principled 6-stage mathematical stack.")

    # =========================================================================
    # SLIDE 19: Forensic Case Study & Commercial FinTech Market Value
    # =========================================================================
    s19 = prs.slides.add_slide(blank_layout)
    add_header(s19, "Phase 5: Venture Pitch & Case Study", "Forensic Case Study & Commercial FinTech Market Value",
               "Live Interception of Account ACC_9941 Laundering Ring and Immediate B2B SaaS ROI for Commercial Banks")

    # Embed Forensic Timeline on Left Top
    fig_case = "papers/University_CSE_Thesis/figures/fig_single_alert_timeline.png"
    if os.path.exists(fig_case):
        s19.shapes.add_picture(fig_case, Inches(0.8), Inches(1.35), Inches(5.6), Inches(2.1))

    # Left Bottom: Case Study ACC_9941 summary
    c_left = s19.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.55), Inches(5.6), Inches(2.25))
    c_left.fill.solid()
    c_left.fill.fore_color.rgb = BG_CARD
    c_left.line.color.rgb = COLOR_RED
    c_left.line.width = Pt(1.2)
    tf = c_left.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.15)
    tf.margin_top = Inches(0.1)
    p = tf.paragraphs[0]
    p.text = "LIVE FORENSIC CATCH: ACC_9941 PEEL CHAIN"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_RED
    p.space_after = Pt(2)

    case_bullets = [
        ("Motijheel Wire Influx (10:15 BST):", "BDT 5.0M reactivates dormant account; primary wire flagged."),
        ("bKash/Nagad Smurfing (10:19 BST):", "50x BDT 99k micro-batches bypass CTR; 12-D invariants detect near-zero retention."),
        ("Chattogram Trade Wash (10:23 BST):", "Injected to Khatunganj hub; edge gate prunes 14 benign chaff links."),
        ("Automated Freeze & SAR (10:28 BST):", "15-node ring frozen in 0.45 ms; 4-agent swarm drafts BFIU SAR in 28.4 sec.")
    ]
    for ctitle, cdesc in case_bullets:
        p = tf.add_paragraph()
        p.text = f"{ctitle} {cdesc}"
        p.font.size = Pt(7.2)
        p.font.color.rgb = DARK_NAVY
        p.space_after = Pt(1)

    # Embed 3D Surveillance Console Screenshot on Right Top
    fig_ui = "papers/University_CSE_Thesis/figures/01_surveillance_desk.png"
    if os.path.exists(fig_ui):
        s19.shapes.add_picture(fig_ui, Inches(6.6), Inches(1.35), Inches(5.933), Inches(2.1))

    # Right Bottom: Venture Unit Economics Card
    c_right = s19.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.6), Inches(3.55), Inches(5.933), Inches(2.25))
    c_right.fill.solid()
    c_right.fill.fore_color.rgb = BG_CARD
    c_right.line.color.rgb = COLOR_GREEN
    c_right.line.width = Pt(1.3)
    tf = c_right.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.15)
    tf.margin_top = Inches(0.1)
    p = tf.paragraphs[0]
    p.text = "B2B FINTECH SAAS BUSINESS VALUE & ROI"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN
    p.space_after = Pt(2)

    biz_bullets = [
        ("99.50%+ Queue Cut:", "Reduces manual alerts from 1,840 to 49 per 10k tx, resolving analyst fatigue."),
        ("99.0% Labor Saved:", "Compresses SAR drafting from 4–6 hrs to <60 sec ($1.2M+ saved annually)."),
        ("Cloud Deployment:", "Kubernetes microservice handling 31,250 tx/s burst throughput under 16GB RAM."),
        ("Monetization:", "Annual license ($150k–$450k/yr) + per-tx screening fee ($0.02–$0.05/tx).")
    ]
    for btitle, bdesc in biz_bullets:
        p = tf.add_paragraph()
        p.text = f"{btitle} {bdesc}"
        p.font.size = Pt(7.2)
        p.font.color.rgb = DARK_NAVY
        p.space_after = Pt(1)

    add_examiner_strip(s19, [
        "Detection Window Economics: Total Influx-to-Quarantine Elapsed Dwell = 13 Minutes 12 Seconds vs industry average of 180 to 240 days.",
        "Production Hardware Footprint: Containerized Docker / FastAPI cluster scales from 4 to 32 pods under <70% CPU target, meeting banking tier SLAs."
    ])
    set_speaker_notes(s19, "Walk the audience through the real 15-node crime ring caught by your software, then pivot to the bank CEO perspective: C-STGB turns compliance from a multi-million-dollar cost center into an automated, sub-millisecond shield.")

    # =========================================================================
    # SLIDE 20: Future Impact, Conclusion & References
    # =========================================================================
    s20 = prs.slides.add_slide(blank_layout)
    add_header(s20, "Phase 5: Future Horizons & Conclusion", "Future Impact in Finance, Conclusion & Key References",
               "Extending C-STGB into Federated Cross-Bank Intelligence, CBDC Surveillance, and Automated Digital Asset Governance")

    # Top Half: 3-Horizon Financial Roadmap
    c_top = s20.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.35), Inches(11.733), Inches(2.3))
    c_top.fill.solid()
    c_top.fill.fore_color.rgb = BG_CARD
    c_top.line.color.rgb = BORDER_CARD
    c_top.line.width = Pt(1.2)
    tf = c_top.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.12)
    p = tf.paragraphs[0]
    p.text = "THREE-HORIZON ROADMAP FOR THE FINANCIAL INDUSTRY"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_BLUE
    p.space_after = Pt(4)

    horizons = [
        ("Horizon 1 (Near-Term — MFS Protection):", "Real-time (<1 ms) anti-smurfing defense for South Asian mobile money rails (bKash, Nagad, Rocket) without slowing consumer P2P velocity."),
        ("Horizon 2 (Mid-Term — Federated Bank Intelligence):", "Flower + Opacus Differential Privacy (ε ≤ 1.0) enables competing commercial banks to detect collaborative inter-bank mule rings without exposing customer PII."),
        ("Horizon 3 (Long-Term — CBDC & DeFi Readiness):", "Frozen-weight zero-shot transferability (69.98% cross-domain F1) protects newly deployed Central Bank Digital Currencies and cross-chain bridges on day one.")
    ]
    for htitle, hdesc in horizons:
        p = tf.add_paragraph()
        p.text = htitle
        p.font.size = Pt(8.2)
        p.font.bold = True
        p.font.color.rgb = DARK_NAVY
        p = tf.add_paragraph()
        p.text = hdesc
        p.font.size = Pt(7.6)
        p.font.color.rgb = SLATE_MUTED
        p.space_after = Pt(2)

    # Bottom Left: Core Conclusions
    c_bot_left = s20.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(3.75), Inches(5.75), Inches(2.05))
    c_bot_left.fill.solid()
    c_bot_left.fill.fore_color.rgb = COLOR_GREEN_BG
    c_bot_left.line.color.rgb = COLOR_GREEN
    c_bot_left.line.width = Pt(1.2)
    tf = c_bot_left.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.18)
    tf.margin_top = Inches(0.1)
    p = tf.paragraphs[0]
    p.text = "CORE DEFENSE CONCLUSIONS"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN
    p.space_after = Pt(2)
    concls = [
        "• Solved 5 GNN Failure Modes: Breaks 1-WL isomorphism, eliminates camouflage over-smoothing, and recovers minority recall.",
        "• Rigorous Coverage Guarantees: 99.12% empirical illicit recall with 99.33% automated straight-through processing.",
        "• Open-Source & Reproducible: Complete 134-page monograph, 56 standalone Python figure scripts, and production FastAPI backend."
    ]
    for c in concls:
        p = tf.add_paragraph()
        p.text = c
        p.font.size = Pt(7.6)
        p.font.color.rgb = DARK_NAVY
        p.space_after = Pt(1)

    # Bottom Right: Key References & Q&A
    c_bot_right = s20.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.783), Inches(3.75), Inches(5.75), Inches(2.05))
    c_bot_right.fill.solid()
    c_bot_right.fill.fore_color.rgb = BG_CARD
    c_bot_right.line.color.rgb = BORDER_CARD
    c_bot_right.line.width = Pt(1.2)
    tf = c_bot_right.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.18)
    tf.margin_top = Inches(0.1)
    p = tf.paragraphs[0]
    p.text = "KEY CORNERSTONE REFERENCES"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = DARK_NAVY
    p.space_after = Pt(2)
    refs = [
        "1. Weber et al., 'Anti-money laundering in Bitcoin: Experimenting with GCNs,' KDD, 2019.",
        "2. Pareja et al., 'EvolveGCN: Evolving GCNs for dynamic graphs,' AAAI, 2020.",
        "3. Zhao et al., 'GraphSMOTE: Imbalanced node classification on graphs,' WSDM, 2021.",
        "4. Angelopoulos & Bates, 'Conformal prediction: A gentle introduction,' FTML, 2023.",
        "5. Egressy et al., 'Provably powerful GNNs for directed multigraphs,' AAAI, 2024."
    ]
    for r in refs:
        p = tf.add_paragraph()
        p.text = r
        p.font.size = Pt(7.0)
        p.font.color.rgb = SLATE_MUTED

    add_examiner_strip(s20, [
        "Monograph Artifact Verification: 134 pages, 56 reproducible Python figures (175 tests / 100% test pass across 30 modules), 14 evaluated datasets, 0 broken references, compiled with Tectonic.",
        "Committee Q&A: The candidates invite questions and critical discussion from the examination board."
    ])
    set_speaker_notes(s20, "Close by summarizing how C-STGB bridges geometric deep learning, conformal statistics, and agentic law to secure the future of digital banking, then invite questions from the examination board.")

    # Save presentation
    output_path = "presentations/C-STGB_Thesis_Defense_Pitch.pptx"
    prs.save(output_path)
    print(f"Successfully generated {output_path} (20 slides, 16:9 widescreen, Two-Zone Design Pattern).")

if __name__ == "__main__":
    create_presentation()
