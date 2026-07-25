import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { campaignApi, dashboardApi } from '../lib/api';

// ===== Campaign Queries =====

export function useCampaign(id: string) {
  return useQuery({
    queryKey: ['campaign', id],
    queryFn: () => campaignApi.get(id).then((res) => res.data),
    enabled: !!id,
    refetchInterval: (query) => {
      const data = query.state.data;
      if (data?.status === 'complete' || data?.status === 'failed') {
        return false;
      }
      return 2000;
    },
  });
}

export function useCampaignStatus(id: string, enabled: boolean = true) {
  return useQuery({
    queryKey: ['campaign-status', id],
    queryFn: () => campaignApi.getStatus(id).then((res) => res.data),
    enabled: !!id && enabled,
    refetchInterval: (query) => {
      const data = query.state.data;
      // Poll every 2s while generating, stop when complete or failed
      if (data?.status === 'complete' || data?.status === 'failed') {
        return false;
      }
      return 2000;
    },
  });
}

export function useCampaignList(page: number = 1, limit: number = 10) {
  return useQuery({
    queryKey: ['campaigns', page, limit],
    queryFn: () => dashboardApi.listCampaigns(page, limit).then((res) => res.data),
  });
}

export function useDashboardStats() {
  return useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: () => dashboardApi.getStats().then((res) => res.data),
  });
}

// ===== Campaign Mutations =====

export function useCreateCampaign() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: {
      product_description: string;
      marketing_goal: string;
      industry: string;
      budget_amount: number;
    }) => campaignApi.create(data).then((res) => res.data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['campaigns'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard-stats'] });
    },
  });
}

export function useDeleteCampaign() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => campaignApi.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['campaigns'] });
      queryClient.invalidateQueries({ queryKey: ['dashboard-stats'] });
    },
  });
}

export function useRegenerateSection() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, section }: { id: string; section: string }) =>
      campaignApi.regenerate(id, section).then((res) => res.data),
    onSuccess: (_data, variables) => {
      queryClient.invalidateQueries({ queryKey: ['campaign', variables.id] });
      queryClient.invalidateQueries({ queryKey: ['campaign-status', variables.id] });
    },
  });
}
