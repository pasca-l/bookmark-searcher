import { useQueryClient, useMutation } from "@tanstack/react-query";
import { orvalMutator } from "../utils/orval-mutator";
import type { Error } from "../api/generated";

export type UseLogoutResult = {
  logout: () => Promise<void>;
  isPending: boolean;
  isError: boolean;
  error: Error | null;
};

export const useLogout = (): UseLogoutResult => {
  const queryClient = useQueryClient();

  const logoutMutation = useMutation<unknown, Error, void>({
    mutationFn: async () => {
      return orvalMutator("/auth/logout", {
        method: "POST",
      });
    },
    onSuccess: () => {
      // clear all queries after logout
      queryClient.clear();

      // reload page to reset auth state
      window.location.reload();
    },
  });

  const logout = async (): Promise<void> => {
    await logoutMutation.mutateAsync();
  };

  return {
    logout,
    isPending: logoutMutation.isPending,
    isError: logoutMutation.isError,
    error: logoutMutation.error ?? null,
  };
};
