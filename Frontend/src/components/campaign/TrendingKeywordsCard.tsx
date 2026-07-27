import React from 'react';
import { TrendingUp, Copy, Check } from 'lucide-react';

export interface TrendingKeyword {
  id: string;
  keyword: string;
  reason: string;
}

interface TrendingKeywordsCardProps {
  trendingKeywords: TrendingKeyword[];
  onCopy: (text: string, id: string, label: string) => void;
  copiedId: string | null;
}

export const TrendingKeywordsCard: React.FC<TrendingKeywordsCardProps> = ({
  trendingKeywords,
  onCopy,
  copiedId,
}) => {
  if (!trendingKeywords || trendingKeywords.length === 0) {
    return <p style={{ color: 'var(--color-text-muted)', fontSize: '0.875rem' }}>No trending keywords generated.</p>;
  }

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '16px' }}>
      {trendingKeywords.map((item, idx) => {
        const idStr = item.id || `trending-${idx}`;
        const copyText = `Keyword: ${item.keyword}\nRationale: ${item.reason}`;

        return (
          <div
            key={idStr}
            className="solid-card"
            style={{
              padding: '16px',
              display: 'flex',
              flexDirection: 'column',
              justify: 'space-between',
              borderLeft: '4px solid #3b82f6',
              borderRadius: 'var(--radius-md)',
              background: 'var(--color-bg-secondary)',
            }}
          >
            <div>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                <span
                  style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: '4px',
                    padding: '4px 10px',
                    borderRadius: 'var(--radius-full)',
                    background: 'rgba(59, 130, 246, 0.15)',
                    color: '#3b82f6',
                    fontSize: '0.8125rem',
                    fontWeight: 600,
                  }}
                >
                  <TrendingUp size={13} />
                  {item.keyword}
                </span>

                <button
                  className="btn btn-ghost btn-sm"
                  style={{ padding: '4px 6px', height: 'auto' }}
                  onClick={() => onCopy(copyText, idStr, item.keyword)}
                  title="Copy Keyword Details"
                >
                  {copiedId === idStr ? (
                    <Check size={14} color="var(--color-success)" />
                  ) : (
                    <Copy size={14} />
                  )}
                </button>
              </div>

              <p style={{ fontSize: '0.8125rem', color: 'var(--color-text-muted)', lineHeight: '1.4', marginTop: '6px' }}>
                {item.reason}
              </p>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default TrendingKeywordsCard;
