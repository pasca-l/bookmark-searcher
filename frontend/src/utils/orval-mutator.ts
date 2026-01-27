type OrvalMutatorConfig = RequestInit & {
  data?: unknown;
  params?: Record<string, string | number | boolean>;
};

const API_BASE_URL = "http://localhost:8000";

export const orvalMutator = async <T>(
  url: string,
  config?: OrvalMutatorConfig,
): Promise<T> => {
  const {
    method = "GET",
    headers,
    data,
    params,
    body,
    ...restConfig
  } = config || {};

  // build query string from params
  const queryString = params
    ? "?" +
      new URLSearchParams(
        Object.entries(params).map(([key, value]) => [key, String(value)]),
      ).toString()
    : "";

  const response = await fetch(`${API_BASE_URL}${url}${queryString}`, {
    ...restConfig,
    method,
    credentials: "include", // send cookies with every request
    headers: {
      "Content-Type": "application/json",
      ...(headers as Record<string, string>),
    },
    // use body if provided (from generated code), otherwise use data
    body: body || (data ? JSON.stringify(data) : undefined),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({
      message: response.statusText,
    }));
    throw new Error(error.message || `HTTP ${response.status}`);
  }

  // handle empty responses (204 No Content, etc.)
  const contentType = response.headers.get("content-type");
  if (!contentType?.includes("application/json")) {
    return undefined as T;
  }

  const responseData = await response.json();

  return {
    data: responseData,
    status: response.status,
    headers: response.headers,
  } as T;
};
