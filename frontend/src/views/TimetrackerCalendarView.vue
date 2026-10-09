<template>
  <div class="calendar-page">
    <!-- Topo da Página -->
    <div class="page-header">
      <div>
        <div class="title">📅 Acompanhamento Diário & Calendário Semanal</div>
        <div class="sub">
          Acompanhamento visual de esforço diário organizado por semana.
          <span v-if="authStore.isGestor">Você visualiza as entregas de toda a sua equipe direta.</span>
          <span v-else-if="authStore.isAdmin">Você possui visão global de todos os colaboradores.</span>
          <span v-else>Visualização do seu histórico pessoal de produção.</span>
        </div>
      </div>

      <!-- Filtro de Colaborador (Para Gestor e Admin) -->
      <div v-if="authStore.isAdmin || authStore.isGestor" class="filter-colaborador">
        <label>Filtrar Colaborador da Equipe</label>
        <select v-model="selectedUserId" class="form-control" @change="loadCalendar">
          <option :value="null">👥 Toda a Equipe / Subordinados</option>
          <option v-for="u in allowedUsers" :key="u.id" :value="u.id">
            👤 {{ u.name }}
          </option>
        </select>
      </div>
    </div>

    <!-- Barra de Navegação da Semana & Controles -->
    <div class="nav-bar card">
      <div class="nav-actions">
        <button class="btn secondary nav-btn" @click="previousWeek" title="Semana Anterior">
          ◀ Anterior
        </button>
        <button class="btn nav-btn" :class="{ primary: isCurrentWeekSelected, secondary: !isCurrentWeekSelected }" @click="goToCurrentWeek" title="Ir para a semana atual">
          Hoje / Semana Atual
        </button>
        <button class="btn secondary nav-btn" @click="nextWeek" title="Próxima Semana">
          Próxima ▶
        </button>
      </div>

      <div class="week-title-container">
        <span class="week-badge">Semana {{ weekNumber }}</span>
        <h2 class="week-range-text">{{ weekRangeLabel }}</h2>
      </div>

      <div class="nav-controls-right">
        <!-- Alternar Início da Semana (Dom ou Seg) -->
        <button
          class="btn secondary small-btn"
          @click="startOnMonday = !startOnMonday"
          :title="startOnMonday ? 'Mudar para início no Domingo' : 'Mudar para início na Segunda-feira'"
        >
          {{ startOnMonday ? 'Início: Seg ➔ Dom' : 'Início: Dom ➔ Sáb' }}
        </button>

        <!-- Ir para data específica -->
        <div class="datepicker-wrapper">
          <span class="small-label">Ir para data:</span>
          <input
            type="date"
            class="form-control date-picker-input"
            :value="pickerDateValue"
            @change="onDatePickerChange"
          />
        </div>
      </div>
    </div>

    <!-- Indicadores da Semana Selecionada -->
    <div class="kpis" style="margin-top: 10px;">
      <div class="kpi primary">
        <div class="v">{{ weekTotalHours }}h</div>
        <div class="l">Horas na Semana</div>
        <div class="n">{{ weekTotalMinutes }} minutos apontados</div>
      </div>
      <div class="kpi">
        <div class="v">{{ weekEntriesCount }}</div>
        <div class="l">Sessões / Apontamentos</div>
        <div class="n">Tarefas registradas</div>
      </div>
      <div class="kpi">
        <div class="v" style="color:var(--purple)">{{ weekDaysWorkedCount }} / 7</div>
        <div class="l">Dias com Produção</div>
        <div class="n">Dias com atividade nesta semana</div>
      </div>
      <div class="kpi">
        <div class="v" style="color:var(--green)">
          {{ weekAverageDailyHours }}h
        </div>
        <div class="l">Média Diária</div>
        <div class="n">Por dia trabalhado</div>
      </div>
    </div>

    <!-- Calendário Semanal em Caixinhas Verticais -->
    <div class="section calendar-section">
      <div v-if="loading" class="card loading-state">
        ⏳ Carregando apontamentos do calendário...
      </div>

      <div v-else class="week-grid">
        <!-- Coluna de Cada Dia -->
        <div
          v-for="col in weekColumns"
          :key="col.dateKey"
          class="day-column"
          :class="{ 'today-column': col.isToday }"
        >
          <!-- Cabeçalho do Dia (Estilo Calendário da Imagem) -->
          <div class="day-header" :class="{ 'weekend-header': col.isWeekend }">
            <div class="day-name" :class="{ 'weekend-text': col.isWeekend }">
              {{ col.weekdayShort }}
            </div>
            <div class="day-number-wrapper">
              <span
                class="day-number"
                :class="{ 'today-circle': col.isToday, 'weekend-number': col.isWeekend && !col.isToday }"
              >
                {{ col.dayNum }}
              </span>
            </div>
            <div class="day-hours-badge" :class="{ 'has-hours': col.totalMinutes > 0 }">
              <span v-if="col.totalMinutes > 0">⏱️ {{ col.totalHours }}h</span>
              <span v-else class="empty-hours">—</span>
            </div>
          </div>

          <!-- Corpo da Coluna: Caixinha Vertical com os Cards das Atividades -->
          <div class="day-body">
            <!-- Lista de Atividades do Dia -->
            <div
              v-for="entry in col.entries"
              :key="entry.id"
              class="activity-card"
              :style="{
                borderLeftColor: getCardTheme(entry).border,
                backgroundColor: getCardTheme(entry).bg
              }"
              @click="openDetailModal(entry)"
            >
              <!-- Linha Superior do Card: Duração e Horário -->
              <div class="card-top-row">
                <span
                  class="time-badge"
                  :style="{
                    color: getCardTheme(entry).text,
                    backgroundColor: getCardTheme(entry).badge
                  }"
                >
                  ⏱️ {{ formatDuration(entry.time_spent_minutes) }}
                </span>
                <span class="entry-time">
                  {{ formatTime(entry.date_recorded) }}
                </span>
              </div>

              <!-- Título da Atividade -->
              <div class="card-title">
                {{ entry.activity_name }}
              </div>

              <!-- Projeto -->
              <div class="card-project">
                📁 {{ entry.project_name }}
              </div>

              <!-- Observação / Descrição da Tarefa (se houver) -->
              <div v-if="entry.description" class="card-note">
                {{ truncateText(entry.description, 75) }}
              </div>

              <!-- Colaborador (visível se tiver múltiplos usuários) -->
              <div class="card-user">
                👤 {{ entry.user_name }}
              </div>
            </div>

            <!-- Estado Vazio para o Dia -->
            <div v-if="col.entries.length === 0" class="empty-day-state">
              <span class="empty-icon">☕</span>
              <span>Sem atividades</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal de Detalhes do Apontamento -->
    <div v-if="showModal && selectedEntry" class="modal-backdrop" @click.self="showModal = false">
      <div class="modal-content">
        <div class="modal-header">
          <h2>Detalhes do Apontamento de Horas</h2>
          <button class="modal-close" @click="showModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="detail-row">
            <span class="detail-label">Atividade:</span>
            <strong style="color:var(--purple); font-size:1.05rem;">{{ selectedEntry.activity_name }}</strong>
          </div>
          <div class="detail-row">
            <span class="detail-label">Projeto:</span>
            <span>📁 {{ selectedEntry.project_name }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Colaborador:</span>
            <span>👤 {{ selectedEntry.user_name }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Data & Horário:</span>
            <span>📅 {{ formatFullDate(selectedEntry.date_recorded) }} às {{ formatTime(selectedEntry.date_recorded) }}</span>
          </div>
          <div class="detail-row">
            <span class="detail-label">Tempo Investido:</span>
            <span class="badge bpink" style="font-size:0.95rem; font-weight:700;">
              ⏱️ {{ formatDuration(selectedEntry.time_spent_minutes) }} ({{ selectedEntry.time_spent_minutes }} minutos)
            </span>
          </div>

          <div class="detail-note-section">
            <label class="detail-label">Descrição das Tarefas / Observações:</label>
            <div class="detail-note-box">
              {{ selectedEntry.description || 'Nenhuma observação informada neste apontamento.' }}
            </div>
          </div>

          <div style="display:flex; justify-content:flex-end; margin-top:20px;">
            <button class="btn secondary" @click="showModal = false">Fechar</button>
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

// Controle de Navegação da Semana
const anchorDate = ref(new Date())
const startOnMonday = ref(false) // false = Dom ➔ Sáb (como no anexo), true = Seg ➔ Dom

// Modal de Detalhes
const showModal = ref(false)
const selectedEntry = ref(null)

// Paleta de Temas Suaves para os Cards (igual à imagem de referência)
const CARD_THEMES = [
  { border: '#3B82F6', bg: '#EFF6FF', text: '#1D4ED8', badge: '#DBEAFE' }, // Azul
  { border: '#10B981', bg: '#ECFDF5', text: '#047857', badge: '#D1FAE5' }, // Verde
  { border: '#F59E0B', bg: '#FFFBEB', text: '#B45309', badge: '#FEF3C7' }, // Laranja / Âmbar
  { border: '#8B5CF6', bg: '#F5F3FF', text: '#6D28D9', badge: '#EDE9FE' }, // Roxo
  { border: '#EC4899', bg: '#FDF2F8', text: '#BE185D', badge: '#FCE7F3' }, // Rosa
  { border: '#06B6D4', bg: '#ECFEFF', text: '#0E7490', badge: '#CFFAFE' }, // Ciano
  { border: '#EF4444', bg: '#FEF2F2', text: '#B91C1C', badge: '#FEE2E2' }, // Vermelho / Coral
]

function getCardTheme(entry) {
  const seed = (entry.project_id || 0) * 11 + (entry.activity_id || 0) * 17 + (entry.id || 0)
  return CARD_THEMES[Math.abs(seed) % CARD_THEMES.length]
}

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

// Retorna a chave YYYY-MM-DD em horário local seguro
function getEntryLocalDateKey(dateStr) {
  if (!dateStr) return null
  const iso = (dateStr.endsWith('Z') || dateStr.includes('+')) ? dateStr : dateStr + 'Z'
  const d = new Date(iso)
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

// Navegação da Semana
function previousWeek() {
  const d = new Date(anchorDate.value)
  d.setDate(d.getDate() - 7)
  anchorDate.value = d
}

function nextWeek() {
  const d = new Date(anchorDate.value)
  d.setDate(d.getDate() + 7)
  anchorDate.value = d
}

function goToCurrentWeek() {
  anchorDate.value = new Date()
}

const isCurrentWeekSelected = computed(() => {
  const today = new Date()
  const currentDays = weekColumns.value
  return currentDays.some(d => d.isToday)
})

const pickerDateValue = computed(() => {
  const d = anchorDate.value
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
})

function onDatePickerChange(event) {
  const val = event.target.value
  if (val) {
    const [y, m, d] = val.split('-').map(Number)
    anchorDate.value = new Date(y, m - 1, d)
  }
}

// Gera as 7 colunas da semana
const weekColumns = computed(() => {
  const anchor = new Date(anchorDate.value)
  anchor.setHours(0, 0, 0, 0)

  let dayOffset = anchor.getDay() // 0 = Dom, 1 = Seg...
  if (startOnMonday.value) {
    dayOffset = (anchor.getDay() + 6) % 7 // 0 = Seg... 6 = Dom
  }

  const startOfWeek = new Date(anchor)
  startOfWeek.setDate(anchor.getDate() - dayOffset)

  const weekdayNames = startOnMonday.value
    ? ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
    : ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']

  const cols = []
  const todayStr = new Date().toDateString()

  for (let i = 0; i < 7; i++) {
    const cur = new Date(startOfWeek)
    cur.setDate(startOfWeek.getDate() + i)

    const year = cur.getFullYear()
    const month = String(cur.getMonth() + 1).padStart(2, '0')
    const day = String(cur.getDate()).padStart(2, '0')
    const dateKey = `${year}-${month}-${day}`

    const isToday = cur.toDateString() === todayStr
    const dayOfWeek = cur.getDay()
    const isWeekend = dayOfWeek === 0 || dayOfWeek === 6

    // Filtra atividades deste dia
    const dayEntries = entries.value.filter(e => {
      return getEntryLocalDateKey(e.date_recorded) === dateKey
    })

    const totalMinutes = dayEntries.reduce((sum, e) => sum + (e.time_spent_minutes || 0), 0)
    const totalHours = (totalMinutes / 60).toFixed(1)

    cols.push({
      dateObj: cur,
      dateKey,
      dayNum: cur.getDate(),
      weekdayShort: weekdayNames[i],
      isToday,
      isWeekend,
      entries: dayEntries,
      totalMinutes,
      totalHours
    })
  }

  return cols
})

// Texto com intervalo de datas da semana
const weekRangeLabel = computed(() => {
  if (weekColumns.value.length === 0) return ''
  const first = weekColumns.value[0].dateObj
  const last = weekColumns.value[6].dateObj

  const d1 = first.getDate()
  const m1 = first.toLocaleDateString('pt-BR', { month: 'short' })
  const d2 = last.getDate()
  const m2 = last.toLocaleDateString('pt-BR', { month: 'short' })
  const year = last.getFullYear()

  if (first.getMonth() === last.getMonth()) {
    return `${d1} a ${d2} de ${first.toLocaleDateString('pt-BR', { month: 'long' })} de ${year}`
  }
  return `${d1} de ${m1} a ${d2} de ${m2} de ${year}`
})

// Número da semana no ano (ISO)
const weekNumber = computed(() => {
  const d = new Date(anchorDate.value)
  d.setHours(0, 0, 0, 0)
  d.setDate(d.getDate() + 4 - (d.getDay() || 7))
  const yearStart = new Date(d.getFullYear(), 0, 1)
  const weekNo = Math.ceil((((d - yearStart) / 86400000) + 1) / 7)
  return weekNo
})

// KPIs da Semana
const weekTotalMinutes = computed(() => {
  return weekColumns.value.reduce((sum, c) => sum + c.totalMinutes, 0)
})

const weekTotalHours = computed(() => {
  return (weekTotalMinutes.value / 60).toFixed(1)
})

const weekEntriesCount = computed(() => {
  return weekColumns.value.reduce((sum, c) => sum + c.entries.length, 0)
})

const weekDaysWorkedCount = computed(() => {
  return weekColumns.value.filter(c => c.entries.length > 0).length
})

const weekAverageDailyHours = computed(() => {
  if (weekDaysWorkedCount.value === 0) return '0.0'
  return (weekTotalMinutes.value / weekDaysWorkedCount.value / 60).toFixed(1)
})

function formatDuration(mins) {
  if (!mins) return '0m'
  const h = Math.floor(mins / 60)
  const m = mins % 60
  if (h === 0) return `${m} min`
  if (m === 0) return `${h}h`
  return `${h}h ${m}m`
}

function formatTime(dtStr) {
  if (!dtStr) return ''
  const iso = (dtStr.endsWith('Z') || dtStr.includes('+')) ? dtStr : dtStr + 'Z'
  return new Date(iso).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
}

function formatFullDate(dtStr) {
  if (!dtStr) return ''
  const iso = (dtStr.endsWith('Z') || dtStr.includes('+')) ? dtStr : dtStr + 'Z'
  return new Date(iso).toLocaleDateString('pt-BR', { weekday: 'long', day: '2-digit', month: '2-digit', year: 'numeric' })
}

function truncateText(txt, limit = 80) {
  if (!txt) return ''
  if (txt.length <= limit) return txt
  return txt.substring(0, limit) + '...'
}

function openDetailModal(entry) {
  selectedEntry.value = entry
  showModal.value = true
}
</script>

<style scoped>
.calendar-page {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 16px;
  flex-wrap: wrap;
}

.filter-colaborador {
  min-width: 260px;
}

.filter-colaborador label {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--muted);
  display: block;
  margin-bottom: 4px;
}

/* Barra de Navegação */
.nav-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 18px;
  gap: 14px;
  flex-wrap: wrap;
}

.nav-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.nav-btn {
  padding: 6px 14px;
  font-size: 0.9rem;
}

.week-title-container {
  display: flex;
  align-items: center;
  gap: 10px;
}

.week-badge {
  background: var(--purple3);
  color: var(--purple);
  font-weight: 700;
  font-size: 0.8rem;
  padding: 3px 10px;
  border-radius: 12px;
  text-transform: uppercase;
}

.week-range-text {
  margin: 0;
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--text);
}

