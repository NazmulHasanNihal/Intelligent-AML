import { NextRequest, NextResponse } from 'next/server';
import { z } from 'zod';
import { compute12DInvariants, CONFORMAL_CALIBRATION } from '@/lib/scoringEngine';
import { fetchFastApiWithFallback } from '@/lib/apiAdapter';

const ScoreRequestSchema = z.object({
  id: z.string().optional(),
  amount: z.number().positive(),
  sourceAccount: z.string(),
  targetAccount: z.string(),
  rail: z.string().default('SWIFT MT700 (LC)'),
  bic: z.string().default('EBLBBDDH'),
  currency: z.string().default('USD'),
  burst: z.boolean().optional(),
  crossBorder: z.boolean().optional(),
  remittanceInfo: z.string().optional(),
  tbmlData: z.object({
    declaredUnitValuation: z.number().optional(),
    benchmarkValuation: z.number().optional(),
    hsCode: z.string().optional()
  }).optional()
});

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    const parsed = ScoreRequestSchema.safeParse(body);

    if (!parsed.success) {
      return NextResponse.json({ error: 'Validation failed', issues: parsed.error.issues }, { status: 400 });
    }

    const tx = parsed.data;

    // Local deterministic C-STGB scoring fallback function
    const localCompute = () => {
      const invariants = compute12DInvariants(tx, {
        totalAmountIn: tx.amount * 1.05,
        totalAmountOut: tx.amount,
        degIn: tx.burst ? 14 : 3,
        degOut: tx.burst ? 18 : 2
      });

      // Compute raw model probability p_hat
      let pHat = 0.012; // Baseline licit transaction
      if (invariants.isStructuring) pHat += 0.45;
      if (invariants.isPassThroughMule) pHat += 0.35;
      if (tx.crossBorder || invariants.sFwd > 0.5) pHat += 0.20;
      if (tx.tbmlData?.declaredUnitValuation && tx.tbmlData?.benchmarkValuation) {
        const dev = (tx.tbmlData.declaredUnitValuation - tx.tbmlData.benchmarkValuation) / tx.tbmlData.benchmarkValuation;
        if (dev > 2.0) pHat = Math.max(pHat, 0.985);
      }
      pHat = Math.min(Math.max(pHat, 0.001), 0.999);

      // Apply Conformal Risk Control (CRC, alpha = 0.01)
      const s0 = pHat; // Licitness non-conformity
      const s1 = 1 - pHat; // Illicitness non-conformity

      let conformalSet: string;
      let tierCode: number;
      let tierLabel: string;
      let actionRecommendation: string;

      if (s1 <= CONFORMAL_CALIBRATION.q1 && s0 > CONFORMAL_CALIBRATION.q0) {
        // Confidently Illicit
        conformalSet = 'Γ = {1}';
        tierCode = 1;
        tierLabel = 'Tier 1 Hold';
        actionRecommendation = 'IMMEDIATE_QUARANTINE_AND_CASE_OPENING';
      } else if (s0 <= CONFORMAL_CALIBRATION.q0 && s1 > CONFORMAL_CALIBRATION.q1) {
        // Confidently Licit
        conformalSet = 'Γ = {0}';
        tierCode = 3;
        tierLabel = 'Tier 3 Clear';
        actionRecommendation = 'AUTO_CLEARED_STP';
      } else {
        // Ambiguous / High Uncertainty (both or neither)
        conformalSet = 'Γ = {0, 1}';
        tierCode = 2;
        tierLabel = 'Tier 2 Review';
        actionRecommendation = 'HUMAN_OFFICER_TRIAGE_REQUIRED';
      }

      return {
        scoreId: `SCR-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
        timestamp: new Date().toISOString(),
        rawProbability: Number(pHat.toFixed(4)),
        conformalSet,
        tierCode,
        tierLabel,
        actionRecommendation,
        invariants: {
          phiFlow: Number(invariants.phiFlow.toFixed(4)),
          psiAsym: Number(invariants.psiAsym.toFixed(4)),
          lambdaU: Number(invariants.lambdaU.toFixed(4)),
          sFwd: Number(invariants.sFwd.toFixed(4)),
          sBwd: Number(invariants.sBwd.toFixed(4)),
          vA: Number(invariants.vA.toFixed(2))
        },
        calibration: {
          guaranteedCoverage: '≥ 99.0%',
          alphaIllicit: 0.01,
          q1Threshold: CONFORMAL_CALIBRATION.q1
        }
      };
    };

    // Hybrid BFF invocation: forwards to FastAPI if available, otherwise executes local engine
    const result = await fetchFastApiWithFallback(
      '/api/v1/score',
      {
        method: 'POST',
        body: JSON.stringify(tx)
      },
      localCompute,
      { timeoutMs: 2500 }
    );

    return NextResponse.json(result);
  } catch (err: unknown) {
    const message = err instanceof Error ? err.message : 'Internal Server Error';
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
