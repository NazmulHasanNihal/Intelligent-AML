import React from 'react';
import { 
  X, 
  ChevronRight, 
  ChevronLeft, 
  Sparkles, 
  CheckCircle2, 
  ShieldCheck, 
  Inbox, 
  Share2, 
  FileText, 
  UserCheck, 
  BarChart3 
} from 'lucide-react';

const BANKER_STEPS = [
  {
    stepNumber: 1,
    targetTab: 'alerts',
    title: '1. Welcome to Your Daily Compliance Alert Queue',
    subtitle: 'Where all wire, card, and crypto transactions are screened in real-time',
    icon: Inbox,
    content: (
      <div className="space-y-2.5 text-xs text-slate-300">
        <p>
          This is your primary morning workstation. Over <b>99.45% of safe customer transfers</b> (corporate payroll, shopping, vendor payments) are automatically cleared in <b>0.45 milliseconds</b>.
        </p>
        <div className="p-2.5 rounded-lg bg-[#0B0E17] border border-white/[0.06] space-y-1 font-mono text-[11px]">
          <div><b className="text-emerald-400">🟢 GREEN:</b> Auto-cleared instantly (Safe).</div>
          <div><b className="text-amber-400">🟡 YELLOW:</b> Placed in your review queue (Takes 10s to check).</div>
          <div><b className="text-rose-400">🔴 RED:</b> Critical flag, funds held, and ready for SAR filing.</div>
        </div>
      </div>
    ),
  },
  {
    stepNumber: 2,
    targetTab: 'alerts',
    title: '2. Inspecting an Account Dossier with 1 Click',
    subtitle: 'See the full story without digging through complex databases',
    icon: ShieldCheck,
    content: (
      <div className="space-y-2.5 text-xs text-slate-300">
        <p>
          Clicking any transaction in the list opens the <b>Slide-Over Dossier</b> on the right.
        </p>
        <p>
          It shows you the exact reason in plain English: e.g. <i>"Smurfing: splitting $9,450 into micro-bursts to avoid the $10,000 threshold"</i>. You can immediately click <b>"Clear Alert"</b> or <b>"Freeze &amp; File SAR"</b>.
        </p>
      </div>
    ),
  },
  {
    stepNumber: 3,
    targetTab: 'investigate',
    title: '3. Visual Network Tracing in Graph Studio',
    subtitle: 'See the hidden chain: who is sending money to whom',
    icon: Share2,
    content: (
      <div className="space-y-2.5 text-xs text-slate-300">
        <p>
          Money launderers hide by bouncing money across 4 or 5 intermediary accounts.
        </p>
        <p>
          The <b>Graph Studio</b> draws a live interactive map:
        </p>
        <ul className="list-disc list-inside space-y-1 text-slate-300 text-[11px]">
          <li><b>Red Nodes:</b> The original suspicious money source.</li>
          <li><b>Yellow Nodes:</b> Pass-through intermediary "money mules".</li>
          <li><b>Filter Slider:</b> Easily hide everyday grocery and retail purchases so only the criminal network remains visible.</li>
        </ul>
      </div>
    ),
  },
  {
    stepNumber: 4,
    targetTab: 'cases',
    title: '4. Autonomous Government SAR Filing (FinCEN Form 111)',
    subtitle: 'AI drafts complete legal reports in 25 seconds instead of 45 minutes',
    icon: FileText,
    content: (
      <div className="space-y-2.5 text-xs text-slate-300">
        <p>
          Under banking law (Bank Secrecy Act), suspicious activity must be reported to the government.
        </p>
        <p>
          Instead of spending 45 minutes manually typing a report, our 3 AI assistants automatically write the complete legal narrative, cite official laws (31 U.S.C. 5318(g)), and let you <b>Download the Official PDF SAR</b> with 1 click.
        </p>
      </div>
    ),
  },
  {
    stepNumber: 5,
    targetTab: 'recourse',
    title: '5. Customer Care & Unfreeze Advisor',
    subtitle: 'Tell customers why an account was held and how to fix it',
    icon: UserCheck,
    content: (
      <div className="space-y-2.5 text-xs text-slate-300">
        <p>
          If a legitimate business customer's payment was flagged, you must explain why without violating privacy regulations.
        </p>
        <p>
          This workspace generates a plain-English explanation and a clear unfreeze checklist (e.g., verifying invoices or updating KYC records).
        </p>
      </div>
    ),
  },
  {
    stepNumber: 6,
    targetTab: 'governance',
    title: '6. Bank Examiner & Audit Verification',
    subtitle: 'Tamper-proof cryptographic seals for Federal Reserve compliance',
    icon: BarChart3,
    content: (
      <div className="space-y-2.5 text-xs text-slate-300">
        <p>
          Every decision made by the AI receives an immutable <b>cryptographic Merkle audit seal</b>.
        </p>
        <p>
          When bank regulators or auditors examine your systems, you have complete proof that your bank complied with <b>Federal Reserve SR 26-2</b> safety standards.
        </p>
      </div>
    ),
  },
];

