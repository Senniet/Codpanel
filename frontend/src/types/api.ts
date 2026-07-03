export interface ApiResponse<T = any> {
  data?: T
  success?: boolean
  message?: string
}
