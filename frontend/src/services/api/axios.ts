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

// Request interceptor
api.interceptors.request.use(
  (config: AxiosRequestConfig) => {
    return config
  },
  (error: AxiosError) => {
    return Promise.reject(error)
  }
)

// Response interceptor — do NOT navigate here. Instead, delegate to AuthStore handler when 401 occurs.
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error: AxiosError) => {
    if (error.response) {
      const status = error.response.status
      // If 401, let the AuthStore handle unauthenticated state (clear user and navigate via router)
      if (status === 401) {
        try {
          const mod = await import('@/app/stores/auth')
          const { useAuthStore } = mod
          const auth = useAuthStore()
          // Call store handler (it will perform router navigation)
          await auth.handleUnauthenticated()
        } catch (e) {
          // ignore errors from handler
        }
      }

      // Robust server message extraction:
      // FastAPI often returns { "detail": { "code": "...", "message": "..." } } for HTTPException.
      // Normalize to a string message for UI consumption.
      let serverMessage: string | undefined = undefined
      const data = (error.response.data ?? {}) as any

      if (typeof data === 'string') {
        serverMessage = data
      } else if (data.detail) {
        if (typeof data.detail === 'string') serverMessage = data.detail
        else if (typeof data.detail === 'object' && data.detail.message) serverMessage = data.detail.message
        else if (typeof data.detail === 'object' && data.detail.code) serverMessage = data.detail.code
      } else if (data.message && typeof data.message === 'string') {
        serverMessage = data.message
      }

      const message = serverMessage || error.message || 'An unexpected error occurred'
      return Promise.reject(new Error(message))
    }

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
