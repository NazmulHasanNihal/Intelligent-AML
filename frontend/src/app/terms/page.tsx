'use client';

import React from 'react';
import Link from 'next/link';
import { ArrowLeft, Scale } from 'lucide-react';
import { Button, Card } from '@/components/ui';

export default function TermsOfUsePage() {
  return (
    <div className="mx-auto max-w-3xl px-4 sm:px-6 py-12 space-y-6">
      <div className="flex items-center justify-between gap-4">
        <Link href="/">
          <Button variant="ghost" size="sm" icon={ArrowLeft}>
            Back to overview
          </Button>
        </Link>
        <span className="rounded-full border border-tier-2-border bg-tier-2-bg px-3 py-1 text-xs font-mono text-tier-2-text">
          Draft Evaluation Terms · Pre-Production Review
        </span>
      </div>

      <Card className="space-y-4">
        <div className="flex items-center gap-2 text-accent-text text-xs font-mono">
          <Scale className="w-4 h-4" aria-hidden="true" />
          <span>Institutional Evaluation &amp; Maker-Checker Mandate</span>
        </div>
        <h1 className="text-2xl font-semibold text-fg">Terms of Institutional Evaluation</h1>
        <p className="text-sm text-muted">
          Evaluation notice governing synthetic sandbox usage and on-premises proof-of-concept deployments.
        </p>

        <div className="space-y-4 text-sm text-fg-secondary leading-relaxed pt-2 border-t border-line">
          <section className="space-y-1">
            <h2 className="text-base font-semibold text-fg">1. Research &amp; Evaluation Scope</h2>
            <p>
              Intelligent-AML Platform v3.0 is provided for AML/CFT algorithm validation, conformal triage benchmarking, and BFIU/FinCEN workflow evaluation.
            </p>
          </section>
          <section className="space-y-1">
            <h2 className="text-base font-semibold text-fg">2. Mandatory Human Ratification (4-Eyes)</h2>
            <p>
              Autonomous scoring outputs do not trigger irreversible account freezes or regulatory filings without independent maker-checker ratification by authorized compliance officers and the MLRO/CAMLCO.
            </p>
          </section>
          <section className="space-y-1">
            <h2 className="text-base font-semibold text-fg">3. No Statutory Certification Claim</h2>
            <p>
              This platform is an architectural research and evaluation system; outputs do not constitute legal advice or regulatory pre-certification by Bangladesh Bank, FinCEN, or AMLA.
            </p>
          </section>
        </div>
      </Card>
    </div>
  );
}
