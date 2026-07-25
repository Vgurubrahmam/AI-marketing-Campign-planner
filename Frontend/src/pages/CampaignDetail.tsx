import { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  ArrowLeft, RefreshCw, Users, Target, Search, DollarSign, Calendar,
  FileText, Download, Copy, Check, Printer, FileCode, Edit2, Save
} from 'lucide-react';
import { useCampaign, useCampaignStatus, useRegenerateSection } from '../hooks/useCampaign';
import { toast } from 'sonner';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';

const SECTION_ORDER = ['persona', 'ad_copy', 'keywords', 'budget', 'schedule', 'summary'];

const SECTION_META: Record<string, { label: string; icon: any; color: string }> = {
  persona: { label: 'Audience Personas', icon: Users, color: '#818cf8' },
  ad_copy: { label: 'Ad Copy', icon: Target, color: '#06b6d4' },
  keywords: { label: 'Keywords', icon: Search, color: '#10b981' },
  budget: { label: 'Budget Allocation', icon: DollarSign, color: '#f59e0b' },
  schedule: { label: 'Publishing Schedule', icon: Calendar, color: '#ec4899' },
  summary: { label: 'Campaign Summary', icon: FileText, color: '#8b5cf6' },
};

const PIE_COLORS = ['#6366f1', '#06b6d4', '#10b981', '#f59e0b', '#ec4899', '#8b5cf6'];

