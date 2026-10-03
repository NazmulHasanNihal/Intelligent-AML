import React, { useState } from 'react';
import { 
  Briefcase, 
  Search, 
  Filter, 
  Plus, 
  Clock, 
  CheckCircle2, 
  AlertTriangle, 
  ChevronRight,
  ShieldCheck,
  UserCheck,
  LayoutGrid,
  List,
  Pin,
  Paperclip,
  ArrowRight,
  FileText
} from 'lucide-react';
import { useAppStore } from '../../lib/store';
import { Card, CardHeader } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';

export const CasesView = () => {
  const { cases, selectCase, caseViewMode, setCaseViewMode } = useAppStore();
  const [filterStatus, setFilterStatus] = useState('ALL');
  const [search, setSearch] = useState('');

  const filteredCases = cases.filter((c) => {
    if (filterStatus !== 'ALL' && c.status !== filterStatus) return false;
    if (search) {
      const q = search.toLowerCase();
      return (c.id || '').toLowerCase().includes(q) ||
             (c.title || '').toLowerCase().includes(q) ||
             (c.subjectEntity || '').toLowerCase().includes(q) ||
             (c.subjectAccount || '').toLowerCase().includes(q);
    }
    return true;
  });

  return (
    <div className="space-y-4 select-none">
      {/* Top Filter, Search & Layout View Toggle */}
      <div className="p-3.5 rounded-lg bg-surface border border-border flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2 flex-wrap flex-1">
          <div className="relative min-w-[200px] flex-1 sm:flex-initial">
            <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-text-muted" />
            <input
              id="case-search-input"
              name="case-search-input"
              aria-label="Search cases by entity or ID"
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search cases by entity or ID..."
              className="ui-input pl-8 w-full h-8 text-xs"
            />
          </div>

          <select
            id="case-status-filter"
            name="case-status-filter"
            aria-label="Filter cases by status"
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="ui-input h-8 text-xs font-mono"
          >
            <option value="ALL">All Case Statuses</option>
            <option value="UNDER_INVESTIGATION">Under Investigation</option>
            <option value="SAR_PENDING_APPROVAL">SAR Pending Four-Eyes Sign-Off</option>
            <option value="SAR_APPROVED_FILED">SAR Approved &amp; Filed</option>
          </select>
        </div>

        {/* Right: Layout Toggle Switch (Grid vs Dense Table) & Stats */}
        <div className="flex items-center gap-2.5 shrink-0">
          <div className="flex items-center gap-0.5 p-0.5 bg-bg rounded border border-border">
            <button
              onClick={() => setCaseViewMode('grid')}
              className={`p-1.5 rounded transition-colors cursor-pointer ${
                caseViewMode === 'grid' 
                  ? 'bg-surface font-semibold text-text shadow-xs' 
                  : 'text-text-muted hover:text-text'
              }`}
              title="Card Grid View"
            >
              <LayoutGrid className="w-3.5 h-3.5" />
            </button>
            <button
              onClick={() => setCaseViewMode('table')}
              className={`p-1.5 rounded transition-colors cursor-pointer ${
                caseViewMode === 'table' 
                  ? 'bg-surface font-semibold text-text shadow-xs' 
                  : 'text-text-muted hover:text-text'
              }`}
              title="Dense Tabular View (Monitor 20+ cases simultaneously)"
            >
              <List className="w-3.5 h-3.5" />
            </button>
          </div>

          <Badge variant="accent" size="sm">
            {filteredCases.length} Investigations
          </Badge>
        </div>
      </div>

      {/* DENSE TABULAR VIEW (Allows monitoring 20+ cases simultaneously) */}
      {caseViewMode === 'table' ? (
        <Card padding={false} className="overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-surfaceRaised border-b border-border text-text-muted font-mono text-[11px] uppercase tracking-wider select-none">
                <tr>
                  <th className="py-2.5 px-3">Docket ID</th>
                  <th className="py-2.5 px-3">Case Title &amp; Target Entity</th>
                  <th className="py-2.5 px-3">Exposure (USD / BDT)</th>
                  <th className="py-2.5 px-3">Risk</th>
                  <th className="py-2.5 px-3">Milestone Progress</th>
                  <th className="py-2.5 px-3">Status</th>
                  <th className="py-2.5 px-3">Statutory SLA</th>
                  <th className="py-2.5 px-3">Dossier</th>
                  <th className="py-2.5 px-3 text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-borderSubtle">
                {filteredCases.map((c) => {
                  const isApproved = c.status === 'SAR_APPROVED_FILED';
                  const isPending = c.status === 'SAR_PENDING_APPROVAL';
                  const completedMilestones = (c.milestones || []).filter(m => m.status === 'completed').length;
                  const totalMilestones = (c.milestones || []).length || 5;

                  return (
                    <tr
                      key={c.id}
                      onClick={() => selectCase(c.id)}
                      className="hover:bg-surfaceHover transition-colors cursor-pointer"
                    >
                      <td className="py-2.5 px-3 font-mono font-bold text-accent">
                        {c.id}
                      </td>
                      <td className="py-2.5 px-3">
                        <div className="font-semibold text-text truncate max-w-[200px]">{c.title}</div>
                        <div className="font-mono text-[10px] text-text-muted truncate max-w-[200px]">{c.subjectEntity}</div>
                      </td>
                      <td className="py-2.5 px-3 font-mono">
                        <span className="font-semibold text-text">${(c.totalExposure || 48500).toLocaleString()}</span>
                        <span className="text-[10px] text-text-muted block">৳{((c.totalExposure || 48500) * 120).toLocaleString()}</span>
                      </td>
                      <td className="py-2.5 px-3 font-mono">
                        <span className="font-bold text-critical">{((c.riskScore || 0.98) * 100).toFixed(1)}%</span>
                      </td>
                      {/* Milestone Progress Bar */}
                      <td className="py-2.5 px-3">
                        <div className="flex items-center gap-1.5 font-mono text-[10px]">
                          <div className="w-16 h-1.5 bg-bg rounded-full overflow-hidden flex border border-border">
                            <div 
                              className={`h-full ${isApproved ? 'bg-cleared' : 'bg-accent'}`}
                              style={{ width: `${(completedMilestones / totalMilestones) * 100}%` }}
                            />
                          </div>
                          <span className="text-text-muted">{completedMilestones}/{totalMilestones}</span>
                        </div>
                      </td>
                      <td className="py-2.5 px-3 font-mono text-[10px]">
                        <Badge 
                          variant={isApproved ? 'cleared' : isPending ? 'critical' : 'review'} 
                          size="sm"
                          dot
                        >
                          {isApproved ? 'SAR FILED' : isPending ? 'PENDING 4-EYES' : 'IN REVIEW'}
                        </Badge>
                      </td>
                      {/* Urgency SLA Badge */}
                      <td className="py-2.5 px-3 font-mono text-[10px]">
                        <span className={`px-1.5 py-0.5 rounded border font-semibold flex items-center gap-1 w-fit ${
                          isApproved ? 'bg-cleared/10 text-cleared border-cleared/30' :
                          (c.statutorySlaHours || 72) <= 12 ? 'bg-critical/15 text-critical border-critical animate-pulse font-bold' :
                          'bg-review/10 text-review border-review/30'
                        }`}>
                          <Clock className="w-3 h-3" />
                          <span>{isApproved ? 'Resolved' : `${c.statutorySlaHours || 72}h Window`}</span>
                        </span>
                      </td>
                      {/* Pinned Evidence Dossier Pill */}
                      <td className="py-2.5 px-3 font-mono text-[10px]">
                        <span className="flex items-center gap-1 text-text-muted">
                          <Pin className="w-3 h-3 text-accent" />
                          <span>{(c.pinnedEvidence || []).length} items</span>
                        </span>
                      </td>
                      <td className="py-2.5 px-3 text-right">
                        <Button variant="ghost" size="sm" className="h-7 text-xs font-mono">
                          Open <ChevronRight className="w-3 h-3 ml-1" />
                        </Button>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </Card>
      ) : (
        /* CARD GRID VIEW (Default) */
        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-3.5">
          {filteredCases.map((c) => {
            const isPendingApproval = c.status === 'SAR_PENDING_APPROVAL';
            const isApproved = c.status === 'SAR_APPROVED_FILED';
            const completedMilestones = (c.milestones || []).filter(m => m.status === 'completed').length;
            const totalMilestones = (c.milestones || []).length || 5;

            return (
              <Card
                key={c.id}
                hover
                onClick={() => selectCase(c.id)}
                className="flex flex-col justify-between space-y-3 p-4 transition-all"
              >
                <div>
                  <div className="flex items-center justify-between gap-2 pb-2.5 border-b border-borderSubtle">
                    <div className="flex items-center gap-1.5">
                      <span className="font-mono text-xs font-bold text-accent">{c.id}</span>
                      <span className="text-text-muted text-[10px]">•</span>
                      <span className="text-[10px] font-mono text-text-muted">{c.statutoryJurisdiction?.split('/')[0] || 'BFIU STR-1'}</span>
                    </div>
                    <Badge 
                      variant={isApproved ? 'cleared' : isPendingApproval ? 'critical' : 'review'} 
                      size="sm"
                      dot
                    >
                      {isApproved ? 'SAR FILED' : isPendingApproval ? 'PENDING 4-EYES' : 'IN REVIEW'}
                    </Badge>
                  </div>

                  <div className="mt-2.5">
                    <h3 className="text-sm font-semibold text-text truncate">{c.title}</h3>
                    <p className="text-xs text-text-muted mt-0.5 truncate">{c.subjectEntity}</p>
                    <p className="font-mono text-[10px] text-text-muted mt-0.5 truncate">{c.subjectAccount}</p>
                  </div>

                  {/* Exposure & Risk Metrics */}
                  <div className="grid grid-cols-2 gap-2 mt-3 p-2 rounded bg-bg border border-borderSubtle text-[11px] font-mono">
                    <div>
                      <span className="text-text-muted text-[10px] block">TOTAL EXPOSURE:</span>
                      <span className="font-bold text-text">${(c.totalExposure || 48500).toLocaleString()} USD</span>
                    </div>
                    <div>
                      <span className="text-text-muted text-[10px] block">RISK POSTERIOR:</span>
                      <span className="font-bold text-critical">{((c.riskScore || 0.98) * 100).toFixed(1)}%</span>
                    </div>
                  </div>

                  {/* Visual Milestone Audit Tracker */}
                  <div className="mt-3 space-y-1.5">
                    <div className="flex justify-between items-center text-[10px] font-mono text-text-muted">
                      <span>Milestones:</span>
                      <span className="font-bold text-text">{completedMilestones} of {totalMilestones} Steps</span>
                    </div>
                    <div className="flex items-center gap-1">
                      {['Triggered', 'Assigned', 'RFI', 'SAR', '4-Eyes'].map((stepName, sIdx) => {
                        const isDone = sIdx < completedMilestones;
                        const isCurrent = sIdx === completedMilestones;

                        return (
                          <div 
                            key={sIdx}
                            className={`flex-1 h-1.5 rounded-full transition-colors ${
                              isDone ? 'bg-accent' : isCurrent ? 'bg-review animate-pulse' : 'bg-bg border border-border'
                            }`}
                            title={stepName}
                          />
                        );
                      })}
                    </div>
                  </div>
                </div>

                {/* Footer: SLA Urgency Clock & Pinned Dossier Count */}
                <div className="pt-2.5 border-t border-borderSubtle flex items-center justify-between text-[11px] font-mono">
                  <div className="flex items-center gap-1.5">
                    <Clock className={`w-3.5 h-3.5 ${
                      isApproved ? 'text-cleared' : (c.statutorySlaHours || 72) <= 12 ? 'text-critical animate-pulse' : 'text-review'
                    }`} />
                    <span className={
                      isApproved ? 'text-cleared font-semibold' :
                      (c.statutorySlaHours || 72) <= 12 ? 'text-critical font-bold' : 'text-text-muted'
                    }>
                      {isApproved ? 'Filed with BFIU' : `${c.statutorySlaHours || 72}h SLA Remaining`}
                    </span>
                  </div>

                  <div className="flex items-center gap-1 text-text-muted">
                    <Pin className="w-3 h-3 text-accent" />
                    <span>{(c.pinnedEvidence || []).length} Pinned</span>
                  </div>
                </div>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
};
