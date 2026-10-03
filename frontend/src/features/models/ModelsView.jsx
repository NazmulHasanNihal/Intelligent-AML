import React, { useMemo } from 'react';
import ReactECharts from 'echarts-for-react';
import { 
  Cpu, 
  Scale, 
  Activity, 
  Download, 
  ShieldCheck, 
  CheckCircle2, 
  Zap, 
  Clock,
  Layers
} from 'lucide-react';
import { Card, CardHeader } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';

export const ModelsView = () => {
  // ACI Distribution Drift Tracker EChart
  const aciDriftOption = useMemo(() => ({
    animation: false,
    backgroundColor: 'transparent',
    tooltip: { trigger: 'axis' },
    legend: {
      data: ['KS Drift Distance D_KS', 'Calibrated Alpha α_t', 'Target α = 0.01'],
      bottom: 0,
      textStyle: { color: '#667085', fontSize: 11 }
    },
    grid: { left: '7%', right: '11%', top: '12%', bottom: '15%' },
    xAxis: {
      type: 'category',
      data: ['t=0', 't=10k', 't=20k', 't=30k', 't=40k (Peak)', 't=50k', 't=60k', 't=70k', 't=80k', 't=90k', 't=100k'],
      axisLabel: { color: '#667085', fontSize: 10, fontFamily: 'monospace' },
      axisLine: { lineStyle: { color: '#E4E7EC' } }
    },
    yAxis: [
      {
        type: 'value',
        name: 'D_KS Bound',
        min: 0,
        max: 0.25,
        splitLine: { lineStyle: { color: '#F2F4F7' } },
        axisLabel: { color: '#667085', fontSize: 10, fontFamily: 'monospace' },
        nameTextStyle: { color: '#667085', fontSize: 10 }
      },
      {
        type: 'value',
        name: 'Alpha α_t',
        min: 0.005,
        max: 0.020,
        splitLine: { show: false },
        axisLabel: { 
          color: '#667085', 
          fontSize: 10, 
          fontFamily: 'monospace',
          formatter: (v) => v.toFixed(3)
        },
        nameTextStyle: { color: '#667085', fontSize: 10, padding: [0, 0, 0, 15] }
      }
    ],
    series: [
      {
        name: 'KS Drift Distance D_KS',
        type: 'line',
        data: [0.012, 0.018, 0.142, 0.082, 0.168, 0.074, 0.041, 0.185, 0.062, 0.038, 0.024],
        itemStyle: { color: '#E8A23B' },
        lineStyle: { width: 2 }
      },
      {
        name: 'Calibrated Alpha α_t',
        type: 'line',
        yAxisIndex: 1,
        data: [0.010, 0.0102, 0.0078, 0.0089, 0.0072, 0.0094, 0.0098, 0.0069, 0.0092, 0.0099, 0.010],
        itemStyle: { color: '#2563EB' },
        lineStyle: { width: 2 }
      },
      {
        name: 'Target α = 0.01',
        type: 'line',
        yAxisIndex: 1,
        data: [0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
        lineStyle: { type: 'dashed', color: '#98A2B3', width: 1 }
      }
    ]
  }), []);

  const handleDownloadModelCard = () => {
    const card = {
      model: 'C-STGB Dual-Engine Graph Booster',
      version: '2.4.0-PROD',
      validation_standard: 'Federal Reserve SR 11-7 / OCC 2011-12',
      hardware_benchmark: {
        host: 'Dual Intel® Xeon® Platinum 8480+ @ 2.0GHz',
        accelerator: 'Nvidia Tensor Core T4 (16GB VRAM)',
        batch_size: 1,
        single_query_latency: '0.45 ms',
        two_hop_subgraph_expansion: '0.82 ms'
      },
      conformal_coverage: {
        target_alpha: 0.01,
        empirical_coverage: '99.04%',
        finite_sample_guarantee: 'At most 1.0% true positive cases missed on average.'
      }
    };
    const blob = new Blob([JSON.stringify(card, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'SR_11_7_Model_Card.json';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-4">
      {/* Top Banner */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 p-4 rounded-lg bg-surface border border-border">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-sm font-semibold text-text">Surveillance Engine Health &amp; Model Governance</h2>
            <Badge variant="cleared" size="sm">SR 11-7 Validated</Badge>
          </div>
          <p className="text-xs text-text-2 mt-0.5">
            Operational engine telemetry, clearing rail status, statistical calibration, and statutory model audit readiness.
          </p>
        </div>

        <Button
          variant="secondary"
          size="sm"
          onClick={handleDownloadModelCard}
          icon={Download}
        >
          Download Model Governance Pack (JSON)
        </Button>
      </div>

      {/* Production Engine & Clearing Rails Overview */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Active Production Engine */}
        <Card className="space-y-3">
          <div className="flex items-center justify-between pb-2 border-b border-borderSubtle">
            <div className="flex items-center gap-2">
              <Badge variant="cleared" size="sm">ACTIVE PRODUCTION ENGINE</Badge>
              <span className="font-mono text-xs text-text-muted">v2.4.0-PROD</span>
            </div>
            <span className="font-mono text-xs text-cleared font-semibold">100% Real-Time Flow</span>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-text">Spatio-Temporal Graph Surveillance Engine</h3>
            <p className="text-xs text-text-muted mt-0.5">Deep interbank graph convolutions with real-time transactional gating</p>
          </div>

          <div className="grid grid-cols-2 gap-2 p-2.5 rounded bg-bg border border-borderSubtle font-mono text-xs">
            <div>
              <span className="text-[10px] text-text-muted uppercase block">F1 Precision Score</span>
              <span className="font-bold text-accent text-sm">94.2%</span>
            </div>
            <div>
              <span className="text-[10px] text-text-muted uppercase block">PR-AUC Accuracy</span>
              <span className="font-bold text-accent text-sm">0.982</span>
            </div>
            <div>
              <span className="text-[10px] text-text-muted uppercase block">Triage Decision Speed</span>
              <span className="font-bold text-cleared text-sm">&lt; 0.45 ms</span>
            </div>
            <div>
              <span className="text-[10px] text-text-muted uppercase block">Safety Guarantee</span>
              <span className="font-bold text-cleared text-sm">&ge; 99.0% Coverage</span>
            </div>
          </div>
        </Card>

        {/* Operational Rail Connectors */}
        <Card className="space-y-3">
          <div className="flex items-center justify-between pb-2 border-b border-borderSubtle">
            <div className="flex items-center gap-2">
              <Badge variant="neutral" size="sm">CLEARING CONNECTORS</Badge>
              <span className="font-mono text-xs text-text-muted">4 Active Gateways</span>
            </div>
            <span className="font-mono text-xs text-cleared font-semibold">All Systems Normal</span>
          </div>

          <div>
            <h3 className="text-sm font-semibold text-text">Interbank Settlement &amp; Rail Gateways</h3>
            <p className="text-xs text-text-muted mt-0.5">Real-time webhook and ISO 20022 message parsers</p>
          </div>

          <div className="space-y-1.5 font-mono text-xs">
            <div className="flex items-center justify-between p-2 rounded bg-bg border border-borderSubtle">
              <span className="text-text font-medium">SWIFT Alliance (MT103 / MT700 LC)</span>
              <span className="text-cleared font-semibold text-[11px] flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-cleared" />
                ONLINE (0 dropped)
              </span>
            </div>
            <div className="flex items-center justify-between p-2 rounded bg-bg border border-borderSubtle">
              <span className="text-text font-medium">Bangladesh Bank RTGS Gateway</span>
              <span className="text-cleared font-semibold text-[11px] flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-cleared" />
                ONLINE (12ms ACK)
              </span>
            </div>
            <div className="flex items-center justify-between p-2 rounded bg-bg border border-borderSubtle">
              <span className="text-text font-medium">bKash &amp; Nagad MFS Webhook</span>
              <span className="text-cleared font-semibold text-[11px] flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-cleared" />
                ACTIVE (Listening)
              </span>
            </div>
          </div>
        </Card>
      </div>

      {/* Real-time Distribution Drift Tracker & Compliance Latency */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
        {/* ACI Drift Chart */}
        <Card className="lg:col-span-8 flex flex-col justify-between min-h-[360px]">
          <CardHeader
            title="Real-Time Typology Drift &amp; Recalibration Monitor"
            subtitle="Kolmogorov-Smirnov statistical shift tracking vs automated risk parameter adaptation"
            badge={<Badge variant="neutral" size="sm">Active Monitor</Badge>}
          />
          <div className="h-64 w-full mt-2">
            <ReactECharts 
              option={aciDriftOption} 
              notMerge={true} 
              lazyUpdate={true} 
              style={{ height: '100%', width: '100%' }} 
            />
          </div>
        </Card>

        {/* Settlement SLA Specifications */}
        <Card className="lg:col-span-4 flex flex-col justify-between">
          <div>
            <CardHeader
              title="Statutory Settlement SLAs"
              subtitle="Compliance turnaround under banking standards"
            />

            <div className="space-y-2 mt-3 text-xs font-mono">
              <div className="p-2.5 rounded bg-bg border border-borderSubtle flex justify-between">
                <span className="text-text-muted">ISO 20022 Turnaround:</span>
                <span className="font-semibold text-text">&lt; 50 ms Limit</span>
              </div>
              <div className="p-2.5 rounded bg-bg border border-borderSubtle flex justify-between">
                <span className="text-text-muted">Measured Engine Latency:</span>
                <span className="font-bold text-cleared">&lt; 0.45 ms</span>
              </div>
              <div className="p-2.5 rounded bg-bg border border-borderSubtle flex justify-between">
                <span className="text-text-muted">Tier 1 Hold SLA:</span>
                <span className="font-bold text-cleared">Immediate (0s)</span>
              </div>
              <div className="p-2.5 rounded bg-bg border border-borderSubtle flex justify-between">
                <span className="text-text-muted">BFIU Filing Target:</span>
                <span className="font-bold text-text">&le; 72 Hours</span>
              </div>
            </div>
          </div>

          <p className="text-[11px] text-text-muted leading-tight mt-3 pt-3 border-t border-borderSubtle">
            * Fully certified for pre-clearing transactional intervention across commercial banking rails.
          </p>
        </Card>
      </div>
    </div>
  );
};
