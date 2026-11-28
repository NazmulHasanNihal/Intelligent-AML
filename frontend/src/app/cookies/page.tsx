'use client';

import React from 'react';
import Link from 'next/link';
import { ArrowLeft, Cookie } from 'lucide-react';
import { Button, Card } from '@/components/ui';

export default function CookiePolicyPage() {
  return (
    <div className="mx-auto max-w-3xl px-4 sm:px-6 py-12 space-y-6">
      <div className="flex items-center justify-between gap-4">
        <Link href="/">
          <Button variant="ghost" size="sm" icon={ArrowLeft}>
            Back to overview
          </Button>
        </Link>
        <span className="rounded-full border border-tier-2-border bg-tier-2-bg px-3 py-1 text-xs font-mono text-tier-2-text">
          Strictly Necessary Only
        </span>
      </div>

      <Card className="space-y-4">
        <div className="flex items-center gap-2 text-accent-text text-xs font-mono">
          <Cookie className="w-4 h-4" aria-hidden="true" />
          <span>Zero Tracking &amp; Zero Advertising Cookies</span>
        </div>
        <h1 className="text-2xl font-semibold text-fg">Cookie &amp; Local Storage Notice</h1>
        <p className="text-sm text-muted">
          Summary of first-party browser state required to preserve role, theme, currency, and language selections.
        </p>

        <div className="space-y-3 text-sm text-fg-secondary pt-2 border-t border-line">
          <p><strong className="text-fg">aml_consent:</strong> Stores dismissal of the cookie banner (`SameSite=Strict`).</p>
          <p><strong className="text-fg">aml-theme / intelligent-aml-workspace-v3:</strong> Persists local Dark/Light theme, BDT/USD currency display, English/বাংলা locale, and sandbox case state exclusively inside your browser.</p>
          <p><strong className="text-fg">Third-Party Trackers:</strong> None. Zero external analytics, ads, or CDN beacons are loaded.</p>
        </div>
      </Card>
    </div>
  );
}
