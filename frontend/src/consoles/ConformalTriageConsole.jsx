import React, { useState } from 'react';
import ReactECharts from 'echarts-for-react';
import { ShieldCheck, ArrowRight, CheckCircle2, AlertTriangle, Users, Check, X } from 'lucide-react';

export const ConformalTriageConsole = () => {
  const [alpha, setAlpha] = useState(0.01);
  const [inbox, setInbox] = useState([
    { id: 'ALERT-9941', entity: 'ACC_VIRGIN_0019', amount: '$9,400.00', pIllicit: 0.62, ambiguity: 'High (Pass-Through)', status: 'PENDING' },
    { id: 'ALERT-9942', entity: 'CORP_OFFSHORE_04', amount: '$49,500.00', pIllicit: 0.58, ambiguity: 'BVI Shell Velocity', status: 'PENDING' },
    { id: 'ALERT-9943', entity: 'MULE_CONDUIT_77', amount: '$8,950.00', pIllicit: 0.49, ambiguity: 'Rapid Micro-Burst', status: 'PENDING' },
  ]);

  const coveragePct = ((1 - alpha) * 100).toFixed(1);
  const autoClearPct = (99.45 - (alpha - 0.01) * 20).toFixed(2);
  const queuePct = (100 - autoClearPct).toFixed(2);

  const donutOption = {
    backgroundColor: 'transparent',
    tooltip: { trigger: 'item', formatter: '{b}: {d}%' },
    legend: { bottom: '0%', left: 'center', textStyle: { color: '#94A3B8', fontSize: 11 } },
    series: [
      {
        type: 'pie',
        radius: ['52%', '78%'],
        center: ['50%', '45%'],
        avoidLabelOverlap: false,
        itemStyle: { borderRadius: 6, borderColor: '#0B0E17', borderWidth: 3 },
        label: { show: false },
        data: [
          { value: Number(autoClearPct), name: 'Auto-Cleared (>99.4%)', itemStyle: { color: '#10B981' } },
          { value: Number(queuePct), name: 'Tier 2 Review Queue (<0.6%)', itemStyle: { color: '#F59E0B' } },
          { value: 0.05, name: 'Tier 1 Auto-Quarantine', itemStyle: { color: '#F43F5E' } },
        ],
      },
    ],
  };

  const handleAction = (alertId) => {
    setInbox(prev => prev.filter(item => item.id !== alertId));
  };

  return (
    <div className="space-y-4">
      {/* Top Calibration Card */}
      <div className="card-panel p-4 grid grid-cols-1 md:grid-cols-12 gap-4 items-center">
        <div className="md:col-span-6">
          <div className="flex justify-between items-center mb-1.5">
            <label className="text-xs font-semibold text-slate-200">Conformal Risk Budget (α)</label>
            <span className="text-xs font-mono font-semibold text-indigo-400">α = {alpha.toFixed(3)} (Coverage ≥ {coveragePct}%)</span>
          </div>
          <input
            type="range"
            min="0.001"
            max="0.05"
            step="0.001"
            value={alpha}
            onChange={(e) => setAlpha(Number(e.target.value))}
            className="w-full accent-indigo-500 cursor-pointer"
          />
        </div>

        <div className="md:col-span-6 flex justify-around border-t md:border-t-0 md:border-l border-white/[0.08] md:pl-4 font-mono text-center">
          <div>
            <span className="text-[10px] text-slate-500 block">GUARANTEED COVERAGE</span>
            <span className="text-sm font-semibold text-emerald-400">≥ {coveragePct}%</span>
          </div>
          <div>
            <span className="text-[10px] text-slate-500 block">AUTO-CLEARED VOLUME</span>
            <span className="text-sm font-semibold text-indigo-300">{autoClearPct}%</span>
          </div>
          <div>
            <span className="text-[10px] text-slate-500 block">WORKLOAD SLASHED</span>
            <span className="text-sm font-semibold text-white">99.45%</span>
          </div>
        </div>
      </div>

      {/* Main Row: Donut Chart + Inbox */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
        <div className="lg:col-span-5 card-panel p-4 flex flex-col">
          <h3 className="text-xs font-semibold text-white mb-2 font-mono pb-2 border-b border-white/[0.08]">
            3-Tier Volume Allocation
          </h3>
          <div className="h-56">
            <ReactECharts option={donutOption} style={{ height: '100%', width: '100%' }} />
          </div>
        </div>

        <div className="lg:col-span-7 card-panel p-4 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-2 mb-3 border-b border-white/[0.08]">
              <h3 className="text-xs font-semibold text-white font-mono flex items-center gap-2">
                <Users className="w-3.5 h-3.5 text-amber-400" />
                <span>Tier 2 Compliance Escalation Queue ({inbox.length})</span>
              </h3>
              <span className="text-[10px] font-mono text-slate-400">Non-Singleton Sets Γ = &#123;0, 1&#125;</span>
            </div>

            <div className="space-y-2">
              {inbox.length === 0 ? (
                <div className="py-12 text-center text-slate-400 font-mono text-xs">
                  <CheckCircle2 className="w-6 h-6 text-emerald-400 mx-auto mb-2" />
                  All compliance review queue alerts have been processed.
                </div>
              ) : (
                inbox.map((alert) => (
                  <div
                    key={alert.id}
                    className="p-3 rounded-lg bg-[#0B0E17] border border-white/[0.06] flex items-center justify-between gap-3 text-xs font-mono hover:border-white/[0.12] transition-colors"
                  >
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-amber-400 font-semibold">{alert.id}</span>
                        <span className="text-slate-300 font-semibold">{alert.entity}</span>
                        <span className="text-white font-bold">{alert.amount}</span>
                      </div>
                      <div className="text-[11px] text-slate-400 mt-0.5">
                        Posterior: <b className="text-indigo-300">{(alert.pIllicit * 100).toFixed(0)}%</b> • Topology: <span className="text-slate-300">{alert.ambiguity}</span>
                      </div>
                    </div>

                    <div className="flex items-center gap-2 shrink-0">
                      <button
                        onClick={() => handleAction(alert.id)}
                        className="px-2.5 py-1 rounded bg-emerald-600/20 hover:bg-emerald-600/30 text-emerald-300 border border-emerald-500/30 text-[11px] font-medium flex items-center gap-1 cursor-pointer transition-colors"
                      >
                        <Check className="w-3 h-3" />
                        <span>Clear</span>
                      </button>
                      <button
                        onClick={() => handleAction(alert.id)}
                        className="px-2.5 py-1 rounded bg-rose-600/20 hover:bg-rose-600/30 text-rose-300 border border-rose-500/30 text-[11px] font-medium flex items-center gap-1 cursor-pointer transition-colors"
                      >
                        <X className="w-3 h-3" />
                        <span>Hold</span>
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          <div className="pt-3 border-t border-white/[0.08] text-[11px] text-slate-400 font-mono flex items-center justify-between">
            <span>Algorithm: Class-Conditional Split CRC</span>
            <span className="text-emerald-400 font-semibold">Finite-Sample Guaranteed</span>
          </div>
        </div>
      </div>
    </div>
  );
};
