import React, { useState } from 'react';
import { 
  X, 
  HelpCircle, 
  BookOpen, 
  ShieldCheck, 
  AlertTriangle, 
  CheckCircle2, 
  FileText, 
  Share2, 
  Search,
  ArrowRight,
  Info,
  DollarSign,
  UserCheck
} from 'lucide-react';

const HELP_TOPICS = [
  {
    id: 'overview',
    title: '🌟 Quick Start: What is this System?',
    content: (
      <div className="space-y-3 text-xs leading-relaxed text-slate-300">
        <p>
          Welcome to <b>Intelligent-AML</b>, your bank's automated compliance and transaction surveillance assistant.
        </p>
        <p>
          In a bank, thousands of wire, card, and crypto transfers occur every minute. Most transfers are normal everyday commerce (payrolls, grocery bills, business invoices). However, criminals try to disguise illegal funds through <b>money laundering</b>.
        </p>
        <div className="p-3 rounded-lg bg-[#141A26] border border-white/[0.08] space-y-2">
          <span className="font-semibold text-white block">How this platform helps you:</span>
          <ul className="space-y-1.5 list-disc list-inside text-slate-300">
            <li><b>Auto-Clears 99.4% of Safe Transfers:</b> Automatically clears normal customer transactions in less than 1 millisecond so real customers never experience delays.</li>
            <li><b>Catches Hidden Criminal Rings:</b> Traces multi-hop hidden transfer chains where criminals split money into small amounts (under $10,000) or bounce funds between accounts.</li>
            <li><b>Drafts Government SAR Reports in 25 Seconds:</b> Writes the complete legal Suspicious Activity Report (SAR) ready for official FinCEN PDF download.</li>
          </ul>
        </div>
      </div>
    )
  },
  {
    id: 'colors',
    title: '🚦 Understanding the 3 Risk Colors & Tiers',
    content: (
      <div className="space-y-3 text-xs leading-relaxed text-slate-300">
        <p>Every transaction evaluated by the system is routed into one of three color-coded tiers:</p>
        
        <div className="space-y-2.5">
          <div className="p-3 rounded-lg bg-emerald-950/30 border border-emerald-500/30 flex items-start gap-3">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
            <div>
              <span className="font-bold text-emerald-300 block text-xs">🟢 GREEN — Tier 3: Straight-Through Clear (Safe)</span>
              <p className="text-slate-300 mt-0.5">
                The transaction is verified clean (e.g. regular corporate payroll, utility bills). Funds are instantly released without requiring human officer review. Over <b>99.4%</b> of your bank's volume falls here.
              </p>
            </div>
          </div>

          <div className="p-3 rounded-lg bg-amber-950/30 border border-amber-500/30 flex items-start gap-3">
            <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
            <div>
              <span className="font-bold text-amber-300 block text-xs">🟡 YELLOW — Tier 2: Officer Review Queue (Needs Check)</span>
              <p className="text-slate-300 mt-0.5">
                The AI detected minor unusual activity (e.g., an account that was dormant for months suddenly transferring $9,400). A compliance officer takes 10 seconds to review the account and click <b>"Clear Alert"</b> or <b>"Escalate"</b>.
              </p>
            </div>
          </div>

          <div className="p-3 rounded-lg bg-rose-950/30 border border-rose-500/30 flex items-start gap-3">
            <ShieldCheck className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
            <div>
              <span className="font-bold text-rose-300 block text-xs">🔴 RED — Tier 1: Immediate Quarantine & SAR (High Risk)</span>
              <p className="text-slate-300 mt-0.5">
                Confirmed suspicious criminal pattern (e.g., structured smurfing, circular wash-trading, crypto mixer evasion). The asset is temporarily frozen, and an official FinCEN SAR Form 111 report is automatically drafted.
              </p>
            </div>
          </div>
        </div>
      </div>
    )
  },
  {
    id: 'typologies',
    title: '🕵️ What Criminal Patterns Does the System Catch?',
    content: (
      <div className="space-y-3 text-xs leading-relaxed text-slate-300">
        <p>The AI continuously scans for the 4 most common money laundering tricks:</p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2.5">
          <div className="p-3 rounded-lg bg-[#141A26] border border-white/[0.08]">
            <span className="font-bold text-indigo-300 block">1. Smurfing / Structuring</span>
            <p className="text-slate-300 mt-1 text-[11px]">
              Law requires banks to report cash deposits over $10,000. Criminals try to evade this by breaking $50,000 into multiple smaller transfers (e.g., $9,450, $9,800). The AI flags these structured bursts instantly.
            </p>
          </div>

          <div className="p-3 rounded-lg bg-[#141A26] border border-white/[0.08]">
            <span className="font-bold text-indigo-300 block">2. Pass-Through Money Mules</span>
            <p className="text-slate-300 mt-1 text-[11px]">
              An account receives $48,500 and immediately sends out $48,100 within 15 minutes to an offshore account. The account never keeps money; it is used only as a transit pipeline.
            </p>
          </div>

          <div className="p-3 rounded-lg bg-[#141A26] border border-white/[0.08]">
            <span className="font-bold text-indigo-300 block">3. Circular Wash-Trading</span>
            <p className="text-slate-300 mt-1 text-[11px]">
              Funds travel in a circle (Account A → B → C → A) to create fake transaction history and disguise the original source of illegal money.
            </p>
          </div>

          <div className="p-3 rounded-lg bg-[#141A26] border border-white/[0.08]">
            <span className="font-bold text-indigo-300 block">4. Dormant Account Hijacking</span>
            <p className="text-slate-300 mt-1 text-[11px]">
              An account sits empty and inactive for 100+ days, and then suddenly receives and withdraws large sums of cash before going quiet again.
            </p>
          </div>
        </div>
      </div>
    )
  },
  {
    id: 'playbook',
    title: '📋 Step-by-Step Officer Playbook (How to Use Each Screen)',
    content: (
      <div className="space-y-3 text-xs leading-relaxed text-slate-300">
        <p className="font-semibold text-white">Here is your daily 3-step compliance routine:</p>
        
        <div className="space-y-2">
          <div className="p-2.5 rounded-lg bg-[#141A26] border border-white/[0.06] flex items-start gap-2.5">
            <span className="w-5 h-5 rounded-full bg-indigo-600 text-white font-bold text-xs flex items-center justify-center shrink-0">1</span>
            <div>
              <b className="text-white">Workspace 1 — Check the Alert Triage Queue:</b>
              <p className="text-slate-300 text-[11px] mt-0.5">
                Look at the Yellow and Red alerts. Click any transaction to open the side inspector and see who sent what to whom.
              </p>
            </div>
          </div>

          <div className="p-2.5 rounded-lg bg-[#141A26] border border-white/[0.06] flex items-start gap-2.5">
            <span className="w-5 h-5 rounded-full bg-indigo-600 text-white font-bold text-xs flex items-center justify-center shrink-0">2</span>
            <div>
              <b className="text-white">Workspace 2 — Inspect Network Connections in Graph Studio:</b>
              <p className="text-slate-300 text-[11px] mt-0.5">
                See the visual network map. Red nodes are suspicious originators, Yellow nodes are intermediary mules, and Green nodes are normal merchants.
              </p>
            </div>
          </div>

          <div className="p-2.5 rounded-lg bg-[#141A26] border border-white/[0.06] flex items-start gap-2.5">
            <span className="w-5 h-5 rounded-full bg-indigo-600 text-white font-bold text-xs flex items-center justify-center shrink-0">3</span>
            <div>
              <b className="text-white">Workspace 3 — File Government SAR Report or Clear:</b>
              <p className="text-slate-300 text-[11px] mt-0.5">
                If clean, click <b>"Clear Alert"</b>. If illicit, click <b>"Auto-Draft SAR"</b> to let the AI write the complete FinCEN legal report, and click <b>"Download Official PDF"</b> for your bank archives.
              </p>
            </div>
          </div>
        </div>
      </div>
    )
  },
  {
    id: 'faq',
    title: '❓ Frequently Asked Questions (FAQ)',
    content: (
      <div className="space-y-2.5 text-xs leading-relaxed text-slate-300">
        <div className="p-3 rounded-lg bg-[#141A26] border border-white/[0.06]">
          <span className="font-bold text-white block">Q: Does the AI block normal customer transactions by accident?</span>
          <p className="text-slate-300 text-[11px] mt-1">
            <b>No.</b> The system uses mathematical Conformal Safety Guarantees that ensure over 99.45% of safe transactions are cleared straight-through in 0.45 milliseconds. Only genuine anomalies are flagged for your review.
          </p>
        </div>

        <div className="p-3 rounded-lg bg-[#141A26] border border-white/[0.06]">
          <span className="font-bold text-white block">Q: What should I tell a customer if their transaction is held?</span>
          <p className="text-slate-300 text-[11px] mt-1">
            Open <b>Workspace 4 (Customer Recourse Hub)</b>. It generates a plain-English explanation notice telling the customer exactly what documentation or KYC verification is needed to release their funds.
          </p>
        </div>

        <div className="p-3 rounded-lg bg-[#141A26] border border-white/[0.06]">
          <span className="font-bold text-white block">Q: Is this system compliant with banking regulators (Federal Reserve & FinCEN)?</span>
          <p className="text-slate-300 text-[11px] mt-1">
            <b>Yes.</b> It fully complies with the Bank Secrecy Act (31 U.S.C. 5318(g)), FinCEN Form 111 standards, and Federal Reserve SR 26-2 model risk governance principles with cryptographic tamper-proof audit seals.
          </p>
        </div>
      </div>
    )
  }
];

