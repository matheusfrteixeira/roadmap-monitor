<template>
  <header class="topbar-container">
    <!-- NÍVEL 1: Barra Principal de Módulos -->
    <div class="topbar-main">
      <router-link to="/dashboard/resumo" class="brand">
        <div class="brand-icon">RM</div>
        <div class="brand-copy">
          <div>RoadMap Corp · Monitoramento</div>
          <small>Gestão de Demandas & Portfólio</small>
        </div>
      </router-link>

      <!-- 4 MÓDULOS PRINCIPAIS -->
      <nav class="module-nav">
        <!-- 1 - Dashboard -->
        <button
          type="button"
          class="module-btn"
          :class="{ active: currentModule === 'dashboard' }"
          @click="navigateModule('/dashboard/resumo')"
        >
          <span class="module-icon">📊</span>
          <span class="module-text">Dashboard</span>
        </button>

        <!-- 2 - Portfólio de Projetos -->
        <button
          type="button"
          class="module-btn"
          :class="{ active: currentModule === 'portfolio' }"
          @click="navigateModule('/portfolio/roadmaps')"
        >
          <span class="module-icon">📁</span>
          <span class="module-text">Portfólio de Projetos</span>
          <span
            v-if="timetrackerStore.isTimerRunning"
            class="badge bpink pulse"
            style="margin-left: 4px; font-size: 0.72rem; padding: 2px 5px;"
            title="Cronômetro em execução"
          >
            ⏱️ {{ timetrackerStore.formattedTimer }}
          </span>
        </button>

        <!-- 3 - Administração (Apenas ADM) -->
        <button
          v-if="authStore.isAdmin"
          type="button"
          class="module-btn"
          :class="{ active: currentModule === 'admin' }"
          @click="navigateModule('/administracao/configuracoes')"
        >
          <span class="module-icon">⚙️</span>
          <span class="module-text">Administração</span>
        </button>

        <!-- 4 - Documentação -->
        <button
          type="button"
          class="module-btn"
          :class="{ active: currentModule === 'docs' }"
          @click="navigateModule('/documentacao')"
        >
          <span class="module-icon">📘</span>
          <span class="module-text">Documentação</span>
        </button>
      </nav>

      <!-- Usuário e Logout -->
      <div class="meta">
        <div class="user-badge" v-if="authStore.user">
          <div class="user-name">{{ authStore.user.name }}</div>
          <div class="user-role">{{ authStore.roleLabel }}</div>
        </div>
        <button
          class="btn secondary"
          @click="handleLogout"
          title="Sair da sessão"
          style="padding: 4px 9px; font-size: 0.78rem; font-weight:700;"
        >
          Sair
        </button>
      </div>
    </div>

    <!-- NÍVEL 2: Sub-Menu Contextual por Módulo -->
    <div class="topbar-subnav">
      <!-- Sub-itens do Módulo 1: Dashboard -->
      <div v-if="currentModule === 'dashboard'" class="subnav-links">
        <span class="subnav-module-title">Dashboard:</span>

        <router-link
          to="/dashboard/resumo"
          class="subnav-item"
          :class="{ active: isSubActive(['/dashboard/resumo', '/resumo', '/dashboard']) }"
        >
          📊 Resumo Executivo
        </router-link>

        <router-link
          to="/dashboard/areas"
          class="subnav-item"
          :class="{ active: isSubActive(['/dashboard/areas', '/areas']) }"
        >
          🏢 Visão por Área
        </router-link>

        <router-link
          to="/dashboard/stakeholders"
          class="subnav-item"
          :class="{ active: isSubActive(['/dashboard/stakeholders', '/stakeholders']) }"
        >
          👥 Visão por Solicitantes e Responsáveis
        </router-link>

        <router-link
          to="/dashboard/evolucao"
          class="subnav-item"
          :class="{ active: isSubActive(['/dashboard/evolucao', '/evolucao']) }"
        >
          📈 Evolução e Tendências
        </router-link>

        <router-link
          to="/dashboard/base"
          class="subnav-item"
          :class="{ active: isSubActive(['/dashboard/base', '/base']) }"
        >
          📋 Base Analítica
        </router-link>
      </div>

      <!-- Sub-itens do Módulo 2: Portfólio de Projetos -->
      <div v-else-if="currentModule === 'portfolio'" class="subnav-links">
        <span class="subnav-module-title">Portfólio:</span>

        <router-link
          to="/portfolio/roadmaps"
          class="subnav-item"
          :class="{ active: isSubActive(['/portfolio/roadmaps', '/portfolio', '/roadmaps']) }"
        >
          🗺️ Roadmaps
        </router-link>

        <router-link
          to="/portfolio/timetracker"
          class="subnav-item timer-item"
          :class="{ active: isSubActive(['/portfolio/timetracker', '/timetracker']) }"
        >
          ⏱️ Timetracker
          <span
            v-if="timetrackerStore.isTimerRunning"
            class="badge bpink"
            style="margin-left:4px; font-size:0.72rem; padding:1.5px 5px;"
          >
            {{ timetrackerStore.formattedTimer }}
          </span>
        </router-link>

        <router-link
          to="/portfolio/acompanhamento"
          class="subnav-item"
          :class="{ active: isSubActive(['/portfolio/acompanhamento', '/acompanhamento', '/timetracker/calendario']) }"
        >
          📅 Acompanhamento Diário
        </router-link>

        <span v-if="route.path.includes('/projeto/')" class="badge bpurple" style="margin-left: 6px; font-size: 0.78rem;">
          📌 Detalhes da Demanda #{{ route.params.id }}
        </span>
      </div>

      <!-- Sub-itens do Módulo 3: Administração -->
      <div v-else-if="currentModule === 'admin'" class="subnav-links">
        <span class="subnav-module-title">Administração:</span>

        <router-link
          to="/administracao/configuracoes"
          class="subnav-item"
          :class="{ active: isSubActive(['/administracao/configuracoes', '/configuracoes', '/administracao']) }"
        >
          ⚙️ Configurações Gerais, Áreas & Usuários
        </router-link>
      </div>

      <!-- Sub-itens do Módulo 4: Documentação -->
      <div v-else-if="currentModule === 'docs'" class="subnav-links">
        <span class="subnav-module-title">Documentação:</span>

        <router-link
          to="/documentacao"
          class="subnav-item"
          :class="{ active: isSubActive(['/documentacao', '/docs']) }"
        >
          📘 Manual & Guia Operacional do Usuário
        </router-link>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useTimetrackerStore } from '@/stores/timetracker'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const timetrackerStore = useTimetrackerStore()

