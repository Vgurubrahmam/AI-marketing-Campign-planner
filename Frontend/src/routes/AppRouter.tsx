import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { PublicLayout, AuthLayout, AppLayout } from '../components/layout/Layouts';
import Landing from '../pages/Landing';
import Login from '../pages/Login';
import Register from '../pages/Register';
import Dashboard from '../pages/Dashboard';
import CampaignGenerate from '../pages/CampaignGenerate';
import CampaignDetail from '../pages/CampaignDetail';

export default function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public routes */}
        <Route element={<PublicLayout />}>
          <Route path="/" element={<Landing />} />
        </Route>

        {/* Auth routes (redirect to dashboard if already logged in) */}
        <Route element={<AuthLayout />}>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
        </Route>

        {/* Protected app routes */}
        <Route path="/app" element={<AppLayout />}>
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="generate" element={<CampaignGenerate />} />
          <Route path="campaign/:id" element={<CampaignDetail />} />
        </Route>

        {/* Fallback */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
