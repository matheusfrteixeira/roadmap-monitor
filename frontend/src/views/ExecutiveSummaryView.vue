<template>
  <div>
    <!-- Hero Banner -->
    <div class="hero">
      <div>
        <h1>Como está a execução e a priorização do portfólio de projetos corporativos?</h1>
        <p>Visão centralizada de demandas, capacidade de entregas, gargalos de prazo e acompanhamento de ritmo.</p>
      </div>
      <div class="hero-badge">ROADMAP CORP → PROJETO → ENTREGÁVEL → ATIVIDADE → TEMPO</div>
    </div>

    <!-- Filtros Globais -->
    <GlobalFilters />

    <!-- 9 KPIs Executivos -->
    <div class="section">
      <div class="title">Visão Executiva do Portfólio</div>
      <div class="sub">Indicadores consolidados calculados dinamicamente em tempo real.</div>

      <div class="kpis">
        <div class="kpi primary">
          <div class="v">{{ roadmapStore.kpis.totalProjects }}</div>
          <div class="l">Total de Projetos</div>
          <div class="n">Carteira Total no Recorte</div>
        </div>

        <div class="kpi">
          <div class="v">{{ roadmapStore.kpis.concProjPct }}%</div>
          <div class="l">Conclusão de Projetos</div>
          <div class="n">{{ roadmapStore.kpis.completedProjects }} projetos concluídos</div>
        </div>

        <div class="kpi">
          <div class="v">{{ roadmapStore.kpis.totalDeliverables }}</div>
          <div class="l">Entregáveis Mapeados</div>
          <div class="n">Fases / marcos estruturais</div>
        </div>

        <div class="kpi">
          <div class="v">{{ roadmapStore.kpis.totalActivities }}</div>
          <div class="l">Total de Atividades</div>
          <div class="n">Tarefas e entregáveis</div>
        </div>

        <div class="kpi">
          <div class="v">{{ roadmapStore.kpis.concAtivPct }}%</div>
          <div class="l">Conclusão de Atividades</div>
          <div class="n">{{ roadmapStore.kpis.completedActivities }} concluídas</div>
        </div>

        <div class="kpi">
          <div class="v">{{ roadmapStore.kpis.pendingActivities }}</div>
          <div class="l">Atividades Pendentes</div>
          <div class="n">Em andamento ou abertas</div>
        </div>

        <div class="kpi">
          <div class="v" :style="{ color: roadmapStore.kpis.delayedActivities > 0 ? 'var(--red)' : 'var(--green)' }">
            {{ roadmapStore.kpis.delayedActivities }}
          </div>
          <div class="l">Atividades Atrasadas</div>
          <div class="n">Prazo de término expirado</div>
        </div>

        <div class="kpi">
          <div class="v" :style="{ color: roadmapStore.kpis.delayedProjects > 0 ? 'var(--red)' : 'inherit' }">
            {{ roadmapStore.kpis.delayedProjects }}
          </div>
          <div class="l">Projetos Atrasados</div>
          <div class="n">Término ultrapassado</div>
        </div>

        <div class="kpi">
          <div class="v" style="color: var(--pink)">
            {{ roadmapStore.kpis.totalTrackedHours }}h
          </div>
          <div class="l">Horas Investidas</div>
          <div class="n">Registradas no Timetracker</div>
        </div>

        <div class="kpi">
          <div class="v" :style="{ color: capacityMetrics.pressure <= 0 ? 'var(--green)' : 'var(--yellow)' }">
            {{ capacityMetrics.monthsCapacity }}m
          </div>
          <div class="l">Capacidade Estimada</div>
          <div class="n">{{ capacityMetrics.projectedDate }}</div>
        </div>
      </div>
    </div>

    <!-- Leitura Executiva e Capacidade de Ritmo -->
    <div class="section grid2">
      <div class="card">
        <h3>Leitura Executiva Automática</h3>
        <div class="small">Diagnóstico do portfólio recalculado com base no recorte dos filtros.</div>
        <div class="callout" style="line-height:1.55; margin-top:8px;">
          Resultado do RoadMap Centralizado: <strong>{{ roadmapStore.kpis.totalProjects }} projetos</strong> no recorte,
          com <strong>{{ roadmapStore.kpis.completedProjects }} concluídos ({{ roadmapStore.kpis.concProjPct }}%)</strong> e
          <strong>{{ roadmapStore.kpis.totalActivities }} atividades</strong> cadastradas.
          <span v-if="roadmapStore.kpis.delayedProjects > 0 || roadmapStore.kpis.delayedActivities > 0">
            Atenção necessária: existem <strong style="color:var(--red)">{{ roadmapStore.kpis.delayedProjects }} projetos</strong> e
            <strong style="color:var(--red)">{{ roadmapStore.kpis.delayedActivities }} atividades em atraso</strong> com data de término vencida,
            com maior concentração crítica na área <strong>{{ topBottleneckArea }}</strong>.
          </span>
          <span v-else>
            Excelente fluxo: nenhuma demanda ou atividade com prazo estourado no filtro aplicado.
          </span>
          <div style="margin-top:6px; font-size:0.8rem; color:var(--muted)">
            {{ capacityNarrative }}
          </div>
        </div>
      </div>

      <div class="card">
        <h3>Projeção de Ritmo & Capacidade</h3>
        <div class="small">Métricas operacionais de vazão e entrada de trabalho.</div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:8px;">
          <div style="background:var(--purple4); border:1px solid var(--line); border-radius:8px; padding:8px 10px;">
            <div class="small" style="color:var(--muted)">Ritmo de Entrega</div>
            <div style="font-size:1.15rem; font-weight:800; color:var(--green)">
              {{ capacityMetrics.deliveryRate }} <span style="font-size:0.75rem; font-weight:normal">tarefas/mês</span>
            </div>
            <div class="small">Média recente concluída</div>
          </div>
          <div style="background:var(--purple4); border:1px solid var(--line); border-radius:8px; padding:8px 10px;">
            <div class="small" style="color:var(--muted)">Taxa de Entrada</div>
            <div style="font-size:1.15rem; font-weight:800; color:var(--purple)">
              {{ capacityMetrics.entryRate }} <span style="font-size:0.75rem; font-weight:normal">novas/mês</span>
            </div>
            <div class="small">Demandas geradas</div>
          </div>
          <div style="background:var(--purple4); border:1px solid var(--line); border-radius:8px; padding:8px 10px;">
            <div class="small" style="color:var(--muted)">Saldo de Pressão</div>
            <div style="font-size:1.15rem; font-weight:800;" :style="{ color: capacityMetrics.pressure <= 0 ? 'var(--green)' : 'var(--red)' }">
              {{ capacityMetrics.pressure > 0 ? '+' : '' }}{{ capacityMetrics.pressure }} <span style="font-size:0.75rem; font-weight:normal">tarefas/mês</span>
            </div>
            <div class="small">Saldo de vazão operacional</div>
          </div>
          <div style="background:var(--purple4); border:1px solid var(--line); border-radius:8px; padding:8px 10px;">
            <div class="small" style="color:var(--muted)">Previsão de Término</div>
            <div style="font-size:1.05rem; font-weight:800; color:var(--purple)">
              {{ capacityMetrics.projectedDate }}
            </div>
            <div class="small">Para as pendências atuais</div>
          </div>
        </div>
      </div>
    </div>

    <!-- NOVOS GRÁFICOS: ONDE ESTÃO OS MAIORES GARGALOS & EXECUÇÃO POR ÁREA -->
    <div class="section grid2">
      <!-- Onde estão os maiores gargalos? -->
      <div class="card">
        <h3>Onde estão os maiores gargalos?</h3>
        <div class="small">Áreas ordenadas por volume de projetos em atraso.</div>
        <div style="margin-top: 10px;">
          <div v-for="b in bottleneckAreas" :key="b.area" style="margin: 8px 0;">
            <div style="display:flex; justify-content:space-between; font-size:0.82rem; margin-bottom:4px;">
              <span style="font-weight:700; color:var(--purple)">{{ b.area }}</span>
              <strong style="color:var(--red)">{{ b.delays }} projetos atrasados ({{ b.pct }}%)</strong>
            </div>
            <div class="track">
              <div class="fill red" :style="{ width: b.pct + '%' }"></div>
            </div>
          </div>
          <div v-if="bottleneckAreas.length === 0" style="text-align:center; padding:18px; color:var(--green)">
            ✔ Nenhum gargalo por atraso registrado no momento!
          </div>
        </div>
      </div>

      <!-- Execução de Atividades por Área -->
      <div class="card">
        <h3>Execução de Atividades por Área</h3>
        <div class="small">Taxa de conclusão de entregáveis e atividades por área requisitante.</div>
        <div style="margin-top: 10px; max-height:280px; overflow-y:auto;">
          <div v-for="ap in areaActivityProgress" :key="ap.area" style="margin: 8px 0;">
            <div style="display:flex; justify-content:space-between; font-size:0.82rem; margin-bottom:4px;">
              <span style="font-weight:700; color:var(--purple)">{{ ap.area }}</span>
              <strong>{{ ap.completed }}/{{ ap.total }} concluídas ({{ ap.pct }}%)</strong>
            </div>
            <div class="track">
              <div class="fill" :class="ap.fillClass" :style="{ width: ap.pct + '%' }"></div>
            </div>
          </div>
          <div v-if="areaActivityProgress.length === 0" style="text-align:center; padding:18px; color:var(--muted)">
            Nenhuma atividade vinculada a áreas no recorte.
          </div>
        </div>
      </div>
    </div>

    <!-- Distribuição por Status e Prioridade -->
    <div class="section grid2">
      <div class="card">
        <h3>Distribuição do Portfólio por Status</h3>
        <div class="small">Visão geral do andamento dos projetos.</div>
        <div style="margin-top: 10px;">
          <div v-for="item in statusDistribution" :key="item.status" style="margin: 8px 0;">
            <div style="display:flex; justify-content:space-between; font-size:0.82rem; margin-bottom:4px;">
              <span>{{ item.status }}</span>
              <strong>{{ item.count }} ({{ item.pct }}%)</strong>
            </div>
            <div class="track">
              <div class="fill" :class="item.colorClass" :style="{ width: item.pct + '%' }"></div>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <h3>Distribuição por Prioridade</h3>
        <div class="small">Classificação de importância estratégica das demandas.</div>
        <div style="margin-top: 10px;">
          <div v-for="item in priorityDistribution" :key="item.priority" style="margin: 8px 0;">
            <div style="display:flex; justify-content:space-between; font-size:0.82rem; margin-bottom:4px;">
              <span>{{ item.priority }}</span>
              <strong>{{ item.count }} ({{ item.pct }}%)</strong>
            </div>
            <div class="track">
              <div class="fill" :style="{ width: item.pct + '%', background: item.color }"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Cronograma Gantt de Projetos -->
    <div class="section" style="margin-top:14px;">
      <div class="title">Cronograma & Linha do Tempo do Portfólio (Gantt)</div>
      <div class="sub">Acompanhe a distribuição temporal, prazos e sobreposições dos projetos ativos.</div>
      <GanttChart :items="ganttProjects" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoadmapStore } from '@/stores/roadmap'
