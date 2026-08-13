// Provide a minimal type for `process.env` so TypeScript doesn't require @types/node
declare const process: { env: { EXPO_PUBLIC_API_URL?: string } };

const API_BASE_URL = (typeof process !== 'undefined' ? process.env.EXPO_PUBLIC_API_URL : undefined) || 'http://localhost:8000';

export async function apiClient<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };

  const response = await fetch(url, { ...options, headers });
  
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Error en API (${response.status}): ${errorText}`);
  }

  return response.json() as Promise<T>;
}
