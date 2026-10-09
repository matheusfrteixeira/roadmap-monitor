import { defineStore } from 'pinia'
import api from '@/services/api'
import { useTimetrackerStore } from './timetracker'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('roadmap_user') || 'null'),
    token: localStorage.getItem('roadmap_token') || null,
    loading: false,
    error: null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
    isAdmin: (state) => state.user?.role === 'admin',
    isGestor: (state) => state.user?.role === 'gestor',
    isAnalista: (state) => state.user?.role === 'analista',
    roleLabel: (state) => {
      if (!state.user?.role) return 'Convidado'
      const labels = { admin: 'Administrador', gestor: 'Gestor', analista: 'Analista' }
      return labels[state.user.role] || state.user.role
    }
  },
  actions: {
    async login(email, password) {
      this.loading = true
      this.error = null
      try {
        const formData = new URLSearchParams()
        formData.append('username', email)
        formData.append('password', password)

        const res = await api.post('/auth/login', formData, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        })

        this.token = res.data.access_token
        localStorage.setItem('roadmap_token', this.token)

        // Busca dados do usuário logado (/me)
        await this.fetchMe()
        return true
      } catch (err) {
        this.error = err.response?.data?.detail || 'Erro ao realizar login. Verifique email e senha.'
        return false
      } finally {
        this.loading = false
      }
    },
    async fetchMe() {
      try {
        const res = await api.get('/users/me')
        this.user = res.data
        localStorage.setItem('roadmap_user', JSON.stringify(this.user))

        try {
          const timetrackerStore = useTimetrackerStore()
          timetrackerStore.initFromStorage(this.user.id)
          await timetrackerStore.fetchMyEntries()
        } catch (e) {
          // ignore
        }
      } catch (err) {
        this.logout()
      }
    },
    logout() {
      try {
        const timetrackerStore = useTimetrackerStore()
        timetrackerStore.clearSessionTimer()
      } catch (e) {
        // ignore
      }
      this.token = null
      this.user = null
      localStorage.removeItem('roadmap_token')
      localStorage.removeItem('roadmap_user')
    }
  }
})

