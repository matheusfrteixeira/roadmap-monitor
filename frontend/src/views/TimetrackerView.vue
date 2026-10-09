<template>
  <div>
    <div class="title">⏱️ Timetracker · Gestão de Tempo & Produtividade</div>
    <div class="sub">Acompanhe seu tempo investido nas demandas, visualize seu extrato de horas e meça sua produtividade.</div>

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

    <div class="card" style="margin-top: 12px; padding: 14px;">
      <DataTable
        :value="timetrackerStore.myEntries"
        v-model:filters="tableFilters"
        dataKey="id"
        paginator
        :rows="10"
        :rowsPerPageOptions="[5, 10, 20, 50]"
        removableSort
        stripedRows
        class="p-datatable-sm"
      >
        <template #header>
          <div style="display:flex; justify-content:space-between; align-items:center; gap:10px; flex-wrap:wrap;">
            <div>
              <h3 style="margin:0 0 2px 0;">Extrato de Apontamentos de Horas</h3>
              <div class="small" style="color:var(--muted)">Histórico de todos os registros de tempo efetuados.</div>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
              <span class="p-input-icon-left">
                <InputText
                  v-model="tableFilters['global'].value"
                  placeholder="Buscar no extrato..."
                  style="font-size:0.85rem; height:32px;"
                />
              </span>
              <Button
                icon="pi pi-refresh"
                label="Atualizar"
                severity="secondary"
                outlined
                size="small"
                :loading="timetrackerStore.loading"
                @click="timetrackerStore.fetchMyEntries"
              />
            </div>
          </div>
        </template>

        <template #empty>
          <div style="text-align:center; padding:30px; color:var(--muted)">
            Você ainda não realizou nenhum apontamento de horas.<br>
            Abra um projeto e clique em "▶️ Iniciar" para começar a medir seu tempo!
          </div>
        </template>

        <!-- Coluna ID -->
        <Column field="id" header="Código" sortable style="width: 120px;">
          <template #body="{ data }">
            <strong>LOG-{{ String(data.id).padStart(4, '0') }}</strong>
          </template>
        </Column>

        <!-- Data / Hora -->
        <Column field="date_recorded" header="Data / Hora" sortable style="width: 170px;">
          <template #body="{ data }">
            {{ formatDateTime(data.date_recorded) }}
          </template>
        </Column>

        <!-- Atividade ID -->
        <Column field="activity_id" header="Atividade" sortable style="width: 140px;">
          <template #body="{ data }">
            <Tag
              :value="'ATIV-' + String(data.activity_id).padStart(4, '0')"
              severity="secondary"
              style="font-weight:700;"
            />
          </template>
        </Column>

        <!-- Duração -->
        <Column field="time_spent_minutes" header="Duração" sortable style="width: 160px;">
          <template #body="{ data }">
            <strong style="color:var(--pink)">{{ data.time_spent_minutes }} min</strong>
            <span class="small" style="margin-left:5px; color:var(--muted);">
              ({{ (data.time_spent_minutes / 60).toFixed(1) }}h)
            </span>
          </template>
        </Column>

        <!-- Descrição -->
        <Column field="description" header="Descrição das Atividades Realizadas">
          <template #body="{ data }">
            <span style="font-size:0.88rem; line-height:1.4;">
              {{ data.description || '—' }}
            </span>
          </template>
        </Column>
      </DataTable>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { FilterMatchMode } from '@primevue/core/api'
import { useTimetrackerStore } from '@/stores/timetracker'

import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Tag from 'primevue/tag'

const timetrackerStore = useTimetrackerStore()

const tableFilters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS }
})

onMounted(async () => {
  await timetrackerStore.fetchMyEntries()
})

function formatDateTime(dt) {
  if (!dt) return '—'
  return new Date(dt).toLocaleString('pt-BR')
}
</script>
