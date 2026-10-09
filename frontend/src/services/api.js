import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 15000,
})

// Adiciona o token JWT automaticamente se estiver logado
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('roadmap_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, (error) => {
  return Promise.reject(error)
})

// Tratamento de erro 401 (desloga se expirado)
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('roadmap_token')
      localStorage.removeItem('roadmap_user')
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

export default api

