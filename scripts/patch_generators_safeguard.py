import re
from pathlib import Path

# 1. Update scripts/generate_all_publication_figures.py for fig19
p1 = Path("scripts/generate_all_publication_figures.py")
c1 = p1.read_text(encoding="utf-8")

old_fig19_pattern = re.compile(r"# FIGURE 19: Class-Conditional CRC vs Marginal.*?save_all_formats\(fig, \"fig19_conformal_risk_mechanism\"\)", re.DOTALL)
new_fig19_code = """# FIGURE 19: Class-Conditional CRC vs Marginal Conformal (Double Column: Spacious 8.2" x 4.0")
print("[19/22] Generating Figure 19: Class-Conditional CRC vs Marginal Risk Mechanism (Upgraded)...")
from scripts.upgrade_user_target_figures import upgrade_fig19_conformal_risk_mechanism
upgrade_fig19_conformal_risk_mechanism()"""

c1, n1 = old_fig19_pattern.subn(new_fig19_code, c1)
p1.write_text(c1, encoding="utf-8")
print(f"Patched fig19 in generate_all_publication_figures.py: {n1} substitution(s)")

# 2. Update scripts/generate_final_10_of_10_figures.py for compliance funnel
p2 = Path("scripts/generate_final_10_of_10_figures.py")
c2 = p2.read_text(encoding="utf-8")

old_funnel_pattern = re.compile(r"14\. COMPLIANCE ALERT-VOLUME FUNNEL CHART.*?save_fig\(fig, \[\"fig_compliance_alert_funnel\", \"fig_compliance_funnel\"\]\)", re.DOTALL)
new_funnel_code = """14. COMPLIANCE ALERT-VOLUME FUNNEL CHART (Ch 5) (Upgraded)
print("14. COMPLIANCE ALERT-VOLUME FUNNEL CHART (Ch 5)...")
from scripts.upgrade_user_target_figures import upgrade_compliance_alert_funnel
upgrade_compliance_alert_funnel()"""

c2, n2 = old_funnel_pattern.subn(new_funnel_code, c2)
p2.write_text(c2, encoding="utf-8")
print(f"Patched compliance funnel in generate_final_10_of_10_figures.py: {n2} substitution(s)")

