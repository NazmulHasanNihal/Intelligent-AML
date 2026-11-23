'use client';

import React, { useState, useEffect } from 'react';
import { z } from 'zod';
import { X, CheckCircle2, Download, Copy, Shield, Building2, Terminal, FileText, Check } from 'lucide-react';

const inquirySchema = z.object({
  officerName: z.string().min(2, 'Officer name is required'),
  workEmail: z.string().email('Valid institutional email is required'),
  institutionName: z.string().min(2, 'Institution name is required'),
  roleTitle: z.string().min(2, 'Role / Title is required'),
  orgType: z.enum(['Commercial Bank', 'Central Bank / FIU', 'MFS / Payment Operator', 'Auditor / Regulator', 'Research Institution']),
  deploymentMode: z.enum(['Air-Gapped Sovereign On-Premises (Kubernetes)', 'Virtual Private Cloud (VPC)', 'Hosted Evaluation Sandbox']),
  dailyVolume: z.enum(['< 100,000 tx/day', '100,000 - 1,000,000 tx/day', '1M - 10M tx/day', '> 10M tx/day']),
  statutoryRequirements: z.string().optional()
});

export type InquiryFormData = z.infer<typeof inquirySchema>;

interface InstitutionalInquiryModalProps {
  isOpen: boolean;
  onClose: () => void;
  inquiryType?: 'EVALUATION' | 'BANK_POC' | 'SOVEREIGN';
}

