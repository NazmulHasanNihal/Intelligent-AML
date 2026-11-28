'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { ArrowRight, ExternalLink } from 'lucide-react';

const SAMPLE_QUEUE = [
  {
    id: 'ALT-994821',
    entity: 'Meghna Industrial & Agro Ltd',
    rail: 'SWIFT MT700',
    amountUsd: '$48,500.00',
    amountBdt: '৳58,20,000',
    setLabel: 'Γ = {1}',
    tierStyle: 'text-tier-1-text bg-tier-1-bg border-tier-1-border',
    action: 'Settlement Hold',
    href: '/triage?alertId=ALT-994821&inspect=true',
  },
  {
    id: 'ALT-994824',
    entity: 'Delta River Logistics Agency',
    rail: 'Cash / BEFTN',
    amountUsd: '$7,950.00',
    amountBdt: '৳9,54,000',
    setLabel: 'Γ = {1}',
    tierStyle: 'text-tier-1-text bg-tier-1-bg border-tier-1-border',
    action: 'Cash Structuring',
    href: '/triage?alertId=ALT-994824&inspect=true',
  },
  {
    id: 'ALT-771204',
    entity: 'Apex Footwear Corporate Payroll',
    rail: 'ISO 20022 RTGS',
    amountUsd: '$218,400.00',
    amountBdt: '৳2,62,08,000',
    setLabel: 'Γ = {0}',
    tierStyle: 'text-tier-3-text bg-tier-3-bg border-tier-3-border',
    action: 'Auto-Cleared',
    href: '/triage?tier=tier3',
  },
];

