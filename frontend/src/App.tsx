import { Authentication } from "./components/Authentication";
import { BookmarkList } from "./components/BookmarkList";
import { BookmarkSearch } from "./components/BookmarkSearch";
import { useAuthCheck } from "./hooks/useAuthCheck";

function App() {
  const { isAuthenticated } = useAuthCheck();

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-3xl font-bold text-gray-900">
              Bookmark Searcher
            </h1>
            <Authentication isAuthenticated={isAuthenticated} />
          </div>
        </div>
      </header>

      {isAuthenticated && (
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="space-y-8">
            <BookmarkSearch />
            <BookmarkList />
          </div>
        </main>
      )}
    </div>
  );
}

export default App;