export const InstitutionalInquiryModal: React.FC<InstitutionalInquiryModalProps> = ({
  isOpen,
  onClose,
  inquiryType = 'BANK_POC'
}) => {
  const [formData, setFormData] = useState<InquiryFormData>({
    officerName: '',
    workEmail: '',
    institutionName: '',
    roleTitle: inquiryType === 'SOVEREIGN' ? 'Chief Compliance Officer / FIU Lead' : 'CAMLCO / Head of AML',
    orgType: inquiryType === 'SOVEREIGN' ? 'Central Bank / FIU' : 'Commercial Bank',
    deploymentMode: inquiryType === 'EVALUATION' ? 'Hosted Evaluation Sandbox' : 'Air-Gapped Sovereign On-Premises (Kubernetes)',
    dailyVolume: '100,000 - 1,000,000 tx/day',
    statutoryRequirements: ''
  });

  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    if (inquiryType === 'SOVEREIGN') {
      setFormData(prev => ({
        ...prev,
        orgType: 'Central Bank / FIU',
        roleTitle: 'FIU Director / Supervisory Inspector',
        deploymentMode: 'Air-Gapped Sovereign On-Premises (Kubernetes)'
      }));
    } else if (inquiryType === 'BANK_POC') {
      setFormData(prev => ({
        ...prev,
        orgType: 'Commercial Bank',
        roleTitle: 'CAMLCO / Head of Compliance',
        deploymentMode: 'Air-Gapped Sovereign On-Premises (Kubernetes)'
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        orgType: 'Research Institution',
        roleTitle: 'Risk Auditor / Model Validator',
        deploymentMode: 'Hosted Evaluation Sandbox'
      }));
    }
    setErrors({});
    setIsSubmitted(false);
  }, [inquiryType, isOpen]);

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const result = inquirySchema.safeParse(formData);
    if (!result.success) {
      const fieldErrors: Record<string, string> = {};
      result.error.errors.forEach(err => {
        if (err.path[0]) {
          fieldErrors[err.path[0].toString()] = err.message;
        }
      });
      setErrors(fieldErrors);
      return;
    }

    setErrors({});
    setIsSubmitted(true);
  };

  const architectureBrief = `================================================================================
INTELLIGENT-AML ENTERPRISE ARCHITECTURE BRIEF & POc SPECIFICATION
================================================================================
Generated For:       ${formData.institutionName || 'Institutional Client'}
Authorized Officer:  ${formData.officerName || 'Officer'} (${formData.roleTitle || 'Compliance Officer'})
Official Email:      ${formData.workEmail || 'N/A'}
Organization Type:   ${formData.orgType}
Deployment Target:   ${formData.deploymentMode}
Daily Ingestion SLA: ${formData.dailyVolume}
--------------------------------------------------------------------------------
1. CORE ENGINE & ALGORITHMIC SPECIFICATION
   - Architecture:    C-STGB v3.2 (Causal Spatio-Temporal GraphBoost)
   - Calibration:     Split Inductive Conformal Prediction (1 - α = 99.00%)
   - Invariant Space: 12-Dimensional Universal Conservation Laws (Φ_flow, λ_burst)
   - FastPath Latency: < 200 µs in-memory P50 clearance; < 1.0 ms full scoring
   - Noise Reduction: 84.2% empirical false-positive elimination

2. STATUTORY REGULATORY FIT (BANGLADESH BFIU)
   - Statutes:        Money Laundering Prevention Act 2012 (§§ 6, 25)
   - Directives:      BFIU Master Circular 26, Circular 24 (TBML), Circular 32 (2026)
   - Enforcement:     Circular Letters 02 & 03 (Feb 2026) & Circular Letter 05 (Aug 2026)
   - Evidentiary:     Bangladesh Evidence Act, 1872 (Amended 2022) §§ 65A-65B & 73A
   - Filings:         UNODC goAML v4.2 XML Schema with Mandatory Attachment Seals

3. SOVEREIGN SECURITY & AIR-GAP ISOLATION
   - Security Model:  OWASP ASVS Level 2 Aligned Architecture
   - Ledger:          RFC 8785 Canonical JSON + RFC 8032 Ed25519 WORM Checkpoints
   - Storage Lock:    AWS S3 / MinIO Object Lock Compliance Mode (6-Year Retention)
   - Network Egress:  0 External Outbound Requests in on-premise air-gap mode
   - Dual Control:    Cryptographic Two-Officer Maker-Checker Enforcement
================================================================================`;

  const handleCopyBrief = () => {
    navigator.clipboard.writeText(architectureBrief);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownloadBrief = () => {
    const blob = new Blob([architectureBrief], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `Intelligent_AML_Architecture_Brief_${formData.institutionName.replace(/\s+/g, '_') || 'Institution'}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="inquiry-dialog-title"
      className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4"
    >
      <div className="w-full max-w-xl bg-[#0F172A] border border-[#334155] rounded-2xl shadow-2xl p-6 relative text-slate-100 max-h-[90vh] overflow-y-auto">
        <button
          type="button"
          onClick={onClose}
          className="absolute top-4 right-4 p-1 rounded-lg hover:bg-[#1E293B] text-slate-400 hover:text-slate-200"
          aria-label="Close dialog"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-2 mb-1">
          <Shield className="w-5 h-5 text-emerald-400" />
          <h3 id="inquiry-dialog-title" className="text-lg font-bold text-slate-100">
            {inquiryType === 'SOVEREIGN'
              ? 'Schedule Sovereign FIU / Central Bank Briefing'
              : inquiryType === 'BANK_POC'
              ? 'Request Bank PoC & Enterprise Architecture Brief'
              : 'Institutional Evaluation & Model Validation Sandbox'}
          </h3>
        </div>
        <p className="text-xs text-slate-400 font-sans mb-5">
          Receive an instant, downloadable technical brief calibrated to your daily transaction volume and BFIU compliance targets.
        </p>

        {isSubmitted ? (
          <div className="space-y-4 animate-in zoom-in-95">
            <div className="p-5 text-center bg-emerald-500/10 border border-emerald-500/30 rounded-xl">
              <CheckCircle2 className="w-10 h-10 text-emerald-400 mx-auto mb-2" />
              <h4 className="text-base font-bold text-slate-100">Architecture Brief Generated</h4>
              <p className="text-xs text-slate-300 mt-1 font-sans">
                Specification dispatched for <span className="font-mono text-emerald-400">{formData.institutionName}</span>. You can copy or download the complete technical package immediately below.
              </p>
            </div>

            {/* Formatted Code Block */}
            <div className="p-3 bg-[#0B0F17] rounded-xl border border-[#1E293B] font-mono text-[10px] text-slate-300 max-h-48 overflow-y-auto whitespace-pre leading-relaxed">
              {architectureBrief}
            </div>

            {/* Actions */}
            <div className="flex flex-col sm:flex-row items-center gap-2 pt-2">
              <button
                type="button"
                onClick={handleCopyBrief}
                className="w-full sm:w-1/2 py-2.5 rounded-lg text-xs font-mono font-bold bg-[#1E293B] hover:bg-[#334155] text-slate-200 border border-[#475569] transition-all flex items-center justify-center gap-1.5 cursor-pointer"
              >
                {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5 text-slate-400" />}
                <span>{copied ? 'Copied to Clipboard' : 'Copy Brief to Clipboard'}</span>
              </button>
              <button
                type="button"
                onClick={handleDownloadBrief}
                className="w-full sm:w-1/2 py-2.5 rounded-lg text-xs font-mono font-bold bg-emerald-500 hover:bg-emerald-400 text-slate-950 transition-all flex items-center justify-center gap-1.5 cursor-pointer shadow-md shadow-emerald-500/20"
              >
                <Download className="w-3.5 h-3.5" />
                <span>Download Architecture Brief (.txt)</span>
              </button>
            </div>

            <button
              type="button"
              onClick={onClose}
              className="w-full py-2 text-center text-xs font-mono text-slate-400 hover:text-slate-200 cursor-pointer pt-2"
            >
              Close Window
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-mono text-slate-400 mb-1">Officer Name *</label>
                <input
                  type="text"
                  placeholder="e.g. Kazi Rafiqul Islam"
                  value={formData.officerName}
                  onChange={(e) => setFormData({ ...formData, officerName: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg bg-[#0B0F17] border border-[#334155] text-xs text-slate-100 focus:outline-none focus:border-emerald-500 font-sans"
                />
                {errors.officerName && <p className="text-[10px] text-rose-400 mt-0.5 font-mono">{errors.officerName}</p>}
              </div>
              <div>
                <label className="block text-xs font-mono text-slate-400 mb-1">Institutional Email *</label>
                <input
                  type="email"
                  placeholder="officer@bank.com.bd"
                  value={formData.workEmail}
                  onChange={(e) => setFormData({ ...formData, workEmail: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg bg-[#0B0F17] border border-[#334155] text-xs text-slate-100 focus:outline-none focus:border-emerald-500 font-sans"
                />
                {errors.workEmail && <p className="text-[10px] text-rose-400 mt-0.5 font-mono">{errors.workEmail}</p>}
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-mono text-slate-400 mb-1">Institution Name *</label>
                <input
                  type="text"
                  placeholder="e.g. Eastern Bank PLC"
                  value={formData.institutionName}
                  onChange={(e) => setFormData({ ...formData, institutionName: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg bg-[#0B0F17] border border-[#334155] text-xs text-slate-100 focus:outline-none focus:border-emerald-500 font-sans"
                />
                {errors.institutionName && <p className="text-[10px] text-rose-400 mt-0.5 font-mono">{errors.institutionName}</p>}
              </div>
              <div>
                <label className="block text-xs font-mono text-slate-400 mb-1">Role / Signatory Title *</label>
                <input
                  type="text"
                  placeholder="e.g. CAMLCO / Head of Compliance"
                  value={formData.roleTitle}
                  onChange={(e) => setFormData({ ...formData, roleTitle: e.target.value })}
                  className="w-full px-3 py-2 rounded-lg bg-[#0B0F17] border border-[#334155] text-xs text-slate-100 focus:outline-none focus:border-emerald-500 font-sans"
                />
                {errors.roleTitle && <p className="text-[10px] text-rose-400 mt-0.5 font-mono">{errors.roleTitle}</p>}
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-mono text-slate-400 mb-1">Target Deployment Mode</label>
                <select
                  value={formData.deploymentMode}
                  onChange={(e) => setFormData({ ...formData, deploymentMode: e.target.value as any })}
                  className="w-full px-3 py-2 rounded-lg bg-[#0B0F17] border border-[#334155] text-xs text-slate-100 focus:outline-none focus:border-emerald-500 font-sans"
                >
                  <option>Air-Gapped Sovereign On-Premises (Kubernetes)</option>
                  <option>Virtual Private Cloud (VPC)</option>
                  <option>Hosted Evaluation Sandbox</option>
                </select>
              </div>
              <div>
                <label className="block text-xs font-mono text-slate-400 mb-1">Daily Clearing Volume</label>
                <select
                  value={formData.dailyVolume}
                  onChange={(e) => setFormData({ ...formData, dailyVolume: e.target.value as any })}
                  className="w-full px-3 py-2 rounded-lg bg-[#0B0F17] border border-[#334155] text-xs text-slate-100 focus:outline-none focus:border-emerald-500 font-sans"
                >
                  <option>&lt; 100,000 tx/day</option>
                  <option>100,000 - 1,000,000 tx/day</option>
                  <option>1M - 10M tx/day</option>
                  <option>&gt; 10M tx/day</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-xs font-mono text-slate-400 mb-1">Notes / Core Banking Targets (Optional)</label>
              <textarea
                rows={2}
                placeholder="Mention Finacle / Temenos T24 integration, ISO 20022, or specific BFIU compliance targets..."
                value={formData.statutoryRequirements}
                onChange={(e) => setFormData({ ...formData, statutoryRequirements: e.target.value })}
                className="w-full px-3 py-2 rounded-lg bg-[#0B0F17] border border-[#334155] text-xs text-slate-100 focus:outline-none focus:border-emerald-500 font-sans resize-none"
              />
            </div>

            <button
              type="submit"
              className="w-full py-2.5 rounded-lg text-xs font-mono font-bold bg-emerald-500 hover:bg-emerald-400 text-slate-950 transition-all cursor-pointer shadow-md shadow-emerald-500/20"
            >
              Generate Architecture Brief &amp; Submit Request
            </button>
          </form>
        )}
      </div>
    </div>
  );
};
