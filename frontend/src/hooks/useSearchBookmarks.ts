import type { SearchBookmarks200Item, Error } from "../api/generated";
import { useSearchBookmarks as useSearchBookmarksGenerated } from "./../api/generated";

type Args = {
  query: string;
};

export type UseSearchBookmarksResult =
  | { status: "idle"; results: []; search: () => void }
  | { status: "loading"; results: []; search: () => void }
  | {
      status: "success";
      results: SearchBookmarks200Item[];
      search: () => void;
    }
  | { status: "error"; results: []; error: Error; search: () => void };

export const useSearchBookmarks = ({
  query,
}: Args): UseSearchBookmarksResult => {
  const {
    data: response,
    isLoading,
    isError,
    error,
    refetch,
    isFetched, // whether the query has ever been fetched
  } = useSearchBookmarksGenerated(
    {
      query,
    },
    { query: { enabled: false } }
  );

  const handleSearch = () => {
    refetch();
  };

  if (isLoading) {
    return {
      status: "loading",
      results: [],
      search: handleSearch,
    } as const;
  }

  if (isError) {
    return {
      status: "error",
      results: [],
      error: error ?? { status_code: 500, message: "Unknown error occurred" },
      search: handleSearch,
    } as const;
  }

  if (!isFetched) {
    return {
      status: "idle",
      results: [],
      search: handleSearch,
    } as const;
  }

  const results = Array.isArray(response?.data) ? response.data : [];

  return {
    status: "success",
    results,
    search: handleSearch,
  };
};
