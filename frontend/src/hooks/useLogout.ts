import { useQueryClient } from "@tanstack/react-query";
import { useLogoutUser } from "../api/generated";
import type { Error } from "../api/generated";

export type UseLogoutResult = {
  logout: () => void;
  isPending: boolean;
  isError: boolean;
  error: Error | null;
};

export const useLogout = (): UseLogoutResult => {
  const queryClient = useQueryClient();

  const mutation = useLogoutUser({
    mutation: {
      onSuccess: () => {
        // clear all queries after logout
        queryClient.clear();

        // reload page to reset auth state
        window.location.reload();
      },
    },
  });

  const logout = (): void => {
    mutation.mutate();
  };

  return {
    logout,
    isPending: mutation.isPending,
    isError: mutation.isError,
    error: mutation.error ?? null,
  };
};
