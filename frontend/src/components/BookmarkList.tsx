import { useState } from "react";
import { useGetBookmarks } from "../hooks/useGetBookmarks";
import { useCreateBookmark } from "../hooks/useCreateBookmark";

export const BookmarkList = () => {
  const [url, setUrl] = useState("");
  const bookmarksResult = useGetBookmarks();
  const createBookmarkResult = useCreateBookmark();

  const handleAddBookmark = (e: React.FormEvent) => {
    e.preventDefault();
    if (!url.trim()) return;
    createBookmarkResult.createBookmark(url);
    setUrl("");
  };

  return (
    <section>
      <h2>Your Bookmarks</h2>

      <form onSubmit={handleAddBookmark}>
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="Enter URL to bookmark..."
          required
          disabled={createBookmarkResult.status === "loading"}
        />
        <button
          type="submit"
          disabled={createBookmarkResult.status === "loading" || !url.trim()}
        >
          {createBookmarkResult.status === "loading"
            ? "Adding..."
            : "Add Bookmark"}
        </button>
      </form>

      {createBookmarkResult.status === "error" && (
        <div>Failed to add bookmark: {createBookmarkResult.error.message}</div>
      )}

      {bookmarksResult.status === "loading" && (
        <div>
          <p>Loading bookmarks...</p>
        </div>
      )}

      {bookmarksResult.status === "error" && (
        <div>
          Failed to load bookmarks: {bookmarksResult.error.message}
          <button onClick={bookmarksResult.refetch}>Retry</button>
        </div>
      )}

      {bookmarksResult.status === "success" &&
        bookmarksResult.bookmarks.length > 0 && (
          <div>
            {bookmarksResult.bookmarks.map((bookmark) => (
              <div key={bookmark.id}>
                <a
                  href={bookmark.url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  {bookmark.title || "title not found"}
                </a>
                <span>
                  {bookmark.created_at
                    ? new Date(bookmark.created_at).toLocaleString()
                    : "Unknown"}
                </span>
              </div>
            ))}
          </div>
        )}

      {bookmarksResult.status === "success" &&
        bookmarksResult.bookmarks.length === 0 && (
          <div>
            <p>No bookmarks yet. Add your first bookmark above!</p>
          </div>
        )}
    </section>
  );
};
