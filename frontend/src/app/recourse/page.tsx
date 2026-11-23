'use client';

import React from 'react';
import Link from 'next/link';
import {
  ShieldAlert,
  AlertTriangle,
  Lock,
  ArrowRight,
  SlidersHorizontal,
  FileCheck2
} from 'lucide-react';

export default function CounterfactualRecourseRedirectPage() {
  return (
    <div className="p-6 max-w-[1200px] mx-auto space-y-6">
      <div className="p-8 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-2xl space-y-6">
        <div className="flex items-center gap-3 pb-4 border-b border-[#1E293B]">
          <div className="p-2.5 rounded-xl bg-amber-500/20 text-amber-400 border border-amber-500/30">
            <Lock className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-slate-100 font-sans">
              Statutory Anti-Tipping-Off Access Control
            </h1>
            <p className="text-xs text-slate-400 font-mono mt-0.5">
              Governed by Money Laundering Prevention Act 2012 § 6 &amp; Bank Secrecy Act 31 U.S.C. § 5318(g)(2)
            </p>
          </div>
        </div>

        <div className="p-4 bg-amber-950/20 border border-amber-800/40 rounded-xl space-y-2 text-xs text-amber-300">
          <div className="flex items-center gap-2 font-semibold">
            <AlertTriangle className="w-4 h-4 text-amber-400 shrink-0" />
            <span>Compliance Notice: Customer Adverse Action Coaching Prohibited</span>
          </div>
          <p className="leading-relaxed text-slate-300">
            In anti-money laundering and counter-terrorist financing operations, counterfactual sensitivity parameters (e.g. structuring windows, velocity thresholds, and pass-through ratios) cannot be disclosed to customers under penalty of criminal tipping-off statutes.
          </p>
          <p className="leading-relaxed text-slate-300">
            All rule sensitivity modeling, shadow-mode champion/challenger simulation, and institutional whitelisting have been consolidated into the secured <strong>Internal Analyst Compliance Rule Studio</strong>.
          </p>
        </div>

        <div className="flex items-center justify-between pt-2">
          <Link
            href="/"
            className="px-4 py-2 rounded-xl bg-[#1E293B] hover:bg-[#334155] text-slate-300 text-xs font-semibold transition-colors"
          >
            Return to Executive Overview
          </Link>

          <Link
            href="/rules"
            className="px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold flex items-center gap-2 transition-colors shadow-lg shadow-emerald-600/20"
          >
            <SlidersHorizontal className="w-4 h-4" />
            <span>Open Compliance Rule Studio</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </div>
    </div>
  );
}
