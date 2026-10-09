<template>
  <div>
    <div class="title">⏱️ Timetracker · Gestão de Tempo & Produtividade</div>
    <div class="sub">Acompanhe seu tempo investido nas demandas, visualize seu extrato de horas e aponte sessões.</div>

    <div class="kpis" style="margin-top: 10px;">
      <div class="kpi primary">
        <div class="v">{{ timetrackerStore.totalTrackedHours }}h</div>
        <div class="l">Total de Horas</div>
        <div class="n">Apontadas por você</div>
      </div>
      <div class="kpi">
        <div class="v">{{ timetrackerStore.totalTrackedMinutes }} min</div>
        <div class="l">Minutos Totais</div>
        <div class="n">Registrados no sistema</div>
      </div>
      <div class="kpi">
        <div class="v">{{ timetrackerStore.myEntries.length }}</div>
        <div class="l">Total de Sessões</div>
        <div class="n">Apontamentos efetuados</div>
      </div>
      <div class="kpi">
        <div class="v" style="color: var(--pink)">
          {{ timetrackerStore.isTimerRunning ? 'Ativo' : 'Parado' }}
        </div>
        <div class="l">Status do Cronômetro</div>
        <div class="n">{{ timetrackerStore.formattedTimer }}</div>
      </div>
    </div>

    <div class="card" style="margin-top: 12px;">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <h3>Extrato de Apontamentos de Horas</h3>
        <button class="btn secondary" @click="timetrackerStore.fetchMyEntries" style="padding:6px 12px;">
          ↻ Atualizar
        </button>
      </div>
      <div class="small">Histórico em ordem cronológica reversa de todos os registros de tempo.</div>

      <div class="tw" style="margin-top: 10px;">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Data / Hora</th>
              <th>Atividade ID</th>
              <th>Duração</th>
              <th>Descrição das Atividades Realizadas</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="entry in timetrackerStore.myEntries" :key="entry.id">
              <td><strong>LOG-{{ String(entry.id).padStart(4, '0') }}</strong></td>
              <td>{{ formatDateTime(entry.date_recorded) }}</td>
              <td>
                <span class="badge bpurple">ATIV-{{ String(entry.activity_id).padStart(4, '0') }}</span>
              </td>
              <td>
                <strong style="color:var(--pink)">{{ entry.time_spent_minutes }} min</strong>
                <span class="small" style="margin-left:4px;">({{ (entry.time_spent_minutes / 60).toFixed(1) }}h)</span>
              </td>
              <td style="max-width:400px; white-space:normal;">
                {{ entry.description || '—' }}
              </td>
            </tr>
            <tr v-if="timetrackerStore.myEntries.length === 0">
              <td colspan="5" style="text-align:center; padding:25px; color:var(--muted)">
                Você ainda não realizou nenhum apontamento de horas.
                Abra um projeto e clique em "▶️ Iniciar" para começar a medir seu tempo!
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useTimetrackerStore } from '@/stores/timetracker'

const timetrackerStore = useTimetrackerStore()

onMounted(async () => {
  await timetrackerStore.fetchMyEntries()
})

function formatDateTime(dt) {
  if (!dt) return '—'
  return new Date(dt).toLocaleString('pt-BR')
}
</script>

