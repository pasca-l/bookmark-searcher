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
    <section className="rounded-lg border bg-card text-card-foreground shadow-sm">
      <div className="flex flex-col space-y-1.5 p-6">
        <h2 className="text-2xl font-semibold leading-none tracking-tight">Your Bookmarks</h2>
      </div>
      <div className="p-6 pt-0">
        <form onSubmit={handleAddBookmark} className="flex gap-2 mb-6">
          <input
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Enter URL to bookmark..."
            required
            disabled={createBookmarkResult.status === "loading"}
            className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-base ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium file:text-foreground placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 md:text-sm"
          />
          <button
            type="submit"
            disabled={createBookmarkResult.status === "loading" || !url.trim()}
            className="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-blue-600 text-white hover:bg-blue-700 h-10 px-4 py-2"
          >
            {createBookmarkResult.status === "loading"
              ? "Adding..."
              : "Add Bookmark"}
          </button>
        </form>

        {createBookmarkResult.status === "error" && (
          <div className="rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700 mb-4">
            Failed to add bookmark: {createBookmarkResult.error.message}
          </div>
        )}

        {bookmarksResult.status === "loading" && (
          <div className="flex items-center justify-center py-8">
            <p className="text-sm text-gray-600">Loading bookmarks...</p>
          </div>
        )}

        {bookmarksResult.status === "error" && (
          <div className="rounded-lg border border-red-200 bg-red-50 p-4">
            <p className="text-sm text-red-700 mb-3">Failed to load bookmarks: {bookmarksResult.error.message}</p>
            <button
              onClick={bookmarksResult.refetch}
              className="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-red-500 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-red-600 text-white hover:bg-red-700 h-9 px-3"
            >
              Retry
            </button>
          </div>
        )}

        {bookmarksResult.status === "success" &&
          bookmarksResult.bookmarks.length > 0 && (
            <div>
              <div className="mb-4">
                <h3 className="text-lg font-semibold">
                  All Bookmarks ({bookmarksResult.bookmarks.length})
                </h3>
              </div>
              <div className="space-y-3">
                {bookmarksResult.bookmarks.map((bookmark) => (
                  <div
                    key={bookmark.id}
                    className="rounded-lg border bg-card text-card-foreground shadow-sm p-4 hover:bg-gray-50 transition-colors"
                  >
                    <a
                      href={bookmark.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="font-medium text-blue-600 hover:underline"
                    >
                      {bookmark.title || "title not found"}
                    </a>
                    <p className="text-xs text-gray-500 mt-1.5">
                      Added: {bookmark.created_at
                        ? new Date(bookmark.created_at).toLocaleString()
                        : "Unknown"}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

        {bookmarksResult.status === "success" &&
          bookmarksResult.bookmarks.length === 0 && (
            <div className="rounded-lg border border-gray-200 bg-gray-50 p-4 text-center text-sm text-gray-600">
              <p>No bookmarks yet. Add your first bookmark above!</p>
            </div>
          )}
      </div>
    </section>
  );
};
