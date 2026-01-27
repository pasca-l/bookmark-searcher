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
      <div>
        {isLoginPending && <p>Logging in...</p>}
        {isLoginError && loginError && (
          <p>Login failed: {loginError.message}</p>
        )}
        {!isLoginPending && <div ref={buttonRef}></div>}
      </div>
    );
  }

  return (
    <>
      <div>TODO: show user info</div>
      <div>
        <button onClick={logout} disabled={isLogoutPending}>
          {isLogoutPending ? "Logging out..." : "Logout"}
        </button>
        {isLogoutError && logoutError && (
          <p>Logout failed: {logoutError.message}</p>
        )}
      </div>
    </>
  );
};