.nav-controls-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.small-btn {
  padding: 5px 10px;
  font-size: 0.82rem;
  font-weight: 600;
}

.datepicker-wrapper {
  display: flex;
  align-items: center;
  gap: 6px;
}

.small-label {
  font-size: 0.82rem;
  color: var(--muted);
  font-weight: 600;
}

.date-picker-input {
  padding: 4px 8px;
  font-size: 0.85rem;
  width: 140px;
}

/* Loading */
.loading-state {
  text-align: center;
  padding: 40px;
  color: var(--muted);
  font-size: 1rem;
}

/* Grid Semanal de 7 Colunas */
.calendar-section {
  overflow-x: auto;
  padding-bottom: 12px;
}

.week-grid {
  display: grid;
  grid-template-columns: repeat(7, minmax(150px, 1fr));
  gap: 10px;
  min-width: 1080px;
}

/* Coluna de Cada Dia */
.day-column {
  background: #FAF9FC;
  border: 1px solid #EBE6F2;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  min-height: 480px;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.day-column.today-column {
  background: #F4F7FE;
  border-color: #93C5FD;
  box-shadow: 0 0 0 1.5px #60A5FA;
}

/* Cabeçalho do Dia (Estilo Imagem de Referência) */
.day-header {
  padding: 12px 8px 8px;
  text-align: center;
  border-bottom: 1px solid #ECE7F2;
  background: #fff;
  border-top-left-radius: 11px;
  border-top-right-radius: 11px;
}

