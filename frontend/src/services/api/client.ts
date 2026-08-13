const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL || 'http://localhost:8000';

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
