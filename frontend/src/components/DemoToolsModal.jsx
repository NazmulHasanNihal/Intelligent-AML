import React, { useState } from 'react';
import * as Dialog from '@radix-ui/react-dialog';
import { 
  X, 
  FlaskConical, 
  Layers, 
  RotateCcw, 
  ShieldAlert, 
  Zap, 
  ChevronRight, 
  CheckCircle2, 
  Activity, 
  Network, 
  ArrowRight,
  Sparkles
} from 'lucide-react';
import { useAppStore } from '../lib/store';
import { Badge } from './ui/Badge';
import { Button } from './ui/Button';

export const DemoToolsModal = () => {
  const { 
    isDemoToolsOpen, 
    setDemoToolsOpen, 
    injectScenario, 
    navigate,
    telemetry,
    metrics
  } = useAppStore();

  const [activeTab, setActiveTab] = useState('scenarios');
  const [lastInjectedResults, setLastInjectedResults] = useState(null);
  const [selectedScenarioId, setSelectedScenarioId] = useState('structuring');

  const SCENARIOS = [
    {
      id: 'structuring',
      title: 'TBML Trade Structuring (Near-CTR Limits)',
      typology: 'Trade Over-Invoicing / CTR Structuring',
      severity: 'Critical Tier 1',
      description: 'Simulates 3 burst LC remittances ($9,450, $9,600, $9,800) beneath the $10k (৳1,000,000 BDT BFIU CTR threshold) from Meghna Industrial to Gulf Star Dubai.',
      forensicProfile: 'Identifies structured export documentary remittances just beneath BFIU Circular 26 CTR statutory limit ($10k / ৳1,000,000 BDT) accompanied by extreme ASYCUDA customs price over-invoicing (+333.7%). Triggers automated Tier 1 quarantine.',
      txCount: 3,
      totalExposure: '$28,850 (৳3.46M BDT)'
    },
    {
      id: 'cycle3_loop',
      title: 'Cycle-3 Trade Wash Layering Loop',
      typology: 'Circular Flow / Cross-Border Round-Tripping',
      severity: 'Critical Tier 1',
      description: 'Transfers $47,600 (৳5.7M BDT) in a closed 3-node cycle (Meghna Industrial -> Tanvir Rahman -> Gulf Star Commodities Dubai -> Meghna Industrial).',
      forensicProfile: 'Identifies circular interbank fund flow (Meghna Industrial -> Tanvir Rahman -> Gulf Star Dubai -> Meghna Industrial) with near-zero economic absorption (mass balance ratio ~1.0). Flagged as cross-border wash layering.',
      txCount: 3,
      totalExposure: '$47,600 (৳5.71M BDT)'
    },
    {
      id: 'camouflage_chaff',
      title: 'Benign Retail Noise & Chaff Filtering',
      typology: 'Benign Noise Filtering / Retail POS',
      severity: 'Noise Filter Test',
      description: 'Injects 4 retail micro-transactions (Shwapno Supermarket, Grameenphone Bill, Daraz POS, Pathao Courier) alongside corporate trade flows.',
      forensicProfile: 'Dynamic graph trust filtering strips benign high-frequency consumer retail noise (supermarket POS, telecom bills, courier charges) from corporate accounts, maintaining clear forensic visibility on trade remissions.',
      txCount: 4,
      totalExposure: '$37.90 (৳4,548 BDT)'
    },
    {
      id: 'cold_start_mule',
      title: 'Cold-Start Dormant Account Flare',
      typology: 'Mule Account / Instant Pass-Through',
      severity: 'High Tier 1',
      description: 'A dormant payroll account with 0 recent transactions suddenly receives and relays $38,400 (৳4.6M BDT) via RTGS within 6 minutes.',
      forensicProfile: 'Identifies sudden activation of dormant commercial payroll account receiving and relaying high-value RTGS wires ($38.4k / ৳4.61M BDT) within minutes with zero prior commercial trade baseline.',
      txCount: 1,
      totalExposure: '$38,400 (৳4.61M BDT)'
    }
  ];

  const handleInject = (scenarioId) => {
    setSelectedScenarioId(scenarioId);
    const results = injectScenario(scenarioId);
    setLastInjectedResults(results);
    setActiveTab('results');
  };

  return (
    <Dialog.Root open={isDemoToolsOpen} onOpenChange={setDemoToolsOpen}>
      <Dialog.Portal>
        {/* Dimmed backdrop */}
        <Dialog.Overlay className="fixed inset-0 z-50 bg-black/60 backdrop-blur-[2px] animate-fadeIn" />

        {/* Solid Opaque Dialog Body */}
        <Dialog.Content
          aria-describedby={undefined}
          className="fixed left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 z-50 w-[min(760px,94vw)] max-h-[85vh]
                     overflow-y-auto rounded-lg border border-border bg-popover text-foreground shadow-2xl p-5 focus:outline-none"
        >
          {/* Header */}
          <div className="flex items-start justify-between pb-3 border-b border-border">
            <div>
              <div className="flex items-center gap-2">
                <FlaskConical className="w-5 h-5 text-accent" />
                <Dialog.Title className="text-base font-semibold text-text">
                  Operational Typology &amp; Threat Simulator
                </Dialog.Title>
                <Badge variant="accent" size="sm">FIU Threat Engine</Badge>
              </div>
              <p className="text-xs text-text-2 mt-1">
                Simulate suspicious money laundering typologies across live banking rails to verify automated triage and hold execution.
              </p>
            </div>
            <Dialog.Close asChild>
              <button className="text-text-muted hover:text-text p-1 rounded hover:bg-surfaceHover transition-colors cursor-pointer">
                <X className="w-4 h-4" />
              </button>
            </Dialog.Close>
          </div>

          {/* Tab Bar */}
          <div className="flex items-center gap-2 border-b border-border pt-3 pb-2 text-xs font-medium">
            <button
              onClick={() => setActiveTab('scenarios')}
              className={`pb-1.5 px-1 border-b-2 transition-colors cursor-pointer ${
                activeTab === 'scenarios' 
                  ? 'border-accent text-accent font-semibold' 
                  : 'border-transparent text-text-muted hover:text-text'
              }`}
            >
              Select Typology Scenario ({SCENARIOS.length})
            </button>
            <button
              onClick={() => setActiveTab('results')}
              disabled={!lastInjectedResults}
              className={`pb-1.5 px-1 border-b-2 transition-colors cursor-pointer ${
                activeTab === 'results' 
                  ? 'border-accent text-accent font-semibold' 
                  : lastInjectedResults ? 'border-transparent text-text-muted hover:text-text' : 'border-transparent text-border cursor-not-allowed'
              }`}
            >
              Scoring Invariant Output {lastInjectedResults ? `(${lastInjectedResults.length} Txs)` : ''}
            </button>
          </div>

          {/* Tab Content */}
          <div className="mt-4">
            {activeTab === 'scenarios' ? (
              <div className="space-y-3">
                {SCENARIOS.map((sc) => (
                  <div
                    key={sc.id}
                    className="p-3.5 rounded-lg border border-border bg-surface hover:border-accent/60 transition-all flex flex-col justify-between gap-2.5"
                  >
                    <div>
                      <div className="flex items-center justify-between gap-2">
                        <div className="flex items-center gap-2">
                          <span className="font-semibold text-text text-sm">{sc.title}</span>
                          <Badge 
                            variant={sc.severity.includes('Critical') ? 'critical' : sc.severity.includes('High') ? 'critical' : 'neutral'} 
                            size="sm"
                          >
                            {sc.severity}
                          </Badge>
                        </div>
                        <span className="text-xs font-mono font-bold text-accent">{sc.totalExposure}</span>
                      </div>

                      <p className="text-xs text-text-2 mt-1 leading-relaxed">
                        {sc.description}
                      </p>

                      <div className="mt-2 p-2 rounded bg-bg border border-borderSubtle text-[11px] font-mono text-text-muted">
                        <span className="text-accent font-semibold block text-[10px] uppercase tracking-wider mb-0.5">
                          Forensic Detection Profile (BFIU / Regulatory Criteria)
                        </span>
                        {sc.forensicProfile}
                      </div>
                    </div>

                    <div className="flex items-center justify-between pt-1 border-t border-borderSubtle">
                      <span className="text-[11px] font-mono text-text-muted">
                        {sc.txCount} transactions • Real-Time Engine Triage
                      </span>
                      <Button
                        variant="primary"
                        size="sm"
                        onClick={() => handleInject(sc.id)}
                        icon={Zap}
                        className="text-xs bg-[#2563EB] hover:bg-[#1D4ED8] text-white font-semibold shadow-xs"
                      >
                        Simulate Scenario
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="space-y-4">
                {/* Injection summary banner */}
                <div className="p-3 rounded-lg bg-cleared-bg/40 border border-cleared text-xs text-text flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-cleared shrink-0" />
                    <span>
                      Successfully simulated and triaged {lastInjectedResults?.length || 0} events. Live telemetry updated.
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => {
                        setDemoToolsOpen(false);
                        navigate('alerts');
                      }}
                      className="text-xs h-7"
                    >
                      View in Alerts
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => {
                        setDemoToolsOpen(false);
                        navigate('network');
                      }}
                      className="text-xs h-7"
                    >
                      View in Network
                    </Button>
                  </div>
                </div>

                {/* Scored transaction rows */}
                <div className="space-y-2">
                  {lastInjectedResults?.map((tx) => (
                    <div
                      key={tx.id}
                      className="p-3 rounded border border-border bg-surface text-xs font-mono space-y-2"
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <span className="font-bold text-accent">{tx.id}</span>
                          <span className="text-text">{tx.sourceEntity}</span>
                          <ArrowRight className="w-3 h-3 text-text-muted" />
                          <span className="text-text">{tx.targetEntity}</span>
                        </div>
                        <span className="font-bold text-text">${Number(tx.amount).toLocaleString()}</span>
                      </div>

                      <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 pt-1 border-t border-borderSubtle text-[11px]">
                        <div>
                          <span className="text-text-muted block text-[10px]">DISPOSITION</span>
                          <span className="font-bold text-text">
                            {tx.conformalSet.includes('Illicit') ? 'Tier 1 Quarantine' : 'Tier 3 Clear'}
                          </span>
                        </div>
                        <div>
                          <span className="text-text-muted block text-[10px]">RISK SCORE</span>
                          <span className="font-bold text-critical">
                            {(tx.riskScore * 100).toFixed(1)}%
                          </span>
                        </div>
                        <div>
                          <span className="text-text-muted block text-[10px]">TRIAGE ACTION</span>
                          <span className="font-bold text-text truncate block">{tx.queueAction}</span>
                        </div>
                        <div>
                          <span className="text-text-muted block text-[10px]">DECISION SPEED</span>
                          <span className="font-bold text-cleared">{tx.latencyMs} ms</span>
                        </div>
                      </div>

                      {tx.reasons && tx.reasons.length > 0 && (
                        <div className="text-[10px] text-text-2 bg-bg p-1.5 rounded">
                          <span className="font-semibold text-text">Typology Triggers: </span>
                          {tx.reasons.join(' | ')}
                        </div>
                      )}
                    </div>
                  ))}
                </div>

                <div className="flex justify-end pt-2">
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={() => setActiveTab('scenarios')}
                  >
                    Back to Scenarios
                  </Button>
                </div>
              </div>
            )}
          </div>
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
};
