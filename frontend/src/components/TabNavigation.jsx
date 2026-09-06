import React from 'react';
import { Zap, Share2, Target, Sliders, FileText, BarChart3 } from 'lucide-react';

export const TabNavigation = ({ activeTab, setActiveTab }) => {
  const tabs = [
    { id: 'telemetry', label: '1. Live Scoring', icon: Zap, badge: 'SLA <1ms' },
    { id: 'graph', label: '2. Forensic Graph Studio', icon: Share2, badge: '8 Typologies' },
    { id: 'triage', label: '3. Conformal Triage', icon: Target, badge: '99% Coverage' },
    { id: 'recourse', label: '4. Counterfactual Sandbox', icon: Sliders, badge: 'What-If' },
    { id: 'sar', label: '5. Multi-Agent SAR Drafter', icon: FileText, badge: 'Form 111' },
    { id: 'benchmark', label: '6. Benchmark & Governance', icon: BarChart3, badge: '13 Datasets' },
  ];

  return (
    <div className="w-full overflow-x-auto pb-2 mb-6 border-b border-slate-800/80">
      <div className="flex items-center gap-2 min-w-max">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;

          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`flex items-center gap-2.5 px-4 py-3 rounded-xl text-xs font-bold transition-all duration-200 ${
                isActive
                  ? 'bg-gradient-to-r from-sky-500/20 to-indigo-500/20 text-sky-300 border border-sky-500/40 shadow-glow'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900/60 border border-transparent'
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? 'text-sky-400' : 'text-slate-500'}`} />
              <span>{tab.label}</span>
              {tab.badge && (
                <span
                  className={`text-[10px] px-1.5 py-0.5 rounded font-mono font-semibold ${
                    isActive
                      ? 'bg-sky-500/30 text-sky-200 border border-sky-400/40'
                      : 'bg-slate-800 text-slate-400'
                  }`}
                >
                  {tab.badge}
                </span>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
};
