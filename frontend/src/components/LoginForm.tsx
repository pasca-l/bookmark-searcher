import { useState } from "react";
import { useLogin } from "../hooks/useLogin";
import { useRegister } from "../hooks/useRegister";

export const LoginForm = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const {
    login,
    isPending: isLoginPending,
    isError: isLoginError,
    error: loginError,
  } = useLogin();

  const {
    register,
    isPending: isRegisterPending,
    isError: isRegisterError,
    error: registerError,
  } = useRegister();

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    login(username, password);
  };

  const handleRegister = (e: React.FormEvent) => {
    e.preventDefault();
    register(username, password);
  };

  const isPending = isLoginPending || isRegisterPending;

  return (
    <div className="flex flex-col gap-4 max-w-md mx-auto w-full">
      <form className="flex flex-col gap-4 bg-white p-8 rounded-lg shadow-md">
        <div className="flex flex-col gap-2">
          <label
            htmlFor="username"
            className="text-sm font-medium text-gray-700"
          >
            Username
          </label>
          <input
            id="username"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            minLength={3}
            className="rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            disabled={isPending}
            placeholder="Enter your username"
          />
        </div>
        <div className="flex flex-col gap-2">
          <label
            htmlFor="password"
            className="text-sm font-medium text-gray-700"
          >
            Password
          </label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={8}
            className="rounded-md border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            disabled={isPending}
            placeholder="Enter your password"
          />
          <p className="text-xs text-gray-500">Minimum 8 characters</p>
        </div>

        <div className="flex gap-3 mt-2">
          <button
            type="submit"
            onClick={handleLogin}
            disabled={isPending}
            className="flex-1 inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-blue-600 text-white hover:bg-blue-700 h-10 px-4"
          >
            {isLoginPending ? "Signing in..." : "Sign In"}
          </button>
          <button
            type="button"
            onClick={handleRegister}
            disabled={isPending}
            className="flex-1 inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-green-500 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-green-600 text-white hover:bg-green-700 h-10 px-4"
          >
            {isRegisterPending ? "Creating..." : "Create Account"}
          </button>
        </div>
      </form>

      {isLoginError && loginError && (
        <div className="bg-red-50 border border-red-200 rounded-md p-3">
          <p className="text-sm text-red-600">
            Login failed: {loginError.message}
          </p>
        </div>
      )}
      {isRegisterError && registerError && (
        <div className="bg-red-50 border border-red-200 rounded-md p-3">
          <p className="text-sm text-red-600">
            Registration failed: {registerError.message}
          </p>
        </div>
      )}
    </div>
  );
};
