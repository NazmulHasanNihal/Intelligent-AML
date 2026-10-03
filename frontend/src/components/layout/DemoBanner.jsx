import React, { useEffect } from 'react';
import { 
  Play, 
  Pause, 
  Radio, 
  Zap, 
  ShieldAlert, 
  CheckCircle2, 
  SlidersHorizontal, 
  HelpCircle,
  FlaskConical,
  Activity
} from 'lucide-react';
import { useAppStore } from '../../lib/store';
import { streamService } from '../../lib/streamGenerator';
import { Badge } from '../ui/Badge';
import { Button } from '../ui/Button';

export const DemoBanner = () => {
  const { 
    telemetry, 
    metrics, 
    isStreamRunning, 
    streamSpeed, 
    liveTransactions,
    toggleStreamRunning, 
    setStreamSpeed,
    processStreamTransaction,
    setDemoToolsOpen,
    openDrawer
  } = useAppStore();

  // Initialize the stream service with the store's processing function
  useEffect(() => {
    streamService.init((tx) => {
      processStreamTransaction(tx);
    });

    return () => {
      streamService.stop();
    };
  }, [processStreamTransaction]);

  const latestTx = liveTransactions[0];

  return (
    <div className="bg-surfaceRaised border-b border-border text-xs px-3 sm:px-4 py-2 flex flex-wrap items-center justify-between gap-3 shadow-xs">
      {/* Left: Stream Status & Ticker Controls */}
      <div className="flex items-center gap-2.5 flex-wrap">
        {/* Status Pill */}
        <div className={`flex items-center gap-1.5 px-2 py-0.5 rounded-full border text-[11px] font-mono font-medium ${
          isStreamRunning 
            ? 'bg-cleared-bg border-cleared text-cleared' 
            : 'bg-review-bg border-review text-review'
        }`}>
          <span className={`w-2 h-2 rounded-full ${isStreamRunning ? 'bg-cleared animate-pulse' : 'bg-review'}`} />
          <span>{isStreamRunning ? 'LIVE STREAM' : 'PAUSED'}</span>
        </div>

        {/* Play/Pause Button */}
        <button
          onClick={toggleStreamRunning}
          title={isStreamRunning ? 'Pause live transaction arrival' : 'Resume live transaction arrival'}
          className="p-1 rounded hover:bg-surfaceHover text-text-2 hover:text-text transition-colors cursor-pointer border border-border"
        >
          {isStreamRunning ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
        </button>

        {/* Speed Controls (1x, 2x, 5x, 10x) */}
        <div className="flex items-center gap-0.5 p-0.5 bg-bg rounded border border-border font-mono text-[10px]">
          {[
            { val: 1, label: '1x', tip: '1.7 tx/s - Real-world Bank Pace (~150k tx/day)' },
            { val: 2, label: '2x', tip: '4.0 tx/s - Interbank Rush Hour Flow' },
            { val: 5, label: '5x', tip: '15 tx/s - Clearing Window Peak Surge' },
            { val: 10, label: '10x', tip: '50 tx/s - High-throughput Stress Volume' }
          ].map((item) => (
            <button
              key={item.val}
              onClick={() => setStreamSpeed(item.val)}
              title={item.tip}
              className={`px-1.5 py-0.5 rounded transition-colors cursor-pointer ${
                streamSpeed === item.val 
                  ? 'bg-surface font-semibold text-text shadow-xs' 
                  : 'text-text-muted hover:text-text'
              }`}
            >
              {item.label}
            </button>
          ))}
        </div>

        {/* Real-world Velocity Badge */}
        <div className="hidden lg:flex items-center gap-1.5 px-2 py-0.5 rounded bg-bg border border-border text-[10px] font-mono text-text-muted">
          <Activity className="w-3 h-3 text-accent animate-pulse" />
          <span className="text-text font-medium">
            {streamSpeed === 1 ? '1.7 tx/s (Bank Pace)' : 
             streamSpeed === 2 ? '4.0 tx/s (Rush Hour)' : 
             streamSpeed === 5 ? '15.0 tx/s (Peak Surge)' : 
             '50.0 tx/s (Stress Volume)'}
          </span>
        </div>

        {/* Real-Time Ingestion Watermark & Consumer Lag Indicator */}
        <div className="hidden 2xl:flex items-center gap-1.5 px-2 py-0.5 rounded bg-bg border border-border text-[10px] font-mono text-text-muted">
          <span className="w-1.5 h-1.5 rounded-full bg-cleared animate-ping" />
          <span>Lag: <strong className="text-cleared">0 msgs</strong> (0.12 ms)</span>
          <span>• Watermark: <strong className="text-text">Head Synchronized</strong></span>
        </div>

        {/* Live Mathematical Telemetry Snapshot */}
        <div className="hidden md:flex items-center gap-2 text-text-2 font-mono text-[11px] pl-2 border-l border-border">
          <span className="text-text font-bold tabular-nums">
            {telemetry.totalProcessed24h.toLocaleString()} txs
          </span>
          <span className="text-text-muted">•</span>
          <span className="text-cleared font-semibold">{metrics.stpRate}% STP</span>
          <span className="text-text-muted">•</span>
          <span className="text-critical">{telemetry.tier1Quarantined.toLocaleString()} T1</span>
          <span className="text-text-muted">•</span>
          <span className="text-review">{telemetry.tier2ReviewQueue.toLocaleString()} T2</span>
        </div>
      </div>

      {/* Middle: Latest Arrived Transaction Pill */}
      {latestTx && (
        <div 
          onClick={() => openDrawer({
            account: latestTx.sourceAccount,
            entityName: latestTx.sourceEntity,
            tier: latestTx.tierLabel,
            tierCode: latestTx.tierCode,
            amount: latestTx.amount,
            riskScore: latestTx.riskScore,
            whyFlagged: latestTx.reasons?.join('; ') || 'Live stream scored transaction'
          })}
          title="Click to inspect this incoming transaction in Drawer"
          className="hidden xl:flex items-center gap-2 px-2.5 py-1 rounded bg-bg border border-border text-[11px] font-mono hover:border-accent cursor-pointer transition-colors max-w-md truncate"
        >
          <span className="text-accent font-semibold">{latestTx.id}</span>
          <span className="text-text truncate max-w-[140px]">{latestTx.sourceEntity}</span>
          <span className="text-text-muted font-bold">${Number(latestTx.amount).toLocaleString()}</span>
          <Badge 
            variant={latestTx.tierCode === 1 ? 'critical' : latestTx.tierCode === 2 ? 'review' : 'cleared'} 
            size="sm"
          >
            {latestTx.tierCode === 1 ? 'Tier 1' : latestTx.tierCode === 2 ? 'Tier 2' : 'Tier 3 Clear'}
          </Badge>
        </div>
      )}

      {/* Right: Operational Threat Simulation Trigger */}
      <div className="flex items-center gap-2 shrink-0">
        <Button
          variant="outline"
          size="sm"
          onClick={() => setDemoToolsOpen(true)}
          icon={ShieldAlert}
          className="text-xs h-7"
        >
          Simulate Threat Scenario
        </Button>
      </div>
    </div>
  );
};
