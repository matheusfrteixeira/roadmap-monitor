<template>
  <div>
    <div style="display:flex; justify-content:space-between; align-items:flex-end; gap:12px; flex-wrap:wrap;">
      <div>
        <div class="title">📋 Base Analítica Unificada</div>
        <div class="sub">Selecione os parâmetros e gere relatórios com paginação, ordenação e exportação CSV.</div>
      </div>
      <div v-if="hasGenerated && filteredRows.length > 0">
        <Button
          label="Exportar CSV"
          icon="pi pi-download"
          class="p-button-outlined"
          @click="exportCSV"
        />
      </div>
    </div>

    <!-- Painel de Filtros para Geração -->
    <div class="card" style="margin-top: 10px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
        <span class="small" style="font-weight:700; color:var(--purple)">Parâmetros da Consulta</span>
        <Button
          v-if="hasGenerated"
          label="Limpar Consulta"
          icon="pi pi-filter-slash"
          severity="secondary"
          text
          size="small"
          @click="resetQuery"
        />
      </div>

      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:12px;">
        <div class="form-group" style="margin-bottom:0;">
          <label style="font-size:0.82rem; font-weight:700; color:var(--muted); display:block; margin-bottom:4px;">Tipo de Registro</label>
          <Select
            v-model="filterType"
            :options="typeOptions"
            optionLabel="label"
            optionValue="value"
            placeholder="Selecione o tipo"
            style="width:100%;"
          />
        </div>

        <div class="form-group" style="margin-bottom:0;">
          <label style="font-size:0.82rem; font-weight:700; color:var(--muted); display:block; margin-bottom:4px;">Status</label>
          <Select
            v-model="filterStatus"
            :options="statusFilterOptions"
            optionLabel="label"
            optionValue="value"
            placeholder="Todos os Status"
            style="width:100%;"
          />
        </div>

        <div class="form-group" style="margin-bottom:0;">
          <label style="font-size:0.82rem; font-weight:700; color:var(--muted); display:block; margin-bottom:4px;">Buscar por Texto</label>
          <div class="p-input-icon-left" style="width:100%;">
            <InputText
              v-model="filterSearch"
              placeholder="Nome, código, demandante..."
              style="width:100%;"
              @keyup.enter="handleGenerate"
            />
          </div>
        </div>
      </div>

      <div style="margin-top: 14px; display:flex; justify-content: flex-end;">
        <Button
          label="Gerar Relatório Analítico"
          icon="pi pi-search"
          @click="handleGenerate"
        />
      </div>
    </div>

    <!-- ESTADO INICIAL (A princípio não aparece nada) -->
    <div v-if="!hasGenerated" class="card" style="margin-top:12px; text-align:center; padding:45px 16px;">
      <div style="font-size:36px; margin-bottom:10px;">📊</div>
      <h3 style="color:var(--purple); margin-bottom:6px;">Aguardando geração da consulta</h3>
      <p style="margin:0; font-size:0.86rem; color:var(--muted); max-width:440px; margin:auto; line-height:1.5;">
        Selecione os parâmetros de filtro desejados acima e clique em 
        <strong>"Gerar Relatório Analítico"</strong> para consultar a base de dados.
      </p>
    </div>

    <!-- ESTADO GERADO (DataTable PrimeVue) -->
    <div v-else class="section" style="margin-top:12px;">
      <!-- Mini Indicadores do Resultado -->
      <div class="kpis" style="margin-bottom:12px;">
        <div class="kpi primary">
          <div class="v">{{ filteredRows.length }}</div>
          <div class="l">Linhas Retornadas</div>
          <div class="n">No recorte da consulta</div>
        </div>
        <div class="kpi">
          <div class="v">{{ countProjects }}</div>
          <div class="l">Projetos</div>
          <div class="n">Itens do portfólio</div>
        </div>
        <div class="kpi">
          <div class="v">{{ countActivities }}</div>
          <div class="l">Atividades</div>
          <div class="n">Entregáveis</div>
        </div>
        <div class="kpi">
          <div class="v" style="color:var(--green)">{{ countCompleted }}</div>
          <div class="l">Itens Concluídos</div>
          <div class="n">Status ou progresso 100%</div>
        </div>
      </div>

      <!-- PrimeVue DataTable -->
      <div class="card" style="padding: 12px;">
        <DataTable
          ref="dt"
          :value="filteredRows"
          v-model:filters="tableFilters"
          dataKey="uniqueKey"
          paginator
          :rows="15"
          :rowsPerPageOptions="[10, 15, 25, 50, 100]"
          removableSort
          stripedRows
          responsiveLayout="scroll"
          class="p-datatable-sm"
        >
          <!-- Cabeçalho da Tabela -->
          <template #header>
            <div style="display:flex; justify-content:space-between; align-items:center; gap:10px; flex-wrap:wrap;">
              <span style="font-weight:700; color:var(--purple); font-size:0.95rem;">
                Registros Analíticos ({{ filteredRows.length }})
              </span>
              <div style="display:flex; align-items:center; gap:8px;">
                <span class="p-input-icon-left">
                  <InputText
                    v-model="tableFilters['global'].value"
                    placeholder="Filtrar tabela..."
                    style="font-size:0.85rem; height:32px;"
                  />
                </span>
                <Button
                  icon="pi pi-download"
                  severity="secondary"
                  outlined
                  size="small"
                  title="Exportar dados da tabela"
                  @click="exportCSV"
                />
              </div>
            </div>
          </template>

          <template #empty>
            <div style="text-align:center; padding:25px; color:var(--muted)">
              Nenhum registro encontrado para os filtros selecionados.
            </div>
          </template>

          <!-- Colunas -->
          <Column field="type" header="Tipo" sortable style="width: 100px;">
            <template #body="{ data }">
              <Tag
                :value="data.type"
                :severity="data.type === 'PROJETO' ? 'primary' : 'warning'"
                style="font-size:0.75rem; font-weight:700;"
              />
            </template>
          </Column>

          <Column field="code" header="Código" sortable style="width: 110px;">
            <template #body="{ data }">
              <strong>{{ data.code }}</strong>
            </template>
          </Column>

          <Column field="name" header="Nome / Demanda" sortable style="min-width: 250px;">
            <template #body="{ data }">
              <span :style="{ fontWeight: 700, color: data.type === 'PROJETO' ? 'var(--purple)' : 'inherit' }">
                {{ data.name }}
              </span>
            </template>
          </Column>

          <Column field="status" header="Status" sortable style="width: 130px;">
            <template #body="{ data }">
              <Tag
                :value="data.status"
                :severity="getStatusSeverity(data.status)"
              />
            </template>
          </Column>

          <Column field="start_date" header="Início" sortable style="width: 110px;">
            <template #body="{ data }">
              {{ formatDate(data.start_date) }}
            </template>
          </Column>

          <Column field="end_date" header="Término" sortable style="width: 110px;">
            <template #body="{ data }">
              {{ formatDate(data.end_date) }}
            </template>
          </Column>

          <Column field="progress" header="Progresso" sortable style="width: 140px;">
            <template #body="{ data }">
              <div style="display:flex; align-items:center; gap:8px;">
                <ProgressBar
                  :value="data.progress"
                  :showValue="false"
                  style="height: 8px; flex: 1;"
                />
                <span style="font-weight:700; font-size:0.82rem; min-width:34px; text-align:right;">
                  {{ data.progress }}%
                </span>
              </div>
            </template>
          </Column>
        </DataTable>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { FilterMatchMode } from '@primevue/core/api'