import GlobalFilters from '@/components/GlobalFilters.vue'
import GanttChart from '@/components/GanttChart.vue'

const roadmapStore = useRoadmapStore()

const ganttProjects = computed(() => {
  return roadmapStore.filteredProjects.map(p => ({
    id: p.id,
    code: `PROJ-${String(p.id).padStart(3, '0')}`,
    name: p.name,
    start_date: p.start_date,
    end_date: p.end_date,
    progress: p.progress,
    status: p.status
  }))
})

// Onde estão os maiores gargalos?
const bottleneckAreas = computed(() => {
  const map = {}
  const today = new Date()
  today.setHours(0, 0, 0, 0)

  let totalDelays = 0
  roadmapStore.filteredProjects.forEach(p => {
    const isDelayed = p.status !== 'Concluído' && p.end_date && new Date(p.end_date) < today
    if (isDelayed) {
      const area = p.area_name || 'Não Informada'
      map[area] = (map[area] || 0) + 1
      totalDelays++
    }
  })

  if (totalDelays === 0) return []

  return Object.keys(map).map(area => ({
    area,
    delays: map[area],
    pct: ((map[area] / totalDelays) * 100).toFixed(1)
  })).sort((a, b) => b.delays - a.delays)
})

const topBottleneckArea = computed(() => {
  return bottleneckAreas.value.length > 0 ? bottleneckAreas.value[0].area : 'Nenhuma'
})

