'use client';

import React from 'react';
import Link from 'next/link';
import { ArrowLeft, Shield } from 'lucide-react';
import { Button, Card } from '@/components/ui';

export default function PrivacyPolicyPage() {
  return (
    <div className="mx-auto max-w-3xl px-4 sm:px-6 py-12 space-y-6">
      <div className="flex items-center justify-between gap-4">
        <Link href="/">
          <Button variant="ghost" size="sm" icon={ArrowLeft}>
            Back to overview
          </Button>
        </Link>
        <span className="rounded-full border border-tier-2-border bg-tier-2-bg px-3 py-1 text-xs font-mono text-tier-2-text">
          Draft Governance Notice · Pre-Production Review
        </span>
      </div>

      <Card className="space-y-4">
        <div className="flex items-center gap-2 text-accent-text text-xs font-mono">
          <Shield className="w-4 h-4" aria-hidden="true" />
          <span>Data Residency &amp; Server-Side Privacy Governance</span>
        </div>
        <h1 className="text-2xl font-semibold text-fg">Privacy Policy &amp; Sovereign Data Residency</h1>
        <p className="text-sm text-muted">
          Aligned with Bangladesh Bank ICT Security Guidelines and Banking Companies Act 1991 § 46 confidentiality controls.
        </p>

        <div className="space-y-4 text-sm text-fg-secondary leading-relaxed pt-2 border-t border-line">
          <section className="space-y-1">
            <h2 className="text-base font-semibold text-fg">1. On-Premises Sovereign Boundary</h2>
            <p>
              When deployed in private intranet mode (<code className="font-mono text-xs bg-surface px-1.5 py-0.5 rounded">APP_MODE=onprem</code>), transaction payloads, watchlist lookups, and goAML XML packages stay inside the bank&apos;s private network with zero external egress.
            </p>
          </section>
          <section className="space-y-1">
            <h2 className="text-base font-semibold text-fg">2. Default PII Masking &amp; 60-Second Reveal Gate</h2>
            <p>
              National IDs, TINs, account numbers, and beneficial owner identifiers render masked by default. Every unmask event records the requesting officer, justification, and UTC timestamp to the tamper-evident hash chain and expires after 60 seconds.
            </p>
          </section>
          <section className="space-y-1">
            <h2 className="text-base font-semibold text-fg">3. Public Sandbox Telemetry</h2>
            <p>
              Public evaluation sessions operate exclusively on deterministic synthetic data with no real banking customers and strictly necessary session cookies.
            </p>
          </section>
        </div>
      </Card>
    </div>
  );
}
