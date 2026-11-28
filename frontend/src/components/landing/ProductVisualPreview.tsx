'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { ArrowRight, ExternalLink, ShieldAlert, CheckCircle2, AlertTriangle } from 'lucide-react';

const SAMPLE_QUEUE = [
  {
    id: 'ALT-994821',
    entity: 'Meghna Industrial & Agro Ltd',
    rail: 'SWIFT MT700',
    amountUsd: '$945,000.00',
    amountBdt: '৳11,34,00,000',
    setLabel: 'Γ = {1}',
    tier: 'Tier 1 Hold',
    tierStyle: 'text-rose-400 bg-rose-500/10 border-rose-500/30',
    action: 'Settlement Hold',
    href: '/triage?alertId=ALT-994821&inspect=true'
  },
  {
    id: 'ALT-884012',
    entity: 'Tanvir MFS Merchant Hub',
    rail: 'bKash / Nagad Agent',
    amountUsd: '$7,950.00',
    amountBdt: '৳9,54,000',
    setLabel: 'Γ = {0, 1}',
    tier: 'Tier 2 Review',
    tierStyle: 'text-amber-400 bg-amber-500/10 border-amber-500/30',
    action: 'Analyst Queue',
    href: '/triage?tier=tier2'
  },
  {
    id: 'ALT-771204',
    entity: 'Apex Footwear Corporate Payroll',
    rail: 'ISO 20022 RTGS',
    amountUsd: '$218,400.00',
    amountBdt: '৳2,62,08,000',
    setLabel: 'Γ = {0}',
    tier: 'Tier 3 Clear',
    tierStyle: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30',
    action: 'Auto-Cleared',
    href: '/triage?tier=tier3'
  }
];

