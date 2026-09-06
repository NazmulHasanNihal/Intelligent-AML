import React, { useState, useEffect } from 'react';
import { 
  Play, 
  Pause, 
  Zap, 
  ShieldAlert, 
  CheckCircle2, 
  Clock, 
  Activity, 
  Sliders, 
  ArrowRight,
  TrendingUp,
  AlertTriangle,
  Radio,
  RefreshCw,
  Sparkles
} from 'lucide-react';

const MOCK_STREAM_TXS = [
  { id: 'TX-994821', src: 'US-JPMC-4829 (Apex Global)', dst: 'GB-BARC-1109 (Elena Mule)', amount: '$9,450.00', risk: 0.94, tier: 'TIER_1_QUARANTINE', burst: true, time: '08:42:01', rail: 'SWIFT' },
  { id: 'TX-994819', src: '0x3a9f (Darknet UTXO)', dst: '0x7b12 (Mixer Pool)', amount: '$95,000.00', risk: 0.98, tier: 'TIER_1_QUARANTINE', burst: true, time: '08:41:58', rail: 'BTC UTXO' },
  { id: 'TX-994818', src: 'US-CITI-0019 (Marcus Vance)', dst: 'SG-DBS-8819 (Transit)', amount: '$4,800.00', risk: 0.52, tier: 'TIER_2_REVIEW_QUEUE', burst: false, time: '08:41:55', rail: 'ACH' },
  { id: 'TX-994817', src: 'US-WF-0091 (BlueWave Corp)', dst: 'US-JPMC-2201 (Amazon AWS)', amount: '$14,250.00', risk: 0.02, tier: 'TIER_3_STRAIGHT_THROUGH_CLEAR', burst: false, time: '08:41:52', rail: 'Fedwire' },
  { id: 'TX-994816', src: 'DE-DB-9901 (Rheinland Freight)', dst: 'FR-BNP-3312 (Euro Hub)', amount: '$6,200.00', risk: 0.44, tier: 'TIER_2_REVIEW_QUEUE', burst: false, time: '08:41:48', rail: 'SEPA' },
  { id: 'TX-994815', src: 'HK-HSBC-8812 (Asia Trading)', dst: 'US-JPMC-4829 (Apex Global)', amount: '$47,600.00', risk: 0.96, tier: 'TIER_1_QUARANTINE', burst: true, time: '08:41:44', rail: 'SWIFT' },
  { id: 'TX-994814', src: 'US-BOA-7712 (Target Retail POS)', dst: 'US-CITI-9902 (Merchant Settled)', amount: '$85.40', risk: 0.01, tier: 'TIER_3_STRAIGHT_THROUGH_CLEAR', burst: false, time: '08:41:39', rail: 'Visa Net' },
];

