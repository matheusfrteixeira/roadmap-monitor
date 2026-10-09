<template>
  <div>
    <div style="display:flex; justify-content:space-between; align-items:flex-end; gap:12px;">
      <div>
        <div class="title">📅 Acompanhamento Diário & Calendário de Produção</div>
        <div class="sub">
          Linha do tempo de esforço diário.
          <span v-if="authStore.isGestor">Você visualiza as entregas de toda a sua equipe direta.</span>
          <span v-else-if="authStore.isAdmin">Você possui visão global de todos os colaboradores.</span>
          <span v-else>Visualização do seu histórico pessoal de produção.</span>
        </div>
      </div>

      <!-- Seletor de Colaborador (Para Gestor e Admin) -->
      <div v-if="authStore.isAdmin || authStore.isGestor" style="min-width: 250px;">
        <label style="font-size:0.86rem; font-weight:700; color:var(--muted); display:block; margin-bottom:4px;">Filtrar Colaborador da Equipe</label>
        <select v-model="selectedUserId" class="form-control" @change="loadCalendar">
          <option :value="null">👥 Toda a Equipe / Subordinados</option>
          <option v-for="u in allowedUsers" :key="u.id" :value="u.id">
            👤 {{ u.name }} ({{ u.email }})
          </option>
        </select>
      </div>
    </div>

    <!-- Indicadores do Período -->
    <div class="kpis" style="margin-top: 10px;">
      <div class="kpi primary">
        <div class="v">{{ totalPeriodHours }}h</div>
        <div class="l">Horas Apontadas</div>
        <div class="n">No período selecionado</div>
      </div>
      <div class="kpi">
        <div class="v">{{ entries.length }}</div>
        <div class="l">Total de Sessões</div>
        <div class="n">Registros no histórico</div>
      </div>
      <div class="kpi">
        <div class="v">{{ daysCount }}</div>
        <div class="l">Dias com Produção</div>
        <div class="n">Dias com apontamento</div>
      </div>
      <div class="kpi">
        <div class="v" style="color:var(--green)">
          {{ daysCount > 0 ? (totalPeriodMinutes / daysCount / 60).toFixed(1) : 0 }}h
        </div>
        <div class="l">Média Diária</div>
        <div class="n">Por dia trabalhado</div>
      </div>
    </div>

    <!-- Linha do Tempo Diária -->
    <div class="section">
      <div v-if="loading" style="text-align:center; padding:30px; color:var(--muted);">
        Carregando acompanhamento diário...
      </div>

      <div v-else-if="groupedDays.length === 0" class="card" style="text-align:center; padding:35px; color:var(--muted); margin-top:10px;">
        Nenhum apontamento encontrado para este recorte de usuário ou data.
      </div>

      <div v-else style="display:flex; flex-direction:column; gap:12px; margin-top:10px;">
        <div v-for="day in groupedDays" :key="day.dateKey" class="card">
          <!-- Cabeçalho do Dia -->
          <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid var(--line); padding-bottom:8px; margin-bottom:10px;">
            <div style="display:flex; align-items:center; gap:8px;">
              <span class="badge bpurple">
                📅 {{ day.dateLabel }}
              </span>
              <span class="small" style="color:var(--muted)">({{ day.entries.length }} apontamentos)</span>
            </div>
            <div style="font-weight:800; color:var(--pink)">
              Total do Dia: {{ (day.totalMinutes / 60).toFixed(1) }}h ({{ day.totalMinutes }} min)
            </div>
          </div>

          <!-- Cards das Atividades desse dia -->
          <div style="display:grid; grid-template-columns:repeat(auto-fill, minmax(320px, 1fr)); gap:10px;">
            <div
              v-for="e in day.entries"
              :key="e.id"
              class="entry-card"
            >
              <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:6px;">
                <span class="badge bpink">
                  ⏱️ {{ e.time_spent_minutes }} min ({{ (e.time_spent_minutes / 60).toFixed(1) }}h)
                </span>
                <span class="badge bgray">
                  {{ formatTime(e.date_recorded) }}
                </span>
              </div>

              <div style="margin-top:4px;">
                <div class="small" style="color:var(--muted)">Projeto: <strong>{{ e.project_name }}</strong></div>
                <strong style="color:var(--purple); font-size:1.05rem; display:block; margin:2px 0;">
                  {{ e.activity_name }}
                </strong>
              </div>

              <!-- Descrição do Trabalho Feito -->
              <div class="entry-description">
                {{ e.description || 'Sessão concluída sem observações adicionais.' }}
              </div>

              <!-- Usuário responsável pelo apontamento -->
              <div class="small" style="margin-top:8px; color:var(--muted); text-align:right;">
                Colaborador: <strong>{{ e.user_name }}</strong>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const authStore = useAuthStore()
const entries = ref([])
const loading = ref(false)
const selectedUserId = ref(null)
const allowedUsers = ref([])

onMounted(async () => {
  await Promise.all([
    loadAllowedUsers(),
    loadCalendar()
  ])
})

async function loadAllowedUsers() {
  if (authStore.isAdmin || authStore.isGestor) {
    try {
      const res = await api.get('/users/')
      if (authStore.isAdmin) {
        allowedUsers.value = res.data
      } else if (authStore.isGestor) {
        // Apenas ele e subordinados diretos
        allowedUsers.value = res.data.filter(u => u.manager_id === authStore.user?.id || u.id === authStore.user?.id)
      }
    } catch (err) {
      console.error('Erro ao carregar lista de usuários:', err)
    }
  }
}

async function loadCalendar() {
  loading.value = true
  try {
    const params = {}
    if (selectedUserId.value) {
      params.user_id = selectedUserId.value
    }
    const res = await api.get('/timetracker/calendar', { params })
    entries.value = res.data
  } catch (err) {
    console.error('Erro ao carregar calendário:', err)
  } finally {
    loading.value = false
  }
}

const totalPeriodMinutes = computed(() => {
  return entries.value.reduce((sum, e) => sum + (e.time_spent_minutes || 0), 0)
})

const totalPeriodHours = computed(() => {
  return (totalPeriodMinutes.value / 60).toFixed(1)
})

const groupedDays = computed(() => {
  const map = {}
  entries.value.forEach(e => {
    const dateObj = new Date(e.date_recorded)
    const dateKey = e.date_recorded ? e.date_recorded.split('T')[0] : 'Indefinido'
    if (!map[dateKey]) {
      map[dateKey] = {
        dateKey,
        dateLabel: dateObj.toLocaleDateString('pt-BR', { weekday: 'long', day: '2-digit', month: '2-digit', year: 'numeric' }),
        entries: [],
        totalMinutes: 0
      }
    }
    map[dateKey].entries.push(e)
    map[dateKey].totalMinutes += (e.time_spent_minutes || 0)
  })

  // Ordena por data decrescente
  return Object.values(map).sort((a, b) => b.dateKey.localeCompare(a.dateKey))
})

const daysCount = computed(() => {
  return groupedDays.value.length
})

function formatTime(dtStr) {
  if (!dtStr) return ''
  return new Date(dtStr).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.entry-card {
  background: #FAF8FC;
  border: 1px solid #ECE7F2;
  border-radius: 8px;
  padding: 10px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.entry-description {
  background: #fff;
  border-radius: 6px;
  border: 1px solid #EFEBF4;
  padding: 8px 10px;
  font-size: 0.88rem;
  color: #4A4452;
  margin-top: 8px;
  line-height: 1.45;
  white-space: pre-wrap;
}
</style>

