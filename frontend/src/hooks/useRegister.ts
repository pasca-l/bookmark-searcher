import { useQueryClient } from "@tanstack/react-query";
import { useRegisterUser } from "../api/generated";
import type { Error } from "../api/generated";

export type UseRegisterResult = {
  register: (username: string, password: string) => void;
  isPending: boolean;
  isError: boolean;
  error: Error | null;
};

export const useRegister = (): UseRegisterResult => {
  const queryClient = useQueryClient();

  const mutation = useRegisterUser({
    mutation: {
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: ["auth-check"] });
      },
    },
  });

  const register = (username: string, password: string): void => {
    mutation.mutate({ data: { username, password } });
  };

  return {
    register,
    isPending: mutation.isPending,
    isError: mutation.isError,
    error: mutation.error ?? null,
  };
};
