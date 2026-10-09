<template>
  <div class="gantt-container">
    <div v-if="validItems.length === 0" class="gantt-empty">
      Nenhum item com datas de início e término definidas para exibir na linha do tempo.
    </div>
    <div v-else class="gantt-scroll">
      <!-- Cabeçalho de Datas -->
      <div class="gantt-header">
        <div class="gantt-item-label-header">Item / Demanda</div>
        <div class="gantt-timeline-header">
          <div
            v-for="(day, idx) in timelineDays"
            :key="idx"
            class="gantt-day-col"
            :class="{ 'is-weekend': day.isWeekend, 'is-today': day.isToday }"
          >
            <div class="day-num">{{ day.dayNum }}</div>
            <div class="day-month">{{ day.monthShort }}</div>
          </div>
        </div>
      </div>

      <!-- Linhas dos Itens -->
      <div class="gantt-body">
        <div v-for="item in validItems" :key="item.id" class="gantt-row">
          <div class="gantt-item-title" :title="item.name">
            <strong>{{ item.code ? item.code + ' · ' : '' }}</strong>{{ item.name }}
            <span class="badge" :class="getStatusBadgeClass(item.status)" style="margin-left: 6px;">
              {{ item.status }}
            </span>
            <span v-if="item.is_delayed" class="badge bred" style="margin-left: 4px; font-weight:800;">
              ⚠️ Atrasada
            </span>
          </div>

          <div class="gantt-timeline-track">
            <!-- Barra do Item -->
            <div
              class="gantt-bar"
              :style="getItemBarStyle(item)"
              :title="`${item.name}\nPeríodo: ${formatDate(item.start_date)} até ${formatDate(item.end_date)}\nProgresso: ${item.progress || 0}%`"
            >
              <div class="gantt-bar-fill" :style="{ width: (item.progress || 0) + '%' }"></div>
              <span class="gantt-bar-text">{{ item.progress || 0 }}%</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  items: {
    type: Array,
    default: () => []
  }
})

function parseDate(dStr) {
  if (!dStr) return null
  const parts = dStr.split('-')
  if (parts.length !== 3) return null
  return new Date(parseInt(parts[0]), parseInt(parts[1]) - 1, parseInt(parts[2]))
}

function formatDate(dStr) {
  if (!dStr) return '—'
  const d = parseDate(dStr)
  return d ? d.toLocaleDateString('pt-BR') : dStr
}

const validItems = computed(() => {
  return props.items.filter(i => i.start_date && i.end_date)
})

const timelineRange = computed(() => {
  if (validItems.value.length === 0) return { start: new Date(), end: new Date(), totalDays: 1 }

  let minTime = Infinity
  let maxTime = -Infinity

  validItems.value.forEach(i => {
    const s = parseDate(i.start_date)
    const e = parseDate(i.end_date)
    if (s && s.getTime() < minTime) minTime = s.getTime()
    if (e && e.getTime() > maxTime) maxTime = e.getTime()
  })

  // Margem de 2 dias antes e 5 dias depois
  const start = new Date(minTime)
  start.setDate(start.getDate() - 2)

  const end = new Date(maxTime)
  end.setDate(end.getDate() + 5)

  const diffTime = Math.abs(end - start)
  const totalDays = Math.max(7, Math.ceil(diffTime / (1000 * 60 * 60 * 24)))

  return { start, end, totalDays }
})

const timelineDays = computed(() => {
  const days = []
  const current = new Date(timelineRange.value.start)
  const today = new Date()
  today.setHours(0,0,0,0)

  const monthNames = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

  for (let i = 0; i <= timelineRange.value.totalDays; i++) {
    const isWeekend = current.getDay() === 0 || current.getDay() === 6
    const isToday = current.getTime() === today.getTime()

    days.push({
      date: new Date(current),
      dayNum: current.getDate(),
      monthShort: monthNames[current.getMonth()],
      isWeekend,
      isToday
    })
    current.setDate(current.getDate() + 1)
  }
  return days
})

