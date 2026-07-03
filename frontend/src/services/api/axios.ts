import axios, { AxiosError, AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import type { ApiResponse } from '@/types'

const baseURL = import.meta.env.VITE_API_BASE ?? '/api'

const api: AxiosInstance = axios.create({
  baseURL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// Request interceptor — useful for adding headers or logging
api.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    // Example: we could attach a request id or other headers here
    return config
  },
  (error: AxiosError) => {
    return Promise.reject(error)
  }
)

// Response interceptor — global error handling and 401 redirect
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error: AxiosError) => {
    if (error.response) {
      const status = error.response.status
      // Global 401 handler — redirect to login (backend manages the HttpOnly cookie)
      if (status === 401) {
        const redirect = window.location.pathname + window.location.search
        window.location.href = `/login?redirect=${encodeURIComponent(redirect)}`
        return Promise.reject(error)
      }

      // Try to surface server-provided error message
      const serverMessage = (error.response.data && (error.response.data as any).detail) || (error.response.data && (error.response.data as any).message)
      const message = serverMessage || error.message || 'An unexpected error occurred'
      return Promise.reject(new Error(message))
    }

    // Network or other errors
    return Promise.reject(error)
  }
)

export default api

// Helper typed wrappers (optional)
export async function get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
  const res = await api.get<ApiResponse<T>>(url, config)
  // If backend returns { data: ... } normalize, otherwise return raw
  return (res.data as unknown as any).data ?? (res.data as unknown as T)
}

export async function post<T = any>(url: string, payload?: any, config?: AxiosRequestConfig): Promise<T> {
  const res = await api.post<ApiResponse<T>>(url, payload, config)
  return (res.data as unknown as any).data ?? (res.data as unknown as T)
}
