import { defineStore } from 'pinia'
import api from '@/services/api'
import { useRoadmapStore } from './roadmap'
import { useAuthStore } from './auth'

function getUserTimerKey(userId) {
  return userId ? `roadmap_active_timer_user_${userId}` : null
}

let syncChannel = null
function getSyncChannel() {
  if (typeof BroadcastChannel === 'undefined') return null
  if (!syncChannel) {
    try {
      syncChannel = new BroadcastChannel('roadmap_timetracker_channel')
    } catch (e) {
      console.warn('BroadcastChannel não disponível:', e)
    }
  }
  return syncChannel
}

function broadcast(msg) {
  try {
    const ch = getSyncChannel()
    if (ch) ch.postMessage(msg)
  } catch (e) {}
}

export const useTimetrackerStore = defineStore('timetracker', {
  state: () => ({
    // Cronômetro Ativo do Usuário Autenticado
    activeTimer: null,
    timerSeconds: 0,
    timerInterval: null,
    currentUserId: null,
    // Polling & Sincronização
    pollInterval: null,
    isSyncing: false,
    _listenersAttached: false,
    // Histórico de lançamentos
    myEntries: [],
    loading: false,
    error: null,
  }),
  getters: {
    isTimerRunning: (state) => !!state.activeTimer,
    formattedTimer: (state) => {
      const hrs = Math.floor(state.timerSeconds / 3600).toString().padStart(2, '0')
      const mins = Math.floor((state.timerSeconds % 3600) / 60).toString().padStart(2, '0')
      const secs = (state.timerSeconds % 60).toString().padStart(2, '0')
      return `${hrs}:${mins}:${secs}`
    },
    totalTrackedMinutes: (state) => {
      return state.myEntries.reduce((sum, entry) => sum + (entry.time_spent_minutes || 0), 0)
    },
    totalTrackedHours: (state) => {
      return (state.totalTrackedMinutes / 60).toFixed(1)
    }
  },
  actions: {
    startTickInterval() {
      if (this.timerInterval) clearInterval(this.timerInterval)
      this.timerInterval = setInterval(() => {
        if (this.activeTimer && this.activeTimer.startTime) {
          this.timerSeconds = Math.max(0, Math.floor((Date.now() - this.activeTimer.startTime) / 1000))
        } else {
          this.timerSeconds++
        }
      }, 1000)
    },
    stopTickInterval() {
      if (this.timerInterval) {
        clearInterval(this.timerInterval)
        this.timerInterval = null
      }
    },
    startBackgroundPoller() {
      if (this.pollInterval) return
      // Consulta periodicamente o backend a cada 3.5s para sincronizar entre diferentes navegadores,
      // abas anônimas ou outros dispositivos do mesmo usuário
      this.pollInterval = setInterval(() => {
        if (this.currentUserId && !this.isSyncing) {
          this.syncWithServer()
        }
      }, 3500)
    },
    stopBackgroundPoller() {
      if (this.pollInterval) {
        clearInterval(this.pollInterval)
        this.pollInterval = null
      }
    },
    async syncWithServer() {
      if (this.isSyncing) return
      try {
        const authStore = useAuthStore()
        if (!authStore.isAuthenticated || !authStore.user?.id) return
        await this.fetchActiveTimer(true)
      } catch (e) {}
    },
    setupSyncListeners() {
      if (this._listenersAttached) return
      this._listenersAttached = true

      // 1. BroadcastChannel: sincronização instantânea (0ms) entre abas do mesmo navegador
      const channel = getSyncChannel()
      if (channel) {
        channel.onmessage = (event) => {
          const msg = event?.data
          if (!msg || !this.currentUserId || msg.userId !== this.currentUserId) return

          if (msg.type === 'TIMER_STARTED' && msg.timer) {
            this.activeTimer = msg.timer
            this.timerSeconds = Math.max(0, Math.floor((Date.now() - msg.timer.startTime) / 1000))
            this.startTickInterval()
          } else if (msg.type === 'TIMER_STOPPED') {
            this.stopTickInterval()
            this.activeTimer = null
            this.timerSeconds = 0
            try {
              const roadmapStore = useRoadmapStore()
              roadmapStore.fetchAll()
              this.fetchMyEntries()
            } catch (e) {}
          }
        }
      }

      // 2. Storage event: fallback para abas normais
      window.addEventListener('storage', (e) => {
        if (!this.currentUserId) return
        const key = getUserTimerKey(this.currentUserId)
        if (e.key === key) {
          if (!e.newValue) {
            if (this.activeTimer) {
              this.stopTickInterval()
              this.activeTimer = null
              this.timerSeconds = 0
              try {
                const roadmapStore = useRoadmapStore()
                roadmapStore.fetchAll()
                this.fetchMyEntries()
              } catch (err) {}
            }
          } else {
            this.fetchActiveTimer(true)
          }
        }
      })

      // 3. Foco da janela / visibilidade: sincroniza na hora exata em que o usuário volta para a janela/aba
      window.addEventListener('focus', () => {
        if (this.currentUserId) this.syncWithServer()
      })
      document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible' && this.currentUserId) {
          this.syncWithServer()
        }
      })
    },
    async fetchActiveTimer(isBackgroundSync = false) {
      try {
        const res = await api.get('/timetracker/active')
        const data = res.data

        if (data && data.activity_id) {
          const serverElapsed = typeof data.elapsed_seconds === 'number' ? Math.max(0, data.elapsed_seconds) : 0
          
          let startIso = data.start_time
          if (typeof startIso === 'string' && !startIso.endsWith('Z') && !startIso.includes('+')) {
            startIso += 'Z'
          }
          const computedStartTime = Date.now() - (serverElapsed * 1000)

          this.currentUserId = data.user_id

          // Se já estamos rodando a mesma atividade:
          if (this.activeTimer && this.activeTimer.activityId === data.activity_id) {
            // Sincroniza se o relógio divergiu em mais de 2 segundos
            if (Math.abs(this.timerSeconds - serverElapsed) > 2) {
              this.timerSeconds = serverElapsed
              this.activeTimer.startTime = computedStartTime
            }
          } else {
            // Nova atividade ativa ou primeira carga
            this.activeTimer = {
              id: data.id,
              userId: data.user_id,
              activityId: data.activity_id,
              activityName: data.activity_name,
              projectId: data.project_id,
              projectName: data.project_name,
              startTime: computedStartTime,
              startIso: startIso
            }
            this.timerSeconds = serverElapsed
            this.startTickInterval()
          }

          const key = getUserTimerKey(data.user_id)
          if (key) {
            localStorage.setItem(key, JSON.stringify(this.activeTimer))
          }
          return data
        } else {
          // Servidor retornou null: nenhum timer rodando para este usuário
          const wasRunning = !!this.activeTimer
          if (wasRunning) {
            this.stopTickInterval()
            this.activeTimer = null
            this.timerSeconds = 0

            if (this.currentUserId) {
              const key = getUserTimerKey(this.currentUserId)
              if (key) localStorage.removeItem(key)
            }

            // Se estava rodando e parou remotamente, atualiza as telas abertas
            if (isBackgroundSync) {
              try {
                const roadmapStore = useRoadmapStore()
                await roadmapStore.fetchAll()
                await this.fetchMyEntries()
              } catch (e) {}
            }
          }
          return null
        }
      } catch (err) {
        if (err.response?.status !== 401) {
          console.error('Erro ao consultar cronômetro ativo no servidor:', err)
        }
        return null
      }
    },
    async startTimer(activity) {
      if (!activity) return

      let userId = this.currentUserId
      if (!userId) {
        try {
          const authStore = useAuthStore()
          userId = authStore.user?.id
        } catch (e) {}
      }

      if (!userId) {
        console.warn('Não é possível iniciar o cronômetro sem um usuário autenticado.')
        return
      }

      // Se este usuário já estiver cronometrando a MESMA atividade, mantém a execução contínua
      if (this.activeTimer && this.activeTimer.activityId === activity.id && this.activeTimer.userId === userId) {
        return
      }

      this.isSyncing = true
      try {
        // Envia ao backend: o servidor já finaliza e grava automaticamente qualquer timer anterior deste usuário!
        const res = await api.post('/timetracker/start', { activity_id: activity.id })
        const data = res.data

        const serverElapsed = typeof data.elapsed_seconds === 'number' ? Math.max(0, data.elapsed_seconds) : 0
        let startIso = data.start_time
        if (typeof startIso === 'string' && !startIso.endsWith('Z') && !startIso.includes('+')) {
          startIso += 'Z'
        }
        const computedStartTime = Date.now() - (serverElapsed * 1000)

        this.currentUserId = data.user_id
        this.activeTimer = {
          id: data.id,
          userId: data.user_id,
          activityId: data.activity_id,
          activityName: data.activity_name,
          projectId: data.project_id,
          projectName: data.project_name,
          startTime: computedStartTime,
          startIso: startIso
        }
        this.timerSeconds = serverElapsed
        this.startTickInterval()

        const key = getUserTimerKey(data.user_id)
        if (key) {
          localStorage.setItem(key, JSON.stringify(this.activeTimer))
        }

        broadcast({
          type: 'TIMER_STARTED',
          userId: data.user_id,
          timer: this.activeTimer
        })

        // Atualiza horas e KPIs nas outras telas
        try {
          const roadmapStore = useRoadmapStore()
          await roadmapStore.fetchAll()
        } catch (e) {}

        return data
      } catch (err) {
        console.error('Erro ao iniciar cronômetro no backend:', err)
        throw err
      } finally {
        this.isSyncing = false
      }
    },
    async stopTimer(description = '') {
      if (!this.activeTimer) return null

      this.isSyncing = true
      this.stopTickInterval()

      const userId = this.currentUserId || this.activeTimer?.userId

      try {
        const res = await api.post('/timetracker/stop', { description: description || '' })
        this.activeTimer = null
        this.timerSeconds = 0

        const key = getUserTimerKey(userId)
        if (key) {
          localStorage.removeItem(key)
        }

        if (res.data) {
          this.myEntries.unshift(res.data)
        }

        broadcast({
          type: 'TIMER_STOPPED',
          userId: userId
        })

        // Sincroniza dados e horas do roadmapStore
        try {
          const roadmapStore = useRoadmapStore()
          await roadmapStore.fetchAll()
        } catch (e) {}

        return res.data
      } catch (err) {
        console.error('Erro ao parar cronômetro no backend:', err)
        throw err
      } finally {
        this.isSyncing = false
      }
    },
    async logTime(activityId, minutes, description) {
      const payload = {
        activity_id: activityId,
        time_spent_minutes: parseInt(minutes),
        description: description || ''
      }
      const res = await api.post('/timetracker/', payload)
      this.myEntries.unshift(res.data)
      return res.data
    },
    async fetchMyEntries() {
      this.loading = true
      try {
        const res = await api.get('/timetracker/me')
        this.myEntries = res.data
      } catch (err) {
        console.error('Erro ao buscar extrato de horas:', err)
      } finally {
        this.loading = false
      }
    },
    initFromStorage(userId = null) {
      if (!userId) {
        try {
          const authStore = useAuthStore()
          userId = authStore.user?.id
        } catch (e) {}
      }

      if (!userId) {
        this.clearSessionTimer()
        return
      }

      this.currentUserId = userId
      this.setupSyncListeners()
      this.startBackgroundPoller()

      // Remove chave legada global se existir
      if (localStorage.getItem('roadmap_active_timer')) {
        localStorage.removeItem('roadmap_active_timer')
      }

      const key = getUserTimerKey(userId)
      const stored = key ? localStorage.getItem(key) : null

      if (stored) {
        try {
          const parsed = JSON.parse(stored)
          if (parsed && parsed.userId === userId && parsed.startTime) {
            const elapsed = Math.floor((Date.now() - parsed.startTime) / 1000)
            this.activeTimer = parsed
            this.timerSeconds = Math.max(0, elapsed)
            this.startTickInterval()
          }
        } catch (e) {
          console.error('Erro ao restaurar cache do timer do usuário:', e)
        }
      }

      // Consulta o backend para obter o estado oficial do banco de dados (sobrevive a fechar o navegador)
      this.fetchActiveTimer()
    },
    clearSessionTimer() {
      this.stopTickInterval()
      this.stopBackgroundPoller()
      this.activeTimer = null
      this.timerSeconds = 0
      this.currentUserId = null
      this.myEntries = []
    }
  }
})