import { useRoadmapStore } from '@/stores/roadmap'

import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Select from 'primevue/select'
import Tag from 'primevue/tag'
import ProgressBar from 'primevue/progressbar'

const roadmapStore = useRoadmapStore()
const dt = ref(null)

const hasGenerated = ref(false)
const filterType = ref('ALL')
const filterStatus = ref('')
const filterSearch = ref('')

const activeFilterType = ref('ALL')
const activeFilterStatus = ref('')
const activeFilterSearch = ref('')

const tableFilters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS }
})

const typeOptions = [
  { label: 'Todos (Projetos & Atividades)', value: 'ALL' },
  { label: 'Apenas Projetos', value: 'PROJETO' },
  { label: 'Apenas Atividades', value: 'ATIVIDADE' }
]

const statusFilterOptions = [
  { label: 'Todos os Status', value: '' },
  { label: 'Concluído', value: 'Concluído' },
  { label: 'Em Andamento', value: 'Em Andamento' },
  { label: 'Não Iniciado', value: 'Não Iniciado' },
  { label: 'Em Espera', value: 'Em Espera' },
  { label: 'Cancelado', value: 'Cancelado' }
]

function handleGenerate() {
  activeFilterType.value = filterType.value
  activeFilterStatus.value = filterStatus.value
  activeFilterSearch.value = filterSearch.value
  hasGenerated.value = true
}