.today-column .day-header {
  background: #EFF6FF;
  border-bottom-color: #BFDBFE;
}

.day-name {
  font-size: 0.86rem;
  font-weight: 700;
  text-transform: capitalize;
  color: #6D6678;
  margin-bottom: 4px;
}

.day-name.weekend-text {
  color: #E05252;
}

.day-number-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 38px;
  margin-bottom: 4px;
}

.day-number {
  font-size: 1.45rem;
  font-weight: 800;
  color: #2E2838;
}

.day-number.weekend-number {
  color: #E05252;
}

/* Círculo do Dia de Hoje (exatamente igual ao '15' da imagem) */
.day-number.today-circle {
  background: #DBEAFE;
  color: #1D4ED8;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  box-shadow: 0 2px 5px rgba(29, 78, 216, 0.25);
}

.day-hours-badge {
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--muted);
  border-radius: 6px;
  padding: 2px 6px;
  display: inline-block;
}

.day-hours-badge.has-hours {
  background: #F3E8FF;
  color: #7E22CE;
}

.empty-hours {
  color: #B8B0C2;
}

/* Corpo da Coluna: Caixinha Vertical */
.day-body {
  padding: 10px 8px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  flex: 1;
}

/* Card de Atividade (Caixinha Vertical) */
.activity-card {
  border-radius: 8px;
  border-left-width: 4px;
  border-left-style: solid;
  padding: 10px 9px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
  gap: 6px;
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
  border-top: 1px solid rgba(0, 0, 0, 0.04);
  border-right: 1px solid rgba(0, 0, 0, 0.04);
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
}