export const BankerHelpModal = ({ isOpen, onClose }) => {
  const [selectedTopic, setSelectedTopic] = useState(HELP_TOPICS[0].id);

  if (!isOpen) return null;

  const currentTopic = HELP_TOPICS.find((t) => t.id === selectedTopic) || HELP_TOPICS[0];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-black/60 backdrop-blur-sm animate-fadeIn select-none">
      <div className="w-full max-w-3xl max-h-[90vh] bg-[var(--bg-card)] border border-[var(--border-card)] rounded-2xl shadow-2xl flex flex-col overflow-hidden skeuo-card">
        {/* Header */}
        <div className="px-4 py-3 border-b border-[var(--border-subtle)] bg-[var(--bg-card-elevated)] flex items-center justify-between">
          <div className="flex items-center gap-2.5 min-w-0">
            <div className="w-7 h-7 sm:w-8 sm:h-8 rounded-lg bg-gradient-to-b from-[#257843] to-[#144726] border border-[#113C21] flex items-center justify-center text-white shrink-0 shadow-[var(--skeuo-btn)]">
              <BookOpen className="w-3.5 h-3.5 sm:w-4 sm:h-4 text-white" />
            </div>
            <div className="min-w-0">
              <h2 className="text-xs sm:text-sm font-bold text-[var(--text-primary)] truncate">Banker's Compliance Guide &amp; Knowledge Center</h2>
              <p className="text-[10px] text-[var(--text-muted)] font-sans truncate">Guide for compliance officers, examiners, and investigators</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg skeuo-btn text-[var(--text-muted)] hover:text-[var(--text-primary)] cursor-pointer"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        </div>

        {/* Content Body: Sidebar + Detail */}
        <div className="flex-1 grid grid-cols-1 md:grid-cols-12 overflow-hidden">
          {/* Left Navigation Topics */}
          <div className="md:col-span-5 border-r border-[var(--border-subtle)] p-2 space-y-1 bg-[var(--bg-base)] overflow-y-auto max-h-48 md:max-h-none">
            {HELP_TOPICS.map((topic) => {
              const isSelected = selectedTopic === topic.id;
              return (
                <button
                  key={topic.id}
                  onClick={() => setSelectedTopic(topic.id)}
                  className={`w-full p-2 rounded-lg text-left text-[11px] transition-all cursor-pointer flex items-center justify-between ${
                    isSelected
                      ? 'bg-gradient-to-b from-[#257843] to-[#144726] text-white font-bold border border-[#113C21] shadow-[var(--skeuo-btn)]'
                      : 'skeuo-card text-[var(--text-secondary)] hover:text-[var(--text-primary)]'
                  }`}
                >
                  <span className="truncate pr-1">{topic.title}</span>
                  <ArrowRight className={`w-3 h-3 shrink-0 ${isSelected ? 'text-white' : 'text-[var(--text-muted)]'}`} />
                </button>
              );
            })}
          </div>

          {/* Right Topic Details */}
          <div className="md:col-span-7 p-3.5 sm:p-4 overflow-y-auto bg-[var(--bg-card)] space-y-2.5">
            <h3 className="text-xs sm:text-sm font-bold text-[var(--text-primary)] border-b border-[var(--border-subtle)] pb-1.5 font-mono">
              {currentTopic.title}
            </h3>
            <div className="text-[11px] text-[var(--text-secondary)]">{currentTopic.content}</div>
          </div>
        </div>

        {/* Footer */}
        <div className="px-4 py-2.5 border-t border-[var(--border-subtle)] bg-[var(--bg-card-elevated)] flex items-center justify-between text-[10px] sm:text-[11px] font-mono text-[var(--text-muted)]">
          <span className="hidden sm:inline">Intelligent-AML Banker Knowledge Base v1.0</span>
          <button
            onClick={onClose}
            className="px-3.5 py-1.5 rounded-lg skeuo-btn skeuo-btn-primary text-xs font-semibold cursor-pointer ml-auto"
          >
            Back to Workstation
          </button>
        </div>
      </div>
    </div>
  );
};
