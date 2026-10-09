<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-brand">
        <div class="brand-icon-lg">RM</div>
        <h1>RoadMap Corp</h1>
        <p>Monitoramento e Gestão de Portfólio & Demandas</p>
      </div>

      <div v-if="authStore.error" class="alert-error">
        {{ authStore.error }}
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label>Email Corporativo</label>
          <input
            v-model="email"
            type="email"
            required
            class="form-control"
            placeholder="ex: admin@roadmap.com"
          />
        </div>

        <div class="form-group">
          <label>Senha</label>
          <input
            v-model="password"
            type="password"
            required
            class="form-control"
            placeholder="••••••••"
          />
        </div>

        <button type="submit" class="btn" style="width: 100%; justify-content: center; height: 38px;" :disabled="authStore.loading">
          {{ authStore.loading ? 'Entrando...' : 'Entrar no Sistema' }}
        </button>
      </form>

      <div class="login-footer">
        <div class="hint">Acesso padrão de administrador:</div>
        <code>admin@roadmap.com</code> / <code>admin123</code>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useRoadmapStore } from '@/stores/roadmap'
import { useTimetrackerStore } from '@/stores/timetracker'

const authStore = useAuthStore()
const roadmapStore = useRoadmapStore()
const timetrackerStore = useTimetrackerStore()
const router = useRouter()

const email = ref('admin@roadmap.com')
const password = ref('admin123')

async function handleLogin() {
  const success = await authStore.login(email.value, password.value)
  if (success) {
    await Promise.all([
      roadmapStore.fetchAll(),
      timetrackerStore.fetchMyEntries()
    ])
    router.push('/resumo')
  }
}
</script>

<style scoped>
.login-container {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 400px;
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 32px 28px;
  box-shadow: 0 10px 30px rgba(62, 38, 102, 0.08);
}

.login-brand {
  text-align: center;
  margin-bottom: 24px;
}

.brand-icon-lg {
  width: 44px;
  height: 44px;
  background: var(--purple);
  color: #fff;
  border-radius: 10px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 900;
  font-size: 1.25rem;
  margin-bottom: 10px;
}

.login-brand h1 {
  margin: 0;
  font-size: 1.25rem;
  color: var(--purple);
  font-weight: 800;
}

.login-brand p {
  margin: 3px 0 0;
  font-size: 0.84rem;
  color: var(--muted);
}

.alert-error {
  background: var(--redbg);
  color: var(--red);
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 0.82rem;
  font-weight: 600;
  margin-bottom: 14px;
  border: 1px solid #FECDD3;
}

.login-footer {
  margin-top: 20px;
  padding-top: 14px;
  border-top: 1px solid var(--line);
  text-align: center;
  font-size: 0.78rem;
  color: var(--muted);
}

.login-footer code {
  background: var(--purple4);
  padding: 2px 5px;
  border-radius: 4px;
  color: var(--purple);
}
</style>