function resetQuery() {
  hasGenerated.value = false
  filterType.value = 'ALL'
  filterStatus.value = ''
  filterSearch.value = ''
  tableFilters.value.global.value = null
}

const allRows = computed(() => {
  const rows = []
  if (roadmapStore.projects) {
    roadmapStore.projects.forEach(p => {
      rows.push({
        uniqueKey: `p-${p.id}`,
        type: 'PROJETO',
        code: `PROJ-${String(p.id).padStart(3, '0')}`,
        name: p.name,
        status: p.status,
        start_date: p.start_date,
        end_date: p.end_date,
        progress: p.progress || 0
      })
    })
  }

  if (roadmapStore.activities) {
    roadmapStore.activities.forEach(a => {
      rows.push({
        uniqueKey: `a-${a.id}`,
        type: 'ATIVIDADE',
        code: `ATIV-${String(a.id).padStart(4, '0')}`,
        name: a.name,
        status: a.status,
        start_date: a.start_date,
        end_date: a.end_date,
        progress: a.progress || 0
      })
    })
  }
  return rows
})

const filteredRows = computed(() => {
  if (!hasGenerated.value) return []

  return allRows.value.filter(r => {
    if (activeFilterType.value !== 'ALL' && r.type !== activeFilterType.value) {
      return false
    }
    if (activeFilterStatus.value && r.status !== activeFilterStatus.value) {
      return false
    }
    if (activeFilterSearch.value) {
      const s = activeFilterSearch.value.toLowerCase()
      if (!r.name.toLowerCase().includes(s) && !r.code.toLowerCase().includes(s)) {
        return false
      }
    }
    return true
  })
})

const countProjects = computed(() => filteredRows.value.filter(r => r.type === 'PROJETO').length)
const countActivities = computed(() => filteredRows.value.filter(r => r.type === 'ATIVIDADE').length)
const countCompleted = computed(() => filteredRows.value.filter(r => r.status === 'Concluído' || r.progress >= 100).length)

function getStatusSeverity(status) {
  switch (status) {
    case 'Concluído':
      return 'success'
    case 'Em Andamento':
      return 'info'
    case 'Em Espera':
      return 'warn'
    case 'Cancelado':
      return 'danger'
    default:
      return 'secondary'
  }
}

function formatDate(d) {
  if (!d) return '—'
  return new Date(d + 'T00:00:00').toLocaleDateString('pt-BR')
}

function exportCSV() {
  const headers = ['Tipo', 'ID', 'Nome', 'Status', 'Inicio', 'Termino', 'Progresso']
  const csvContent = [
    headers.join(';'),
    ...filteredRows.value.map(r => [
      r.type,
      r.code,
      `"${r.name}"`,
      r.status,
      r.start_date || '',
      r.end_date || '',
      `${r.progress}%`
    ].join(';'))
  ].join('\n')

  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.setAttribute('href', url)
  link.setAttribute('download', `relatorio_analitico_${new Date().toISOString().split('T')[0]}.csv`)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}
</script>
