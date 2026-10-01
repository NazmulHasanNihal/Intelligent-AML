import React from 'react';
import { Play, Radio, UploadCloud, ShieldAlert, Sparkles, CheckCircle2, AlertTriangle, ArrowRight } from 'lucide-react';

export const QuickStartBar = ({ 
  onSelectScenario, 
  onOpenBatchModal,
  isTourActive, 
  onToggleTour, 
  isLiveStreamActive, 
  onToggleLiveStream 
}) => {
  const scenarios = [
    {
      id: 'smurfing',
      title: '🚨 Smurfing Ring ($9.45k)',
      type: 'Tier 1 (Quarantine)',
      badgeClass: 'badge-tier1',
      description: '4-hop cyclic wash loop across 3 banks with 85.7% transfers in $9k-$9.95k CTR avoidance band.',
      data: {
        id: 'TX-994821',
        srcId: 'US-JPMC-4829-1092-8823',
        dstId: 'GB-BARC-1109-MULE-HUB',
        amount: 9450,
        rail: 'SWIFT Wire (MT103)',
        jurisdiction: 'Offshore (Panama / BVI)',
        holderName: 'Apex Global Logistics Ltd',
        counterpartyName: 'Elena Rostova (Conduit Hub)',
        burstVelocity: true,
        fastPath: true,
        alpha: 0.01,
        tier: 'TIER_1_QUARANTINE',
        gammaSet: '{1}',
        gammaLabel: 'Tier 1: Quarantine'
      }
    },
    {
      id: 'peeling',
      title: '🌪️ Crypto Mixer ($95k)',
      type: 'Tier 1 (Quarantine)',
      badgeClass: 'badge-tier1',
      description: 'Darknet UTXO peel chain routing through Wasabi CoinJoin liquidity pool.',
      data: {
        id: 'TX-994819',
        srcId: '0x3a9f-4829-DARK-0012',
        dstId: '0x7b12-MIXER-POOL',
        amount: 95000,
        rail: 'Bitcoin UTXO DAG',
        jurisdiction: 'Decentralized (FATF Grey List)',
        holderName: 'Darknet UTXO Consolidation',
        counterpartyName: 'Mixer Liquidity Pool',
        burstVelocity: true,
        fastPath: false,
        alpha: 0.01,
        tier: 'TIER_1_QUARANTINE',
        gammaSet: '{1}',
        gammaLabel: 'Tier 1: Quarantine'
      }
    },
    {
      id: 'payroll',
      title: '🏢 Corporate Payroll ($1.25M)',
      type: 'Tier 3 (Auto-Clear)',
      badgeClass: 'badge-tier3',
      description: 'Enterprise payroll clearing with finite coverage guarantee. Zero compliance disruption.',
      data: {
        id: 'TX-994817',
        srcId: 'US-WF-0091-8841-CLEAN',
        dstId: 'US-JPMC-2201-AMZN-AWS',
        amount: 1250000,
        rail: 'Fedwire Funds Service',
        jurisdiction: 'Domestic (Clean)',
        holderName: 'BlueWave Distribution Corp',
        counterpartyName: 'Amazon Web Services Inc',
        burstVelocity: false,
        fastPath: true,
        alpha: 0.01,
        tier: 'TIER_3_STRAIGHT_THROUGH_CLEAR',
        gammaSet: '{0}',
        gammaLabel: 'Tier 3: Auto-Cleared'
      }
    },
    {
      id: 'coldstart',
      title: '🔍 Dormant Account ($4.8k)',
      type: 'Tier 2 (Review)',
      badgeClass: 'badge-tier2',
      description: 'Zero activity for 90 days followed by abrupt cross-border cashout burst.',
      data: {
        id: 'TX-994818',
        srcId: 'US-CITI-0019-DORMANT-MULE',
        dstId: 'SG-DBS-8819-TRANSIT',
        amount: 4800,
        rail: 'ACH Direct Clearing',
        jurisdiction: 'Domestic to Singapore',
        holderName: 'Marcus Vance',
        counterpartyName: 'Marina Bay Trade Transit',
        burstVelocity: false,
        fastPath: true,
        alpha: 0.01,
        tier: 'TIER_2_REVIEW_QUEUE',
        gammaSet: '{0, 1}',
        gammaLabel: 'Tier 2: Review Queue'
      }
    }
  ];

  return (
    <div className="skeuo-card p-2 sm:p-2.5 font-sans text-xs">
      <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-2">
        
        {/* Left: 1-Click Scenario Preset Buttons */}
        <div className="flex flex-wrap items-center gap-1.5 min-w-0">
          <span className="text-[10px] font-bold text-[var(--text-muted)] font-mono uppercase tracking-wider flex items-center gap-1 mr-0.5 shrink-0">
            <Sparkles className="w-3 h-3 text-[var(--accent-primary)]" />
            <span>1-Click Scenarios:</span>
          </span>

          {scenarios.map((sc) => (
            <button
              key={sc.id}
              onClick={() => onSelectScenario && onSelectScenario(sc.data)}
              className="px-2.5 py-1 rounded-lg skeuo-btn text-[11px] font-semibold text-[var(--text-primary)] transition-all flex items-center gap-1.5 cursor-pointer active:translate-y-0.5 hover:border-[var(--accent-primary)] group shrink-0"
              title={sc.description}
            >
              <span>{sc.title}</span>
              <span className={`text-[8px] font-mono font-bold px-1.5 py-0.2 rounded-full ${sc.badgeClass}`}>
                {sc.type.split(' ')[0]}
              </span>
            </button>
          ))}

          {/* Quick Batch CSV Ingest Modal Trigger */}
          <button
            onClick={onOpenBatchModal}
            className="px-2.5 py-1 rounded-lg skeuo-btn skeuo-btn-primary text-[11px] font-bold flex items-center gap-1.5 cursor-pointer active:translate-y-0.5 shrink-0"
            title="Upload CSV or select pre-bundled benchmark batch"
          >
            <UploadCloud className="w-3.5 h-3.5" />
            <span>Batch CSV Ingest</span>
          </button>
        </div>

        {/* Right: Stream & Tour Controls */}
        <div className="flex items-center gap-1.5 shrink-0 font-mono text-[10px] self-end lg:self-auto">
          <button
            onClick={onToggleLiveStream}
            className={`px-2.5 py-1 rounded-lg font-bold flex items-center gap-1 transition-all cursor-pointer ${
              isLiveStreamActive
                ? 'bg-emerald-500/15 text-emerald-700 dark:text-emerald-300 border border-emerald-500/30 shadow-inner'
                : 'skeuo-btn text-[var(--text-muted)]'
            }`}
            title={isLiveStreamActive ? 'Pause real-time transaction ticker' : 'Resume real-time transaction ticker'}
          >
            <Radio className={`w-3 h-3 ${isLiveStreamActive ? 'animate-pulse text-emerald-500' : ''}`} />
            <span>{isLiveStreamActive ? 'Live Stream: Active' : 'Live Stream: Paused'}</span>
          </button>

          <button
            onClick={onToggleTour}
            className={`px-2.5 py-1 rounded-lg font-bold flex items-center gap-1 transition-all cursor-pointer ${
              isTourActive
                ? 'bg-[var(--accent-primary)]/15 text-[var(--accent-primary)] border border-[var(--accent-primary)]/40 shadow-inner'
                : 'skeuo-btn text-[var(--text-primary)]'
            }`}
            title="Start Interactive Banker Tour across all 6 consoles"
          >
            <Play className="w-3 h-3 fill-current text-[var(--accent-primary)]" />
            <span>{isTourActive ? 'Tour Active' : 'Guided Tour'}</span>
          </button>
        </div>

      </div>
    </div>
  );
};
