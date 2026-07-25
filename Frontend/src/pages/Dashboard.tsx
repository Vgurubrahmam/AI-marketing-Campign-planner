import { Link } from 'react-router-dom';
import { Plus, BarChart3, Clock, CheckCircle2, Loader2, Trash2 } from 'lucide-react';
import { useCampaignList, useDashboardStats, useDeleteCampaign } from '../hooks/useCampaign';
import { toast } from 'sonner';

export default function Dashboard() {
  const { data: statsData } = useDashboardStats();
  const { data: listData, isLoading } = useCampaignList();
  const deleteMutation = useDeleteCampaign();

  const stats = [
    { label: 'Total Campaigns', value: statsData?.total_campaigns ?? 0, icon: BarChart3, color: '#6366f1' },
    { label: 'This Month', value: statsData?.this_month ?? 0, icon: Clock, color: '#06b6d4' },
    { label: 'Generating', value: statsData?.generating ?? 0, icon: Loader2, color: '#f59e0b' },
    { label: 'Completed', value: statsData?.completed ?? 0, icon: CheckCircle2, color: '#10b981' },
  ];

  const handleDelete = (id: string, e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (confirm('Delete this campaign? This cannot be undone.')) {
      deleteMutation.mutate(id, {
        onSuccess: () => toast.success('Campaign deleted'),
        onError: () => toast.error('Failed to delete campaign'),
      });
    }
  };

  return (
    <div className="page container">
      {/* Header */}
      <div className="animate-fade-in" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '32px' }}>
        <div>
          <h1 style={{ fontSize: '1.75rem', marginBottom: '4px' }}>Dashboard</h1>
          <p style={{ fontSize: '0.875rem' }}>Manage your AI-generated marketing campaigns</p>
        </div>
        <Link to="/app/generate" className="btn btn-primary" style={{ textDecoration: 'none' }}>
          <Plus size={18} />
          New Campaign
        </Link>
      </div>

      {/* Stats Grid */}
      <div className="animate-fade-in-up delay-100" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '40px' }}>
        {stats.map((s) => (
          <div key={s.label} className="glass-card" style={{ padding: '20px', display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div style={{ width: '42px', height: '42px', borderRadius: 'var(--radius-md)', background: `${s.color}15`, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
              <s.icon size={20} style={{ color: s.color }} />
            </div>
            <div>
              <div style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--color-text-primary)', lineHeight: 1 }}>{s.value}</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', marginTop: '2px' }}>{s.label}</div>
            </div>
          </div>
        ))}
      </div>

      {/* Campaign List */}
      <div className="animate-fade-in-up delay-200">
        <h3 style={{ marginBottom: '16px' }}>Recent Campaigns</h3>

        {isLoading ? (
          <div style={{ display: 'grid', gap: '12px' }}>
            {[1, 2, 3].map((i) => (
              <div key={i} className="skeleton" style={{ height: '88px' }} />
            ))}
          </div>
        ) : !listData?.campaigns?.length ? (
          <div className="glass-card" style={{ padding: '60px 40px', textAlign: 'center' }}>
            <div style={{ fontSize: '3rem', marginBottom: '12px' }}>🚀</div>
            <h4 style={{ marginBottom: '8px' }}>No campaigns yet</h4>
            <p style={{ fontSize: '0.875rem', marginBottom: '24px' }}>Create your first AI-powered marketing campaign</p>
            <Link to="/app/generate" className="btn btn-primary" style={{ textDecoration: 'none' }}>
              <Plus size={18} />
              Create Campaign
            </Link>
          </div>
        ) : (
          <div style={{ display: 'grid', gap: '12px' }}>
            {listData.campaigns.map((campaign: any, i: number) => (
              <Link
                key={campaign.id}
                to={`/app/campaign/${campaign.id}`}
                className="solid-card animate-fade-in"
                style={{
                  padding: '20px 24px',
                  textDecoration: 'none',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  animationDelay: `${i * 80}ms`,
                  opacity: 0,
                  animationFillMode: 'forwards',
                }}
              >
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '4px' }}>
                    <h4 style={{ fontSize: '0.9375rem', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                      {campaign.product_description.substring(0, 80)}...
                    </h4>
                    <span className={`badge ${statusBadge(campaign.status)}`}>
                      {campaign.status}
                    </span>
                  </div>
                  <div style={{ display: 'flex', gap: '16px', fontSize: '0.8125rem', color: 'var(--color-text-muted)' }}>
                    <span>{campaign.industry}</span>
                    <span>•</span>
                    <span>{campaign.marketing_goal.replace(/_/g, ' ')}</span>
                    <span>•</span>
                    <span>₹{Number(campaign.budget_amount).toLocaleString('en-IN')}</span>
                    <span>•</span>
                    <span>{new Date(campaign.created_at).toLocaleDateString()}</span>
                  </div>
                </div>

                <button
                  onClick={(e) => handleDelete(campaign.id, e)}
                  className="btn btn-ghost btn-sm"
                  style={{ color: 'var(--color-text-muted)', flexShrink: 0 }}
                  title="Delete campaign"
                >
                  <Trash2 size={14} />
                </button>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function statusBadge(status: string) {
  switch (status) {
    case 'complete': return 'badge-success';
    case 'generating': return 'badge-warning';
    case 'failed': return 'badge-error';
    default: return 'badge-info';
  }
}
