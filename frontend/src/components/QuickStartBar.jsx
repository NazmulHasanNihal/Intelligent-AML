import React from 'react';
import { Play, Radio, ArrowRight } from 'lucide-react';

export const QuickStartBar = ({ onSelectScenario, isTourActive, onToggleTour, isLiveStreamActive, onToggleLiveStream }) => {
  const scenarios = [
    {
      id: 'smurfing',
      title: '🚨 Smurfing Ring ($9.5k)',
      type: 'Tier 1 (Hold)',
      badge: 'badge-red',
      data: {
        srcId: 'ACC_8823_SUSPECT_MULE',
        dstId: 'ACC_1109_MULE_HUB',
        amount: 9450,
        paymentRail: 'Wire (SWIFT)',
        jurisdiction: 'Offshore Haven (BVI/Panama)',
        burstVelocity: true,
        fastPath: true,
        alpha: 0.01,
      }
    },
    {
      id: 'peeling',
      title: '🌪️ Crypto Mixer ($95k)',
      type: 'Tier 1 (Hold)',
      badge: 'badge-red',
      data: {
        srcId: '0x3a9f_DARKNET_WHALE',
        dstId: '0x7b12_MIXER_POOL',
        amount: 95000,
        paymentRail: 'Bitcoin (UTXO)',
        jurisdiction: 'FATF Grey List',
        burstVelocity: true,
        fastPath: false,
        alpha: 0.01,
      }
    },
    {
      id: 'payroll',
      title: '🏢 Corporate Payroll ($1.2M)',
      type: 'Tier 3 (Clear)',
      badge: 'badge-green',
      data: {
        srcId: 'CORP_9912_FORTUNE500',
        dstId: 'FED_SETTLE_CLEARING',
        amount: 1250000,
        paymentRail: 'ACH / Fedwire',
        jurisdiction: 'Domestic (Clean)',
        burstVelocity: false,
        fastPath: true,
        alpha: 0.01,
      }
    },
    {
      id: 'coldstart',
      title: '🔍 Dormant Account ($9.4k)',
      type: 'Tier 2 (Review)',
      badge: 'badge-amber',
      data: {
        srcId: 'ACC_VIRGIN_0019',
        dstId: 'ATM_CASHOUT_STUB',
        amount: 9400,
        paymentRail: 'Mobile Money (MFS)',
        jurisdiction: 'FATF Grey List',
        burstVelocity: false,
        fastPath: true,
        alpha: 0.01,
      }
    }
  ];

  return (
    <div className="card-panel p-3.5 border-slate-800/80 bg-[#081024]/80">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
        {/* Left: Quick Scenarios Label & Buttons */}
        <div className="flex flex-wrap items-center gap-2">
          <span className="text-xs font-bold text-slate-300 font-mono flex items-center gap-1.5 mr-1">
            <span>⚡ 1-Click Scenarios:</span>
          </span>

          {scenarios.map((sc) => (
            <button
              key={sc.id}
              onClick={() => onSelectScenario(sc.data)}
              className="px-3 py-1.5 rounded-lg bg-slate-900/90 hover:bg-slate-800 border border-slate-800 hover:border-cyan-500/40 text-xs font-medium text-slate-200 transition-all flex items-center gap-2 cursor-pointer group"
            >
              <span>{sc.title}</span>
              <span className={`text-[9px] font-mono font-bold px-1.5 py-0.2 rounded ${sc.badge}`}>
                {sc.type}
              </span>
            </button>
          ))}
        </div>

        {/* Right: Stream & Tour Controls */}
        <div className="flex items-center gap-2 shrink-0 font-mono text-xs">
          <button
            onClick={onToggleLiveStream}
            className={`px-3 py-1.5 rounded-lg font-bold flex items-center gap-1.5 transition-all cursor-pointer ${
              isLiveStreamActive
                ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 shadow-glowGreen'
                : 'bg-slate-900 text-slate-400 border border-slate-800 hover:text-slate-200'
            }`}
          >
            <Radio className={`w-3.5 h-3.5 ${isLiveStreamActive ? 'animate-pulse' : ''}`} />
            <span>{isLiveStreamActive ? 'Live Feed: ON' : 'Live Feed: PAUSED'}</span>
          </button>

          <button
            onClick={onToggleTour}
            className={`px-3 py-1.5 rounded-lg font-bold flex items-center gap-1.5 transition-all cursor-pointer ${
              isTourActive
                ? 'bg-sky-500/20 text-sky-300 border border-sky-500/40 shadow-glow'
                : 'bg-slate-900 text-sky-400 border border-slate-800 hover:bg-slate-800'
            }`}
          >
            <Play className="w-3.5 h-3.5 fill-current" />
            <span>{isTourActive ? 'Tour Active' : 'Guided Tour'}</span>
          </button>
        </div>
      </div>
    </div>
  );
};