export const ProductVisualPreview: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'TRIAGE' | 'GRAPH'>('TRIAGE');
  const [selectedNode, setSelectedNode] = useState<'MEGHNA' | 'CUSTOMS' | 'GULFSTAR'>('MEGHNA');

  const nodeDetails = {
    MEGHNA: {
      title: 'Meghna Industrial & Agro Ltd (Applicant)',
      bic: 'EBLBBDDH — Eastern Bank PLC',
      metric: 'Pass-through Φ = 0.998 · Risk 0.984',
      summary: '94% of LC drawdown funds dispersed offshore within 15 minutes across 3 intermediaries.',
    },
    CUSTOMS: {
      title: 'Chittagong Custom House (ASYCUDA #C-1882910)',
      bic: 'HS 5201.00 · Raw Combed Cotton',
      metric: 'Valuation Delta +333.7% ($42.50 vs $9.80/kg)',
      summary: 'Declared commercial invoice exceeds ASYCUDA tariff benchmark by +333.7% on $48,500 MT700 LC.',
    },
    GULFSTAR: {
      title: 'Gulf Star Commodities FZE (Beneficiary)',
      bic: 'EBILAEAD — JAFZA Free Zone, Dubai',
      metric: 'Edge Gate ĝ_ij = 0.91 · 2-Hop Sink',
      summary: 'AIS vessel telemetry shows port diversion to Jebel Ali without declared origin verification.',
    },
  }[selectedNode];

  return (
    <div className="w-full rounded-xl bg-panel border border-line overflow-hidden text-fg">
      <div className="px-4 py-2.5 bg-surface border-b border-line flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <span className="text-xs font-mono text-muted">
            intelligent-aml.workspace
          </span>
          <div className="flex items-center bg-panel p-0.5 rounded-lg border border-line text-xs font-mono">
            <button
              type="button"
              onClick={() => setActiveTab('TRIAGE')}
              className={`px-2.5 py-1 rounded-md cursor-pointer transition-colors ${
                activeTab === 'TRIAGE' ? 'bg-surface-2 text-fg font-semibold' : 'text-muted hover:text-fg'
              }`}
            >
              Alert Queue
            </button>
            <button
              type="button"
              onClick={() => setActiveTab('GRAPH')}
              className={`px-2.5 py-1 rounded-md cursor-pointer transition-colors ${
                activeTab === 'GRAPH' ? 'bg-surface-2 text-fg font-semibold' : 'text-muted hover:text-fg'
              }`}
            >
              Flow Topology
            </button>
          </div>
        </div>

        <Link
          href="/app"
          className="text-xs font-mono font-semibold text-accent-text hover:underline flex items-center gap-1"
        >
          <span>Open Live Console</span>
          <ArrowRight className="w-3.5 h-3.5" aria-hidden="true" />
        </Link>
      </div>

      {activeTab === 'TRIAGE' ? (
        <div className="p-4 sm:p-5 space-y-3">
          <div className="flex flex-wrap items-center justify-between gap-2 text-xs font-mono text-muted pb-2 border-b border-line">
            <span>24h Sample Feed · Split Conformal Threshold α = 0.01</span>
            <span className="text-tier-3-text font-medium">84.2% benign volume cleared automatically</span>
          </div>

          <div className="divide-y divide-line border border-line rounded-lg overflow-hidden bg-canvas">
            <div className="grid grid-cols-12 gap-2 px-3 py-2 text-xs font-mono text-muted bg-surface">
              <span className="col-span-2">Alert</span>
              <span className="col-span-4">Entity &amp; Rail</span>
              <span className="col-span-2 text-right">Exposure</span>
              <span className="col-span-2 text-center">Set</span>
              <span className="col-span-2 text-right">Disposition</span>
            </div>

            {SAMPLE_QUEUE.map((row) => (
              <Link
                key={row.id}
                href={row.href}
                className="grid grid-cols-12 gap-2 items-center px-3 py-2.5 text-xs hover:bg-panel transition-colors group"
              >
                <span className="col-span-2 font-mono font-semibold text-fg group-hover:text-accent-text transition-colors">
                  {row.id}
                </span>
                <div className="col-span-4 min-w-0">
                  <div className="text-fg font-medium truncate">{row.entity}</div>
                  <div className="text-xs font-mono text-muted truncate">{row.rail}</div>
                </div>
                <div className="col-span-2 text-right font-mono tabular-aml">
                  <div className="text-fg">{row.amountUsd}</div>
                  <div className="text-xs text-muted">{row.amountBdt}</div>
                </div>
                <div className="col-span-2 text-center">
                  <span className={`inline-block px-2 py-0.5 rounded-full text-xs font-mono border ${row.tierStyle}`}>
                    {row.setLabel}
                  </span>
                </div>
                <div className="col-span-2 text-right flex items-center justify-end gap-1.5 text-xs font-mono text-fg-secondary">
                  <span className="hidden sm:inline">{row.action}</span>
                  <ExternalLink className="w-3 h-3 text-muted group-hover:text-fg" aria-hidden="true" />
                </div>
              </Link>
            ))}
          </div>
        </div>
      ) : (
        <div className="p-4 sm:p-5 space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-2 text-xs font-mono text-muted">
            <span>Case Investigation Subgraph: CASE-2026-0881 (LC-2026-CTG-88912)</span>
            <span>Click a node to inspect telemetry</span>
          </div>

          <div className="rounded-lg border border-line bg-canvas p-4">
            <svg viewBox="0 0 680 180" className="w-full h-44" role="img" aria-label="Directional TBML transaction flow graph">
              <defs>
                <marker id="arrow-red" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 1 L 10 5 L 0 9 z" fill="#EF4444" />
                </marker>
                <marker id="arrow-amber" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 1 L 10 5 L 0 9 z" fill="#F59E0B" />
                </marker>
              </defs>

              <path d="M 185 90 C 235 90, 245 55, 290 55" stroke="#F59E0B" strokeWidth="2" fill="none" markerEnd="url(#arrow-amber)" />
              <path d="M 415 55 C 460 55, 470 90, 515 90" stroke="#EF4444" strokeWidth="2" strokeDasharray="4 3" fill="none" markerEnd="url(#arrow-red)" />
              <path d="M 185 98 L 515 98" stroke="#EF4444" strokeWidth="2.5" fill="none" markerEnd="url(#arrow-red)" />

              <text x="345" y="122" textAnchor="middle" fill="#EF4444" fontSize="11" fontFamily="monospace">
                MT700 Wire · $48,500 USD (ĝ=0.91)
              </text>
              <text x="235" y="60" textAnchor="middle" fill="#D97706" fontSize="10" fontFamily="monospace">
                BoE #C-1882910
              </text>

              <g onClick={() => setSelectedNode('MEGHNA')} className="cursor-pointer">
                <rect
                  x="20"
                  y="62"
                  width="165"
                  height="56"
                  rx="8"
                  fill={selectedNode === 'MEGHNA' ? 'var(--color-surface-2)' : 'var(--color-panel)'}
                  stroke={selectedNode === 'MEGHNA' ? '#EF4444' : 'var(--color-line-strong)'}
                  strokeWidth="1.5"
                />
                <text x="32" y="84" fill="var(--color-fg)" fontSize="11" fontWeight="bold" fontFamily="sans-serif">
                  Meghna Industrial (BD)
                </text>
                <text x="32" y="102" fill="var(--color-muted)" fontSize="10" fontFamily="monospace">
                  EBLBBDDH · Score 0.984
                </text>
              </g>

              <g onClick={() => setSelectedNode('CUSTOMS')} className="cursor-pointer">
                <rect
                  x="295"
                  y="24"
                  width="120"
                  height="52"
                  rx="8"
                  fill={selectedNode === 'CUSTOMS' ? 'var(--color-surface-2)' : 'var(--color-panel)'}
                  stroke={selectedNode === 'CUSTOMS' ? '#F59E0B' : 'var(--color-line-strong)'}
                  strokeWidth="1.5"
                />
                <text x="307" y="45" fill="var(--color-fg)" fontSize="11" fontWeight="bold" fontFamily="sans-serif">
                  ASYCUDA Customs
                </text>
                <text x="307" y="61" fill="var(--color-tier-2-text)" fontSize="10" fontFamily="monospace">
                  +333.7% Over-Inv
                </text>
              </g>

              <g onClick={() => setSelectedNode('GULFSTAR')} className="cursor-pointer">
                <rect
                  x="520"
                  y="62"
                  width="145"
                  height="56"
                  rx="8"
                  fill={selectedNode === 'GULFSTAR' ? 'var(--color-surface-2)' : 'var(--color-panel)'}
                  stroke={selectedNode === 'GULFSTAR' ? '#EF4444' : 'var(--color-line-strong)'}
                  strokeWidth="1.5"
                />
                <text x="532" y="84" fill="var(--color-fg)" fontSize="11" fontWeight="bold" fontFamily="sans-serif">
                  Gulf Star FZE (AE)
                </text>
                <text x="532" y="102" fill="var(--color-muted)" fontSize="10" fontFamily="monospace">
                  EBILAEAD · JAFZA
                </text>
              </g>
            </svg>

            <div className="mt-3 pt-3 border-t border-line flex flex-wrap items-center justify-between gap-2 text-xs">
              <div>
                <div className="font-semibold text-fg">{nodeDetails.title}</div>
                <div className="text-muted text-xs mt-0.5">{nodeDetails.summary}</div>
              </div>
              <div className="text-right font-mono text-xs">
                <div className="text-accent-text">{nodeDetails.metric}</div>
                <div className="text-muted">{nodeDetails.bic}</div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
