import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, ChevronRight } from 'lucide-react';
import { useCreateCampaign } from '../hooks/useCampaign';
import { toast } from 'sonner';

const GOALS = [
  { value: 'brand_awareness', label: 'Brand Awareness' },
  { value: 'lead_generation', label: 'Lead Generation' },
  { value: 'sales', label: 'Direct Sales' },
  { value: 'engagement', label: 'Engagement & Community' },
];

const INDUSTRIES = [
  { value: 'technology', label: 'Technology' },
  { value: 'ecommerce', label: 'E-Commerce' },
  { value: 'saas', label: 'SaaS' },
  { value: 'healthcare', label: 'Healthcare' },
  { value: 'finance', label: 'Finance' },
  { value: 'education', label: 'Education' },
  { value: 'retail', label: 'Retail' },
  { value: 'real_estate', label: 'Real Estate' },
  { value: 'food_beverage', label: 'Food & Beverage' },
  { value: 'other', label: 'Other' },
];

export default function CampaignGenerate() {
  const navigate = useNavigate();
  const createMutation = useCreateCampaign();

  const [form, setForm] = useState({
    product_description: '',
    marketing_goal: '',
    industry: '',
    budget_amount: '',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  const validate = () => {
    const errs: Record<string, string> = {};
    if (form.product_description.length < 20) {
      errs.product_description = 'Description must be at least 20 characters';
    }
    if (!form.marketing_goal) errs.marketing_goal = 'Please select a goal';
    if (!form.industry) errs.industry = 'Please select an industry';
    if (!form.budget_amount || parseFloat(form.budget_amount) <= 0) {
      errs.budget_amount = 'Budget must be greater than 0';
    }
    setErrors(errs);
    return Object.keys(errs).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;

    createMutation.mutate(
      {
        product_description: form.product_description,
        marketing_goal: form.marketing_goal,
        industry: form.industry,
        budget_amount: parseFloat(form.budget_amount),
      },
      {
        onSuccess: (data) => {
          toast.success('Campaign generation started!');
          navigate(`/app/campaign/${data.campaign_id}`);
        },
        onError: (err: any) => {
          const message = err?.response?.data?.detail?.error?.message || 'Failed to create campaign';
          toast.error(message);
        },
      }
    );
  };

  return (
    <div className="page container" style={{ maxWidth: '720px', margin: '0 auto', padding: '40px 24px' }}>
      <div className="animate-fade-in" style={{ textAlign: 'center', marginBottom: '40px' }}>
        <div style={{
          display: 'inline-flex', alignItems: 'center', justifyContent: 'center',
          width: '56px', height: '56px', borderRadius: 'var(--radius-lg)',
          background: 'var(--gradient-primary)', marginBottom: '16px',
          boxShadow: 'var(--shadow-glow-lg)',
        }}>
          <Sparkles size={28} color="white" />
        </div>
        <h1 style={{ marginBottom: '8px' }}>Create New Campaign</h1>
        <p style={{ maxWidth: '500px', margin: '0 auto' }}>
          Describe your product, set your goals, and let AI build your complete marketing strategy.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="glass-card animate-fade-in-up delay-100" style={{ padding: '36px' }}>
        {/* Product Description */}
        <div style={{ marginBottom: '24px' }}>
          <label className="label" htmlFor="product-description">
            Product or Service Description *
          </label>
          <textarea
            id="product-description"
            className={`input textarea ${errors.product_description ? 'input-error' : ''}`}
            placeholder="Describe what your product or service does, who it's for, and what makes it unique. The more detail you provide, the better the AI can tailor your campaign..."
            value={form.product_description}
            onChange={(e) => setForm({ ...form, product_description: e.target.value })}
            style={{ minHeight: '140px' }}
          />
          {errors.product_description && <span className="error-text">{errors.product_description}</span>}
          <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', marginTop: '4px', textAlign: 'right' }}>
            {form.product_description.length} / 5000
          </div>
        </div>

        {/* Goal + Industry row */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '24px' }}>
          <div>
            <label className="label" htmlFor="marketing-goal">Marketing Goal *</label>
            <select
              id="marketing-goal"
              className={`input select ${errors.marketing_goal ? 'input-error' : ''}`}
              value={form.marketing_goal}
              onChange={(e) => setForm({ ...form, marketing_goal: e.target.value })}
            >
              <option value="">Select a goal...</option>
              {GOALS.map((g) => (
                <option key={g.value} value={g.value}>{g.label}</option>
              ))}
            </select>
            {errors.marketing_goal && <span className="error-text">{errors.marketing_goal}</span>}
          </div>

          <div>
            <label className="label" htmlFor="industry">Industry *</label>
            <select
              id="industry"
              className={`input select ${errors.industry ? 'input-error' : ''}`}
              value={form.industry}
              onChange={(e) => setForm({ ...form, industry: e.target.value })}
            >
              <option value="">Select industry...</option>
              {INDUSTRIES.map((i) => (
                <option key={i.value} value={i.value}>{i.label}</option>
              ))}
            </select>
            {errors.industry && <span className="error-text">{errors.industry}</span>}
          </div>
        </div>

        {/* Budget */}
        <div style={{ marginBottom: '32px' }}>
          <label className="label" htmlFor="budget">Total Campaign Budget (INR ₹) *</label>
          <div style={{ position: 'relative' }}>
            <span style={{
              position: 'absolute', left: '14px', top: '50%', transform: 'translateY(-50%)',
              color: 'var(--color-text-muted)', fontSize: '0.875rem', fontWeight: 500,
            }}>₹</span>
            <input
              id="budget"
              type="number"
              className={`input ${errors.budget_amount ? 'input-error' : ''}`}
              placeholder="1,00,000"
              value={form.budget_amount}
              onChange={(e) => setForm({ ...form, budget_amount: e.target.value })}
              min="1000"
              step="1000"
              style={{ paddingLeft: '30px' }}
            />
          </div>
          {errors.budget_amount && <span className="error-text">{errors.budget_amount}</span>}
        </div>

        {/* Submit */}
        <button
          type="submit"
          className="btn btn-primary btn-lg"
          disabled={createMutation.isPending}
          style={{ width: '100%' }}
        >
          {createMutation.isPending ? (
            <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span className="skeleton" style={{ width: '18px', height: '18px', borderRadius: '50%' }} />
              Generating Campaign...
            </span>
          ) : (
            <>
              Generate Campaign
              <ChevronRight size={18} />
            </>
          )}
        </button>
      </form>
    </div>
  );
}
