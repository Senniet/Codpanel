import axios, { AxiosError, AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios'
import type { ApiResponse } from '@/types/api'

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
    // Could add request ids, auth headers (not needed for HttpOnly cookie) etc.
    return config
  },
  (error: AxiosError) => {
    return Promise.reject(error)
  }
)

// Response interceptor — global error handling (do NOT perform navigation here)
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error: AxiosError) => {
    if (error.response) {
      const status = error.response.status
      // Emit an event for 401 so the AuthStore can handle redirects/cleanup
      if (status === 401) {
        try { window.dispatchEvent(new CustomEvent('unauthenticated')) } catch (e) {}
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

// Helper typed wrappers
export async function get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
  const res = await api.get<ApiResponse<T>>(url, config)
  return (res.data && (res.data as any).data) ?? (res.data as unknown as T)
}

export async function post<T = any>(url: string, payload?: any, config?: AxiosRequestConfig): Promise<T> {
  const res = await api.post<ApiResponse<T>>(url, payload, config)
  return (res.data && (res.data as any).data) ?? (res.data as unknown as T)
}
