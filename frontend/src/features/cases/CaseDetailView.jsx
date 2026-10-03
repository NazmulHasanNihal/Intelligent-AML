import React, { useState } from 'react';
import { 
  ArrowLeft, 
  Briefcase, 
  Clock, 
  ShieldCheck, 
  UserCheck, 
  FileText, 
  Share2, 
  Mail, 
  ShieldAlert, 
  CheckCircle2, 
  AlertTriangle, 
  Plus, 
  Send, 
  Lock, 
  Layers, 
  Check, 
  Paperclip, 
  UploadCloud, 
  File, 
  Pin, 
  PinOff,
  Sparkles,
  ExternalLink
} from 'lucide-react';
import { useAppStore } from '../../lib/store';
import { useAuth } from '../../context/AuthContext';
import { Card, CardHeader } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';

export const CaseDetailView = () => {
  const { 
    cases, 
    selectedCaseId, 
    navigate, 
    addCaseNote, 
    addCaseAttachment, 
    fourEyesSignOffCase, 
    addToast, 
    openFreezeNoticeModal,
    pinEvidence,
    unpinEvidence
  } = useAppStore();
  const { currentBanker } = useAuth();
  const [newNoteText, setNewNoteText] = useState('');
  const [approverError, setApproverError] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

  const activeCase = cases.find(c => c.id === selectedCaseId) || cases[0];

  if (!activeCase) {
    return (
      <div className="p-8 text-center text-text-muted">
        <p>No active case selected.</p>
        <Button variant="secondary" size="sm" onClick={() => navigate('cases')} className="mt-2">
          Back to Cases
        </Button>
      </div>
    );
  }

  const isApproved = activeCase.status === 'SAR_APPROVED_FILED';
  const slaRemainingHours = activeCase.statutorySlaHours || 72;
  const isUrgentSla = slaRemainingHours <= 12;

  const handleAddNote = (e) => {
    e.preventDefault();
    if (!newNoteText.trim()) return;
    addCaseNote(activeCase.id, newNoteText.trim(), currentBanker.name);
    setNewNoteText('');
    addToast('Note Added', 'Internal case note appended to audit record.', 'info');
  };

  const handleFileUpload = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setIsUploading(true);
    setTimeout(() => {
      const newAtt = {
        id: `att-${Date.now()}`,
        name: file.name,
        size: `${(file.size / 1024).toFixed(0)} KB`,
        type: file.type || 'application/octet-stream',
        uploadedAt: new Date().toISOString().substring(11, 16) + ' UTC',
        uploadedBy: currentBanker.name
      };
      addCaseAttachment(activeCase.id, newAtt);
      setIsUploading(false);
      addToast('Document Attached', `${file.name} hashed & added to case docket.`, 'success');
    }, 400);
  };

  const handleSignOff = () => {
    const res = fourEyesSignOffCase(activeCase.id, currentBanker.name);
    if (!res.success) {
      setApproverError(res.error);
      setTimeout(() => setApproverError(null), 5000);
      addToast('Approval Rejected', res.error, 'error');
    } else {
      setApproverError(null);
      addToast('Four-Eyes Ratification Certified', `Dual sign-off completed by ${currentBanker.name}.`, 'success');
    }
  };

  const handleQuickPin = (title, type) => {
    pinEvidence(activeCase.id, {
      title,
      type
    });
  };

  const milestones = activeCase.milestones || [
    { step: 'TRIGGERED', label: 'Triggered', time: '08:14 UTC', status: 'completed' },
    { step: 'ASSIGNED', label: 'Analyst Assigned', time: '08:16 UTC', status: 'completed' },
    { step: 'RFI_DISPATCHED', label: 'RFI Dispatched', time: '08:25 UTC', status: 'completed' },
    { step: 'SAR_DRAFTED', label: 'SAR Drafted', time: '08:35 UTC', status: isApproved ? 'completed' : 'in_progress' },
    { step: 'FOUR_EYES', label: '4-Eyes Approved', time: isApproved ? '08:42 UTC' : null, status: isApproved ? 'completed' : 'pending' }
  ];

  return (
    <div className="space-y-4 select-none">
      {/* Top Navigation & Case Header */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 pb-3 border-b border-border">
        <div className="flex items-center gap-3 min-w-0">
          <Button
            variant="outline"
            size="sm"
            onClick={() => navigate('cases')}
            icon={ArrowLeft}
          >
            All Cases
          </Button>

          <div className="min-w-0">
            <div className="flex items-center gap-2 flex-wrap">
              <span className="font-mono text-xs font-bold text-accent">{activeCase.id}</span>
              <Badge 
                variant={isApproved ? 'cleared' : 'critical'} 
                size="sm"
                dot
              >
                {isApproved ? 'SAR Approved & Filed' : activeCase.status}
              </Badge>

              {/* Active Countdown Urgency Badge */}
              <span className={`px-2 py-0.5 rounded font-mono text-[11px] font-bold flex items-center gap-1 border ${
                isApproved 
                  ? 'bg-cleared-bg text-cleared border-cleared' 
                  : isUrgentSla 
                  ? 'bg-critical-bg text-critical border-critical animate-pulse' 
                  : 'bg-review-bg text-review border-review'
              }`}>
                <Clock className="w-3.5 h-3.5" />
                <span>{isApproved ? 'SLA Met (Filed)' : `${slaRemainingHours}h Window (${isUrgentSla ? 'CRITICAL SLA' : 'Standard'})`}</span>
              </span>
            </div>
            <h1 className="text-base font-bold text-text truncate mt-0.5">{activeCase.title}</h1>
          </div>
        </div>

        {/* Header Action Buttons */}
        <div className="flex items-center gap-2 shrink-0">
          <Button
            variant="outline"
            size="sm"
            onClick={() => navigate('network')}
            icon={Share2}
          >
            View Network
          </Button>

          <Button
            variant="danger"
            size="sm"
            onClick={() => openFreezeNoticeModal({
              accountNumber: activeCase.subjectAccount,
              holderName: activeCase.subjectEntity,
              amount: activeCase.totalExposure,
              caseId: activeCase.id,
              rail: 'SWIFT MT103'
            })}
            icon={ShieldAlert}
            className="text-xs"
          >
            Freeze Notice (PDF)
          </Button>

          <Button
            variant="secondary"
            size="sm"
            onClick={() => navigate('requests')}
            icon={Mail}
          >
            Create RFI
          </Button>

          <Button
            variant="primary"
            size="sm"
            onClick={() => navigate('filings')}
            icon={FileText}
          >
            SAR Drafting
          </Button>
        </div>
      </div>

      {/* Visual Milestone Audit Timeline */}
      <Card className="bg-surfaceRaised border-border p-3.5">
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="font-mono text-xs font-semibold text-text uppercase tracking-wider">
              Statutory Investigation Milestones:
            </span>
            <span className="text-[10px] font-mono text-text-muted">
              {milestones.filter(m => m.status === 'completed').length} of {milestones.length} Completed
            </span>
          </div>

          <div className="grid grid-cols-5 gap-2 pt-1 font-mono text-[11px]">
            {milestones.map((m, idx) => {
              const isDone = m.status === 'completed';
              const isInProg = m.status === 'in_progress';

              return (
                <div 
                  key={idx}
                  className={`p-2 rounded border transition-colors ${
                    isDone 
                      ? 'bg-cleared-bg/60 border-cleared text-cleared' 
                      : isInProg 
                      ? 'bg-accent-subtle/50 border-accent text-accent font-bold animate-pulse' 
                      : 'bg-bg border-border text-text-muted'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-[9px] uppercase tracking-wider font-semibold">Step 0{idx + 1}</span>
                    {isDone && <CheckCircle2 className="w-3.5 h-3.5 text-cleared" />}
                  </div>
                  <span className="block font-sans font-medium text-xs truncate text-text">{m.label}</span>
                  <span className="text-[10px] text-text-muted block mt-0.5">{m.time || 'Pending'}</span>
                </div>
              );
            })}
          </div>
        </div>
      </Card>

      {/* Four-Eyes Dual Sign-off Governance Banner */}
      <Card className="bg-surfaceRaised border-border">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-3">
          <div className="flex items-center gap-2.5 min-w-0">
            <div className={`w-8 h-8 rounded flex items-center justify-center shrink-0 ${
              isApproved ? 'bg-cleared text-white' : 'bg-review text-white'
            }`}>
              <ShieldCheck className="w-4 h-4 text-white" />
            </div>
            <div className="min-w-0">
              <div className="flex items-center gap-2">
                <span className="font-semibold text-xs text-text">Four-Eyes Dual Control Sign-off</span>
                <span className="font-mono text-[10px] text-text-muted">(Federal Reserve SR 11-7 / OCC 2011-12)</span>
              </div>
              <p className="text-xs text-text-2 mt-0.5">
                Initiator: <strong className="text-text">{activeCase.fourEyesInitiator}</strong>
                {activeCase.fourEyesApprover ? (
                  <> • Ratified by CCO: <strong className="text-cleared">{activeCase.fourEyesApprover}</strong></>
                ) : (
                  <> • Awaiting second signatory ratification</>
                )}
              </p>
            </div>
          </div>

          <div className="shrink-0 flex items-center gap-2">
            {!isApproved ? (
              <Button
                variant="primary"
                size="sm"
                onClick={handleSignOff}
                icon={Check}
              >
                Sign Off &amp; File SAR ({currentBanker.name.split(' ')[0]})
              </Button>
            ) : (
              <Badge variant="cleared" size="md">
                Certified &amp; Sealed in Audit Vault
              </Badge>
            )}
          </div>
        </div>

        {approverError && (
          <div className="mt-2.5 p-2 rounded bg-critical-bg border border-critical-border text-xs text-critical-text flex items-center gap-1.5 animate-fadeIn">
            <AlertTriangle className="w-3.5 h-3.5 shrink-0" />
            <span>{approverError}</span>
          </div>
        )}
      </Card>

      {/* Main Two-Column Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-4">
        {/* Left Column: Timeline, Linked Alerts & Sources */}
        <div className="lg:col-span-8 space-y-4">
          {/* Key Evidence & Metrics */}
          <Card>
            <CardHeader
              title="Subject Entity &amp; Transaction Exposure"
              badge={<Badge variant="neutral" size="sm">{activeCase.subjectBic}</Badge>}
            />
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 mt-3 font-mono text-xs">
              <div className="p-2.5 rounded bg-bg border border-borderSubtle">
                <span className="text-[10px] text-text-muted uppercase block">Total Exposure (USD / BDT)</span>
                <span className="font-bold text-text tabular-nums text-sm block">
                  ${activeCase.totalExposure.toLocaleString()}
                </span>
                <span className="text-[10px] text-text-muted font-medium block">
                  ৳{(activeCase.totalExposure * 120).toLocaleString()} BDT
                </span>
              </div>
              <div className="p-2.5 rounded bg-bg border border-borderSubtle">
                <span className="text-[10px] text-text-muted uppercase block">Risk Posterior</span>
                <span className="font-bold text-critical tabular-nums text-sm">
                  {(activeCase.riskScore * 100).toFixed(1)}%
                </span>
                <span className="text-[10px] text-text-muted block mt-0.5">p = 0.0004</span>
              </div>
              <div className="p-2.5 rounded bg-bg border border-borderSubtle">
                <span className="text-[10px] text-text-muted uppercase block">Linked Alerts</span>
                <span className="font-bold text-text text-sm">
                  {activeCase.linkedAlertIds.length} Flagged Wires
                </span>
              </div>
              <div className="p-2.5 rounded bg-bg border border-borderSubtle">
                <span className="text-[10px] text-text-muted uppercase block">Jurisdiction SLA</span>
                <span className="font-bold text-text text-sm">
                  {activeCase.statutoryJurisdiction.split(' ')[0]}
                </span>
                <span className="text-[10px] text-review block mt-0.5">{activeCase.statutorySlaHours}h window</span>
              </div>
            </div>
          </Card>

          {/* Trade-Based AML (TBML) & Customs Intelligence Card */}
          {activeCase.tbmlDetails && (
            <Card className="border-accent/40 bg-surfaceRaised">
              <CardHeader
                title="Trade-Based AML (TBML) &amp; Customs Intelligence"
                subtitle="Letter of Credit pricing vs National Board of Revenue ASYCUDA valuation"
                badge={<Badge variant="critical" size="sm">BFIU MLPA §2(v)</Badge>}
              />
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 mt-3 font-mono text-xs">
                <div className="p-2.5 rounded bg-bg border border-borderSubtle">
                  <span className="text-[10px] text-text-muted uppercase block">LC Reference</span>
                  <span className="font-semibold text-text">{activeCase.tbmlDetails.lcNumber}</span>
                </div>
                <div className="p-2.5 rounded bg-bg border border-borderSubtle">
                  <span className="text-[10px] text-text-muted uppercase block">Commodity HS Code</span>
                  <span className="text-text">{activeCase.tbmlDetails.hsCode}</span>
                </div>
                <div className="p-2.5 rounded bg-bg border border-borderSubtle">
                  <span className="text-[10px] text-text-muted uppercase block">Customs Price Divergence</span>
                  <span className="font-bold text-critical">{activeCase.tbmlDetails.priceDeviation}</span>
                </div>
                <div className="p-2.5 rounded bg-bg border border-borderSubtle">
                  <span className="text-[10px] text-text-muted uppercase block">Stated vs ASYCUDA Tariff</span>
                  <span className="text-text">{activeCase.tbmlDetails.declaredPrice} vs {activeCase.tbmlDetails.benchmarkPrice}</span>
                </div>
              </div>
              <div className="mt-2.5 pt-2 border-t border-borderSubtle flex items-center justify-between text-[11px] font-mono text-text-2">
                <span>Corridor: {activeCase.tbmlDetails.ports}</span>
                <span>Carrier: {activeCase.tbmlDetails.vessel}</span>
              </div>
            </Card>
          )}

          {/* PINNED EVIDENCE DOSSIER */}
          <Card>
            <div className="flex items-center justify-between pb-2 border-b border-borderSubtle">
              <div className="flex items-center gap-2">
                <Pin className="w-4 h-4 text-accent" />
                <h3 className="font-semibold text-text text-sm">Pinned Evidence Dossier</h3>
                <Badge variant="accent" size="sm">{(activeCase.pinnedEvidence || []).length} Items</Badge>
              </div>

              {/* Quick Pin Buttons */}
              <div className="flex items-center gap-1.5 font-mono text-[10px]">
                <button
                  onClick={() => handleQuickPin('Forensic Subgraph Topology Snapshot', 'subgraph')}
                  className="px-2 py-1 rounded bg-surface hover:bg-surfaceHover border border-border text-text cursor-pointer transition-colors"
                >
                  + Pin Subgraph
                </button>
                <button
                  onClick={() => handleQuickPin('ASYCUDA Bill of Lading #CTG-88912', 'document')}
                  className="px-2 py-1 rounded bg-surface hover:bg-surfaceHover border border-border text-text cursor-pointer transition-colors"
                >
                  + Pin Customs B/L
                </button>
              </div>
            </div>

            <div className="space-y-2 mt-3">
              {(activeCase.pinnedEvidence || []).length === 0 ? (
                <p className="text-xs text-text-muted text-center py-4">No evidence pinned yet. Use the buttons above to pin subgraphs or receipts.</p>
              ) : (
                activeCase.pinnedEvidence.map((pin) => (
                  <div key={pin.id} className="p-2.5 rounded bg-bg border border-borderSubtle flex items-center justify-between text-xs font-mono">
                    <div className="flex items-center gap-2">
                      <Pin className="w-3.5 h-3.5 text-accent shrink-0" />
                      <div>
                        <span className="font-semibold text-text font-sans block">{pin.title}</span>
                        <span className="text-[10px] text-text-muted">Type: {pin.type} • Pinned at {pin.timestamp || pin.pinnedAt} by {pin.pinnedBy}</span>
                      </div>
                    </div>
                    <button
                      onClick={() => unpinEvidence(activeCase.id, pin.id)}
                      className="p-1 rounded text-text-muted hover:text-critical cursor-pointer"
                      title="Unpin evidence"
                    >
                      <PinOff className="w-3.5 h-3.5" />
                    </button>
                  </div>
                ))
              )}
            </div>
          </Card>

          {/* Activity Timeline */}
          <Card>
            <CardHeader
              title="Chronological Investigation Timeline"
              subtitle="Audited sequence of alerts, holds, and officer actions"
            />
            <div className="space-y-3 mt-3">
              {(activeCase.timeline || []).map((item) => (
                <div key={item.id} className="flex items-start gap-3 text-xs">
                  <div className="w-1.5 h-1.5 rounded-full bg-accent shrink-0 mt-1.5" />
                  <div className="min-w-0 flex-1">
                    <span className="font-mono text-[11px] text-text-muted">{item.time}</span>
                    <p className="text-text mt-0.5 leading-snug">{item.event}</p>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>

        {/* Right Column: Case Notes & Internal Discussion */}
        <div className="lg:col-span-4 space-y-4">
          <Card className="flex flex-col justify-between min-h-[460px]">
            <div>
              <CardHeader
                title="Investigator Notes &amp; Actions"
                subtitle="Append-only record stored with case"
              />

              {/* Notes List */}
              <div className="space-y-2.5 mt-3 max-h-[300px] overflow-y-auto pr-1">
                {(activeCase.notes || []).map((note) => (
                  <div key={note.id} className="p-2.5 rounded bg-bg border border-borderSubtle text-xs space-y-1">
                    <div className="flex items-center justify-between text-[10px] font-mono text-text-muted">
                      <span className="font-semibold text-text">{note.author}</span>
                      <span>{note.time}</span>
                    </div>
                    <p className="text-text-2 leading-relaxed">{note.text}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Note Input Box */}
            <form onSubmit={handleAddNote} className="mt-4 pt-3 border-t border-borderSubtle space-y-2">
              <textarea
                id="case-note-textarea"
                name="case-note-textarea"
                aria-label="Add confidential officer note"
                value={newNoteText}
                onChange={(e) => setNewNoteText(e.target.value)}
                placeholder="Add confidential officer note..."
                rows={3}
                className="ui-input w-full resize-none text-xs"
              />
              <Button
                type="submit"
                variant="primary"
                size="sm"
                className="w-full"
                icon={Send}
              >
                Append Note
              </Button>
            </form>
          </Card>

          {/* Attachments Card */}
          <Card>
            <CardHeader
              title="Evidence Attachments"
              subtitle="Subpoenas, MT103 receipts, and registry filings"
              badge={<Badge variant="neutral" size="sm">{activeCase.attachments?.length || 0} Files</Badge>}
            />
            
            {/* Attachment Dropzone */}
            <div className="mt-3 p-3 border border-dashed border-border rounded bg-bg text-center">
              <input
                type="file"
                id="case-file-upload"
                className="hidden"
                onChange={handleFileUpload}
                accept=".pdf,.tiff,.csv,.png,.jpg"
              />
              <label htmlFor="case-file-upload" className="cursor-pointer flex flex-col items-center gap-1">
                <UploadCloud className="w-4 h-4 text-accent" />
                <span className="text-xs font-medium text-text">
                  {isUploading ? 'Hashing file...' : 'Attach Subpoena / Evidence'}
                </span>
                <span className="text-[10px] text-text-muted">PDF, TIFF, CSV (SHA-256 sealed)</span>
              </label>
            </div>

            {/* Attachment List */}
            <div className="mt-2.5 space-y-1.5 max-h-[160px] overflow-y-auto">
              {activeCase.attachments && activeCase.attachments.length > 0 ? (
                activeCase.attachments.map((att) => (
                  <div key={att.id} className="flex items-center justify-between p-2 rounded bg-bg border border-borderSubtle text-xs">
                    <div className="flex items-center gap-1.5 min-w-0">
                      <Paperclip className="w-3.5 h-3.5 text-accent shrink-0" />
                      <div className="min-w-0">
                        <p className="font-mono text-[11px] text-text font-medium truncate">{att.name}</p>
                        <p className="text-[10px] text-text-muted">{att.size} • {att.uploadedAt}</p>
                      </div>
                    </div>
                    <Badge variant="cleared" size="sm">Sealed</Badge>
                  </div>
                ))
              ) : (
                <p className="text-xs text-text-muted text-center py-2">No files attached yet.</p>
              )}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
