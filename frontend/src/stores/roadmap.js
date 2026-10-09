import { defineStore } from 'pinia'
import api from '@/services/api'

export const useRoadmapStore = defineStore('roadmap', {
  state: () => ({
    projects: [],
    deliverables: [],
    activities: [],
    areas: [],
    users: [],
    loading: false,
    error: null,
    // Filtros Globais Multiseleção Integrado
    filters: {
      search: '',
      areas: [],
      status: [],
      owners: [],
      priority: [],
      delays: 'all',
      deadline: 'all',
      requesters: [],
      technicalResponsibles: [],
      managers: [],
      projectStart: '',
      projectEnd: '',
      activityStart: '',
      activityEnd: ''
    }
  }),
  getters: {
    filteredProjects: (state) => {
      const today = new Date()
      today.setHours(0, 0, 0, 0)

      // Indexa atividades por project_id para checagem rápida
      const activitiesByProject = new Map()
      state.activities.forEach(a => {
        if (!activitiesByProject.has(a.project_id)) {
          activitiesByProject.set(a.project_id, [])
        }
        activitiesByProject.get(a.project_id).push(a)
      })

      const filterProjStart = state.filters.projectStart ? new Date(state.filters.projectStart + 'T00:00:00') : null
      const filterProjEnd = state.filters.projectEnd ? new Date(state.filters.projectEnd + 'T00:00:00') : null
      const filterActStart = state.filters.activityStart ? new Date(state.filters.activityStart + 'T00:00:00') : null
      const filterActEnd = state.filters.activityEnd ? new Date(state.filters.activityEnd + 'T00:00:00') : null

      return state.projects.filter(p => {
        // 1. Busca textual
        if (state.filters.search) {
          const s = state.filters.search.toLowerCase()
          const matchName = (p.name || '').toLowerCase().includes(s)
          const matchReq = (p.requester || '').toLowerCase().includes(s)
          const matchTicket = (p.ticket_number || '').toLowerCase().includes(s)
          const matchArea = (p.area_name || '').toLowerCase().includes(s)
          const matchOwner = (p.owner_name || '').toLowerCase().includes(s)
          if (!matchName && !matchReq && !matchTicket && !matchArea && !matchOwner) return false
        }

        // 2. Área Requisitante
        if (state.filters.areas && state.filters.areas.length > 0) {
          if (!p.area_name || !state.filters.areas.includes(p.area_name)) return false
        }

        // 3. Situação do Projeto
        if (state.filters.status && state.filters.status.length > 0) {
          if (!p.status || !state.filters.status.includes(p.status)) return false
        }

        // 4. Owner do Projeto
        if (state.filters.owners && state.filters.owners.length > 0) {
          if (!p.owner_name || !state.filters.owners.includes(p.owner_name)) return false
        }

        // 5. Prioridade
        if (state.filters.priority && state.filters.priority.length > 0) {
          if (!p.priority || !state.filters.priority.includes(p.priority)) return false
        }

        // 6. Projetos Atrasados
        const effectiveDelay = state.filters.delays !== 'all' ? state.filters.delays : state.filters.deadline
        if (effectiveDelay && effectiveDelay !== 'all') {
          const isDelayed = p.status !== 'Concluído' && p.end_date && new Date(p.end_date + 'T00:00:00') < today
          if (effectiveDelay === 'overdue' && !isDelayed) return false
          if (effectiveDelay === 'ontime' && isDelayed) return false
          if (effectiveDelay === 'completed' && p.status !== 'Concluído') return false
        }

        // 7. Solicitante
        if (state.filters.requesters && state.filters.requesters.length > 0) {
          if (!p.requester || !state.filters.requesters.includes(p.requester)) return false
        }

        // 8. Responsável Técnico (cruza com os responsáveis das atividades do projeto)
        if (state.filters.technicalResponsibles && state.filters.technicalResponsibles.length > 0) {
          const pAtivs = activitiesByProject.get(p.id) || []
          const hasResponsible = pAtivs.some(a => a.assignee_name && state.filters.technicalResponsibles.includes(a.assignee_name))
          if (!hasResponsible) return false
        }

        // 9. Gestor Imediato
        if (state.filters.managers && state.filters.managers.length > 0) {
          if (!p.manager_name || !state.filters.managers.includes(p.manager_name)) return false
        }

        // 10. Período do Projeto (considera se o período do projeto cruza o intervalo)
        if (filterProjStart || filterProjEnd) {
          const pStart = p.start_date ? new Date(p.start_date + 'T00:00:00') : null
          const pEnd = (p.end_date ? new Date(p.end_date + 'T00:00:00') : null) || pStart
          if (filterProjStart && pEnd && pEnd < filterProjStart) return false
          if (filterProjEnd && pStart && pStart > filterProjEnd) return false
          if (!pStart && !pEnd) return false
        }

        // 11. Período da Atividade (mantém projetos com atividades dentro do intervalo selecionado)
        if (filterActStart || filterActEnd) {
          const pAtivs = activitiesByProject.get(p.id) || []
          const hasActInRange = pAtivs.some(a => {
            const aStart = a.start_date ? new Date(a.start_date + 'T00:00:00') : null
            const aEnd = (a.end_date ? new Date(a.end_date + 'T00:00:00') : null) || aStart
            if (filterActStart && aEnd && aEnd < filterActStart) return false
            if (filterActEnd && aStart && aStart > filterActEnd) return false
            if (!aStart && !aEnd) return false
            return true
          })
          if (!hasActInRange) return false
        }

        return true
      })
    },
    filteredActivities: (state) => {
      const allowedProjectIds = new Set(state.filteredProjects.map(p => p.id))
      let list = state.activities.filter(a => allowedProjectIds.has(a.project_id))

      if (state.filters.technicalResponsibles && state.filters.technicalResponsibles.length > 0) {
        list = list.filter(a => a.assignee_name && state.filters.technicalResponsibles.includes(a.assignee_name))
      }

      const filterActStart = state.filters.activityStart ? new Date(state.filters.activityStart + 'T00:00:00') : null
      const filterActEnd = state.filters.activityEnd ? new Date(state.filters.activityEnd + 'T00:00:00') : null
      if (filterActStart || filterActEnd) {
        list = list.filter(a => {
          const aStart = a.start_date ? new Date(a.start_date + 'T00:00:00') : null
          const aEnd = (a.end_date ? new Date(a.end_date + 'T00:00:00') : null) || aStart
          if (filterActStart && aEnd && aEnd < filterActStart) return false
          if (filterActEnd && aStart && aStart > filterActEnd) return false
          if (!aStart && !aEnd) return false
          return true
        })
      }

      return list
    },
    filteredDeliverables: (state) => {
      const allowedProjectIds = new Set(state.filteredProjects.map(p => p.id))
      let list = state.deliverables.filter(d => allowedProjectIds.has(d.project_id))

      if (
        (state.filters.technicalResponsibles && state.filters.technicalResponsibles.length > 0) ||
        state.filters.activityStart ||
        state.filters.activityEnd
      ) {
        const allowedDeliverableIds = new Set(
          state.filteredActivities
            .map(a => a.deliverable_id)
            .filter(id => id != null)
        )
        list = list.filter(d => allowedDeliverableIds.has(d.id))
      }
      return list
    },
    // KPIs Executivos
    kpis: (state) => {
      const projects = state.filteredProjects
      const totalProjects = projects.length
      const completedProjects = projects.filter(p => p.status === 'Concluído' || p.progress >= 100).length
      const concProjPct = totalProjects > 0 ? ((completedProjects / totalProjects) * 100).toFixed(1) : '0.0'

      const today = new Date()
      today.setHours(0, 0, 0, 0)
      const delayedProjects = projects.filter(p => {
        if (!p.end_date || p.status === 'Concluído') return false
        return new Date(p.end_date + 'T00:00:00') < today
      }).length

      const activities = state.filteredActivities
      const totalActivities = activities.length
      const completedActivities = activities.filter(a => a.status === 'Concluído' || a.progress >= 100).length
      const concAtivPct = totalActivities > 0 ? ((completedActivities / totalActivities) * 100).toFixed(1) : '0.0'
      const pendingActivities = Math.max(0, totalActivities - completedActivities)
      const totalDeliverables = state.filteredDeliverables.length

      const delayedActivities = activities.filter(a => {
        if (!a.end_date || a.status === 'Concluído' || a.progress >= 100) return false
        return new Date(a.end_date + 'T00:00:00') < today
      }).length

      const totalTrackedMinutes = activities.reduce((acc, a) => acc + (a.total_tracked_minutes || 0), 0)
      const totalTrackedHours = (totalTrackedMinutes / 60).toFixed(1)

      return {
        totalProjects,
        completedProjects,
        concProjPct,
        delayedProjects,
        totalDeliverables,
        totalActivities,
        completedActivities,
        concAtivPct,
        pendingActivities,
        delayedActivities,
        totalTrackedMinutes,
        totalTrackedHours
      }
    }
  },
  actions: {
    async fetchAll() {
      this.loading = true
      this.error = null
      try {
        const [projRes, delivRes, ativRes, areasRes, usersRes] = await Promise.all([
          api.get('/projects/'),
          api.get('/deliverables/'),
          api.get('/activities/'),
          api.get('/areas/'),
          api.get('/users/')
        ])
        this.projects = projRes.data
        this.deliverables = delivRes.data
        this.activities = ativRes.data
        this.areas = areasRes.data
        this.users = usersRes.data
      } catch (err) {
        this.error = 'Erro ao carregar dados do roadmap.'
        console.error(err)
      } finally {
        this.loading = false
      }
    },
    async createProject(projectData) {
      const res = await api.post('/projects/', projectData)
      this.projects.push(res.data)
      return res.data
    },
    async updateProject(id, projectData) {
      const res = await api.put(`/projects/${id}`, projectData)
      const idx = this.projects.findIndex(p => p.id === id)
      if (idx !== -1) this.projects[idx] = res.data
      return res.data
    },
    async createDeliverable(deliverableData) {
      const res = await api.post('/deliverables/', deliverableData)
      this.deliverables.push(res.data)
      await this.fetchAll()
      return res.data
    },
    async updateDeliverable(id, deliverableData) {
      const res = await api.put(`/deliverables/${id}`, deliverableData)
      const idx = this.deliverables.findIndex(d => d.id === id)
      if (idx !== -1) this.deliverables[idx] = res.data
      await this.fetchAll()
      return res.data
    },
    async deleteDeliverable(id) {
      await api.delete(`/deliverables/${id}`)
      this.deliverables = this.deliverables.filter(d => d.id !== id)
      await this.fetchAll()
    },
    async createActivity(activityData) {
      const res = await api.post('/activities/', activityData)
      this.activities.push(res.data)
      await this.fetchAll()
      return res.data
    },
    async updateActivity(id, activityData) {
      const res = await api.put(`/activities/${id}`, activityData)
      const idx = this.activities.findIndex(a => a.id === id)
      if (idx !== -1) this.activities[idx] = res.data
      await this.fetchAll()
      return res.data
    },
    async deleteActivity(id) {
      await api.delete(`/activities/${id}`)
      this.activities = this.activities.filter(a => a.id !== id)
      await this.fetchAll()
    },
    resetFilters() {
      this.filters = {
        search: '',
        areas: [],
        status: [],
        owners: [],
        priority: [],
        delays: 'all',
        deadline: 'all',
        requesters: [],
        technicalResponsibles: [],
        managers: [],
        projectStart: '',
        projectEnd: '',
        activityStart: '',
        activityEnd: ''
      }
    }
  }
})
