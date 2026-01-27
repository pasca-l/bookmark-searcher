import { useQueryClient, useMutation } from "@tanstack/react-query";
import { orvalMutator } from "../utils/orval-mutator";
import type { Error } from "../api/generated";

export type UseLoginResult = {
  login: (token: string) => Promise<void>;
  isPending: boolean;
  isError: boolean;
  error: Error | null;
};

export const useLogin = (): UseLoginResult => {
  const queryClient = useQueryClient();

  const loginMutation = useMutation<unknown, Error, string>({
    mutationFn: async (token: string) => {
      return orvalMutator("/auth/login", {
        method: "POST",
        data: { token },
      });
    },
    onSuccess: () => {
      // invalidate auth check to refetch
      queryClient.invalidateQueries({ queryKey: ["auth-check"] });
      queryClient.invalidateQueries({ queryKey: ["/bookmarks"] });
    },
  });

  const login = async (token: string): Promise<void> => {
    await loginMutation.mutateAsync(token);
  };

  return {
    login,
    isPending: loginMutation.isPending,
    isError: loginMutation.isError,
    error: loginMutation.error ?? null,
  };
};