.activity-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.09);
}

.card-top-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.76rem;
}

.time-badge {
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.76rem;
}

.entry-time {
  color: #71697E;
  font-weight: 600;
}

.card-title {
  font-weight: 700;
  color: #1F192C;
  font-size: 0.9rem;
  line-height: 1.25;
}

.card-project {
  font-size: 0.78rem;
  font-weight: 600;
  color: #6D56A0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.card-note {
  background: rgba(255, 255, 255, 0.7);
  border-radius: 4px;
  padding: 4px 6px;
  font-size: 0.76rem;
  color: #4A4255;
  line-height: 1.35;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.card-user {
  font-size: 0.74rem;
  color: #756D80;
  font-weight: 500;
  text-align: right;
  margin-top: 2px;
}

/* Estado de Dia Sem Atividades */
.empty-day-state {
  border: 1px dashed #DDD7E6;
  border-radius: 8px;
  padding: 30px 6px;
  text-align: center;
  color: #A69CB0;
  font-size: 0.8rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.empty-icon {
  font-size: 1.25rem;
  opacity: 0.6;
}

/* Modal */
.modal-body {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-top: 10px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 0;
  border-bottom: 1px solid var(--line);
}

.detail-label {
  font-weight: 700;
  color: var(--muted);
  font-size: 0.88rem;
}

.detail-note-section {
  margin-top: 8px;
}

.detail-note-box {
  background: var(--purple4);
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 12px;
  font-size: 0.9rem;
  color: var(--text);
  line-height: 1.5;
  margin-top: 6px;
  white-space: pre-wrap;
  max-height: 200px;
  overflow-y: auto;
}
</style>
