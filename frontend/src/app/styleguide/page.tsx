'use client';

import React, { useState } from 'react';
import {
  Activity,
  CheckCircle2,
  Database,
  Layers,
  Moon,
  ShieldAlert,
  Sun,
} from 'lucide-react';
import {
  Badge,
  BentoGrid,
  BentoTile,
  Button,
  Card,
  CardHeader,
  DataTable,
  Dialog,
  Drawer,
  EmptyState,
  GlassPanel,
  Input,
  KpiTile,
  PageHeader,
  PiiText,
  RiskPill,
  SegmentedControl,
  Select,
  SkeletonCard,
  Slider,
  StatusPill,
  Stepper,
  Switch,
  Tabs,
  Tooltip,
} from '@/components/ui';
import { useTheme } from '@/lib/theme';

const SAMPLE_ROWS = [
  { id: 'ALT-994821', entity: 'Meghna Industrial & Agro Ltd', amount: '$48,500.00', tier: 1 as const, status: 'UNDER_INVESTIGATION' },
  { id: 'ALT-994824', entity: 'Delta River Logistics Agency', amount: '৳9,54,000', tier: 1 as const, status: 'PENDING_TRIAGE' },
  { id: 'ALT-994829', entity: 'Padma Textile Mills PLC', amount: '৳6,40,000', tier: 2 as const, status: 'UNDER_INVESTIGATION' },
  { id: 'ALT-994835', entity: 'Surma Export Syndicate', amount: '৳3,15,000', tier: 3 as const, status: 'FALSE_POSITIVE_DISMISSED' },
];