function getItemBarStyle(item) {
  const s = parseDate(item.start_date)
  const e = parseDate(item.end_date)
  const rangeStart = timelineRange.value.start
  const totalDays = timelineRange.value.totalDays || 1

  const dayWidth = 32 // largura fixa de cada coluna em px
  const offsetDays = Math.max(0, (s - rangeStart) / (1000 * 60 * 60 * 24))
  const durationDays = Math.max(1, (e - s) / (1000 * 60 * 60 * 24) + 1)

  const left = offsetDays * dayWidth
  const width = Math.max(28, durationDays * dayWidth)

  let bg = '#6D56A0'
  if (item.status === 'Concluído') bg = '#50C878'
  else if (item.is_delayed) bg = '#D84A58'
  else if (item.status === 'Em Espera') bg = '#D69A00'
  else if (item.status === 'Cancelado') bg = '#999999'

  return {
    left: `${left}px`,
    width: `${width}px`,
    background: bg
  }
}

function getStatusBadgeClass(status) {
  if (status === 'Concluído') return 'bgreen'
  if (status === 'Em Andamento') return 'bpurple'
  if (status === 'Em Espera') return 'byellow'
  return 'bgray'
}
</script>

<style scoped>
.gantt-container {
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 10px;
  overflow: hidden;
  margin-top: 10px;
}

.gantt-empty {
  padding: 30px;
  text-align: center;
  color: var(--muted);
  font-size: 0.95rem;
}

.gantt-scroll {
  overflow-x: auto;
  min-width: 100%;
}

.gantt-header {
  display: flex;
  background: #F8F6FA;
  border-bottom: 2px solid var(--line);
  position: sticky;
  top: 0;
  z-index: 5;
}

.gantt-item-label-header {
  width: 250px;
  min-width: 250px;
  padding: 8px 12px;
  font-weight: 800;
  color: var(--purple);
  border-right: 1px solid var(--line);
  font-size: 0.82rem;
  display: flex;
  align-items: center;
}

.gantt-timeline-header {
  display: flex;
}

.gantt-day-col {
  width: 30px;
  min-width: 30px;
  text-align: center;
  padding: 4px 0;
  border-right: 1px solid #ECE7F2;
  font-size: 0.76rem;
}

.gantt-day-col.is-weekend {
  background: #F3EFF8;
}

.gantt-day-col.is-today {
  background: #FCE7F3;
  color: var(--pink);
  font-weight: 800;
}

.day-num {
  font-weight: 700;
  color: var(--text);
  font-size: 0.78rem;
}

.day-month {
  font-size: 0.7rem;
  color: var(--muted);
  text-transform: uppercase;
}

.gantt-body {
  display: flex;
  flex-direction: column;
}

.gantt-row {
  display: flex;
  border-bottom: 1px solid #F1EEF4;
  height: 36px;
  align-items: center;
}

.gantt-row:hover {
  background: #FAF8FC;
}

.gantt-item-title {
  width: 250px;
  min-width: 250px;
  padding: 0 12px;
  font-size: 0.82rem;
  border-right: 1px solid var(--line);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  display: flex;
  align-items: center;
}

.gantt-timeline-track {
  position: relative;
  height: 100%;
  display: flex;
  align-items: center;
  flex: 1;
}

.gantt-bar {
  position: absolute;
  height: 20px;
  border-radius: 5px;
  overflow: hidden;
  display: flex;
  align-items: center;
  box-shadow: 0 1px 4px rgba(0,0,0,0.12);
  transition: all 0.2s;
  cursor: pointer;
}

.gantt-bar:hover {
  filter: brightness(1.08);
}

.gantt-bar-fill {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.35);
  border-right: 2px solid #fff;
}

.gantt-bar-text {
  position: relative;
  z-index: 2;
  padding-left: 5px;
  font-size: 0.74rem;
  font-weight: 800;
  color: #fff;
  white-space: nowrap;
}
</style>