// Execução de Atividades por Área
const areaActivityProgress = computed(() => {
  const map = {}
  // Mapear projeto por id para pegar area
  const projAreaMap = {}
  roadmapStore.filteredProjects.forEach(p => {
    projAreaMap[p.id] = p.area_name || 'Geral'
  })

  roadmapStore.filteredActivities.forEach(a => {
    const area = projAreaMap[a.project_id] || 'Geral'
    if (!map[area]) {
      map[area] = { area, total: 0, completed: 0 }
    }
    map[area].total++
    if (a.status === 'Concluído' || a.progress >= 100) {
      map[area].completed++
    }
  })

  return Object.values(map).map(item => {
    const pct = item.total > 0 ? ((item.completed / item.total) * 100).toFixed(0) : 0
    let fillClass = 'green'
    if (pct < 50) fillClass = 'red'
    else if (pct < 75) fillClass = 'yellow'

    return {
      ...item,
      pct,
      fillClass
    }
  }).sort((a, b) => b.total - a.total)
})

// Projeção de Ritmo & Capacidade
const capacityMetrics = computed(() => {
  const total = roadmapStore.filteredActivities.length
  const completed = roadmapStore.filteredActivities.filter(a => a.status === 'Concluído' || a.progress >= 100).length
  const pending = Math.max(0, total - completed)

  if (total === 0) {
    return {
      deliveryRate: '0.0',
      entryRate: '0.0',
      pressure: '0.0',
      monthsCapacity: '0.0',
      projectedDate: 'Sem pendências'
    }
  }

  // Médias estimadas por histórico de atividades no escopo filtrado
  const deliveryRate = completed > 0 ? Math.max(0.5, (completed / 2.5)).toFixed(1) : (total > 0 ? '1.0' : '0.0')
  const entryRate = (total / 3.0).toFixed(1)
  const pressure = (parseFloat(entryRate) - parseFloat(deliveryRate)).toFixed(1)
  
  const rateNum = parseFloat(deliveryRate)
  const monthsCapacity = rateNum > 0 ? (pending / rateNum).toFixed(1) : '—'

  let projectedDate = 'Sem pendências'
  if (pending > 0 && rateNum > 0) {
    const targetDate = new Date()
    targetDate.setDate(targetDate.getDate() + Math.ceil(parseFloat(monthsCapacity) * 30))
    projectedDate = targetDate.toLocaleDateString('pt-BR', { month: 'short', year: 'numeric' })
  }

  return {
    deliveryRate,
    entryRate,
    pressure,
    monthsCapacity,
    projectedDate
  }
})

