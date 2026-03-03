import { useLogout } from "../hooks/useLogout";

export const LogoutButton = () => {
  const {
    logout,
    isPending: isLogoutPending,
    isError: isLogoutError,
    error: logoutError,
  } = useLogout();

  return (
    <div className="flex items-center gap-4">
      <button
        onClick={logout}
        disabled={isLogoutPending}
        className="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-red-500 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-red-600 text-white hover:bg-red-700 h-9 px-4"
      >
        {isLogoutPending ? "Logging out..." : "Logout"}
      </button>
      {isLogoutError && logoutError && (
        <p className="text-sm text-red-600">Logout failed: {logoutError.message}</p>
      )}
    </div>
  );
};
