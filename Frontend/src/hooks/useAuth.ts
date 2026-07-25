import { useMutation } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { authApi } from '../lib/api';
import { useAuthStore } from '../store/authStore';

export function useLogin() {
  const login = useAuthStore((s) => s.login);
  const navigate = useNavigate();

  return useMutation({
    mutationFn: (data: { email: string; password: string }) =>
      authApi.login(data).then((res) => res.data),
    onSuccess: (data) => {
      login(data.user, data.token);
      navigate('/app/dashboard');
    },
  });
}

export function useRegister() {
  const login = useAuthStore((s) => s.login);
  const navigate = useNavigate();

  return useMutation({
    mutationFn: (data: { email: string; password: string; full_name?: string }) =>
      authApi.register(data).then((res) => res.data),
    onSuccess: (data) => {
      login(data.user, data.token);
      navigate('/app/dashboard');
    },
  });
}

export function useLogout() {
  const logout = useAuthStore((s) => s.logout);
  const navigate = useNavigate();

  return () => {
    logout();
    navigate('/login');
  };
}
