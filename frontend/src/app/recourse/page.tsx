'use client';

import React, { useMemo, useState } from 'react';
import Link from 'next/link';
import {
  AlertTriangle,
  ArrowRight,
  CheckCircle2,
  Copy,
  Lock,
  ShieldAlert,
  SlidersHorizontal,
} from 'lucide-react';
import {
  Badge,
  BentoGrid,
  Button,
  Card,
  CardHeader,
  KpiTile,
  PageHeader,
  RiskPill,
  Slider,
} from '@/components/ui';
import { useBankingStore } from '@/lib/store';
import { JURISDICTIONS } from '@/lib/compliance/jurisdictions';
import { scanTextForTippingOff } from '@/lib/compliance/tippingOff';

export default function AnalystSensitivityRecoursePage() {
  const { activeJurisdiction, addToast, logAuditAction, currentBanker } = useBankingStore();
  const jur = JURISDICTIONS[activeJurisdiction] || JURISDICTIONS.BD_BFIU;

  // Counterfactual internal calibration sliders (Analyst-only sensitivity modeling)
  const [phiFlow, setPhiFlow] = useState(0.99);
  const [burstVelocity, setBurstVelocity] = useState(4.8);
  const [asycudaDeviation, setAsycudaDeviation] = useState(334);
  const [holdingHours, setHoldingHours] = useState(1);

  const [customerNoticeDraft, setCustomerNoticeDraft] = useState(
    'Routine commercial documentation refresh: please submit certified commercial invoice and packing list within 5 banking days.'
  );

  const simulatedRisk = useMemo(() => {
    const flowWeight = phiFlow * 0.35;
    const burstWeight = Math.min(1, burstVelocity / 6) * 0.25;
    const tbmlWeight = Math.min(1, asycudaDeviation / 350) * 0.30;
    const holdDampening = Math.min(0.25, (holdingHours / 72) * 0.25);
    return Number(Math.max(0.02, Math.min(0.99, flowWeight + burstWeight + tbmlWeight - holdDampening + 0.08)).toFixed(3));
  }, [phiFlow, burstVelocity, asycudaDeviation, holdingHours]);

  const simulatedTier: 1 | 2 | 3 = simulatedRisk >= 0.812 ? 1 : simulatedRisk >= 0.185 ? 2 : 3;
  const tippingScan = scanTextForTippingOff(customerNoticeDraft);

  const handleCopySafeNotice = async () => {
    if (tippingScan.containsTippingOff) {
      addToast(
        'Anti-Tipping-Off Block Triggered',
        `Prohibited terms detected (${tippingScan.matchedPhrases.join(', ')}). Customer notice blocked.`,
        'critical'
      );
      return;
    }
    try {
      await navigator.clipboard.writeText(customerNoticeDraft);
    } catch {
      /* ignore */
    }
    await logAuditAction(
      'ANALYST_SENSITIVITY_SIMULATED',
      `Simulated sensitivity counterfactual risk=${simulatedRisk} (Tier ${simulatedTier}) and verified neutral commercial notice.`,
      'ALT-994821',
      currentBanker.name
    );
    addToast('Neutral Commercial Notice Copied', 'Verified clean under anti-tipping-off scanner.', 'success');
  };

  return (
    <div className="mx-auto max-w-6xl px-4 sm:px-6 py-6 space-y-6">
      <PageHeader
        eyebrow="Analyst Eyes Only · Module 10 Companion"
        icon={SlidersHorizontal}
        title="Internal Analyst Sensitivity & False-Positive Calibration"
        subtitle="Test model counterfactual sensitivity while keeping customer AML suspicion strictly sealed."
        actions={
          <Link href="/rules">
            <Button variant="outline" size="sm" icon={ArrowRight}>
              Rule Studio
            </Button>
          </Link>
        }
      />

      {/* Non-Negotiable Anti-Tipping-Off Lock Banner */}
      <div
        role="alert"
        className="rounded-xl border border-tier-1-border bg-tier-1-bg p-4 flex items-start gap-3"
      >
        <Lock className="w-5 h-5 text-tier-1-text shrink-0 mt-0.5" aria-hidden="true" />
        <div className="space-y-1 text-sm">
          <p className="font-semibold text-fg">
            Anti-Tipping-Off Lock Active — Analyst Eyes Only ({jur.antiTippingOffStatute})
          </p>
          <p className="text-xs text-fg-secondary">
            Customer-facing AML decision disclosures, conformal scores, or risk explanations are strictly prohibited by law. External customer outreach may only use neutral commercial KYC documentation requests.
          </p>
        </div>
      </div>

      <BentoGrid columns={3}>
        <KpiTile
          label="Simulated Posterior Risk"
          value={simulatedRisk.toFixed(3)}
          note={simulatedTier === 1 ? 'Set Γ = {1}' : simulatedTier === 2 ? 'Set Γ = {0, 1}' : 'Set Γ = {0}'}
          tone={simulatedTier === 1 ? 'tier1' : simulatedTier === 2 ? 'tier2' : 'tier3'}
          badge={<RiskPill tier={simulatedTier} />}
        />
        <KpiTile
          label="Tier 3 Empirical FNR Bound"
          value="0.76%"
          note="Bounded FNR <= alpha = 0.01"
          tone="tier3"
          icon={CheckCircle2}
        />
        <KpiTile
          label="Active Statutory Regime"
          value={jur.shortCode}
          note={jur.sarSchemaVersion}
          tone="accent"
          icon={ShieldAlert}
        />
      </BentoGrid>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <Card>
          <CardHeader
            title="Internal Counterfactual Calibration (ALT-994821 Baseline)"
            subtitle="Adjust 12D invariant values internally to audit decision boundary stability."
          />
          <div className="pt-4 space-y-4">
            <Slider
              label="Pass-Through Mass Balance (Phi Flow)"
              min={0.05}
              max={1}
              step={0.01}
              value={phiFlow}
              onChange={setPhiFlow}
              valueLabel={phiFlow.toFixed(2)}
            />
            <Slider
              label="Hawkes Arrival Burst Multiplier (lambda)"
              min={0.1}
              max={6}
              step={0.1}
              value={burstVelocity}
              onChange={setBurstVelocity}
              valueLabel={`${burstVelocity.toFixed(1)}/hr`}
            />
            <Slider
              label="ASYCUDA Unit-Price Divergence (%)"
              min={0}
              max={400}
              step={5}
              value={asycudaDeviation}
              onChange={setAsycudaDeviation}
              valueLabel={`+${asycudaDeviation}%`}
            />
            <Slider
              label="Counterparty Liquidity Holding Window (hours)"
              min={0}
              max={72}
              step={2}
              value={holdingHours}
              onChange={setHoldingHours}
              valueLabel={`${holdingHours}h`}
            />
            <div className="pt-2 flex flex-wrap gap-2">
              <Button
                variant="secondary"
                size="sm"
                onClick={() => {
                  setPhiFlow(0.99);
                  setBurstVelocity(4.8);
                  setAsycudaDeviation(334);
                  setHoldingHours(1);
                }}
              >
                Reset to ALT-994821 ($48,500 TBML)
              </Button>
              <Button
                variant="subtle"
                size="sm"
                onClick={() => {
                  setPhiFlow(0.22);
                  setBurstVelocity(0.4);
                  setAsycudaDeviation(10);
                  setHoldingHours(60);
                }}
              >
                Simulate Licit Commercial Trade
              </Button>
            </div>
          </div>
        </Card>

        <Card>
          <CardHeader
            title="Neutral Commercial Documentation Request Builder"
            subtitle="Scanned continuously against prohibited AML/STR terms before outbound dispatch."
            badge={
              tippingScan.containsTippingOff ? (
                <Badge variant="tier1">Tipping-Off Violation</Badge>
              ) : (
                <Badge variant="tier3">Neutral &amp; Compliant</Badge>
              )
            }
          />
          <div className="pt-4 space-y-4">
            <textarea
              rows={5}
              value={customerNoticeDraft}
              onChange={(e) => setCustomerNoticeDraft(e.target.value)}
              aria-label="Commercial documentation request draft"
              className="w-full rounded-lg border border-line bg-surface p-3 text-sm text-fg focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-accent"
            />
            {tippingScan.containsTippingOff && (
              <div className="rounded-lg border border-tier-1-border bg-tier-1-bg p-3 text-xs text-tier-1-text flex items-start gap-2">
                <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" aria-hidden="true" />
                <div>
                  Blocked terms: <strong>{tippingScan.matchedPhrases.join(', ')}</strong>. Never reference STR, SAR, FinCEN, BFIU, or AML scoring models.
                </div>
              </div>
            )}
            <div className="flex flex-wrap items-center justify-between gap-2">
              <Button
                variant="ghost"
                size="sm"
                onClick={() =>
                  setCustomerNoticeDraft(
                    'Routine commercial documentation refresh: please submit certified commercial invoice and packing list within 5 banking days.'
                  )
                }
              >
                Insert Safe Commercial Template
              </Button>
              <Button
                variant="primary"
                size="sm"
                icon={Copy}
                onClick={() => void handleCopySafeNotice()}
                disabled={tippingScan.containsTippingOff}
              >
                Verify &amp; Copy Commercial Notice
              </Button>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
