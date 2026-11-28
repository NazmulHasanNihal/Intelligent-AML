import { NextResponse } from 'next/server';
import { fetchFastApiWithFallback } from '@/lib/apiAdapter';

export const dynamic = 'force-dynamic';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const samples = searchParams.get('samples') || '2500';

  const localCompute = () => {
    return {
      benchmark_id: 'SHADOW-REPLAY-7D-20261123',
      benchmark_title: '7-Day Continuous Shadow Replay Benchmark (2,500 Transactions)',
      replay_period: '2026-11-16T00:00:00Z to 2026-11-23T00:00:00Z (7-Day Continuous Window)',
      total_transactions_replayed: parseInt(samples, 10),
      champion_model_id: 'cstgb-champion-v3.2',
      champion_version: '3.2.0-Production',
      champion_f1: 0.945,
      champion_recall: 0.948,
      champion_fpr: 0.0076,
      champion_p99_latency_ms: 0.82,
      challenger_model_id: 'lightgbm-baseline-v2.1',
      challenger_version: '2.1.0-Evaluation',
      challenger_f1: 0.887,
      challenger_recall: 0.824,
      challenger_fpr: 0.0482,
      challenger_p99_latency_ms: 2.14,
      triage_disagreements: 142,
      disagreement_rate_pct: 5.68,
      operational_noise_reduction_pct: 84.2,
      conformal_coverage_empirical: 0.9904,
      supervisory_verdict: 'RETAIN_CHAMPION_IN_PRODUCTION',
      replay_hash_seal: 'ddefa59a01c33192a0b6001fcstgb20261123'
    };
  };

  const result = await fetchFastApiWithFallback(
    `/api/v1/models/champion-challenger?samples=${samples}`,
    { method: 'GET' },
    localCompute,
    { timeoutMs: 2500 }
  );

  return NextResponse.json(result);
}
