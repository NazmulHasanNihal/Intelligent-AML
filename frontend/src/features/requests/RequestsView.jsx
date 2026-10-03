import React, { useState } from 'react';
import { 
  Mail, 
  Plus, 
  Lock, 
  AlertTriangle, 
  FileCheck, 
  Clock, 
  Download, 
  CheckCircle2, 
  ExternalLink, 
  Shield, 
  ShieldAlert, 
  Send,
  UploadCloud,
  File,
  Paperclip,
  BellRing,
  ArrowRight,
  ChevronDown,
  Sparkles,
  Loader2,
  FileSearch,
  Anchor
} from 'lucide-react';
import { useAppStore } from '../../lib/store';
import { Card, CardHeader } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';

export const RequestsView = () => {
  const { 
    rfiRequests, 
    createRFI, 
    updateRFIStatus,
    uploadRFIDocument,
    sendCustomerReminder,
    addToast, 
    openFreezeNoticeModal,
    navigate
  } = useAppStore();

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [template, setTemplate] = useState('DOCUMENT_REQUEST_RFI');
  const [targetAccount, setTargetAccount] = useState('BD22-EBLB-4829-1092-8823');
  const [targetEntity, setTargetEntity] = useState('Meghna Industrial & Agro Processing Ltd');
  const [amount, setAmount] = useState('$48,500.00 USD (৳5,820,000 BDT)');
  
  const [ocrLoadingId, setOcrLoadingId] = useState(null);
  const [ocrData, setOcrData] = useState({});

  const handleRunOcrAudit = async (rfiId) => {
    setOcrLoadingId(rfiId);
    try {
      const res = await fetch('/api/v1/rfi/ingest-document', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          rfi_id: rfiId,
          document_name: 'EXP-2026-0912-4412.pdf',
          document_type: 'BANGLADESH_BANK_EXP_FORM'
        })
      });
      if (res.ok) {
        const data = await res.json();
        setOcrData(prev => ({ ...prev, [rfiId]: data }));
        addToast('OCR Extraction Complete', 'Extracted LC-2026-CTG-88912 & ASYCUDA price deviation', 'critical');
      } else {
        throw new Error('API returned non-200');
      }
    } catch {
      // Offline fallback
      setOcrData(prev => ({
        ...prev,
        [rfiId]: {
          document_name: 'EXP-2026-0912-4412.pdf',
          extracted_fields: {
            lc_number: 'LC-2026-CTG-88912',
            commodity: 'Combed Cotton Knitting Yarn (Grade A)',
            declared_unit_price: 42.50,
            hs_code: 'HS 5201.00',
            bill_of_lading: 'BL-CTG-DXB-98124',
            vessel_name: 'MV Meghna Trader (IMO 9482101)'
          },
          customs_audit: {
            benchmark_unit_price: 9.80,
            price_deviation_pct: 333.67,
            valuation_status: 'SUSPICIOUS_OVERINVOICING',
            tbml_overinvoicing_flag: true
          },
          vessel_tracking: {
            carrier_imo: '9482101',
            route: 'Chattogram Port (BD) -> Jebel Ali Port (UAE)',
            vessel_ais_status: 'ACTIVE_CONDUIT'
          },
          evidence_seal: '7f9c2d1b8e4a0563fa1289dcbb6209e4a317e05698b712c4819e602418a912b7'
        }
      }));
      addToast('OCR Ingestion Simulated', 'Extracted trade metadata & customs benchmark verification', 'critical');
    } finally {
      setOcrLoadingId(null);
    }
  };

  const handleCreate = (e) => {
    e.preventDefault();
    createRFI({
      caseId: 'CASE-2026-0881',
      targetAccount,
      targetEntity,
      amount,
      templateType: template,
      subject: `[SUPPORTING DOCUMENTATION] Request for Information (RFI) — Reference #${targetAccount.slice(-6)}`,
      complianceOfficer: 'Sarah Jenkins',
      dueDate: new Date(Date.now() + 5 * 24 * 3600 * 1000).toISOString().substring(0, 10),
      requiredDocs: [
        'Executed commercial sales contract or corporate invoice',
        'Carrier Bill of Lading or customs declaration',
        'Beneficial ownership (UBO) verification for entities >25% equity'
      ]
    });
    setIsModalOpen(false);
  };

  const handleDocumentDrop = (rfiId, file) => {
    if (!file) return;
    uploadRFIDocument(rfiId, {
      name: file.name,
      size: `${(file.size / 1024).toFixed(0)} KB`,
      type: file.type || 'application/pdf'
    });
  };

  return (
    <div className="space-y-4 select-none">
      {/* Strict Anti-Tipping-Off Safeguard Banner (31 U.S.C. § 5318(g)(2)) */}
      <div className="p-3.5 rounded-lg bg-surfaceRaised border border-border flex items-start gap-3 text-xs">
        <Lock className="w-4 h-4 text-critical shrink-0 mt-0.5" />
        <div className="text-text-2 leading-relaxed">
          <strong className="text-text font-mono uppercase">
            Strict Compliance Notice (31 U.S.C. § 5318(g)(2) / MLPA 2012 §27):
          </strong>
          <span className="block mt-0.5">
            Tipping off internal AML detection thresholds, suspicious flags, or investigation existence to customers is a statutory violation. All customer communications must utilize routine commercial Customer Due Diligence (CDD) and standard RFI verification channels.
          </span>
        </div>
      </div>

      {/* Top Header & Actions */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 p-4 rounded-lg bg-surface border border-border">
        <div>
          <h2 className="text-sm font-semibold text-text">Customer Due Diligence (RFI) Hub</h2>
          <p className="text-xs text-text-2 mt-0.5">
            Manage routine commercial document requests (EXP Forms, trade contracts, and customs documentation).
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Button
            variant="danger"
            size="sm"
            onClick={() => openFreezeNoticeModal({
              accountNumber: targetAccount,
              holderName: targetEntity,
              amount: 48500,
              caseId: 'CASE-2026-0881',
              rail: 'SWIFT MT103'
            })}
            icon={ShieldAlert}
            className="text-xs"
          >
            Issue Freeze Notice (PDF)
          </Button>

          <Button
            variant="primary"
            size="sm"
            onClick={() => setIsModalOpen(true)}
            icon={Plus}
          >
            Issue New RFI
          </Button>
        </div>
      </div>

      {/* RFI Cards with Document Ingestion, State Selectors, and SLA Reminder */}
      <div className="space-y-4">
        {rfiRequests.map((rfi) => {
          const isPending = rfi.status === 'PENDING_CUSTOMER_UPLOAD';
          const isReview = rfi.status === 'UNDER_OFFICER_REVIEW';
          const isSatisfied = rfi.status === 'SATISFIED_CLEARED';
          const isEscalated = rfi.status === 'ESCALATED_TO_SAR';

          return (
            <Card key={rfi.id} className="space-y-3.5 p-4">
              {/* Header: RFI ID, Account, and Status Selector */}
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 pb-3 border-b border-borderSubtle">
                <div className="flex items-center gap-2.5 flex-wrap">
                  <span className="font-mono text-xs font-bold text-accent">{rfi.id}</span>
                  <span className="font-mono text-xs text-text font-semibold">{rfi.targetEntity}</span>
                  <span className="text-xs text-text-muted font-mono">({rfi.targetAccount})</span>
                </div>

                <div className="flex items-center gap-2 flex-wrap">
                  {/* Manual Status Transition Dropdown */}
                  <div className="flex items-center gap-1 font-mono text-[11px]">
                    <label htmlFor={`rfi-status-${rfi.id}`} className="text-text-muted cursor-pointer">Workflow Status:</label>
                    <select
                      id={`rfi-status-${rfi.id}`}
                      name={`rfi-status-${rfi.id}`}
                      aria-label={`Update workflow status for RFI ${rfi.id}`}
                      value={rfi.status}
                      onChange={(e) => updateRFIStatus(rfi.id, e.target.value)}
                      className={`ui-input py-0.5 text-[11px] font-mono h-7 font-bold ${
                        isSatisfied ? 'text-cleared' : isEscalated ? 'text-critical' : isReview ? 'text-accent' : 'text-review'
                      }`}
                    >
                      <option value="PENDING_CUSTOMER_UPLOAD">Pending Customer Upload</option>
                      <option value="UNDER_OFFICER_REVIEW">Under Officer Review</option>
                      <option value="SATISFIED_CLEARED">Satisfied / Cleared</option>
                      <option value="ESCALATED_TO_SAR">Escalated to SAR</option>
                    </select>
                  </div>
                </div>
              </div>

              {/* Subject & Details */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-3 font-mono text-xs">
                <div className="md:col-span-2">
                  <span className="text-text-muted text-[10px] block">COMMUNICATION SUBJECT:</span>
                  <span className="font-semibold text-text text-[11px] font-sans block mt-0.5">{rfi.subject}</span>
                </div>
                <div>
                  <span className="text-text-muted text-[10px] block">TRANSACTION EXPOSURE:</span>
                  <span className="font-bold text-text block mt-0.5">{rfi.amount}</span>
                </div>
              </div>

              {/* Required Documentation Checklist */}
              <div className="p-3 bg-bg rounded-lg border border-borderSubtle space-y-2">
                <span className="text-xs font-semibold text-text block">Required Supporting Documentation:</span>
                <div className="space-y-1">
                  {(rfi.requiredDocs || []).map((doc, dIdx) => (
                    <div key={dIdx} className="flex items-center gap-2 text-[11px] text-text-2">
                      <div className="w-1.5 h-1.5 rounded-full bg-accent" />
                      <span>{doc}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Customer Document Ingestion Drag-and-Drop Pipeline */}
              <div className="grid grid-cols-1 md:grid-cols-12 gap-3 pt-1">
                {/* Ingestion Dropzone & OCR Trigger */}
                <div className="md:col-span-6 p-3 border border-dashed border-border hover:border-accent rounded-lg bg-surfaceRaised/50 text-center transition-colors flex flex-col justify-between">
                  <div>
                    <input
                      type="file"
                      id={`doc-upload-${rfi.id}`}
                      className="hidden"
                      onChange={(e) => {
                        const file = e.target.files?.[0];
                        if (file) handleDocumentDrop(rfi.id, file);
                      }}
                      accept=".pdf,.tiff,.csv,.jpg,.png"
                    />
                    <label htmlFor={`doc-upload-${rfi.id}`} className="cursor-pointer flex flex-col items-center gap-1.5 py-1">
                      <UploadCloud className="w-5 h-5 text-accent" />
                      <span className="text-xs font-semibold text-text">Customer Document Ingestion Pipeline</span>
                      <span className="text-[10px] text-text-muted">Drag &amp; drop or click to ingest EXP Form, B/L, or Commercial Contract</span>
                    </label>
                  </div>

                  <div className="pt-2 border-t border-borderSubtle mt-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleRunOcrAudit(rfi.id)}
                      disabled={ocrLoadingId === rfi.id}
                      icon={ocrLoadingId === rfi.id ? Loader2 : FileSearch}
                      className="w-full text-xs font-mono"
                    >
                      {ocrLoadingId === rfi.id ? 'Extracting via Neural OCR...' : 'Run Automated OCR & ASYCUDA Audit'}
                    </Button>
                  </div>
                </div>

                {/* Ingested Documents List */}
                <div className="md:col-span-6 space-y-1.5 font-mono text-[11px]">
                  <span className="text-[10px] text-text-muted uppercase block font-sans font-semibold">
                    Ingested Document Artifacts ({(rfi.uploadedDocs || []).length}):
                  </span>
                  {(rfi.uploadedDocs || []).length === 0 ? (
                    <div className="p-2.5 rounded bg-bg border border-borderSubtle text-text-muted text-[10px]">
                      Awaiting incoming customer transmission. Click "Run Automated OCR" to simulate receipt.
                    </div>
                  ) : (
                    (rfi.uploadedDocs || []).map((doc) => (
                      <div key={doc.id} className="p-2 rounded bg-bg border border-borderSubtle flex items-center justify-between">
                        <div className="flex items-center gap-2 truncate">
                          <Paperclip className="w-3.5 h-3.5 text-accent shrink-0" />
                          <span className="truncate text-text font-medium">{doc.name}</span>
                        </div>
                        <Badge variant="cleared" size="sm">Sealed</Badge>
                      </div>
                    ))
                  )}
                </div>
              </div>

              {/* OCR Extracted Intelligence & ASYCUDA Price Deviation Panel */}
              {ocrData[rfi.id] && (
                <div className="mt-3 p-3.5 rounded-lg bg-surface border border-accent/30 space-y-3 font-mono text-xs">
                  <div className="flex items-center justify-between border-b border-borderSubtle pb-2">
                    <div className="flex items-center gap-2">
                      <FileSearch className="w-4 h-4 text-accent" />
                      <span className="font-bold text-text">OCR Extracted Shipping Bill: {ocrData[rfi.id].document_name}</span>
                      <Badge variant="critical" size="sm">Over-Invoicing Anomaly</Badge>
                    </div>
                    <Badge variant="cleared" size="sm">FRE 902(11) Cryptographically Sealed</Badge>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-[11px]">
                    <div className="space-y-1.5 p-2 rounded bg-surfaceRaised border border-borderSubtle">
                      <span className="text-[10px] text-text-muted uppercase font-bold block">Documentary LC Extraction:</span>
                      <div>LC Number: <strong className="text-text">{ocrData[rfi.id].extracted_fields.lc_number}</strong></div>
                      <div>Commodity: <strong className="text-text">{ocrData[rfi.id].extracted_fields.commodity}</strong></div>
                      <div>HS Tariff Code: <strong className="text-accent">{ocrData[rfi.id].extracted_fields.hs_code}</strong></div>
                      <div>Bill of Lading: <strong className="text-text">{ocrData[rfi.id].extracted_fields.bill_of_lading}</strong></div>
                    </div>

                    <div className="space-y-1.5 p-2 rounded bg-critical/5 border border-critical/20">
                      <span className="text-[10px] text-critical uppercase font-bold block">ASYCUDA Customs Audit:</span>
                      <div>Declared Valuation: <strong className="text-critical text-sm">${ocrData[rfi.id].extracted_fields.declared_unit_price} / kg</strong></div>
                      <div>NBR Customs Benchmark: <strong className="text-text">${ocrData[rfi.id].customs_audit.benchmark_unit_price} / kg</strong></div>
                      <div className="text-critical font-bold">
                        Variance Deviation: +{ocrData[rfi.id].customs_audit.price_deviation_pct}% Over-Invoicing
                      </div>
                    </div>
                  </div>

                  <div className="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-borderSubtle text-[10px]">
                    <div className="flex items-center gap-1.5 text-text-muted">
                      <Anchor className="w-3.5 h-3.5 text-accent" />
                      <span>Carrier: <strong className="text-text">{ocrData[rfi.id].vessel_tracking.carrier_imo ? `${ocrData[rfi.id].extracted_fields.vessel_name}` : 'MV Meghna Trader'}</strong></span>
                      <span>•</span>
                      <span>Route: <strong className="text-text">{ocrData[rfi.id].vessel_tracking.route}</strong></span>
                    </div>

                    <Button
                      variant="primary"
                      size="sm"
                      onClick={() => {
                        addToast('Evidence Appended', 'OCR Trade Invoice appended to Case CASE-2026-0881', 'critical');
                        navigate('cases');
                      }}
                      className="text-xs h-6 bg-critical hover:bg-critical/90"
                    >
                      Attach to Case Dossier
                    </Button>
                  </div>
                </div>
              )}

              {/* Footer: Customer SLA Clock & Auto-Reminder Engine */}
              <div className="pt-2.5 border-t border-borderSubtle flex flex-wrap items-center justify-between gap-3 text-xs font-mono">
                <div className="flex items-center gap-2">
                  <Clock className="w-3.5 h-3.5 text-review" />
                  <span className="text-text-muted">Customer SLA Deadline:</span>
                  <span className="font-bold text-text">{rfi.dueDate} (5-Day Turnaround)</span>
                </div>

                <div className="flex items-center gap-2">
                  {/* Auto-Reminder Engine Button */}
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => sendCustomerReminder(rfi.id)}
                    icon={BellRing}
                    className="h-7 text-xs"
                  >
                    Dispatch Automated SLA Reminder
                  </Button>
                </div>
              </div>
            </Card>
          );
        })}
      </div>

      {/* New RFI Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 overflow-hidden bg-black/60 flex items-center justify-center p-4 animate-fadeIn">
          <div className="w-full max-w-lg bg-surface border border-border rounded-xl shadow-2xl p-5 space-y-4 text-xs">
            <div className="flex items-center justify-between pb-2 border-b border-border">
              <h3 className="font-semibold text-text text-sm">Issue Compliant Information Request (RFI)</h3>
              <button onClick={() => setIsModalOpen(false)} className="text-text-muted hover:text-text cursor-pointer">
                ✕
              </button>
            </div>

            <form onSubmit={handleCreate} className="space-y-3 font-mono">
              <div>
                <label htmlFor="rfi-target-account" className="text-text font-semibold block mb-1">Target Account:</label>
                <input
                  id="rfi-target-account"
                  name="rfi-target-account"
                  type="text"
                  value={targetAccount}
                  onChange={(e) => setTargetAccount(e.target.value)}
                  className="ui-input w-full h-8 text-xs font-mono"
                />
              </div>

              <div>
                <label htmlFor="rfi-target-entity" className="text-text font-semibold block mb-1">Target Entity Name:</label>
                <input
                  id="rfi-target-entity"
                  name="rfi-target-entity"
                  type="text"
                  value={targetEntity}
                  onChange={(e) => setTargetEntity(e.target.value)}
                  className="ui-input w-full h-8 text-xs font-sans"
                />
              </div>

              <div>
                <label htmlFor="rfi-amount" className="text-text font-semibold block mb-1">Exposure Amount:</label>
                <input
                  id="rfi-amount"
                  name="rfi-amount"
                  type="text"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  className="ui-input w-full h-8 text-xs"
                />
              </div>

              <div>
                <label htmlFor="rfi-template" className="text-text font-semibold block mb-1">RFI Template Type:</label>
                <select
                  id="rfi-template"
                  name="rfi-template"
                  value={template}
                  onChange={(e) => setTemplate(e.target.value)}
                  className="ui-input w-full h-8 text-xs"
                >
                  <option value="DOCUMENT_REQUEST_RFI">Document Request (Invoice &amp; EXP Form)</option>
                  <option value="SOURCE_OF_FUNDS_DECLARATION">Source of Wealth &amp; Capital Declaration</option>
                  <option value="UBO_BENEFICIAL_OWNERSHIP">Beneficial Ownership (UBO) Registry Update</option>
                </select>
              </div>

              <div className="pt-3 flex justify-end gap-2 font-sans">
                <Button variant="secondary" size="sm" onClick={() => setIsModalOpen(false)}>
                  Cancel
                </Button>
                <Button variant="primary" size="sm" type="submit" icon={Send}>
                  Dispatch RFI Notice
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
