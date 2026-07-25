import { Navigate, Outlet } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import Navbar from '../layout/Navbar';

export function AppLayout() {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="bg-grid" style={{ minHeight: '100vh' }}>
      <Navbar />
      <main>
        <Outlet />
      </main>
    </div>
  );
}

export function AuthLayout() {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);

  if (isAuthenticated) {
    return <Navigate to="/app/dashboard" replace />;
  }

  return (
    <div className="bg-grid bg-glow" style={{ minHeight: '100vh' }}>
      <Navbar />
      <main>
        <Outlet />
      </main>
    </div>
  );
}

export function PublicLayout() {
  return (
    <div style={{ minHeight: '100vh' }}>
      <Navbar />
      <main>
        <Outlet />
      </main>
    </div>
  );
}
