import { Link } from 'react-router-dom';
import { Sparkles, Target, TrendingUp, Zap, BarChart3, Calendar, Users } from 'lucide-react';

export default function Landing() {
  return (
    <div>
      {/* Hero Section */}
      <section
        className="bg-glow"
        style={{
          position: 'relative',
          overflow: 'hidden',
          padding: '100px 0 80px',
        }}
      >
        {/* Floating orbs */}
        <div style={{ position: 'absolute', top: '15%', left: '10%', width: '300px', height: '300px', borderRadius: '50%', background: 'radial-gradient(circle, rgba(99, 102, 241, 0.08), transparent 70%)', filter: 'blur(40px)' }} className="animate-float" />
        <div style={{ position: 'absolute', bottom: '20%', right: '10%', width: '250px', height: '250px', borderRadius: '50%', background: 'radial-gradient(circle, rgba(6, 182, 212, 0.08), transparent 70%)', filter: 'blur(40px)' }} className="animate-float delay-300" />

        <div className="container" style={{ position: 'relative', zIndex: 1, textAlign: 'center' }}>
          {/* Badge */}
          <div className="animate-fade-in" style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', padding: '6px 16px', borderRadius: 'var(--radius-full)', background: 'var(--color-primary-muted)', border: '1px solid rgba(99, 102, 241, 0.2)', marginBottom: '24px' }}>
            <Sparkles size={14} style={{ color: 'var(--color-primary-light)' }} />
            <span style={{ fontSize: '0.8125rem', color: 'var(--color-primary-light)', fontWeight: 500 }}>AI-Powered Marketing Intelligence</span>
          </div>

          {/* Heading */}
          <h1 className="animate-fade-in delay-100" style={{ fontSize: 'clamp(2.5rem, 5vw, 4rem)', fontWeight: 800, lineHeight: 1.1, marginBottom: '20px', letterSpacing: '-0.03em', maxWidth: '800px', margin: '0 auto 20px' }}>
            Build Winning Campaigns{' '}
            <span style={{ background: 'var(--gradient-primary)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
              in Minutes
            </span>
          </h1>

          <p className="animate-fade-in delay-200" style={{ fontSize: '1.125rem', maxWidth: '600px', margin: '0 auto 40px', color: 'var(--color-text-secondary)', lineHeight: 1.7 }}>
            From audience personas to ad copy, keyword strategy to budget allocation — let AI craft your entire marketing campaign while you focus on what matters.
          </p>

          {/* CTAs */}
          <div className="animate-fade-in delay-300" style={{ display: 'flex', gap: '12px', justifyContent: 'center', flexWrap: 'wrap' }}>
            <Link to="/register" className="btn btn-primary btn-lg" style={{ textDecoration: 'none' }}>
              <Zap size={18} />
              Start Building Free
            </Link>
            <Link to="/login" className="btn btn-secondary btn-lg" style={{ textDecoration: 'none' }}>
              Log In
            </Link>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="bg-grid" style={{ padding: '80px 0' }}>
        <div className="container">
          <div style={{ textAlign: 'center', marginBottom: '60px' }}>
            <h2 className="animate-fade-in-up" style={{ marginBottom: '12px' }}>
              Everything You Need, Generated Instantly
            </h2>
            <p className="animate-fade-in-up delay-100" style={{ maxWidth: '500px', margin: '0 auto' }}>
              One form. Six AI-powered outputs. Complete campaign strategy in under a minute.
            </p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '20px' }}>
            {features.map((f, i) => (
              <div key={f.title} className="glass-card animate-fade-in-up" style={{ padding: '28px', animationDelay: `${(i + 1) * 100}ms`, opacity: 0, animationFillMode: 'forwards' }}>
                <div style={{ width: '42px', height: '42px', borderRadius: 'var(--radius-md)', background: f.bg, display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '16px' }}>
                  <f.icon size={20} style={{ color: f.color }} />
                </div>
                <h4 style={{ marginBottom: '8px' }}>{f.title}</h4>
                <p style={{ fontSize: '0.875rem' }}>{f.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section style={{ padding: '80px 0', textAlign: 'center' }}>
        <div className="container">
          <div className="solid-card" style={{ padding: '60px 40px', background: 'var(--gradient-primary)', border: 'none', position: 'relative', overflow: 'hidden' }}>
            <div style={{ position: 'absolute', top: '-50px', right: '-50px', width: '200px', height: '200px', borderRadius: '50%', background: 'rgba(255,255,255,0.1)', filter: 'blur(40px)' }} />
            <h2 style={{ color: 'white', marginBottom: '12px', position: 'relative' }}>Ready to Transform Your Marketing?</h2>
            <p style={{ color: 'rgba(255,255,255,0.8)', maxWidth: '500px', margin: '0 auto 32px', position: 'relative' }}>
              Join marketers who are saving hours on campaign planning with AI-powered strategy generation.
            </p>
            <Link to="/register" className="btn btn-lg" style={{ background: 'white', color: 'var(--color-primary)', fontWeight: 600, textDecoration: 'none', position: 'relative' }}>
              Get Started Free
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer style={{ padding: '24px 0', borderTop: '1px solid var(--color-border)' }}>
        <div className="container" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span style={{ fontSize: '0.8125rem', color: 'var(--color-text-muted)' }}>
            © 2025 CampaignAI. Built for hackathon demo.
          </span>
          <div style={{ display: 'flex', gap: '16px' }}>
            <span style={{ fontSize: '0.8125rem', color: 'var(--color-text-muted)' }}>Powered by Llama 3.1</span>
          </div>
        </div>
      </footer>
    </div>
  );
}

const features = [
  {
    title: 'Audience Personas',
    description: 'AI-generated customer profiles with demographics, pain points, and preferred channels — tailored to your product.',
    icon: Users,
    color: '#818cf8',
    bg: 'rgba(99, 102, 241, 0.1)',
  },
  {
    title: 'Multi-Platform Ad Copy',
    description: 'Platform-specific headlines, body copy, and CTAs for Google, Meta, LinkedIn, and Instagram — respecting character limits.',
    icon: Target,
    color: '#06b6d4',
    bg: 'rgba(6, 182, 212, 0.1)',
  },
  {
    title: 'SEO & PPC Keywords',
    description: 'Targeted keyword lists with intent classification (informational, transactional, navigational) and relevance scoring.',
    icon: TrendingUp,
    color: '#10b981',
    bg: 'rgba(16, 185, 129, 0.1)',
  },
  {
    title: 'Smart Budget Allocation',
    description: 'Rule-based channel allocation with AI-generated reasoning — numbers you can trust, strategy you can explain.',
    icon: BarChart3,
    color: '#f59e0b',
    bg: 'rgba(245, 158, 11, 0.1)',
  },
  {
    title: 'Publishing Schedule',
    description: '28-day campaign cadence with launch, optimize, and scale phases — specific actions for each channel, each day.',
    icon: Calendar,
    color: '#ec4899',
    bg: 'rgba(236, 72, 153, 0.1)',
  },
  {
    title: 'Lightning Fast',
    description: 'Full campaign strategy in under 60 seconds. From product description to actionable marketing plan — powered by Llama 3.1.',
    icon: Zap,
    color: '#8b5cf6',
    bg: 'rgba(139, 92, 246, 0.1)',
  },
];
