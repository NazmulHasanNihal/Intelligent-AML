import React from 'react';
import { ArrowLeft, ArrowRight, CheckCircle2, ChevronRight, Activity, Zap, Inbox, Share2, FileText, BarChart3, UserCheck } from 'lucide-react';

const PIPELINE_STAGES = [
  { id: 'command-center', step: 1, name: '1. Ingest', fullName: 'Real-Time Ingestion', icon: Zap },
  { id: 'command-center', step: 2, name: '2. Score', fullName: 'Dual C-STGB Scoring', icon: Activity },
  { id: 'alerts', step: 3, name: '3. Conformal Triage', fullName: 'CRC 3-Tier Allocation', icon: Inbox },
  { id: 'investigate', step: 4, name: '4. Investigation', fullName: '3D Graph Forensics', icon: Share2 },
  { id: 'cases', step: 5, name: '5. Regulatory Filing', fullName: 'FinCEN / goAML Filing', icon: FileText },
  { id: 'governance', step: 6, name: '6. Governance', fullName: 'SR 11-7 Audit Vault', icon: BarChart3 },
];

export const WorkflowStageFooter = ({ activeTab, setActiveTab }) => {
  const currentStageIndex = PIPELINE_STAGES.findIndex(s => s.id === activeTab);
  const activeStep = currentStageIndex >= 0 ? PIPELINE_STAGES[currentStageIndex].step : 1;

  const prevStage = currentStageIndex > 0 ? PIPELINE_STAGES[currentStageIndex - 1] : null;
  const nextStage = currentStageIndex < PIPELINE_STAGES.length - 1 ? PIPELINE_STAGES[currentStageIndex + 1] : null;

  return (
    <div className="skeuo-card p-2 sm:p-2.5 rounded-2xl flex flex-col md:flex-row items-center justify-between gap-2.5 mt-2.5 sm:mt-3 border-[var(--border-card)]">
      
      {/* Left Action / Previous Button */}
      <div className="flex items-center gap-2 w-full md:w-auto justify-between md:justify-start">
        {prevStage ? (
          <button
            onClick={() => setActiveTab(prevStage.id)}
            className="px-2.5 sm:px-3 py-1 sm:py-1.5 rounded-xl skeuo-btn skeuo-btn-secondary text-[11px] font-mono font-medium flex items-center gap-1.5 cursor-pointer"
          >
            <ArrowLeft className="w-3.5 h-3.5 text-[var(--accent-primary)]" />
            <span className="hidden sm:inline">Back:</span> <span>{prevStage.name}</span>
          </button>
        ) : (
          <div className="flex items-center gap-1.5 text-[10px] sm:text-[11px] font-mono text-[var(--text-muted)] px-2">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
            <span>Pipeline: Real-Time Active</span>
          </div>
        )}

        <div className="md:hidden text-[10px] font-mono text-[var(--text-muted)]">
          Stage {activeStep} of {PIPELINE_STAGES.length}
        </div>
      </div>

      {/* Center: Pinned Workflow Execution Progress Ribbon */}
      <div className="hidden sm:flex items-center gap-1 overflow-x-auto py-0.5 px-1 skeuo-well rounded-xl max-w-full">
        {PIPELINE_STAGES.map((st, idx) => {
          const isCurrent = st.id === activeTab;
          const isPassed = idx < currentStageIndex;

          return (
            <React.Fragment key={st.step}>
              <button
                onClick={() => setActiveTab(st.id)}
                title={st.fullName}
                className={`flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-[10px] font-mono transition-all cursor-pointer ${
                  isCurrent
                    ? 'bg-gradient-to-b from-[#257843] to-[#174E2B] text-white font-bold shadow-sm'
                    : isPassed
                    ? 'text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-black/[0.04] dark:hover:bg-white/[0.04]'
                    : 'text-[var(--text-muted)] hover:text-[var(--text-secondary)]'
                }`}
              >
                {isPassed ? (
                  <CheckCircle2 className="w-3 h-3 text-emerald-500 shrink-0" />
                ) : (
                  <span className={`w-1.5 h-1.5 rounded-full shrink-0 ${isCurrent ? 'bg-emerald-300 animate-ping' : 'bg-[var(--border-subtle)]'}`} />
                )}
                <span className="whitespace-nowrap">{st.name}</span>
              </button>
              {idx < PIPELINE_STAGES.length - 1 && (
                <ChevronRight className="w-3 h-3 text-[var(--border-subtle)] shrink-0" />
              )}
            </React.Fragment>
          );
        })}
      </div>

      {/* Right Action / Next Button */}
      <div className="flex items-center gap-2 w-full md:w-auto justify-end">
        {nextStage ? (
          <button
            onClick={() => setActiveTab(nextStage.id)}
            className="px-3 sm:px-3.5 py-1 sm:py-1.5 rounded-xl skeuo-btn skeuo-btn-primary text-[11px] font-mono font-semibold flex items-center gap-1.5 cursor-pointer shadow-sm w-full md:w-auto justify-center"
          >
            <span className="hidden sm:inline">Next Stage:</span> <span>{nextStage.name}</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        ) : (
          <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg skeuo-well text-[10px] sm:text-[11px] font-mono text-[var(--accent-primary)] font-semibold">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Audit-Sealed Compliance</span>
          </div>
        )}
      </div>
    </div>
  );
};
