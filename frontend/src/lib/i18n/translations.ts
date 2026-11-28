/**
 * Intelligent-AML Enterprise i18n Dictionary
 * Supporting English (en) and Bangla (bn) for Bangladesh BFIU & International Compliance.
 */

export type Language = 'en' | 'bn';
export type DisplayCurrency = 'BDT' | 'USD';

export const TRANSLATIONS = {
  en: {
    // Navigation Modules
    nav_overview: '1. Executive Surveillance',
    nav_triage: '2. Alert Triage',
    nav_screening: '3. Sanctions & PEP',
    nav_customers: '4. Customer 360° KYC',
    nav_cases: '5. Institutional Cases',
    nav_graph: '6. Forensic Cash Flow',
    nav_tbml: '7. Trade Finance TBML',
    nav_sar: '8. SAR & CTR Workbench',
    nav_rfi: '9. Compliance RFI Hub',
    nav_rules: '10. Rule Studio & Recourse',
    nav_governance: '11. Model Ops & WORM',

    // Short Labels
    short_overview: 'Overview',
    short_triage: 'Triage',
    short_screening: 'Screening',
    short_customers: 'Customers',
    short_cases: 'Cases',
    short_graph: 'Graph',
    short_tbml: 'TBML',
    short_sar: 'SAR/CTR',
    short_rfi: 'RFI',
    short_rules: 'Rules',
    short_governance: 'Governance',

    // Actions & Tiers
    tier1_hold: 'Tier 1 Hold',
    tier2_review: 'Tier 2 Review',
    tier3_clear: 'Tier 3 Clear',
    btn_signoff: 'Sign Off Case',
    btn_export_goaml: 'Export BFIU goAML XML',
    btn_export_json: 'Export Docket JSON',
    btn_print_dossier: 'Print Formal Case Dossier',
    btn_reveal_pii: 'Reveal PII',
    btn_mask_pii: 'Mask PII',
    btn_verify_chain: 'Verify Cryptographic Chain',
    btn_tamper_test: 'Simulate Tamper Test',
    btn_restore_chain: 'Restore Chain Integrity',
    btn_request_demo: 'Request Institutional Demo',
    btn_launch_app: 'Launch Banking OS',
    btn_explore_demo: 'Explore Live Demo',

    // General Labels
    app_title: 'Intelligent-AML Enterprise Banking OS',
    statutory_mandate: 'BFIU MLPA 2012 Compliance Mandate',
    ctr_ceiling: 'CTR Ceiling: ৳1,000,000 BDT',
    structuring_band: 'Structuring Band: ৳800k - ৳999k BDT',
    bb_rate: 'BB Reference Rate: 120.00 BDT/USD',
    maker_checker: 'Maker-Checker Dual Control',
    audit_worm: 'Tamper-Evident Ed25519 WORM',
    search_placeholder: 'Search alerts (ALT-994821), accounts (BD22...), cases...',

    // Landing Page
    landing_badge: 'TIER-1 AIR-GAP READY ANTI-MONEY LAUNDERING OS',
    landing_headline: 'Eliminate 84% of False Positives with Provable Conformal Risk Guarantees.',
    landing_subheadline: 'Engineered for Central Banks, Commercial Institutions, and MFS Providers. Combining Continuous Spatio-Temporal Graph Boosting (C-STGB) with finite-sample statistical false alarm control under Bangladesh Bank & BFIU regimes.',
    landing_stat_f1: '94.5% Macro F1 Score',
    landing_stat_noise: '84.2% Operational Noise Reduction',
    landing_stat_latency: '< 200 µs Autonomous Clearance',
    landing_stat_coverage: '99.04% Calibrated Coverage (1 - α)',
    
    // Conformal Tiering
    conformal_title: 'Automated 3-Tier Inductive Conformal Architecture',
    conformal_desc: 'Unlike black-box neural networks, our system outputs calibrated prediction sets with finite-sample statistical guarantees.',
    tier1_desc: 'Immediate automated freeze for high-risk topological subgraphs and confirmed watchlist matches.',
    tier2_desc: 'Statistically calibrated human review queue. Prioritized for senior analysts with Shapley invariant explanations.',
    tier3_desc: 'Autonomous microsecond clearance for routine, provably benign transactions without human delay.',

    // Security & Compliance
    security_title: 'Institutional Security & Regulatory Soundness',
    security_badge: 'OWASP ASVS LEVEL 2 ALIGNED',
    security_point1: 'Ed25519-Signed Tamper-Evident WORM Ledger',
    security_point2: 'Mandatory Server-Side Dual Control (Maker-Checker)',
    security_point3: 'Server-Side PII Masking with Audited 60s Reveal Gate',
    security_point4: 'UNODC goAML v4.2 XML Schema & BFIU Master Circular 26',

    // Pricing
    pricing_title: 'Transparent Institutional Deployment Models',
    plan_starter: 'Institutional Evaluation Sandbox',
    plan_bank: 'Tier-1 Bank On-Premises',
    plan_fiu: 'National FIU / Central Bank',

    // Print Dossier
    dossier_confidential: 'CONFIDENTIAL // LAW ENFORCEMENT & REGULATORY SUBMISSION',
    dossier_subtitle: 'OFFICIAL INVESTIGATION DOSSIER — BANGLADESH FINANCIAL INTELLIGENCE UNIT (BFIU)',
    dossier_statutory_cert: 'Admissibility-ready under Sections 65A–65B & 73A of the Evidence Act 1872 (Amended 2022) with responsible officer certificate.'
  },
  bn: {
    // Navigation Modules
    nav_overview: '১. নির্বাহী নজরদারি',
    nav_triage: '২. সতর্কতা বাছাই',
    nav_screening: '৩. নিষেধাজ্ঞা ও পিইপি বাছাই',
    nav_customers: '৪. গ্রাহক ৩৬০° কেওয়াইসি',
    nav_cases: '৫. প্রাতিষ্ঠানিক মামলা',
    nav_graph: '৬. আর্থিক লেনদেন প্রবাহ',
    nav_tbml: '৭. বাণিজ্যভিত্তিক অর্থপাচার',
    nav_sar: '৮. এসটিআর ও সিটিআর ডকেট',
    nav_rfi: '৯. তথ্যের অনুরোধ (আরএফআই)',
    nav_rules: '১০. নীতি ও পাল্টা ব্যবস্থা',
    nav_governance: '১১. মডেল গভর্নেন্স ও অডিট লেজার',

    // Short Labels
    short_overview: 'নজরদারি',
    short_triage: 'বাছাই',
    short_screening: 'স্ক্রিনিং',
    short_customers: 'গ্রাহক',
    short_cases: 'মামলা',
    short_graph: 'প্রবাহ গ্রাফ',
    short_tbml: 'বাণিজ্য এএমএল',
    short_sar: 'এসটিআর/সিটিআর',
    short_rfi: 'আরএফআই',
    short_rules: 'নীতিমালা',
    short_governance: 'গভর্নেন্স',

    // Actions & Tiers
    tier1_hold: 'স্তর ১ স্থগিত',
    tier2_review: 'স্তর ২ পর্যালোচনা',
    tier3_clear: 'স্তর ৩ ছাড়',
    btn_signoff: 'মামলা অনুমোদন করুন',
    btn_export_goaml: 'বিএফআইইউ গো-এএমএল এক্সএমএল',
    btn_export_json: 'ডকেট জেএসওএন রপ্তানি',
    btn_print_dossier: 'প্রাতিষ্ঠানিক ডজিয়ার প্রিন্ট',
    btn_reveal_pii: 'তথ্য উন্মোচন',
    btn_mask_pii: 'তথ্য গোপন',
    btn_verify_chain: 'অডিট চেইন যাচাই',
    btn_tamper_test: 'টেম্পার টেস্ট সিমুলেশন',
    btn_restore_chain: 'চেইন পুনঃস্থাপন',
    btn_request_demo: 'প্রাতিষ্ঠানিক ডেমো অনুরোধ',
    btn_launch_app: 'ব্যাংকিং ওএস চালু করুন',
    btn_explore_demo: 'সরাসরি ডেমো দেখুন',

    // General Labels
    app_title: 'ইন্টেলিজেন্ট-এএমএল প্রাতিষ্ঠানিক ব্যাংকিং ওএস',
    statutory_mandate: 'বিএফআইইউ এমএলপিএ ২০১২ আইনগত বিধান',
    ctr_ceiling: 'সিটিআর সীমা: ৳১০,০০,০০০ টাকা',
    structuring_band: 'কাঠামোবদ্ধ লেনদেন সীমা: ৳৮ লক্ষ - ৳৯.৯৯ লক্ষ',
    bb_rate: 'বাংলাদেশ ব্যাংক রেফারেন্স রেট: ১২০.০০ টাকা/ডলার',
    maker_checker: 'মেকার-চেকার দ্বৈত নিয়ন্ত্রণ',
    audit_worm: 'ট্যাম্পার-প্রুফ Ed25519 অডিট লেজার',
    search_placeholder: 'সতর্কতা (ALT-994821), হিসাব নং (BD22...), মামলা খুঁজুন...',

    // Landing Page
    landing_badge: 'টিয়ার-১ এয়ার-গ্যাপ সমর্থিত অ্যান্টি-মানি লন্ডারিং ওএস',
    landing_headline: 'প্রমাণযোগ্য কনফরমাল রিস্ক কন্ট্রোল দ্বারা ৮৪% অপ্রয়োজনীয় সতর্কতা হ্রাস করুন।',
    landing_subheadline: 'কেন্দ্রীয় ব্যাংক, বাণিজ্যিক আর্থিক প্রতিষ্ঠান এবং এমএফএস সেবাদাতাদের জন্য বিশেষভাবে নির্মিত। অবিচ্ছিন্ন স্প্যাশিও-টেম্পোরাল গ্রাফ বুস্টিং (C-STGB) ও বাংলাদেশ ব্যাংক ও বিএফআইইউ বিধিমালা সমর্থিত।',
    landing_stat_f1: '৯৪.৫% ম্যাক্রো এফ১ স্কোর',
    landing_stat_noise: '৮৪.২% অপ্রয়োজনীয় সতর্কতা হ্রাস',
    landing_stat_latency: '< ২০০ মাইক্রোসেকেন্ড স্বয়ংক্রিয় ছাড়',
    landing_stat_coverage: '৯৯.০৪% ক্যালিব্রেটেড নির্ভুলতা (১ - α)',

    // Conformal Tiering
    conformal_title: 'স্বয়ংক্রিয় ৩-স্তরবিশিষ্ট ইনডাক্টিভ কনফরমাল আর্কিটেকচার',
    conformal_desc: 'অস্পষ্ট ব্ল্যাক-বক্স মডেলের পরিবর্তে আমাদের সিস্টেম গাণিতিকভাবে প্রমাণিত নির্ভুলতার সাথে ফলাফল প্রদান করে।',
    tier1_desc: 'উচ্চ-ঝুঁকিপূর্ণ নোড ও স্যাংশন তালিকার জন্য তাৎক্ষণিক স্বয়ংক্রিয় স্থগিতাদেশ।',
    tier2_desc: 'গাণিতিকভাবে ক্যালিব্রেটেড বিশ্লেষক পর্যালোচনা। শ্যাপলে ব্যাখ্যার সাথে অগ্রাধিকারপ্রাপ্ত কিউ।',
    tier3_desc: 'সাধারণ ও নিরাপদ লেনদেনের জন্য মাইক্রোসেকেন্ডে স্বয়ংক্রিয় ছাড়।',

    // Security & Compliance
    security_title: 'প্রাতিষ্ঠানিক নিরাপত্তা ও আইনগত পরিপালন',
    security_badge: 'ওওয়াস্প এএসভিএস লেভেল ২ মানসম্পন্ন',
    security_point1: 'Ed25519 স্বাক্ষরিত ট্যাম্পার-প্রুফ অডিট লেজার',
    security_point2: 'বাধ্যতামূলক সার্ভার-সাইড মেকার-চেকার নিয়ন্ত্রণ',
    security_point3: '৬০-সেকেন্ড মেয়াদি নিরীক্ষিত গ্রাহক তথ্য উন্মোচন গেইট',
    security_point4: 'ইউএনওডিসি গো-এএমএল ৪.২ এক্সএমএল ও বিএফআইইউ মাস্টার সার্কুলার ২৬',

    // Pricing
    pricing_title: 'স্বচ্ছ প্রাতিষ্ঠানিক ডেপ্লয়মেন্ট মডেল',
    plan_starter: 'প্রাতিষ্ঠানিক মূল্যায়ন স্যান্ডবক্স',
    plan_bank: 'টিয়ার-১ ব্যাংক অন-প্রিমিসেস',
    plan_fiu: 'জাতীয় এফআইইউ / কেন্দ্রীয় ব্যাংক',

    // Print Dossier
    dossier_confidential: 'গোপনীয় // আইন প্রয়োগকারী ও নিয়ন্ত্রক সংস্থার ব্যবহারের জন্য',
    dossier_subtitle: 'অফিসিয়াল তদন্ত ডজিয়ার — বাংলাদেশ ফিন্যান্সিয়াল ইন্টেলিজেন্স ইউনিট (বিএফআইইউ)',
    dossier_statutory_cert: 'সাক্ষ্য আইন ১৮৭২ (সংশোধিত ২০২২) এর ধারা ৬৫বি অনুযায়ী প্রত্যয়িত। ট্যাম্পার-প্রুফ লেজার হতে সংরক্ষিত।'
  }
};
