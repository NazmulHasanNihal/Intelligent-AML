import React, { useState } from 'react';
import { 
  X, 
  HelpCircle, 
  CheckCircle2, 
  AlertTriangle, 
  ShieldAlert, 
  ShieldCheck, 
  Search, 
  Bot, 
  FileText, 
  Lock, 
  Activity, 
  ArrowRight,
  BookOpen,
  Users,
  Compass,
  Zap,
  Globe
} from 'lucide-react';
import { useAppStore } from '../lib/store';

export const PlainEnglishGuideModal = () => {
  const { isPlainEnglishGuideOpen, setPlainEnglishGuideOpen } = useAppStore();
  const [activeTab, setActiveTab] = useState('overview'); // 'overview' | 'tiers' | 'jargon' | 'ai-swarm'
  const [jargonSearch, setJargonSearch] = useState('');

  if (!isPlainEnglishGuideOpen) return null;

  const JARGON_DICTIONARY = [
    {
      term: 'STP (Straight-Through Processing)',
      plain: 'Instant Auto-Approval (No Human Needed)',
      explanation: 'Clean, everyday transactions (like salaries, grocery bills, and normal shopping) get approved automatically in less than a second without making customers wait.',
      example: '98.6% of honest payments pass through instantly without human delay.'
    },
    {
      term: 'Tier 1 Auto-Quarantine',
      plain: 'Immediate Account Freeze (Severe Crime Match)',
      explanation: 'When a payment matches a known terrorist, sanctioned warlord, or massive illegal scheme, the system stops the money immediately before it leaves the bank.',
      example: 'A wire transfer linked to a sanctioned overseas company is halted in 0.45 ms.'
    },
    {
      term: 'Tier 2 Review Queue',
      plain: 'Yellow Alert / Human Check Needed',
      explanation: 'The transaction looks unusual or suspicious, but not definitely illegal. It is placed in a human officer’s inbox for investigation.',
      example: 'A student account suddenly receives $20,000 from 5 different foreign accounts in 2 hours.'
    },
    {
      term: 'Maker-Checker / Four-Eyes Principle',
      plain: 'The Two-Officer Sign-Off Rule',
      explanation: 'To prevent bribery, favoritism, or mistakes, no single person can freeze an account or file a criminal report alone. One officer investigates (the Maker), and a different senior officer must approve it (the Checker).',
      example: 'Officer Sarah prepares the fraud report; Chief Officer Nazmul must review and sign it before it goes to the police.'
    },
    {
      term: 'SAR / STR (Suspicious Activity Report)',
      plain: 'Official Crime Report for Financial Police',
      explanation: 'A formal legal document sent to government financial intelligence units (like FinCEN in the US or BFIU in Bangladesh) notifying them that money laundering has been detected.',
      example: 'The AI swarm writes an official 5-page report detailing fake shipping invoices and money trails.'
    },
    {
      term: 'Smurfing / Structuring',
      plain: 'Breaking Big Cash into Small Pieces',
      explanation: 'Banks are required to report any cash deposit of $10,000 or more. Criminals try to evade this by breaking $50,000 into five separate $9,900 deposits across different branches.',
      example: 'Depositing $9,500 every morning to stay under the $10,000 radar.'
    },
    {
      term: 'Pass-Through Conduit / Money Mule',
      plain: 'Money In, Money Out Fast (Hot Potato Account)',
      explanation: 'An account used solely to forward dirty money so the original source cannot be traced. The money arrives and is sent out again within minutes.',
      example: 'An account receives $45,000 and sends it out to 8 different people within 18 minutes, keeping a $0 balance.'
    },
    {
      term: 'Circular Wash-Trading / Cycle-3 Loop',
      plain: 'The Carousel Trick (Money Travelling in Circles)',
      explanation: 'Company A sends money to Company B, Company B sends it to Company C, and Company C sends it back to Company A with fake invoices to fool tax authorities into thinking real business happened.',
      example: 'Three shell companies invoice each other for the same shipment of yarn without moving any physical goods.'
    },
    {
      term: 'Cryptographic WORM Audit Vault',
      plain: 'Digital Wax Seal / Tamper-Proof Ledger',
      explanation: 'WORM stands for "Write Once, Read Many." Once an action is recorded, it is mathematically sealed with SHA-256 encryption. Even the bank president or database administrator cannot delete or alter it.',
      example: 'Guarantees in court that evidence was never doctored or destroyed by corrupt employees.'
    },
    {
      term: 'Conformal Prediction / Risk-Control',
      plain: 'Honest AI Confidence Gauge',
      explanation: 'Normal AI guesses without telling you if it could be wrong. Conformal prediction gives a mathematical guarantee: "We guarantee with 99% statistical confidence that this transaction is safe before auto-clearing it."',
      example: 'The bank can prove to government regulators that false-alarm risks are mathematically bounded.'
    },
    {
      term: 'Population Stability Index (PSI) / Drift',
      plain: 'AI Health & Accuracy Monitor',
      explanation: 'Over time, criminals invent new laundering tricks. This monitor checks whether real-world customer behavior has shifted so the AI does not become blind to new fraud methods.',
      example: 'Alerts the engineering team if a sudden boom in cryptocurrency payments confuses the standard models.'
    },
    {
      term: 'RFI (Request for Information)',
      plain: 'Customer Follow-Up Notice',
      explanation: 'A polite, formal message sent to a customer asking: "Can you please upload an invoice, receipt, or contract to explain this large payment?"',
      example: 'The bank asks an importer for a port bill of lading to verify a $100,000 cotton purchase.'
    }
  ];

  const filteredJargon = JARGON_DICTIONARY.filter(item => 
    item.term.toLowerCase().includes(jargonSearch.toLowerCase()) ||
    item.plain.toLowerCase().includes(jargonSearch.toLowerCase()) ||
    item.explanation.toLowerCase().includes(jargonSearch.toLowerCase())
  );

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 animate-fadeIn">
      <div className="bg-surface border border-border rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] flex flex-col overflow-hidden text-foreground">
        
        {/* Modal Header */}
        <div className="px-6 py-4 border-b border-border flex items-center justify-between bg-surfaceRaised shrink-0">
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg bg-accent/10 border border-accent/30 flex items-center justify-center text-accent">
              <BookOpen className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-base font-bold text-foreground flex items-center gap-2">
                Plain-English Guide & Jargon Buster
                <span className="text-[10px] font-mono font-medium px-2 py-0.5 rounded-full bg-accent/15 text-accent border border-accent/20">
                  Beginner Friendly
                </span>
              </h2>
              <p className="text-xs text-muted">
                Simple, human-understandable explanations for everyday users, managers, and non-engineers.
              </p>
            </div>
          </div>
          <button
            onClick={() => setPlainEnglishGuideOpen(false)}
            className="p-1.5 rounded-lg hover:bg-surfaceHover text-muted hover:text-foreground transition-colors cursor-pointer"
            aria-label="Close Plain English Guide"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Navigation Tabs */}
        <div className="flex border-b border-border bg-surface px-6 pt-2 gap-2 shrink-0 overflow-x-auto">
          {[
            { id: 'overview', label: '🌟 What Does This App Do?', icon: Compass },
            { id: 'tiers', label: '🚦 The 3 Safety Tiers', icon: ShieldCheck },
            { id: 'jargon', label: '📖 Jargon Buster Dictionary', icon: BookOpen },
            { id: 'ai-swarm', label: '🤖 The 4 AI Detectives', icon: Bot },
          ].map(tab => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-3.5 py-2 text-xs font-medium rounded-t-lg border-b-2 transition-colors cursor-pointer whitespace-nowrap ${
                  isActive 
                    ? 'border-accent text-accent bg-accent/5 font-semibold' 
                    : 'border-transparent text-muted hover:text-foreground hover:bg-surfaceHover'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>

        {/* Modal Scrollable Body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          
          {/* TAB 1: OVERVIEW */}
          {activeTab === 'overview' && (
            <div className="space-y-5 animate-fadeIn">
              <div className="p-4 rounded-xl bg-accent/5 border border-accent/20">
                <h3 className="text-sm font-bold text-accent flex items-center gap-2">
                  <Zap className="w-4 h-4" />
                  The 30-Second Elevator Pitch
                </h3>
                <p className="text-xs text-foreground/90 mt-1.5 leading-relaxed">
                  Every year, criminals wash <strong>$2 Trillion</strong> of illegal money through legitimate banks. 
                  Older bank software raises false alarms on <strong>98% of honest people</strong>, forcing human officers to drown in paperwork. 
                  <strong> Intelligent-AML fixes this:</strong> it uses smart AI to instantly approve <strong>98.6% of honest payments</strong>, 
                  locks dangerous criminals immediately, and helps human investigators solve complicated fraud rings with visual maps.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-4 rounded-xl bg-surfaceRaised border border-border flex flex-col justify-between">
                  <div>
                    <div className="w-8 h-8 rounded-lg bg-cleared/15 text-cleared flex items-center justify-center font-bold text-sm mb-2.5">
                      98.6%
                    </div>
                    <h4 className="text-xs font-bold text-foreground">Auto-Approved Payments</h4>
                    <p className="text-[11px] text-muted mt-1 leading-relaxed">
                      Honest salaries, groceries, and invoices clear in <strong>0.12 milliseconds</strong> without human waiting.
                    </p>
                  </div>
                  <span className="text-[10px] font-mono text-cleared mt-3 block font-semibold">
                    ✓ Zero Customer Delays
                  </span>
                </div>

                <div className="p-4 rounded-xl bg-surfaceRaised border border-border flex flex-col justify-between">
                  <div>
                    <div className="w-8 h-8 rounded-lg bg-critical/15 text-critical flex items-center justify-center font-bold text-sm mb-2.5">
                      0.45ms
                    </div>
                    <h4 className="text-xs font-bold text-foreground">Instant Crime Freeze</h4>
                    <p className="text-[11px] text-muted mt-1 leading-relaxed">
                      Confirmed sanctions and illegal cartels are frozen on the spot before dirty money leaves the bank.
                    </p>
                  </div>
                  <span className="text-[10px] font-mono text-critical mt-3 block font-semibold">
                    ✓ 100% Capital Contained
                  </span>
                </div>

                <div className="p-4 rounded-xl bg-surfaceRaised border border-border flex flex-col justify-between">
                  <div>
                    <div className="w-8 h-8 rounded-lg bg-accent/15 text-accent flex items-center justify-center font-bold text-sm mb-2.5">
                      4 AI
                    </div>
                    <h4 className="text-xs font-bold text-foreground">AI Detective Team</h4>
                    <p className="text-[11px] text-muted mt-1 leading-relaxed">
                      Automated AI agents map complex shell company networks and write official police reports in seconds.
                    </p>
                  </div>
                  <span className="text-[10px] font-mono text-accent mt-3 block font-semibold">
                    ✓ Courtroom-Ready Reports
                  </span>
                </div>
              </div>

              <div className="p-4 rounded-xl bg-surfaceRaised border border-border space-y-2">
                <h4 className="text-xs font-bold text-foreground flex items-center gap-2">
                  <Globe className="w-4 h-4 text-accent" />
                  What Real-World Problems Does This Solve?
                </h4>
                <ul className="text-xs text-muted space-y-1.5 list-disc list-inside">
                  <li><strong>Stops Innocent Customers from Getting Blocked:</strong> Normal parents sending tuition or businesses paying suppliers aren’t held up for days.</li>
                  <li><strong>Catches "Invisible" Laundering Tricks:</strong> Uncovers criminals who break money into tiny chunks ($9,500) to sneak past normal $10,000 bank limits.</li>
                  <li><strong>Prevents Bribery & Corruption:</strong> Requires two separate officers to sign off before anyone can freeze or unfreeze bank accounts.</li>
                  <li><strong>Tamper-Proof Proof in Court:</strong> Evidence is digitally sealed with SHA-256 encryption, so crooked employees cannot delete incriminating logs.</li>
                </ul>
              </div>
            </div>
          )}

          {/* TAB 2: THE 3 SAFETY TIERS */}
          {activeTab === 'tiers' && (
            <div className="space-y-4 animate-fadeIn">
              <p className="text-xs text-muted">
                Every transaction that passes through the bank is automatically categorized like a traffic light:
              </p>

              <div className="p-4 rounded-xl bg-cleared/10 border border-cleared/30 space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="w-3.5 h-3.5 rounded-full bg-cleared shrink-0" />
                    <h4 className="text-sm font-bold text-cleared">Tier 3: Green Light (Instant Auto-Clear / STP)</h4>
                  </div>
                  <span className="text-xs font-mono font-bold text-cleared px-2 py-0.5 rounded bg-cleared/20">
                    98.6% of Volume
                  </span>
                </div>
                <p className="text-xs text-foreground/90 leading-relaxed">
                  <strong>What it means:</strong> The payment is clean, normal, and verified. The customer gets their money in milliseconds without any human officer needing to look at it.
                </p>
                <div className="text-[11px] text-muted bg-surface/60 p-2 rounded border border-border">
                  💡 <em>Real-World Example:</em> A monthly corporate salary of $4,500, utility bills, or paying for groceries at a supermarket.
                </div>
              </div>

              <div className="p-4 rounded-xl bg-review/10 border border-review/30 space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="w-3.5 h-3.5 rounded-full bg-review shrink-0" />
                    <h4 className="text-sm font-bold text-review">Tier 2: Yellow Light (Needs Human Officer Check)</h4>
                  </div>
                  <span className="text-xs font-mono font-bold text-review px-2 py-0.5 rounded bg-review/20">
                    1.1% of Volume
                  </span>
                </div>
                <p className="text-xs text-foreground/90 leading-relaxed">
                  <strong>What it means:</strong> The payment has an unusual pattern that requires a human compliance officer to inspect. It is placed into the analyst review queue with an investigation timer (SLA).
                </p>
                <div className="text-[11px] text-muted bg-surface/60 p-2 rounded border border-border">
                  💡 <em>Real-World Example:</em> A retail bakery account that normally receives $200 suddenly gets three separate foreign transfers of $9,800 within 30 minutes.
                </div>
              </div>

              <div className="p-4 rounded-xl bg-critical/10 border border-critical/30 space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="w-3.5 h-3.5 rounded-full bg-critical shrink-0" />
                    <h4 className="text-sm font-bold text-critical">Tier 1: Red Light (Immediate Freeze / Auto-Quarantine)</h4>
                  </div>
                  <span className="text-xs font-mono font-bold text-critical px-2 py-0.5 rounded bg-critical/20">
                    0.3% of Volume
                  </span>
                </div>
                <p className="text-xs text-foreground/90 leading-relaxed">
                  <strong>What it means:</strong> Definite match with international sanctions (UN, US OFAC, EU, BFIU), terror financing, or massive customs trade fraud. The transaction is halted instantly, the money is locked in an escrow vault, and an official legal case is opened.
                </p>
                <div className="text-[11px] text-muted bg-surface/60 p-2 rounded border border-border">
                  💡 <em>Real-World Example:</em> An import invoice claiming $42.50 per kg of cotton when standard government customs rate is only $9.80, with funds routed directly to a sanctioned offshore shell company in Dubai.
                </div>
              </div>
            </div>
          )}

          {/* TAB 3: JARGON BUSTER */}
          {activeTab === 'jargon' && (
            <div className="space-y-4 animate-fadeIn">
              <div className="flex items-center justify-between gap-3">
                <p className="text-xs text-muted">
                  Search any complicated banking or tech term to see what it actually means in plain English:
                </p>
                <div className="relative w-64 shrink-0">
                  <Search className="w-3.5 h-3.5 text-muted absolute left-2.5 top-1/2 -translate-y-1/2" />
                  <input
                    type="text"
                    value={jargonSearch}
                    onChange={(e) => setJargonSearch(e.target.value)}
                    placeholder="Search jargon (e.g., STP, smurfing)..."
                    className="w-full pl-8 pr-3 py-1.5 text-xs rounded-lg bg-surfaceRaised border border-border text-foreground placeholder:text-muted focus:outline-none focus:border-accent"
                  />
                </div>
              </div>

              <div className="space-y-3">
                {filteredJargon.map((item, idx) => (
                  <div key={idx} className="p-3.5 rounded-lg bg-surfaceRaised border border-border space-y-1.5">
                    <div className="flex items-center justify-between gap-2">
                      <span className="font-mono text-xs font-bold text-accent">{item.term}</span>
                      <span className="text-xs font-bold text-cleared bg-cleared/10 px-2 py-0.5 rounded border border-cleared/20">
                        = {item.plain}
                      </span>
                    </div>
                    <p className="text-xs text-foreground/90 leading-relaxed">
                      {item.explanation}
                    </p>
                    <div className="text-[11px] text-muted font-mono bg-surface p-1.5 rounded border border-borderSubtle">
                      <strong>Example:</strong> {item.example}
                    </div>
                  </div>
                ))}

                {filteredJargon.length === 0 && (
                  <div className="text-center py-8 text-xs text-muted">
                    No jargon terms found matching "{jargonSearch}". Try typing "STP", "Maker", "SAR", or "Freeze".
                  </div>
                )}
              </div>
            </div>
          )}

          {/* TAB 4: THE 4 AI DETECTIVES */}
          {activeTab === 'ai-swarm' && (
            <div className="space-y-4 animate-fadeIn">
              <p className="text-xs text-muted">
                Instead of relying on a single fallible AI, this system uses a team of 4 specialized AI detectives that check each other’s work:
              </p>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="p-4 rounded-xl bg-surfaceRaised border border-border space-y-2">
                  <div className="flex items-center gap-2">
                    <div className="w-7 h-7 rounded-lg bg-accent/15 text-accent flex items-center justify-center font-bold text-xs">
                      🕵️‍♂️
                    </div>
                    <div>
                      <h4 className="text-xs font-bold text-foreground">1. The Forensic Investigator Agent</h4>
                      <span className="text-[10px] font-mono text-muted">"Follows the Money"</span>
                    </div>
                  </div>
                  <p className="text-xs text-muted leading-relaxed">
                    Traces money across banks, mobile wallets, and international borders. Identifies middleman shell accounts and tracks how fast money moved.
                  </p>
                </div>

                <div className="p-4 rounded-xl bg-surfaceRaised border border-border space-y-2">
                  <div className="flex items-center gap-2">
                    <div className="w-7 h-7 rounded-lg bg-cleared/15 text-cleared flex items-center justify-center font-bold text-xs">
                      ⚖️
                    </div>
                    <div>
                      <h4 className="text-xs font-bold text-foreground">2. The Legal Auditor Agent</h4>
                      <span className="text-[10px] font-mono text-muted">"Knows the Law"</span>
                    </div>
                  </div>
                  <p className="text-xs text-muted leading-relaxed">
                    Checks the activity against international laws (US FinCEN, UN Sanctions, Bangladesh Bank BFIU Circular 26). Cites exact statutory sections for legal filing.
                  </p>
                </div>

                <div className="p-4 rounded-xl bg-surfaceRaised border border-border space-y-2">
                  <div className="flex items-center gap-2">
                    <div className="w-7 h-7 rounded-lg bg-review/15 text-review flex items-center justify-center font-bold text-xs">
                      ✍️
                    </div>
                    <div>
                      <h4 className="text-xs font-bold text-foreground">3. The SAR Narrative Drafter Agent</h4>
                      <span className="text-[10px] font-mono text-muted">"Writes the Police Report"</span>
                    </div>
                  </div>
                  <p className="text-xs text-muted leading-relaxed">
                    Takes the evidence and writes a clean, 5-page courtroom-grade legal complaint in minutes, including transaction tables and customs invoices.
                  </p>
                </div>

                <div className="p-4 rounded-xl bg-surfaceRaised border border-border space-y-2">
                  <div className="flex items-center gap-2">
                    <div className="w-7 h-7 rounded-lg bg-critical/15 text-critical flex items-center justify-center font-bold text-xs">
                      🛡️
                    </div>
                    <div>
                      <h4 className="text-xs font-bold text-foreground">4. The Chief Verification Agent</h4>
                      <span className="text-[10px] font-mono text-muted">"Guarantees 0% Hallucination"</span>
                    </div>
                  </div>
                  <p className="text-xs text-muted leading-relaxed">
                    Audits every single dollar amount, account ID, and date against the bank’s core ledger. If a single number doesn’t match reality, it rejects the draft.
                  </p>
                </div>
              </div>

              <div className="p-3.5 rounded-xl bg-accent/5 border border-accent/20 flex items-center gap-3">
                <CheckCircle2 className="w-5 h-5 text-accent shrink-0" />
                <p className="text-xs text-foreground/90">
                  <strong>Human in the Loop:</strong> Even after the AI team compiles the report, it <em>cannot</em> be submitted without two human bank officers physically reviewing and signing off.
                </p>
              </div>
            </div>
          )}

        </div>

        {/* Modal Footer */}
        <div className="px-6 py-3.5 border-t border-border bg-surfaceRaised flex items-center justify-between shrink-0">
          <span className="text-xs text-muted font-mono">
            Designed for compliance officers, auditors & non-technical bank leaders
          </span>
          <button
            onClick={() => setPlainEnglishGuideOpen(false)}
            className="px-4 py-1.5 rounded-lg bg-accent text-white font-medium text-xs hover:bg-accentHover transition-colors cursor-pointer"
          >
            Got it, Let's Explore!
          </button>
        </div>

      </div>
    </div>
  );
};