export const InteractiveBankerTour = ({
  isOpen,
  currentStep,
  onNext,
  onPrev,
  onClose,
  onJumpToTab
}) => {
  if (!isOpen) return null;

  const step = BANKER_STEPS[currentStep] || BANKER_STEPS[0];
  const Icon = step.icon;
  const isLast = currentStep === BANKER_STEPS.length - 1;

  return (
    <div className="fixed bottom-3 right-3 sm:bottom-5 sm:right-5 z-50 w-[calc(100vw-24px)] sm:w-full sm:max-w-md bg-[var(--bg-card)] border border-[var(--border-card)] rounded-2xl shadow-2xl p-3.5 sm:p-4 space-y-3 animate-fadeIn select-none skeuo-card max-h-[85vh] overflow-y-auto">
      {/* Header */}
      <div className="flex items-center justify-between pb-2 border-b border-[var(--border-subtle)]">
        <div className="flex items-center gap-2 min-w-0">
          <div className="w-6 h-6 sm:w-7 sm:h-7 rounded-lg bg-gradient-to-b from-[#257843] to-[#144726] border border-[#113C21] flex items-center justify-center text-white shrink-0 shadow-[var(--skeuo-btn)]">
            <Icon className="w-3.5 h-3.5 text-white" />
          </div>
          <div className="min-w-0">
            <span className="text-[9px] font-mono text-[var(--accent-primary)] font-semibold uppercase tracking-wider block truncate">
              Guided Tour • Step {step.stepNumber} of {BANKER_STEPS.length}
            </span>
            <h3 className="text-xs sm:text-sm font-bold text-[var(--text-primary)] tracking-tight truncate">{step.title}</h3>
          </div>
        </div>

        <button
          onClick={onClose}
          className="p-1 rounded-lg skeuo-btn text-[var(--text-muted)] hover:text-[var(--text-primary)] cursor-pointer ml-1.5 shrink-0"
          title="Exit Tour"
        >
          <X className="w-3.5 h-3.5" />
        </button>
      </div>

      {/* Body */}
      <div>
        <p className="text-[11px] text-[var(--text-muted)] font-medium mb-1.5">{step.subtitle}</p>
        <div className="text-[11px] text-[var(--text-secondary)]">{step.content}</div>
      </div>

      {/* Progress Dots & Buttons */}
      <div className="pt-2 border-t border-[var(--border-subtle)] flex items-center justify-between gap-2">
        {/* Progress Bar */}
        <div className="flex items-center gap-1">
          {BANKER_STEPS.map((s, idx) => (
            <button
              key={idx}
              onClick={() => {
                onJumpToTab(s.targetTab, idx);
              }}
              className={`h-1.5 rounded-full transition-all cursor-pointer ${
                idx === currentStep ? 'w-4 bg-[var(--accent-primary)] shadow-sm' : 'w-1.5 bg-[var(--border-subtle)] hover:bg-[var(--accent-primary)]/50'
              }`}
            />
          ))}
        </div>

        {/* Next / Previous Controls */}
        <div className="flex items-center gap-1.5">
          {currentStep > 0 && (
            <button
              onClick={onPrev}
              className="px-2.5 py-1 rounded-lg skeuo-btn skeuo-btn-secondary text-[11px] font-medium cursor-pointer flex items-center gap-1"
            >
              <ChevronLeft className="w-3 h-3" />
              <span>Back</span>
            </button>
          )}

          <button
            onClick={onNext}
            className="px-3 py-1 rounded-lg skeuo-btn skeuo-btn-primary text-xs font-semibold cursor-pointer flex items-center gap-1 shadow-sm"
          >
            <span>{isLast ? 'Complete 🎉' : 'Next'}</span>
            <ChevronRight className="w-3 h-3" />
          </button>
        </div>
      </div>
    </div>
  );
};
