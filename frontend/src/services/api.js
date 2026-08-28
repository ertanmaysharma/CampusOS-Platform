import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  response => response,
  async error => {
    // No response = network error (server down, CORS blocked, etc.)
    if (!error.response) {
      console.error('Network error:', error.message || 'Could not connect to server')
      return Promise.reject(error)
    }

    if (error.response?.status === 401) {
      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          const res = await axios.post('/api/auth/refresh', {}, {
            headers: { Authorization: `Bearer ${refreshToken}` }
          })
          const newToken = res.data.data.access_token
          localStorage.setItem('access_token', newToken)
          error.config.headers.Authorization = `Bearer ${newToken}`
          return api(error.config)
        } catch {
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          window.location.href = '/login'
        }
      } else {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export default api
