import axios from 'axios'

const baseURL = import.meta.env.VITE_API_BASE ?? '/api'

const api = axios.create({
  baseURL,
  headers: {
    'Content-Type': 'application/json'
  }
})

export default api