export const ProductVisualPreview: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'TRIAGE' | 'GRAPH'>('TRIAGE');
  const [selectedNode, setSelectedNode] = useState<'MEGHNA' | 'CUSTOMS' | 'GULFSTAR'>('MEGHNA');

  const nodeDetails = {
    MEGHNA: {
      title: 'Meghna Industrial & Agro Ltd (Applicant)',
      bic: 'EBLBBDDH — Eastern Bank PLC',
      metric: 'Pass-through Φ = 0.992 · Risk 0.942',
      summary: '94% of LC drawdown funds dispersed offshore within 15 minutes across 3 intermediaries.'
    },
    CUSTOMS: {
      title: 'Chittagong Custom House (ASYCUDA #C-1882910)',
      bic: 'HS 5205.12.00 · Combed Cotton Yarn',
      metric: 'Valuation Delta +333.7% ($9.45 vs $2.18/kg)',
      summary: 'Declared commercial invoice exceeds 90-day ASYCUDA tariff benchmark by $727,000 USD.'
    },
    GULFSTAR: {
      title: 'Gulf Star Commodities FZE (Beneficiary)',
      bic: 'EBILAEAD — JAFZA Free Zone, Dubai',
      metric: 'Edge Gate ĝ_ij = 0.91 · 2-Hop Sink',
      summary: 'AIS vessel telemetry shows port diversion to Jebel Ali without Port Klang discharge.'
    }
  }[selectedNode];

  return (
    <div className="w-full rounded-xl bg-panel border border-line overflow-hidden text-slate-200">
      {/* Window Header */}
      <div className="px-4 py-2.5 bg-canvas border-b border-line flex flex-wrap items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <span className="text-[11px] font-mono text-slate-400">
            intelligent-aml.workspace
          </span>
          <div className="flex items-center bg-panel p-0.5 rounded-md border border-line text-xs font-mono">
            <button
              type="button"
              onClick={() => setActiveTab('TRIAGE')}
              className={`px-2.5 py-1 rounded cursor-pointer transition-colors ${
                activeTab === 'TRIAGE' ? 'bg-surface-2 text-slate-100 font-semibold' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Alert Queue
            </button>
            <button
              type="button"
              onClick={() => setActiveTab('GRAPH')}
              className={`px-2.5 py-1 rounded cursor-pointer transition-colors ${
                activeTab === 'GRAPH' ? 'bg-surface-2 text-slate-100 font-semibold' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              Flow Topology
            </button>
          </div>
        </div>

        <Link
          href="/app"
          className="text-[11px] font-mono font-semibold text-emerald-400 hover:text-emerald-300 flex items-center gap-1"
        >
          <span>Open Live Console</span>
          <ArrowRight className="w-3 h-3" />
        </Link>
      </div>

      {activeTab === 'TRIAGE' ? (
        <div className="p-4 sm:p-5 space-y-3">
          <div className="flex flex-wrap items-center justify-between gap-2 text-[11px] font-mono text-slate-400 pb-2 border-b border-line">
            <span>24h Sample Feed · Split Conformal Threshold α = 0.01</span>
            <span className="text-emerald-400">84.2% benign volume cleared automatically</span>
          </div>

          <div className="divide-y divide-[#1E2734] border border-line rounded-lg overflow-hidden bg-canvas">
            <div className="grid grid-cols-12 gap-2 px-3 py-2 text-xs font-mono text-slate-500 bg-panel">
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
                <span className="col-span-2 font-mono font-semibold text-slate-200 group-hover:text-emerald-400 transition-colors">
                  {row.id}
                </span>
                <div className="col-span-4 min-w-0">
                  <div className="text-slate-100 font-medium truncate">{row.entity}</div>
                  <div className="text-xs font-mono text-slate-500 truncate">{row.rail}</div>
                </div>
                <div className="col-span-2 text-right font-mono tabular-nums">
                  <div className="text-slate-200">{row.amountUsd}</div>
                  <div className="text-xs text-slate-500">{row.amountBdt}</div>
                </div>
                <div className="col-span-2 text-center">
                  <span className={`inline-block px-2 py-0.5 rounded text-xs font-mono border ${row.tierStyle}`}>
                    {row.setLabel}
                  </span>
                </div>
                <div className="col-span-2 text-right flex items-center justify-end gap-1.5 text-xs font-mono text-slate-300">
                  <span className="hidden sm:inline">{row.action}</span>
                  <ExternalLink className="w-3 h-3 text-slate-500 group-hover:text-slate-200" />
                </div>
              </Link>
            ))}
          </div>
        </div>
      ) : (
        <div className="p-4 sm:p-5 space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-2 text-xs font-mono text-slate-400">
            <span>Case Investigation Subgraph: CASE-2026-0881 (LC-CTG-2026-9921)</span>
            <span>Click a node to inspect telemetry</span>
          </div>

          <div className="rounded-lg border border-line bg-canvas p-4">
            <svg viewBox="0 0 680 180" className="w-full h-44" role="img" aria-label="Directional TBML transaction flow graph">
              <defs>
                <marker id="arrow-red" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 1 L 10 5 L 0 9 z" fill="#f43f5e" />
                </marker>
                <marker id="arrow-amber" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                  <path d="M 0 1 L 10 5 L 0 9 z" fill="#f59e0b" />
                </marker>
              </defs>

              {/* Edges */}
              <path d="M 185 90 C 235 90, 245 55, 290 55" stroke="#f59e0b" strokeWidth="2" fill="none" markerEnd="url(#arrow-amber)" />
              <path d="M 415 55 C 460 55, 470 90, 515 90" stroke="#f43f5e" strokeWidth="2" strokeDasharray="4 3" fill="none" markerEnd="url(#arrow-red)" />
              <path d="M 185 98 L 515 98" stroke="#f43f5e" strokeWidth="2.5" fill="none" markerEnd="url(#arrow-red)" />

              {/* Edge Labels */}
              <text x="345" y="122" textAnchor="middle" fill="#fda4af" fontSize="10" fontFamily="monospace">
                MT700 Wire · $945,000 USD (ĝ=0.91)
              </text>
              <text x="235" y="60" textAnchor="middle" fill="#fcd34d" fontSize="9" fontFamily="monospace">
                BoE #C-1882910
              </text>

              {/* Node 1: Meghna */}
              <g onClick={() => setSelectedNode('MEGHNA')} className="cursor-pointer">
                <rect
                  x="20"
                  y="62"
                  width="165"
                  height="56"
                  rx="8"
                  fill={selectedNode === 'MEGHNA' ? '#192231' : '#0D121A'}
                  stroke={selectedNode === 'MEGHNA' ? '#f43f5e' : '#263244'}
                  strokeWidth="1.5"
                />
                <text x="32" y="84" fill="#f8fafc" fontSize="11" fontWeight="bold" fontFamily="sans-serif">
                  Meghna Industrial (BD)
                </text>
                <text x="32" y="102" fill="#94a3b8" fontSize="9.5" fontFamily="monospace">
                  EBLBBDDH · Score 0.942
                </text>
              </g>

              {/* Node 2: Customs */}
              <g onClick={() => setSelectedNode('CUSTOMS')} className="cursor-pointer">
                <rect
                  x="295"
                  y="24"
                  width="120"
                  height="52"
                  rx="8"
                  fill={selectedNode === 'CUSTOMS' ? '#192231' : '#0D121A'}
                  stroke={selectedNode === 'CUSTOMS' ? '#f59e0b' : '#263244'}
                  strokeWidth="1.5"
                />
                <text x="307" y="45" fill="#f8fafc" fontSize="10.5" fontWeight="bold" fontFamily="sans-serif">
                  ASYCUDA Customs
                </text>
                <text x="307" y="61" fill="#fbbf24" fontSize="9.5" fontFamily="monospace">
                  +333.7% Over-Inv
                </text>
              </g>

              {/* Node 3: Gulf Star */}
              <g onClick={() => setSelectedNode('GULFSTAR')} className="cursor-pointer">
                <rect
                  x="520"
                  y="62"
                  width="145"
                  height="56"
                  rx="8"
                  fill={selectedNode === 'GULFSTAR' ? '#192231' : '#0D121A'}
                  stroke={selectedNode === 'GULFSTAR' ? '#f43f5e' : '#263244'}
                  strokeWidth="1.5"
                />
                <text x="532" y="84" fill="#f8fafc" fontSize="11" fontWeight="bold" fontFamily="sans-serif">
                  Gulf Star FZE (AE)
                </text>
                <text x="532" y="102" fill="#94a3b8" fontSize="9.5" fontFamily="monospace">
                  EBILAEAD · JAFZA
                </text>
              </g>
            </svg>

            <div className="mt-3 pt-3 border-t border-line flex flex-wrap items-center justify-between gap-2 text-xs">
              <div>
                <div className="font-semibold text-slate-100">{nodeDetails.title}</div>
                <div className="text-slate-400 text-xs mt-0.5">{nodeDetails.summary}</div>
              </div>
              <div className="text-right font-mono text-xs">
                <div className="text-emerald-400">{nodeDetails.metric}</div>
                <div className="text-slate-500">{nodeDetails.bic}</div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