// Módulo Ativo Determinado pela Rota
const currentModule = computed(() => {
  if (route.meta?.module) {
    return route.meta.module
  }
  const path = route.path
  if (path.startsWith('/dashboard') || path === '/resumo' || path === '/areas' || path === '/stakeholders' || path === '/evolucao' || path === '/base') {
    return 'dashboard'
  }
  if (path.startsWith('/portfolio') || path === '/roadmaps' || path.startsWith('/projeto') || path.startsWith('/timetracker') || path.startsWith('/acompanhamento')) {
    return 'portfolio'
  }
  if (path.startsWith('/administracao') || path.startsWith('/configuracoes')) {
    return 'admin'
  }
  if (path.startsWith('/documentacao') || path.startsWith('/docs')) {
    return 'docs'
  }
  return 'dashboard'
})

function navigateModule(targetPath) {
  router.push(targetPath)
}

function isSubActive(paths) {
  return paths.some(p => route.path === p || (p !== '/' && route.path.startsWith(p + '/')))
}

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.topbar-container {
  position: sticky;
  top: 0;
  z-index: 40;
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 14px;
  box-shadow: 0 3px 12px rgba(62, 38, 102, 0.05);
  margin-bottom: 12px;
  overflow: hidden;
}

/* Nível 1: Barra Principal */
.topbar-main {
  min-height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 18px;
  gap: 16px;
  border-bottom: 1px solid var(--line);
}

.brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 800;
  color: var(--purple);
  min-width: 220px;
  font-size: 1.05rem;
  text-decoration: none;
  cursor: pointer;
}

.brand-icon {
  width: 32px;
  height: 32px;
  background: var(--purple);
  color: #fff;
  border-radius: 7px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: 1.1rem;
}

.brand-copy {
  min-width: 0;
  line-height: 1.2;
}

.brand small {
  display: block;
  color: #918899;
  font-size: 0.76rem;
  font-weight: 600;
  margin-top: 1px;
}

.module-nav {
  display: flex;
  align-items: center;
  gap: 5px;
  flex: 1;
  justify-content: center;
}

.module-btn {
  background: transparent;
  border: 1px solid transparent;
  color: #655A70;
  font-weight: 600;
  font-size: 0.84rem;
  padding: 6px 13px;
  border-radius: 16px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  transition: all 0.2s ease;
}

.module-btn:hover {
  background: var(--purple3);
  color: var(--purple);
}

.module-btn.active {
  background: var(--purple);
  color: #fff;
  font-weight: 700;
  box-shadow: 0 2px 6px rgba(62, 38, 102, 0.25);
}

.meta {
  display: flex;
  align-items: center;
  gap: 8px;
  text-align: right;
}

.user-badge {
  background: var(--purple4);
  border: 1px solid #DDD8E4;
  border-radius: 6px;
  padding: 3px 8px;
  text-align: left;
}

.user-badge .user-name {
  font-weight: 700;
  color: var(--purple);
  font-size: 0.82rem;
}

.user-badge .user-role {
  font-size: 0.72rem;
  color: var(--muted);
}

/* Nível 2: Sub-Navegação */
.topbar-subnav {
  background: #FAF9FC;
  padding: 4px 16px;
  min-height: 36px;
  display: flex;
  align-items: center;
}

.subnav-links {
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.subnav-module-title {
  font-size: 0.76rem;
  font-weight: 800;
  text-transform: uppercase;
  color: #8C8299;
  letter-spacing: 0.5px;
  margin-right: 2px;
}

.subnav-item {
  text-decoration: none;
  font-size: 0.8rem;
  font-weight: 600;
  color: #554A62;
  background: #fff;
  border: 1px solid var(--line);
  padding: 4px 10px;
  border-radius: 12px;
  transition: all 0.18s ease;
  display: inline-flex;
  align-items: center;
  gap: 5px;
}

.subnav-item:hover {
  border-color: var(--purple2);
  color: var(--purple);
  background: #F3EFF9;
}

.subnav-item.active {
  background: var(--purple2);
  color: #fff;
  border-color: var(--purple2);
  font-weight: 700;
}

.subnav-item.timer-item.active {
  background: var(--pink);
  border-color: var(--pink);
  color: #fff;
}

.pulse {
  animation: pulseAnim 1.8s infinite;
}

@keyframes pulseAnim {
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.08); opacity: 0.85; }
  100% { transform: scale(1); opacity: 1; }
}

@media (max-width: 900px) {
  .topbar-main {
    flex-direction: column;
    align-items: stretch;
  }
  .module-nav {
    flex-wrap: wrap;
    justify-content: flex-start;
  }
  .meta {
    justify-content: space-between;
  }
}
</style>
