import { Link, useNavigate } from 'react-router-dom';
import { Sparkles, LogOut, LayoutDashboard, Plus } from 'lucide-react';
import { useAuthStore } from '../../store/authStore';

export default function Navbar() {
  const { user, isAuthenticated, logout } = useAuthStore();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <nav
      style={{
        position: 'sticky',
        top: 0,
        zIndex: 50,
        background: 'rgba(15, 15, 26, 0.85)',
        backdropFilter: 'blur(20px)',
        borderBottom: '1px solid var(--color-border)',
      }}
    >
      <div className="container" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', height: '64px' }}>
        {/* Logo */}
        <Link to={isAuthenticated ? '/app/dashboard' : '/'} style={{ display: 'flex', alignItems: 'center', gap: '10px', textDecoration: 'none' }}>
          <div style={{
            width: '36px',
            height: '36px',
            borderRadius: 'var(--radius-md)',
            background: 'var(--gradient-primary)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: 'var(--shadow-glow)',
          }}>
            <Sparkles size={20} color="white" />
          </div>
          <span style={{ fontSize: '1.125rem', fontWeight: 700, color: 'var(--color-text-primary)', letterSpacing: '-0.02em' }}>
            CampaignAI
          </span>
        </Link>

        {/* Actions */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          {isAuthenticated ? (
            <>
              <Link to="/app/dashboard" className="btn btn-ghost btn-sm" style={{ textDecoration: 'none' }}>
                <LayoutDashboard size={16} />
                Dashboard
              </Link>
              <Link to="/app/generate" className="btn btn-primary btn-sm" style={{ textDecoration: 'none' }}>
                <Plus size={16} />
                New Campaign
              </Link>
              <div style={{ width: '1px', height: '24px', background: 'var(--color-border)', margin: '0 4px' }} />
              <span style={{ fontSize: '0.8125rem', color: 'var(--color-text-muted)' }}>
                {user?.full_name || user?.email}
              </span>
              <button onClick={handleLogout} className="btn btn-ghost btn-sm" title="Logout">
                <LogOut size={16} />
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn btn-ghost btn-sm" style={{ textDecoration: 'none' }}>
                Log in
              </Link>
              <Link to="/register" className="btn btn-primary btn-sm" style={{ textDecoration: 'none' }}>
                Get Started
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}
