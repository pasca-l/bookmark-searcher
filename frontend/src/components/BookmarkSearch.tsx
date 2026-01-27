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
    <section>
      <h2>Search By Query</h2>

      <form onSubmit={handleSearch}>
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search your bookmarks..."
          disabled={searchResult.status === "loading"}
        />
        <button
          type="submit"
          disabled={searchResult.status === "loading" || !searchQuery.trim()}
        >
          {searchResult.status === "loading" ? "Searching..." : "Search"}
        </button>
      </form>

      {searchResult.status === "error" && (
        <div>Search failed: {searchResult.error.message}</div>
      )}

      {searchResult.status === "success" && searchResult.results.length > 0 && (
        <div>
          <h3>Search Results</h3>
          <div>
            {searchResult.results.map((result, idx) => (
              <div key={idx}>
                <a
                  href={result.bookmark.url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {result.bookmark.title || "title not found"}
                </a>
                <p>{result.chunk_content}</p>
                <span>Similarity: {(result.similarity * 100).toFixed(1)}%</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {searchResult.status === "success" &&
        searchResult.results.length === 0 && (
          <div>
            <p>No results found for "{searchQuery}"</p>
          </div>
        )}

      {searchResult.status === "idle" && (
        <div>
          <p>Enter a query and click search to find bookmarks</p>
        </div>
      )}
    </section>
  );
};
