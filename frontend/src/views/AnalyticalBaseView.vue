<template>
  <div>
    <div style="display:flex; justify-content:space-between; align-items:flex-end;">
      <div>
        <div class="title">📋 Base Analítica Unificada</div>
        <div class="sub">Selecione os filtros e gere relatórios detalhados com exportação em formato CSV.</div>
      </div>
      <button v-if="hasGenerated && filteredRows.length > 0" class="btn" @click="exportCSV">
        ⬇ Exportar CSV ({{ filteredRows.length }} linhas)
      </button>
    </div>

    <!-- Painel de Filtros para Geração -->
    <div class="card" style="margin-top: 10px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
        <span class="small" style="font-weight:700; color:var(--purple)">Parâmetros da Consulta</span>
        <button v-if="hasGenerated" class="btn secondary" style="font-size:0.78rem; padding:4px 9px;" @click="resetQuery">
          Limpar Consulta
        </button>
      </div>

      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(180px, 1fr)); gap:10px;">
        <div class="form-group" style="margin-bottom:0;">
          <label>Tipo de Registro</label>
          <select v-model="filterType" class="form-control">
            <option value="ALL">Todos (Projetos & Atividades)</option>
            <option value="PROJETO">Apenas Projetos</option>
            <option value="ATIVIDADE">Apenas Atividades</option>
          </select>
        </div>

        <div class="form-group" style="margin-bottom:0;">
          <label>Status</label>
          <select v-model="filterStatus" class="form-control">
            <option value="">Todos os Status</option>
            <option value="Concluído">Concluído</option>
            <option value="Em Andamento">Em Andamento</option>
            <option value="Não Iniciado">Não Iniciado</option>
            <option value="Em Espera">Em Espera</option>
            <option value="Cancelado">Cancelado</option>
          </select>
        </div>

        <div class="form-group" style="margin-bottom:0;">
          <label>Buscar por Texto</label>
          <input v-model="filterSearch" class="form-control" placeholder="Nome, código, solicitante..." />
        </div>
      </div>

      <div style="margin-top: 10px; display:flex; justify-content: flex-end;">
        <button class="btn" style="height:33px; padding:0 16px; font-size:0.84rem;" @click="handleGenerate">
          🔍 Gerar Relatório Analítico
        </button>
      </div>
    </div>

    <!-- ESTADO INICIAL (A princípio não aparece nada) -->
    <div v-if="!hasGenerated" class="card" style="margin-top:12px; text-align:center; padding:40px 16px;">
      <div style="font-size:32px; margin-bottom:8px;">📊</div>
      <h3 style="color:var(--purple); margin-bottom:4px;">Aguardando geração da consulta</h3>
      <p style="margin:0; font-size:0.84rem; color:var(--muted); max-width:400px; margin:auto;">
        Selecione os parâmetros de filtro desejados acima e clique em 
        <strong>"Gerar Relatório Analítico"</strong> para consultar a base de dados.
      </p>
    </div>

    <!-- ESTADO GERADO (Tabela e resultados na tela) -->
    <div v-else class="section">
      <!-- Mini Indicadores do Resultado -->
      <div class="kpis" style="margin-bottom:10px;">
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

      <div class="card">
        <div class="tw">
          <table>
            <thead>
              <tr>
                <th style="width:70px;">Tipo</th>
                <th style="width:90px;">Código</th>
                <th>Nome / Demanda</th>
                <th>Status</th>
                <th>Início</th>
                <th>Término</th>
                <th>Progresso</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in filteredRows" :key="item.uniqueKey">
                <td>
                  <span class="badge" :class="item.type === 'PROJETO' ? 'bpurple' : 'bpink'">
                    {{ item.type }}
                  </span>
                </td>
                <td><strong>{{ item.code }}</strong></td>
                <td>
                  <strong :style="{ color: item.type === 'PROJETO' ? 'var(--purple)' : 'inherit' }">
                    {{ item.name }}
                  </strong>
                </td>
                <td>
                  <span class="badge" :class="getStatusClass(item.status)">
                    {{ item.status }}
                  </span>
                </td>
                <td>{{ item.start_date || '—' }}</td>
                <td>{{ item.end_date || '—' }}</td>
                <td>
                  <div style="display:flex; align-items:center; gap:5px;">
                    <div class="track" style="width:60px;">
                      <div class="fill" :style="{ width: item.progress + '%' }"></div>
                    </div>
                    <span>{{ item.progress }}%</span>
                  </div>
                </td>
              </tr>
              <tr v-if="filteredRows.length === 0">
                <td colspan="7" style="text-align:center; padding:30px; color:var(--muted)">
                  Nenhum registro encontrado para os filtros selecionados.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoadmapStore } from '@/stores/roadmap'

const roadmapStore = useRoadmapStore()

const hasGenerated = ref(false)
const filterType = ref('ALL')
const filterStatus = ref('')
const filterSearch = ref('')

const activeFilterType = ref('ALL')
const activeFilterStatus = ref('')
const activeFilterSearch = ref('')

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
}

const allRows = computed(() => {
  const rows = []
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

function getStatusClass(s) {
  if (s === 'Concluído') return 'bgreen'
  if (s === 'Em Andamento') return 'bpurple'
  if (s === 'Em Espera') return 'byellow'
  return 'bgray'
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