const capacityNarrative = computed(() => {
  const c = capacityMetrics.value
  if (roadmapStore.filteredActivities.length === 0) {
    return 'Nenhuma atividade localizada no recorte de filtros selecionado.'
  }
  return `Ritmo histórico de entrega: ~${c.deliveryRate} tarefas/mês, com criação média de ~${c.entryRate} demandas/mês (saldo de pressão: ${c.pressure > 0 ? '+' : ''}${c.pressure} tarefas/mês). Capacidade estimada para conclusão das pendências: ${c.monthsCapacity} meses.`
})

// Distribuição de Status
const statusDistribution = computed(() => {
  const projs = roadmapStore.filteredProjects
  const total = projs.length || 1
  const map = {}
  projs.forEach(p => {
    map[p.status] = (map[p.status] || 0) + 1
  })
  const colorMap = {
    'Concluído': 'green',
    'Em Andamento': 'blue',
    'Não Iniciado': '',
    'Em Espera': 'yellow',
    'Cancelado': 'red'
  }
  return Object.keys(map).map(status => ({
    status,
    count: map[status],
    pct: ((map[status] / total) * 100).toFixed(0),
    colorClass: colorMap[status] || ''
  }))
})

// Distribuição de Prioridade
const priorityDistribution = computed(() => {
  const projs = roadmapStore.filteredProjects
  const total = projs.length || 1
  const map = {}
  projs.forEach(p => {
    map[p.priority] = (map[p.priority] || 0) + 1
  })
  const colorMap = {
    'Crítica': 'var(--red)',
    'Alta': 'var(--pink)',
    'Normal': 'var(--purple)',
    'Média': 'var(--yellow)',
    'Baixa': '#94A3B8',
    '🎯 Executivo': 'var(--purple2)'
  }
  return Object.keys(map).map(priority => ({
    priority,
    count: map[priority],
    pct: ((map[priority] / total) * 100).toFixed(0),
    color: colorMap[priority] || 'var(--purple)'
  }))
})
</script>
