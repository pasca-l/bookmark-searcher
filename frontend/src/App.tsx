import { Authentication } from "./components/Authentication";
import { BookmarkList } from "./components/BookmarkList";
import { BookmarkSearch } from "./components/BookmarkSearch";
import { useAuthCheck } from "./hooks/useAuthCheck";

function App() {
  const { isAuthenticated } = useAuthCheck();

  return (
    <div>
      <header>
        <h1>Bookmark Searcher</h1>
        <Authentication isAuthenticated={isAuthenticated} />
      </header>

      {isAuthenticated && (
        <main>
          <BookmarkList />
          <BookmarkSearch />
        </main>
      )}
    </div>
  );
}

export default App;
