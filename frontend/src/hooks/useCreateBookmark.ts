import type { Bookmark, Error } from "../api/generated";
import { useCreateBookmark as useCreateBookmarkGenerated } from "./../api/generated";
import { useQueryClient } from "@tanstack/react-query";

export type UseCreateBookmarkResult =
  | { status: "idle"; createBookmark: (url: string) => void }
  | { status: "loading"; createBookmark: (url: string) => void }
  | {
      status: "success";
      bookmark: Bookmark;
      createBookmark: (url: string) => void;
    }
  | { status: "error"; error: Error; createBookmark: (url: string) => void };

export const useCreateBookmark = (): UseCreateBookmarkResult => {
  const queryClient = useQueryClient();

  const {
    mutate,
    data: response,
    isPending,
    isError,
    error,
    isSuccess,
  } = useCreateBookmarkGenerated({
    mutation: {
      onSuccess: () => {
        // invalidate and refetch bookmarks list after successful creation
        queryClient.invalidateQueries({ queryKey: ["/bookmarks"] });
      },
    },
  });

  const handleCreateBookmark = (url: string) => {
    mutate({ data: { url } });
  };

  if (isPending) {
    return {
      status: "loading",
      createBookmark: handleCreateBookmark,
    };
  }

  if (isError) {
    return {
      status: "error",
      error: error ?? { status_code: 500, message: "Unknown error occurred" },
      createBookmark: handleCreateBookmark,
    };
  }

  if (isSuccess && response?.status === 201) {
    return {
      status: "success",
      bookmark: response.data,
      createBookmark: handleCreateBookmark,
    };
  }

  return {
    status: "idle",
    createBookmark: handleCreateBookmark,
  };
};