export default function StyleguidePage() {
  const { theme, setTheme } = useTheme();
  const [tab, setTab] = useState<'tokens' | 'controls' | 'data'>('tokens');
  const [segment, setSegment] = useState('BDT');
  const [switched, setSwitched] = useState(true);
  const [alphaVal, setAlphaVal] = useState(1);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [drawerOpen, setDrawerOpen] = useState(false);

  return (
    <div className="mx-auto max-w-6xl px-4 sm:px-6 py-6 space-y-6">
      <PageHeader
        eyebrow="Design system · noindex"
        icon={Layers}
        title="Intelligent-AML Design System"
        subtitle="Semantic Night Ledger dark and Federal Paper light primitives with AA contrast."
        actions={
          <div className="flex items-center gap-2">
            <Button
              variant="secondary"
              icon={theme === 'light' ? Moon : Sun}
              onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
            >
              {theme === 'light' ? 'Dark mode' : 'Light mode'}
            </Button>
            <Button variant="primary" onClick={() => setDialogOpen(true)}>
              Open Dialog
            </Button>
            <Button variant="outline" onClick={() => setDrawerOpen(true)}>
              Open Drawer
            </Button>
          </div>
        }
      />

      <Tabs
        value={tab}
        onChange={setTab}
        label="Styleguide sections"
        options={[
          { value: 'tokens', label: 'Palette & Typography' },
          { value: 'controls', label: 'Controls & Primitives' },
          { value: 'data', label: 'Tables, Steppers & Skeletons', count: SAMPLE_ROWS.length },
        ]}
      />

      {tab === 'tokens' && (
        <div className="space-y-6">
          <BentoGrid columns={4}>
            <KpiTile label="Macro F1 Score" value="94.5%" note="Benchmarked vs GBDT/TGN" tone="accent" icon={Activity} />
            <KpiTile label="Tier 1 Holds" value="12" note="SLA <= 60 min" tone="tier1" icon={ShieldAlert} />
            <KpiTile label="Tier 2 Queue" value="34" note="Analyst triage required" tone="tier2" icon={Database} />
            <KpiTile label="Conformal Coverage" value="99.04%" note="Bounded FNR <= 0.01" tone="tier3" icon={CheckCircle2} />
          </BentoGrid>

          <BentoGrid columns={3}>
            <BentoTile colSpan={2}>
              <CardHeader title="Semantic Color Matrix" subtitle="Adaptive CSS custom properties across Dark & Light" />
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 pt-4">
                {[
                  { name: 'Canvas', cls: 'bg-canvas border border-line text-fg' },
                  { name: 'Panel', cls: 'bg-panel border border-line text-fg' },
                  { name: 'Surface', cls: 'bg-surface border border-line text-fg' },
                  { name: 'Accent Pine', cls: 'bg-accent text-accent-fg' },
                  { name: 'Tier 1 Hold', cls: 'bg-tier-1-bg border border-tier-1-border text-tier-1-text' },
                  { name: 'Tier 2 Review', cls: 'bg-tier-2-bg border border-tier-2-border text-tier-2-text' },
                ].map((s) => (
                  <div key={s.name} className={`rounded-lg p-3 text-xs font-mono font-medium ${s.cls}`}>
                    {s.name}
                  </div>
                ))}
              </div>
            </BentoTile>

            <BentoTile>
              <CardHeader title="Typographic Scale" subtitle="Geist + JetBrains Mono + Noto Sans Bengali" />
              <div className="space-y-2 pt-3">
                <p className="text-2xl font-semibold text-fg">Display 24px Title</p>
                <p className="text-lg font-semibold text-fg">Section 18px Heading</p>
                <p className="text-sm text-fg-secondary">Body 14px operational text with ৳5,820,000.00 tabular numerals.</p>
                <p className="text-xs text-muted">Minimum 12px UI label (বাংলা ফন্ট প্রিভিউ: নির্বাহী নজরদারি)।</p>
              </div>
            </BentoTile>
          </BentoGrid>
        </div>
      )}

      {tab === 'controls' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <Card>
            <CardHeader title="Buttons, Pills & PII Masking" subtitle="Interactive button hierarchy and risk tier badges" />
            <div className="pt-4 space-y-4">
              <div className="flex flex-wrap gap-2">
                <Button variant="primary">Primary Action</Button>
                <Button variant="secondary">Secondary</Button>
                <Button variant="outline">Outline</Button>
                <Button variant="ghost">Ghost</Button>
                <Button variant="danger">Quarantine Hold</Button>
                <Button variant="subtle">Subtle</Button>
              </div>
              <div className="flex flex-wrap items-center gap-2">
                <RiskPill tier={1} />
                <RiskPill tier={2} />
                <RiskPill tier={3} />
                <StatusPill status="PENDING_FOUR_EYES" />
                <Badge variant="accent">BFIU goAML v4.2</Badge>
              </div>
              <div className="pt-1 text-xs text-muted flex items-center gap-3">
                <span>Masked PII demo:</span>
                <PiiText value="BD22-EBLB-4829-1092-8823" type="account" />
                <Tooltip content="60-second audited reveal">
                  <Badge variant="neutral">Audited</Badge>
                </Tooltip>
              </div>
            </div>
          </Card>

          <Card>
            <CardHeader title="Form Inputs, Switches & Sliders" subtitle="Accessible controls with visible focus states" />
            <div className="pt-4 space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <Input placeholder="Search account or BIC..." aria-label="Sample input" />
                <Select aria-label="Sample jurisdiction">
                  <option value="BD_BFIU">BD_BFIU (Bangladesh Bank)</option>
                  <option value="US_FINCEN">US_FINCEN (BSA)</option>
                  <option value="EU_AMLA">EU_AMLA (6AMLD)</option>
                </Select>
              </div>
              <div className="flex flex-wrap items-center justify-between gap-4">
                <SegmentedControl
                  label="Currency switcher sample"
                  value={segment}
                  onChange={setSegment}
                  options={[
                    { value: 'BDT', label: '৳ BDT' },
                    { value: 'USD', label: '$ USD' },
                  ]}
                />
                <div className="flex items-center gap-2 text-xs text-fg">
                  <Switch checked={switched} onCheckedChange={setSwitched} label="Sample switch" />
                  <span>Live Conformal Gate</span>
                </div>
              </div>
              <Slider
                label="Target error bound alpha (%)"
                min={1}
                max={5}
                step={0.5}
                value={alphaVal}
                onChange={setAlphaVal}
                valueLabel={`${alphaVal}%`}
              />
            </div>
          </Card>
        </div>
      )}

      {tab === 'data' && (
        <div className="space-y-6">
          <DataTable
            ariaLabel="Styleguide sample ledger"
            data={SAMPLE_ROWS}
            rowKey={(r) => r.id}
            columns={[
              { key: 'id', header: 'Alert ID', render: (r) => <span className="font-mono font-semibold">{r.id}</span> },
              { key: 'entity', header: 'Entity', render: (r) => r.entity },
              { key: 'amount', header: 'Amount', align: 'right', render: (r) => <span className="font-mono tabular-aml">{r.amount}</span> },
              { key: 'tier', header: 'Tier', render: (r) => <RiskPill tier={r.tier} /> },
              { key: 'status', header: 'Status', render: (r) => <StatusPill status={r.status} /> },
            ]}
          />

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <GlassPanel>
              <CardHeader title="Investigation Milestone Stepper" />
              <div className="pt-4">
                <Stepper
                  steps={[
                    { title: 'C-STGB Scoring & Tier Assignment', detail: 'Conformal prediction bounded risk', status: 'COMPLETE' },
                    { title: 'Officer Evidence Packet Review', detail: 'ASYCUDA unit price check pending sign-off', status: 'IN_PROGRESS' },
                    { title: 'MLRO Four-Eyes Ratification', detail: 'Awaiting independent checker seal', status: 'PENDING' },
                  ]}
                />
              </div>
            </GlassPanel>
            <div className="space-y-4">
              <SkeletonCard />
              <EmptyState title="Empty state preview" description="Uniform zero-data state across all modules." />
            </div>
          </div>
        </div>
      )}

      <Dialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        title="Four-Eyes Confirmation"
        description="Accessible modal container with Escape key and backdrop dismissal."
      >
        <p className="text-sm text-fg-secondary mb-4">
          All tokens adapt smoothly between Night Ledger dark mode and Federal Paper light mode.
        </p>
        <div className="flex justify-end gap-2">
          <Button variant="ghost" onClick={() => setDialogOpen(false)}>Cancel</Button>
          <Button variant="primary" onClick={() => setDialogOpen(false)}>Confirm</Button>
        </div>
      </Dialog>

      <Drawer
        open={drawerOpen}
        onClose={() => setDrawerOpen(false)}
        title="Forensic Inspector Drawer"
        subtitle="Right-anchored slide-over detail sheet"
      >
        <p className="text-sm text-fg-secondary">
          Supports keyboard Escape dismissal and semantic surface hierarchy without harsh color inversions.
        </p>
      </Drawer>
    </div>
  );
}
