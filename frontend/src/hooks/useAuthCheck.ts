import { useQuery } from "@tanstack/react-query";
import { orvalMutator } from "../utils/orval-mutator";

export type UseAuthCheckResult =
  | { status: "loading"; isAuthenticated: false }
  | { status: "authenticated"; isAuthenticated: true }
  | { status: "unauthenticated"; isAuthenticated: false };

export const useAuthCheck = (): UseAuthCheckResult => {
  const { data, isLoading, isError } = useQuery({
    queryKey: ["auth-check"],
    queryFn: async () => {
      await orvalMutator("/private", { method: "GET" });
      return true;
    },
    retry: false,
    staleTime: 5 * 60 * 1000,
  });

  if (isLoading) {
    return { status: "loading", isAuthenticated: false };
  }

  if (isError || !data) {
    return { status: "unauthenticated", isAuthenticated: false };
  }

  return { status: "authenticated", isAuthenticated: true };
};
