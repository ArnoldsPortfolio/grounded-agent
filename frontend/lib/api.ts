export const API = "/api";
export function saveToken(token: string, email: string): void {
  localStorage.setItem("access", token);
  localStorage.setItem("email", email);
}
export function token(): string | null {
  return localStorage.getItem("access");
}
export async function api<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers);
  headers.set("Content-Type", "application/json");
  const access = token();
  if (access) headers.set("Authorization", `Bearer ${access}`);
  const res = await fetch(`${API}${path}`, { ...init, headers });
  const data = await res.json();
  if (!res.ok) throw new Error(data.message ?? data.detail ?? "request failed");
  return data as T;
}
