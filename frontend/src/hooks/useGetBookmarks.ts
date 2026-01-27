import type { Bookmark, Error } from "../api/generated";
import { useGetBookmarks as useGetBookmarksGenerated } from "../api/generated";

export type UseGetBookmarksResult =
  | { status: "loading"; bookmarks: []; refetch: () => void }
  | { status: "success"; bookmarks: Bookmark[]; refetch: () => void }
  | { status: "error"; bookmarks: []; error: Error; refetch: () => void };

export const useGetBookmarks = (): UseGetBookmarksResult => {
  const {
    data: response,
    isLoading,
    isError,
    error,
    refetch,
  } = useGetBookmarksGenerated();

  const handleRefetch = () => {
    refetch();
  };

  if (isLoading) {
    return {
      status: "loading" as const,
      bookmarks: [],
      refetch: handleRefetch,
    };
  }

  if (isError) {
    return {
      status: "error" as const,
      bookmarks: [],
      error: error ?? { status_code: 500, message: "Unknown error occurred" },
      refetch: handleRefetch,
    };
  }

  const bookmarks = Array.isArray(response?.data) ? response.data : [];

  return {
    status: "success",
    bookmarks,
    refetch: handleRefetch,
  };
};
