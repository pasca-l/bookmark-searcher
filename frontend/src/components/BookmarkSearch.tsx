import { useState } from "react";
import { useSearchBookmarks } from "../hooks/useSearchBookmarks";

export const BookmarkSearch = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const searchResult = useSearchBookmarks({ query: searchQuery });

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    searchResult.search();
  };

  return (
    <section className="rounded-lg border bg-card text-card-foreground shadow-sm">
      <div className="flex flex-col space-y-1.5 p-6">
        <h2 className="text-2xl font-semibold leading-none tracking-tight">
          Search Bookmarks
        </h2>
      </div>
      <div className="p-6 pt-0">
        <form onSubmit={handleSearch} className="flex gap-2 mb-6">
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search your bookmarks..."
            disabled={searchResult.status === "loading"}
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-base ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 md:text-sm"
          />
          <button
            type="submit"
            disabled={searchResult.status === "loading" || !searchQuery.trim()}
            className="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-blue-600 text-white hover:bg-blue-700 h-10 px-4 py-2"
          >
            {searchResult.status === "loading" ? "Searching..." : "Search"}
          </button>
        </form>

        {searchResult.status === "error" && (
          <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">
            Search failed: {searchResult.error.message}
          </div>
        )}

        {searchResult.status === "success" &&
          searchResult.results.length > 0 && (
            <div>
              <div className="mb-4">
                <h3 className="text-lg font-semibold mb-3">
                  Search Results ({searchResult.results.length})
                </h3>
              </div>
              <div className="space-y-4">
                {searchResult.results.map((result, idx) => (
                  <div
                    key={idx}
                    className="rounded-lg border bg-card text-card-foreground shadow-sm p-4 hover:bg-gray-50 transition-colors"
                  >
                    <a
                      href={result.bookmark.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="font-medium text-lg text-blue-600 hover:underline"
                    >
                      {result.bookmark.title || "title not found"}
                    </a>
                    <p className="text-sm text-gray-700 mt-2 leading-relaxed">
                      {result.chunk_content}
                    </p>
                    <span className="inline-block mt-2 px-2.5 py-0.5 text-xs font-medium rounded-full bg-blue-100 text-blue-800">
                      Similarity: {(result.similarity * 100).toFixed(1)}%
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}

        {searchResult.status === "success" &&
          searchResult.results.length === 0 && (
            <div className="rounded-lg border border-yellow-200 bg-yellow-50 p-4 text-sm text-yellow-800">
              <p>No results found for "{searchQuery}"</p>
            </div>
          )}

        {searchResult.status === "idle" && (
          <div className="rounded-lg border border-gray-200 bg-gray-50 p-4 text-center text-sm text-gray-600">
            <p>Enter a query and click search to find bookmarks</p>
          </div>
        )}
      </div>
    </section>
  );
};
