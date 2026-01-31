import { useLogin } from "../hooks/useLogin";
import { useLogout } from "../hooks/useLogout";
import { useGoogleLogin } from "../hooks/useGoogleLogin";

const GOOGLE_CLIENT_ID = import.meta.env.VITE_GOOGLE_CLIENT_ID;

export const Authentication = ({
  isAuthenticated,
}: {
  isAuthenticated: boolean;
}) => {
  const {
    login,
    isPending: isLoginPending,
    isError: isLoginError,
    error: loginError,
  } = useLogin();
  const {
    logout,
    isPending: isLogoutPending,
    isError: isLogoutError,
    error: logoutError,
  } = useLogout();

  const { buttonRef } = useGoogleLogin(GOOGLE_CLIENT_ID, login, {
    theme: "outline",
    size: "large",
    text: "signin_with",
    shape: "rectangular",
  });

  if (!isAuthenticated) {
    return (
      <div className="flex items-center gap-4">
        {isLoginPending && (
          <p className="text-sm text-gray-600">Logging in...</p>
        )}
        {isLoginError && loginError && (
          <p className="text-sm text-red-600">Login failed: {loginError.message}</p>
        )}
        {!isLoginPending && <div ref={buttonRef}></div>}
      </div>
    );
  }

  return (
    <div className="flex items-center gap-4">
      <button
        onClick={logout}
        disabled={isLogoutPending}
        className="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-red-500 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-red-600 text-white hover:bg-red-700 h-9 px-3"
      >
        {isLogoutPending ? "Logging out..." : "Logout"}
      </button>
      {isLogoutError && logoutError && (
        <p className="text-sm text-red-600">Logout failed: {logoutError.message}</p>
      )}
    </div>
  );
};
