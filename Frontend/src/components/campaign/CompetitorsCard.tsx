import React from 'react';
import { Shield, Sparkles, Copy, Check } from 'lucide-react';

export interface Competitor {
  id: string;
  name: string;
  positioning: string;
  differentiator_opportunity: string;
}

interface CompetitorsCardProps {
  competitors: Competitor[];
  onCopy: (text: string, id: string, label: string) => void;
  copiedId: string | null;
}

export const CompetitorsCard: React.FC<CompetitorsCardProps> = ({
  competitors,
  onCopy,
  copiedId,
}) => {
  if (!competitors || competitors.length === 0) {
    return <p style={{ color: 'var(--color-text-muted)', fontSize: '0.875rem' }}>No competitor research generated.</p>;
  }

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(290px, 1fr))', gap: '16px' }}>
      {competitors.map((comp, idx) => {
        const idStr = comp.id || `competitor-${idx}`;
        const copyText = `Competitor: ${comp.name}\nPositioning: ${comp.positioning}\nDifferentiator Opportunity: ${comp.differentiator_opportunity}`;

        return (
          <div
            key={idStr}
            className="solid-card"
            style={{
              padding: '18px',
              display: 'flex',
              flexDirection: 'column',
              justify: 'space-between',
              borderLeft: '4px solid #f43f5e',
              borderRadius: 'var(--radius-md)',
              background: 'var(--color-bg-secondary)',
            }}
          >
            <div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '10px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <div
                    style={{
                      width: '28px',
                      height: '28px',
                      borderRadius: 'var(--radius-md)',
                      background: 'rgba(244, 63, 94, 0.15)',
                      display: 'flex',
                      alignItems: 'center',
                      justify: 'center',
                    }}
                  >
                    <Shield size={15} color="#f43f5e" />
                  </div>
                  <h4 style={{ fontSize: '0.9375rem', fontWeight: 600 }}>{comp.name}</h4>
                </div>

                <button
                  className="btn btn-ghost btn-sm"
                  style={{ padding: '4px 6px', height: 'auto' }}
                  onClick={() => onCopy(copyText, idStr, comp.name)}
                  title="Copy Competitor Details"
                >
                  {copiedId === idStr ? (
                    <Check size={14} color="var(--color-success)" />
                  ) : (
                    <Copy size={14} />
                  )}
                </button>
              </div>

              <div style={{ marginBottom: '12px' }}>
                <span
                  style={{
                    fontSize: '0.75rem',
                    textTransform: 'uppercase',
                    letterSpacing: '0.05em',
                    color: 'var(--color-text-muted)',
                    fontWeight: 600,
                    display: 'block',
                    marginBottom: '4px',
                  }}
                >
                  Market Positioning
                </span>
                <p style={{ fontSize: '0.8125rem', color: 'var(--color-text-primary)', lineHeight: '1.4' }}>
                  {comp.positioning}
                </p>
              </div>

              <div
                style={{
                  padding: '10px 12px',
                  borderRadius: 'var(--radius-sm)',
                  background: 'rgba(244, 63, 94, 0.08)',
                  border: '1px solid rgba(244, 63, 94, 0.2)',
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: '5px', marginBottom: '4px' }}>
                  <Sparkles size={13} color="#f43f5e" />
                  <span style={{ fontSize: '0.75rem', fontWeight: 600, color: '#f43f5e' }}>
                    Differentiator Opportunity
                  </span>
                </div>
                <p style={{ fontSize: '0.8125rem', color: 'var(--color-text-primary)', lineHeight: '1.4' }}>
                  {comp.differentiator_opportunity}
                </p>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default CompetitorsCard;
