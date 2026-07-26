import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://campaign-ai-backend-2i65.onrender.com/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// JWT interceptor — attach token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor — auto-logout on 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      // Only redirect if not already on auth pages
      if (!window.location.pathname.includes('/login') && !window.location.pathname.includes('/register')) {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// ===== Auth API =====
export const authApi = {
  register: (data: { email: string; password: string; full_name?: string }) =>
    api.post('/auth/register', data),
  login: (data: { email: string; password: string }) =>
    api.post('/auth/login', data),
  me: () => api.get('/auth/me'),
};

// ===== Campaign API =====
export const campaignApi = {
  create: (data: {
    product_description: string;
    marketing_goal: string;
    industry: string;
    budget_amount: number;
  }) => api.post('/campaigns', data),

  get: (id: string) => api.get(`/campaigns/${id}`),

  getStatus: (id: string) => api.get(`/campaigns/${id}/status`),

  delete: (id: string) => api.delete(`/campaigns/${id}`),

  regenerate: (id: string, section: string) =>
    api.post(`/campaigns/${id}/regenerate`, { section }),
};

// ===== Dashboard API =====
export const dashboardApi = {
  listCampaigns: (page: number = 1, limit: number = 10) =>
    api.get(`/dashboard/campaigns?page=${page}&limit=${limit}`),

  getStats: () => api.get('/dashboard/stats'),
};

export default api;