export const LiveStreamTicker = ({ isActive, onSelectTx, sharedStats, onStatsUpdate }) => {
  const [isPlaying, setIsPlaying] = useState(true);
  const [speed, setSpeed] = useState(1); // 1x, 2x, 5x
  const [transactions, setTransactions] = useState(MOCK_STREAM_TXS);

  useEffect(() => {
    if (!isPlaying) return;

    const interval = setInterval(() => {
      const randomTx = MOCK_STREAM_TXS[Math.floor(Math.random() * MOCK_STREAM_TXS.length)];
      const newTx = {
        ...randomTx,
        id: `TX-${Math.floor(994000 + Math.random() * 1000)}`,
        time: new Date().toLocaleTimeString('en-US', { hour12: false }),
      };

      setTransactions(prev => [newTx, ...prev.slice(0, 15)]);

      if (onStatsUpdate && sharedStats) {
        onStatsUpdate({
          ...sharedStats,
          processed: sharedStats.processed + 1,
          cleared: randomTx.tier === 'TIER_3_STRAIGHT_THROUGH_CLEAR' ? sharedStats.cleared + 1 : sharedStats.cleared,
          quarantined: randomTx.tier === 'TIER_1_QUARANTINE' ? sharedStats.quarantined + 1 : sharedStats.quarantined,
          reviewQueue: randomTx.tier === 'TIER_2_REVIEW_QUEUE' ? sharedStats.reviewQueue + 1 : sharedStats.reviewQueue,
        });
      }
    }, 2400 / speed);

    return () => clearInterval(interval);
  }, [isPlaying, speed, sharedStats, onStatsUpdate]);

  return (
    <div className="skeuo-card p-2 sm:py-1.5 sm:px-3 flex flex-col md:flex-row items-stretch md:items-center justify-between gap-2 text-xs font-sans">
      {/* Left: Stream Indicator & Speed Controls */}
      <div className="flex items-center gap-2 shrink-0">
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full skeuo-pill-active shadow-sm font-semibold">
          <div className="relative flex h-2 w-2">
            {isPlaying && <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-white opacity-75"></span>}
            <span className={`relative inline-flex rounded-full h-2 w-2 ${isPlaying ? 'bg-white' : 'bg-slate-400'}`}></span>
          </div>
          <span className="font-bold text-white text-[10px] font-mono tracking-wider">LIVE STREAM</span>
        </div>

        {/* Play / Pause Toggle */}
        <button
          onClick={() => setIsPlaying(prev => !prev)}
          className="skeuo-btn p-1.5 rounded-lg text-[var(--text-primary)] cursor-pointer"
          title={isPlaying ? 'Pause Transaction Stream' : 'Resume Live Stream'}
        >
          {isPlaying ? <Pause className="w-3 h-3 text-[var(--accent-primary)]" /> : <Play className="w-3 h-3 text-[var(--accent-primary)]" />}
        </button>

        {/* Speed Controls */}
        <div className="flex items-center gap-0.5 skeuo-well p-0.5 rounded-lg font-mono text-[10px]">
          {[1, 2, 5].map((s) => (
            <button
              key={s}
              onClick={() => setSpeed(s)}
              className={`px-1.5 py-0.5 rounded transition-all cursor-pointer ${
                speed === s ? 'bg-[var(--accent-primary)] text-white font-bold shadow-sm' : 'text-[var(--text-muted)] hover:text-[var(--text-primary)]'
              }`}
            >
              {s}x
            </button>
          ))}
        </div>
      </div>

      {/* Center: Live Transaction Ticker Stream Items */}
      <div className="flex-1 overflow-x-auto overflow-y-hidden no-scrollbar flex items-center gap-1.5 py-0.5 min-w-0">
        {transactions.slice(0, 5).map((tx) => {
          const isQuarantine = tx.tier === 'TIER_1_QUARANTINE';
          const isReview = tx.tier === 'TIER_2_REVIEW_QUEUE';
          return (
            <div
              key={tx.id}
              onClick={() => onSelectTx && onSelectTx(tx)}
              className={`flex items-center gap-1.5 px-2.5 py-1 rounded-xl border shrink-0 transition-all cursor-pointer skeuo-btn active:scale-[0.98] ${
                isQuarantine
                  ? 'border-rose-500/40 text-rose-700 dark:text-rose-300'
                  : isReview
                  ? 'border-amber-500/40 text-amber-800 dark:text-amber-300'
                  : 'border-[var(--border-subtle)] text-[var(--text-primary)]'
              }`}
              title={`Click to inspect ${tx.id}`}
            >
              <span className="font-mono font-bold text-[10px] text-[var(--accent-primary)]">{tx.id}</span>
              <span className="text-[10px] text-[var(--text-secondary)] truncate max-w-[100px]">{tx.src.split(' ')[0]}</span>
              <span className="font-mono text-[10px] font-bold text-[var(--text-primary)]">{tx.amount}</span>
              <span className={`text-[9px] font-mono px-1.5 py-0.2 rounded-full font-bold shadow-inner ${
                isQuarantine ? 'bg-rose-500/20 text-rose-700 dark:text-rose-300' : isReview ? 'bg-amber-500/20 text-amber-800 dark:text-amber-300' : 'bg-emerald-500/20 text-emerald-800 dark:text-emerald-300'
              }`}>
                {(tx.risk * 100).toFixed(0)}%
              </span>
            </div>
          );
        })}
      </div>

      {/* Right: Micro Telemetry Summary */}
      <div className="hidden xl:flex items-center gap-2.5 shrink-0 font-mono text-[10px] text-[var(--text-secondary)] border-l border-[var(--border-subtle)] pl-2.5">
        <div>
          <span className="text-[8px] text-[var(--text-muted)] block uppercase">THROUGHPUT</span>
          <span className="text-[var(--text-primary)] font-bold">31.2k tx/s</span>
        </div>
        <div>
          <span className="text-[8px] text-[var(--text-muted)] block uppercase">STREAM LATENCY</span>
          <span className="text-[var(--accent-primary)] font-bold">0.45ms</span>
        </div>
      </div>
    </div>
  );
};
