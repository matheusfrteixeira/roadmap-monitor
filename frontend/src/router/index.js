import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import LoginView from '@/views/LoginView.vue'
import ExecutiveSummaryView from '@/views/ExecutiveSummaryView.vue'
import AreasView from '@/views/AreasView.vue'
import StakeholdersView from '@/views/StakeholdersView.vue'
import EvolutionView from '@/views/EvolutionView.vue'
import AnalyticalBaseView from '@/views/AnalyticalBaseView.vue'

import PortfolioView from '@/views/PortfolioView.vue'
import ProjectDetailView from '@/views/ProjectDetailView.vue'
import TimetrackerView from '@/views/TimetrackerView.vue'
import TimetrackerCalendarView from '@/views/TimetrackerCalendarView.vue'

import SettingsView from '@/views/SettingsView.vue'
import DocumentationView from '@/views/DocumentationView.vue'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: { public: true }
  },
  {
    path: '/',
    redirect: '/dashboard/resumo'
  },
  // 1 - DASHBOARD
  {
    path: '/dashboard/resumo',
    alias: ['/resumo', '/dashboard'],
    name: 'dashboard-resumo',
    component: ExecutiveSummaryView,
    meta: { module: 'dashboard' }
  },
  {
    path: '/dashboard/areas',
    alias: '/areas',
    name: 'dashboard-areas',
    component: AreasView,
    meta: { module: 'dashboard' }
  },
  {
    path: '/dashboard/stakeholders',
    alias: '/stakeholders',
    name: 'dashboard-stakeholders',
    component: StakeholdersView,
    meta: { module: 'dashboard' }
  },
  {
    path: '/dashboard/evolucao',
    name: 'dashboard-evolucao',
    component: EvolutionView,
    meta: { module: 'dashboard' }
  },
  {
    path: '/dashboard/base',
    name: 'dashboard-base',
    component: AnalyticalBaseView,
    meta: { module: 'dashboard' }
  },

  // 2 - PORTFÓLIO DE PROJETOS
  {
    path: '/portfolio/roadmaps',
    alias: ['/portfolio', '/roadmaps'],
    name: 'portfolio-roadmaps',
    component: PortfolioView,
    meta: { module: 'portfolio' }
  },
  {
    path: '/portfolio/projeto/:id',
    alias: '/projeto/:id',
    name: 'portfolio-projeto-detail',
    component: ProjectDetailView,
    props: true,
    meta: { module: 'portfolio' }
  },
  {
    path: '/portfolio/timetracker',
    alias: '/timetracker',
    name: 'portfolio-timetracker',
    component: TimetrackerView,
    meta: { module: 'portfolio' }
  },
  {
    path: '/portfolio/acompanhamento',
    alias: ['/timetracker/calendario', '/acompanhamento', '/acompanhamento-diario'],
    name: 'portfolio-acompanhamento',
    component: TimetrackerCalendarView,
    meta: { module: 'portfolio' }
  },

  // 3 - ADMINISTRAÇÃO
  {
    path: '/administracao/configuracoes',
    alias: ['/configuracoes', '/administracao'],
    name: 'admin-configuracoes',
    component: SettingsView,
    meta: { module: 'admin', adminOnly: true }
  },

  // 4 - DOCUMENTAÇÃO
  {
    path: '/documentacao',
    alias: '/docs',
    name: 'documentacao',
    component: DocumentationView,
    meta: { module: 'docs' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation Guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (!to.meta.public && !authStore.isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && authStore.isAuthenticated) {
    next('/dashboard/resumo')
  } else if (to.meta.adminOnly && !authStore.isAdmin) {
    next('/dashboard/resumo')
  } else {
    next()
  }
})

export default router