export default function CampaignDetail() {
  const { id } = useParams<{ id: string }>();
  const { data: statusData } = useCampaignStatus(id!, true);
  const { data: campaign } = useCampaign(id!);
  const regenerate = useRegenerateSection();
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const isGenerating = statusData?.status === 'generating';
  const sectionStatus = statusData?.section_status || {};
  const statusDoneCount = Object.values(sectionStatus).filter((s) => s === 'done').length;

  const handleRegenerate = (section: string) => {
    regenerate.mutate(
      { id: id!, section },
      {
        onSuccess: () => toast.success(`Regenerating ${SECTION_META[section]?.label}...`),
        onError: () => toast.error('Regeneration failed'),
      }
    );
  };

  const handleCopyText = (text: string, idStr: string, label: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(idStr);
    toast.success(`Copied ${label} to clipboard`);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const exportMarkdown = () => {
    if (!campaign) return;
    const md = generateMarkdown(campaign);
    downloadBlob(md, `campaign-plan-${campaign.id.substring(0, 8)}.md`, 'text/markdown');
    toast.success('Campaign exported as Markdown');
  };

  const exportJson = () => {
    if (!campaign) return;
    const json = JSON.stringify(campaign, null, 2);
    downloadBlob(json, `campaign-plan-${campaign.id.substring(0, 8)}.json`, 'application/json');
    toast.success('Campaign exported as JSON');
  };

  const exportPdf = () => {
    window.print();
  };

  return (
    <div className="page container" style={{ maxWidth: '960px', margin: '0 auto', padding: '32px 24px' }}>
      {/* Header */}
      <div className="animate-fade-in" style={{ marginBottom: '32px' }}>
        <Link to="/app/dashboard" style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', fontSize: '0.875rem', color: 'var(--color-text-muted)', marginBottom: '16px' }}>
          <ArrowLeft size={14} />
          Back to Dashboard
        </Link>

        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '16px' }}>
          <div>
            <h1 style={{ fontSize: '1.5rem', marginBottom: '8px' }}>Campaign Details</h1>
            {campaign && (
              <div style={{ display: 'flex', gap: '12px', fontSize: '0.8125rem', color: 'var(--color-text-muted)', flexWrap: 'wrap' }}>
                <span>{campaign.industry}</span>
                <span>•</span>
                <span>{campaign.marketing_goal.replace(/_/g, ' ')}</span>
                <span>•</span>
                <span>₹{Number(campaign.budget_amount).toLocaleString('en-IN')}</span>
              </div>
            )}
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <span className={`badge ${isGenerating ? 'badge-warning' : statusData?.status === 'complete' ? 'badge-success' : 'badge-error'}`}>
              {statusData?.status || 'loading'}
            </span>

            {/* Export Menu */}
            {campaign && (
              <div style={{ display: 'flex', gap: '8px' }}>
                <button onClick={exportMarkdown} className="btn btn-secondary btn-sm" title="Export Markdown">
                  <Download size={14} />
                  Markdown
                </button>
                <button onClick={exportJson} className="btn btn-secondary btn-sm" title="Export JSON">
                  <FileCode size={14} />
                  JSON
                </button>
                <button onClick={exportPdf} className="btn btn-secondary btn-sm" title="Print / Save PDF">
                  <Printer size={14} />
                  Print
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Progress bar */}
        {isGenerating && (
          <div style={{ marginTop: '16px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.75rem', color: 'var(--color-text-muted)', marginBottom: '6px' }}>
              <span>Generating campaign...</span>
              <span>{statusDoneCount} / {SECTION_ORDER.length} sections</span>
            </div>
            <div style={{ height: '4px', borderRadius: 'var(--radius-full)', background: 'var(--color-bg-tertiary)', overflow: 'hidden' }}>
              <div
                style={{
                  height: '100%',
                  borderRadius: 'var(--radius-full)',
                  background: 'var(--gradient-primary)',
                  transition: 'width 0.5s ease',
                  width: `${(statusDoneCount / SECTION_ORDER.length) * 100}%`,
                }}
              />
            </div>
          </div>
        )}
      </div>

      {/* Sections */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
        {SECTION_ORDER.map((section) => {
          const meta = SECTION_META[section];
          const status = sectionStatus[section] || 'pending';
          const Icon = meta.icon;

          return (
            <div key={section} className={`glass-card ${status === 'done' ? 'animate-fade-in-up' : ''}`} style={{ overflow: 'hidden' }}>
              {/* Section Header */}
              <div style={{
                display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                padding: '16px 24px', borderBottom: status === 'done' ? '1px solid var(--color-border)' : 'none',
              }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <div style={{
                    width: '36px', height: '36px', borderRadius: 'var(--radius-md)',
                    background: `${meta.color}15`, display: 'flex', alignItems: 'center', justifyContent: 'center',
                  }}>
                    <Icon size={18} style={{ color: meta.color }} />
                  </div>
                  <div>
                    <h4 style={{ fontSize: '0.9375rem' }}>{meta.label}</h4>
                    <span style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>
                      {status === 'done' ? 'Complete' : status === 'pending' ? 'Waiting...' : status === 'generating' ? 'Generating...' : 'Failed'}
                    </span>
                  </div>
                </div>

                {status === 'done' && (
                  <button
                    className="btn btn-ghost btn-sm"
                    onClick={() => handleRegenerate(section)}
                    disabled={regenerate.isPending}
                  >
                    <RefreshCw size={14} />
                    Regenerate
                  </button>
                )}
              </div>

              {/* Section Content */}
              {status === 'pending' || status === 'generating' ? (
                <div style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
                  <div className="skeleton" style={{ height: '16px', width: '60%' }} />
                  <div className="skeleton" style={{ height: '16px', width: '80%' }} />
                  <div className="skeleton" style={{ height: '16px', width: '45%' }} />
                </div>
              ) : status === 'done' && campaign ? (
                <div style={{ padding: '20px 24px' }}>
                  {section === 'persona' && <PersonaSection personas={campaign.personas} onCopy={handleCopyText} copiedId={copiedId} />}
                  {section === 'ad_copy' && <AdCopySection copies={campaign.ad_copies} onCopy={handleCopyText} copiedId={copiedId} />}
                  {section === 'keywords' && <KeywordSection keywords={campaign.keywords} onCopy={handleCopyText} copiedId={copiedId} />}
                  {section === 'budget' && <BudgetSection budgets={campaign.budgets} />}
                  {section === 'schedule' && <ScheduleSection plans={campaign.publishing_plans} />}
                  {section === 'summary' && <SummarySection summary={campaign.summary} onCopy={handleCopyText} copiedId={copiedId} campaign={campaign} />}
                </div>
              ) : status === 'failed' ? (
                <div style={{ padding: '24px', textAlign: 'center' }}>
                  <p style={{ color: 'var(--color-error)', fontSize: '0.875rem', marginBottom: '12px' }}>Generation failed for this section</p>
                  <button className="btn btn-secondary btn-sm" onClick={() => handleRegenerate(section)}>
                    <RefreshCw size={14} /> Retry
                  </button>
                </div>
              ) : null}
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ===== Section Components =====

function PersonaSection({ personas, onCopy, copiedId }: { personas: any[]; onCopy: any; copiedId: string | null }) {
  if (!personas?.length) return <p style={{ color: 'var(--color-text-muted)' }}>No personas generated</p>;

  return (
    <div style={{ display: 'grid', gap: '16px' }}>
      {personas.map((p: any, i: number) => {
        const idStr = p.id || `persona-${i}`;
        const personaText = `${p.persona_name}\nDemographics: ${JSON.stringify(p.demographics)}\nPain Points: ${p.pain_points?.join(', ')}\nChannels: ${p.channels?.join(', ')}\nMessaging: ${p.messaging_angle || ''}`;

        return (
          <div key={idStr} className="solid-card" style={{ padding: '20px', position: 'relative' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <div style={{
                  width: '40px', height: '40px', borderRadius: 'var(--radius-full)',
                  background: `${PIE_COLORS[i % PIE_COLORS.length]}20`,
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontSize: '1.1rem',
                }}>
                  {['👩‍💼', '👨‍💻', '👩‍🔬'][i] || '👤'}
                </div>
                <h4 style={{ fontSize: '0.9375rem' }}>{p.persona_name}</h4>
              </div>

              <button
                className="btn btn-ghost btn-sm"
                onClick={() => onCopy(personaText, idStr, p.persona_name)}
                title="Copy Persona Details"
              >
                {copiedId === idStr ? <Check size={14} color="var(--color-success)" /> : <Copy size={14} />}
              </button>
            </div>

            {p.demographics && (
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginBottom: '12px' }}>
                {Object.entries(p.demographics).map(([k, v]) => (
                  <span key={k} className="badge badge-primary" style={{ fontSize: '0.6875rem' }}>
                    {String(v)}
                  </span>
                ))}
              </div>
            )}

            {p.pain_points?.length > 0 && (
              <div style={{ marginBottom: '10px' }}>
                <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-text-muted)', display: 'block', marginBottom: '6px' }}>Pain Points</span>
                <ul style={{ paddingLeft: '16px', fontSize: '0.8125rem', color: 'var(--color-text-secondary)', display: 'flex', flexDirection: 'column', gap: '4px' }}>
                  {p.pain_points.map((pp: string, j: number) => <li key={j}>{pp}</li>)}
                </ul>
              </div>
            )}

            {p.channels?.length > 0 && (
              <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                {p.channels.map((ch: string, j: number) => (
                  <span key={j} className="badge badge-info" style={{ fontSize: '0.6875rem' }}>{ch}</span>
                ))}
              </div>
            )}

            {p.messaging_angle && (
              <p style={{ fontSize: '0.8125rem', marginTop: '10px', fontStyle: 'italic', color: 'var(--color-text-muted)' }}>
                💡 {p.messaging_angle}
              </p>
            )}
          </div>
        );
      })}
    </div>
  );
}

function AdCopySection({ copies, onCopy, copiedId }: { copies: any[]; onCopy: any; copiedId: string | null }) {
  if (!copies?.length) return <p style={{ color: 'var(--color-text-muted)' }}>No ad copy generated</p>;

  const platformColors: Record<string, string> = {
    google: '#4285F4', meta: '#0084FF', linkedin: '#0A66C2', instagram: '#E4405F',
  };

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
      {copies.map((c: any, i: number) => {
        const idStr = c.id || `ad-${i}`;
        const copyText = `Headline: ${c.headline}\nBody: ${c.body}\nCTA: ${c.cta}`;

        return (
          <div key={idStr} className="solid-card" style={{ padding: '20px', position: 'relative' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
              <span className="badge" style={{
                background: `${platformColors[c.platform] || '#666'}20`,
                color: platformColors[c.platform] || '#666',
                fontWeight: 600, textTransform: 'capitalize',
              }}>
                {c.platform}
              </span>

              <button
                className="btn btn-ghost btn-sm"
                onClick={() => onCopy(copyText, idStr, `${c.platform} ad copy`)}
                title="Copy Ad Copy"
              >
                {copiedId === idStr ? <Check size={14} color="var(--color-success)" /> : <Copy size={14} />}
              </button>
            </div>
            <h4 style={{ fontSize: '0.9375rem', marginBottom: '8px', lineHeight: 1.3 }}>{c.headline}</h4>
            <p style={{ fontSize: '0.8125rem', marginBottom: '12px', lineHeight: 1.6 }}>{c.body}</p>
            <div style={{
              display: 'inline-block', padding: '6px 14px', borderRadius: 'var(--radius-md)',
              background: 'var(--gradient-primary)', color: 'white', fontSize: '0.8125rem', fontWeight: 500,
            }}>
              {c.cta}
            </div>
          </div>
        );
      })}
    </div>
  );
}

function KeywordSection({ keywords, onCopy, copiedId }: { keywords: any[]; onCopy: any; copiedId: string | null }) {
  if (!keywords?.length) return <p style={{ color: 'var(--color-text-muted)' }}>No keywords generated</p>;

  const allKeywordsText = keywords.map((k: any) => `${k.keyword} (${k.keyword_type}, ${k.intent || 'n/a'})`).join('\n');

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '12px' }}>
        <button
          className="btn btn-ghost btn-sm"
          onClick={() => onCopy(allKeywordsText, 'all-keywords', 'All Keywords')}
        >
          {copiedId === 'all-keywords' ? <Check size={14} color="var(--color-success)" /> : <Copy size={14} />}
          Copy Keywords List
        </button>
      </div>

      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.8125rem' }}>
          <thead>
            <tr style={{ borderBottom: '1px solid var(--color-border)' }}>
              <th style={{ textAlign: 'left', padding: '8px 12px', color: 'var(--color-text-muted)', fontWeight: 500 }}>Keyword</th>
              <th style={{ textAlign: 'left', padding: '8px 12px', color: 'var(--color-text-muted)', fontWeight: 500 }}>Type</th>
              <th style={{ textAlign: 'left', padding: '8px 12px', color: 'var(--color-text-muted)', fontWeight: 500 }}>Intent</th>
              <th style={{ textAlign: 'right', padding: '8px 12px', color: 'var(--color-text-muted)', fontWeight: 500 }}>Relevance</th>
            </tr>
          </thead>
          <tbody>
            {keywords.map((k: any, i: number) => (
              <tr key={k.id || i} style={{ borderBottom: '1px solid var(--color-border)' }}>
                <td style={{ padding: '10px 12px', color: 'var(--color-text-primary)' }}>{k.keyword}</td>
                <td style={{ padding: '10px 12px' }}>
                  <span className={`badge ${k.keyword_type === 'ppc' ? 'badge-warning' : 'badge-primary'}`}>{k.keyword_type}</span>
                </td>
                <td style={{ padding: '10px 12px' }}>
                  <span className={`badge ${k.intent === 'transactional' ? 'badge-success' : k.intent === 'informational' ? 'badge-info' : 'badge-primary'}`}>{k.intent || '—'}</span>
                </td>
                <td style={{ padding: '10px 12px', textAlign: 'right' }}>
                  {k.relevance_score ? (
                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'flex-end', gap: '8px' }}>
                      <div style={{ width: '60px', height: '4px', borderRadius: 'var(--radius-full)', background: 'var(--color-bg-tertiary)', overflow: 'hidden' }}>
                        <div style={{ width: `${(k.relevance_score * 100)}%`, height: '100%', background: 'var(--color-success)', borderRadius: 'var(--radius-full)' }} />
                      </div>
                      <span style={{ color: 'var(--color-text-muted)', fontSize: '0.75rem', minWidth: '30px' }}>
                        {(k.relevance_score * 100).toFixed(0)}%
                      </span>
                    </div>
                  ) : '—'}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function BudgetSection({ budgets }: { budgets: any[] }) {
  if (!budgets?.length) return <p style={{ color: 'var(--color-text-muted)' }}>No budget allocation generated</p>;

  const chartData = budgets.map((b: any) => ({
    name: b.channel,
    value: Number(b.allocation_percent),
  }));

  return (
    <div style={{ display: 'grid', gridTemplateColumns: '240px 1fr', gap: '24px', alignItems: 'start' }}>
      {/* Pie Chart */}
      <div style={{ height: '220px' }}>
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              outerRadius={90}
              innerRadius={50}
              dataKey="value"
              paddingAngle={2}
            >
              {chartData.map((_: any, i: number) => (
                <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{
                background: 'var(--color-bg-secondary)',
                border: '1px solid var(--color-border)',
                borderRadius: 'var(--radius-md)',
                color: 'var(--color-text-primary)',
                fontSize: '0.8125rem',
              }}
              formatter={(value: any) => `${value}%`}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Allocation list */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        {budgets.map((b: any, i: number) => (
          <div key={b.id || i} style={{ display: 'flex', alignItems: 'flex-start', gap: '10px' }}>
            <div style={{
              width: '10px', height: '10px', borderRadius: '2px', marginTop: '5px', flexShrink: 0,
              background: PIE_COLORS[i % PIE_COLORS.length],
            }} />
            <div style={{ flex: 1 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2px' }}>
                <span style={{ fontSize: '0.8125rem', fontWeight: 500, color: 'var(--color-text-primary)' }}>{b.channel}</span>
                <span style={{ fontSize: '0.8125rem', fontWeight: 600, color: 'var(--color-text-primary)' }}>
                  ₹{Number(b.amount).toLocaleString('en-IN')} ({Number(b.allocation_percent).toFixed(0)}%)
                </span>
              </div>
              {b.reasoning && (
                <p style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', lineHeight: 1.5 }}>{b.reasoning}</p>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function ScheduleSection({ plans }: { plans: any[] }) {
  if (!plans?.length) return <p style={{ color: 'var(--color-text-muted)' }}>No schedule generated</p>;

  return (
    <div style={{ position: 'relative', paddingLeft: '20px' }}>
      {/* Timeline line */}
      <div style={{
        position: 'absolute', left: '7px', top: '8px', bottom: '8px',
        width: '2px', background: 'var(--color-border)',
      }} />

      {plans.map((p: any, i: number) => (
        <div key={p.id || i} style={{
          position: 'relative', paddingBottom: i < plans.length - 1 ? '20px' : 0,
          paddingLeft: '20px',
        }}>
          {/* Dot */}
          <div style={{
            position: 'absolute', left: '-4px', top: '6px',
            width: '10px', height: '10px', borderRadius: '50%',
            background: PIE_COLORS[i % PIE_COLORS.length],
            border: '2px solid var(--color-bg-primary)',
          }} />

          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '4px' }}>
            <span className="badge badge-primary" style={{ fontSize: '0.6875rem' }}>Day {p.day_offset}</span>
            <span style={{ fontSize: '0.8125rem', fontWeight: 500, color: 'var(--color-text-primary)' }}>{p.channel}</span>
          </div>
          <p style={{ fontSize: '0.8125rem', color: 'var(--color-text-secondary)', lineHeight: 1.5 }}>{p.content_summary}</p>
        </div>
      ))}
    </div>
  );
}

function SummarySection({ summary, onCopy, copiedId, campaign }: { summary?: string; onCopy: any; copiedId: string | null; campaign?: any }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedText, setEditedText] = useState(summary || '');

  useState(() => {
    if (summary) setEditedText(summary);
  });

  const fallbackSummary = campaign
    ? `This AI-generated marketing campaign strategy targets key audience segments within the ${campaign.industry} sector. With a total budget of ₹${Number(campaign.budget_amount).toLocaleString('en-IN')}, the multi-channel approach allocates resources across search, social, and content channels to achieve ${campaign.marketing_goal.replace(/_/g, ' ')}. The 28-day timeline follows a structured launch, optimization, and scaling roadmap.`
    : 'Executive summary synthesizing campaign strategy...';

  const textToDisplay = editedText || summary || fallbackSummary;

  return (
    <div style={{ padding: '4px 0' }}>
      <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '8px', marginBottom: '8px' }}>
        <button
          className="btn btn-ghost btn-sm"
          onClick={() => {
            if (isEditing) {
              toast.success('Summary updated!');
              setIsEditing(false);
            } else {
              setIsEditing(true);
            }
          }}
        >
          {isEditing ? <Save size={14} color="var(--color-success)" /> : <Edit2 size={14} />}
          {isEditing ? 'Save Changes' : 'Edit Summary'}
        </button>

        <button
          className="btn btn-ghost btn-sm"
          onClick={() => onCopy(textToDisplay, 'summary-text', 'Executive Summary')}
        >
          {copiedId === 'summary-text' ? <Check size={14} color="var(--color-success)" /> : <Copy size={14} />}
          Copy
        </button>
      </div>

      {isEditing ? (
        <textarea
          className="input textarea"
          value={editedText}
          onChange={(e) => setEditedText(e.target.value)}
          style={{ minHeight: '120px', width: '100%', fontSize: '0.875rem' }}
        />
      ) : (
        <p style={{ fontSize: '0.875rem', lineHeight: 1.8, color: 'var(--color-text-secondary)', whiteSpace: 'pre-line' }}>
          {textToDisplay}
        </p>
      )}
    </div>
  );
}

// ===== Helpers =====

function downloadBlob(content: string, filename: string, type: string) {
  const blob = new Blob([content], { type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

function generateMarkdown(campaign: any) {
  let md = `# AI Marketing Campaign Plan\n\n`;
  md += `**Industry:** ${campaign.industry}\n`;
  md += `**Goal:** ${campaign.marketing_goal.replace(/_/g, ' ')}\n`;
  md += `**Total Budget:** ₹${Number(campaign.budget_amount).toLocaleString('en-IN')}\n`;
  md += `**Created Date:** ${new Date(campaign.created_at).toLocaleDateString()}\n\n`;

  if (campaign.summary) {
    md += `## Executive Summary\n${campaign.summary}\n\n`;
  }

  if (campaign.personas?.length) {
    md += `## Audience Personas\n\n`;
    campaign.personas.forEach((p: any) => {
      md += `### ${p.persona_name}\n`;
      if (p.demographics) {
        md += `**Demographics:** ${Object.entries(p.demographics).map(([k, v]) => `${k}: ${v}`).join(', ')}\n\n`;
      }
      if (p.pain_points?.length) {
        md += `**Pain Points:**\n` + p.pain_points.map((pt: string) => `- ${pt}`).join('\n') + `\n\n`;
      }
      if (p.channels?.length) {
        md += `**Channels:** ${p.channels.join(', ')}\n\n`;
      }
      if (p.messaging_angle) {
        md += `**Messaging Angle:** ${p.messaging_angle}\n\n`;
      }
    });
  }

  if (campaign.ad_copies?.length) {
    md += `## Ad Copy\n\n`;
    campaign.ad_copies.forEach((c: any) => {
      md += `### [${c.platform.toUpperCase()}] ${c.headline}\n`;
      md += `${c.body}\n\n`;
      md += `**CTA:** ${c.cta}\n\n`;
    });
  }

  if (campaign.keywords?.length) {
    md += `## Targeted Keywords\n\n`;
    md += `| Keyword | Type | Intent | Relevance |\n`;
    md += `|---|---|---|---|\n`;
    campaign.keywords.forEach((k: any) => {
      md += `| ${k.keyword} | ${k.keyword_type} | ${k.intent || '-'} | ${(k.relevance_score ? (k.relevance_score * 100).toFixed(0) + '%' : '-')} |\n`;
    });
    md += `\n`;
  }

  if (campaign.budgets?.length) {
    md += `## Budget Allocation\n\n`;
    campaign.budgets.forEach((b: any) => {
      md += `- **${b.channel}:** ₹${Number(b.amount).toLocaleString('en-IN')} (${b.allocation_percent}%)\n  ${b.reasoning || ''}\n`;
    });
    md += `\n`;
  }

  if (campaign.publishing_plans?.length) {
    md += `## Publishing Schedule\n\n`;
    campaign.publishing_plans.forEach((p: any) => {
      md += `- **Day ${p.day_offset} [${p.channel}]:** ${p.content_summary}\n`;
    });
  }

  return md;
}
