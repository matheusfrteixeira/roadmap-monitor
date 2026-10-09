<template>
  <div>
    <div class="title">📈 Evolução & Tendências do Portfólio</div>
    <div class="sub">Comparativo mensal do ritmo de execução, novas demandas geradas e histórico de conclusão.</div>

    <GlobalFilters />

    <div class="kpis" style="margin-top: 10px;">
      <div class="kpi primary">
        <div class="v">{{ roadmapStore.kpis.totalProjects }}</div>
        <div class="l">Total de Demandas</div>
        <div class="n">Volume acumulado</div>
      </div>
      <div class="kpi">
        <div class="v" style="color:var(--green)">{{ roadmapStore.kpis.completedProjects }}</div>
        <div class="l">Entregas Concluídas</div>
        <div class="n">Projetos finalizados</div>
      </div>
      <div class="kpi">
        <div class="v" style="color:var(--yellow)">
          {{ roadmapStore.kpis.totalProjects - roadmapStore.kpis.completedProjects }}
        </div>
        <div class="l">Demandas em Aberto</div>
        <div class="n">Work in progress</div>
      </div>
      <div class="kpi">
        <div class="v" style="color:var(--pink)">{{ roadmapStore.kpis.totalTrackedHours }}h</div>
        <div class="l">Horas Investidas</div>
        <div class="n">Registradas no Timetracker</div>
      </div>
    </div>

    <!-- Comparativo Mensal -->
    <div class="card" style="margin-top: 12px;">
      <h3>Ritmo de Execução Mensal (Criadas vs Concluídas)</h3>
      <div class="small">Acompanhamento do saldo de entregas mês a mês.</div>

      <div class="tw" style="margin-top: 10px;">
        <table>
          <thead>
            <tr>
              <th>Mês / Ano</th>
              <th>Demandas Criadas</th>
              <th>Demandas Concluídas</th>
              <th>Taxa de Vazão (%)</th>
              <th>Tendência de Capacidade</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="m in monthlyTrends" :key="m.monthKey">
              <td><strong style="color:var(--purple)">{{ m.monthLabel }}</strong></td>
              <td><span class="badge bpurple">{{ m.created }}</span></td>
              <td><span class="badge bgreen">{{ m.completed }}</span></td>
              <td>
                <div style="display:flex; align-items:center; gap:6px;">
                  <div class="track" style="width:70px;">
                    <div class="fill green" :style="{ width: m.rate + '%' }"></div>
                  </div>
                  <span>{{ m.rate }}%</span>
                </div>
              </td>
              <td>
                <span v-if="m.completed >= m.created" class="badge bgreen">
                  ▲ Capacidade Positiva
                </span>
                <span v-else class="badge byellow">
                  ▼ Acúmulo de Carteira
                </span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Diagnósticos e Projeções -->
    <div class="section grid2">
      <div class="card">
        <h3>Diagnóstico de Capacidade</h3>
        <div class="callout warning">
          <strong>Pressão na Carteira de Projetos:</strong><br>
          A relação atual de demandas em andamento versus a capacidade média de entregas indica uma taxa de conclusão de 
          <strong>{{ roadmapStore.kpis.concProjPct }}%</strong>.
          Mantenha a priorização alinhada com os owners para evitar gargalos de prazo.
        </div>
      </div>

      <div class="card">
        <h3>Recomendações Estratégicas</h3>
        <div class="callout">
          <strong>Ações de Mitigação de Prazo:</strong><br>
          1. Reavaliar projetos com prazo vencido e replanejar dependências.<br>
          2. Utilizar o <strong>Timetracker</strong> para identificar entregáveis com desvio de esforço real vs planejado.<br>
          3. Nivelar a alocação de responsáveis técnicos nas áreas com maior carteira.
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoadmapStore } from '@/stores/roadmap'
import GlobalFilters from '@/components/GlobalFilters.vue'

const roadmapStore = useRoadmapStore()

const monthlyTrends = computed(() => {
  const map = {}
  const now = new Date()

  // Inicializa últimos 6 meses
  for (let i = 5; i >= 0; i--) {
    const d = new Date(now.getFullYear(), now.getMonth() - i, 1)
    const key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`
    const label = d.toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' })
    map[key] = {
      monthKey: key,
      monthLabel: label.charAt(0).toUpperCase() + label.slice(1),
      created: 0,
      completed: 0
    }
  }

  // Agrupa projetos
  roadmapStore.filteredProjects.forEach(p => {
    if (p.start_date) {
      const startKey = p.start_date.substring(0, 7)
      if (map[startKey]) map[startKey].created++
    }
    if (p.end_date && (p.status === 'Concluído' || p.progress >= 100)) {
      const endKey = p.end_date.substring(0, 7)
      if (map[endKey]) map[endKey].completed++
    }
  })

  return Object.values(map).map(m => ({
    ...m,
    rate: m.created > 0 ? Math.min(100, Math.round((m.completed / m.created) * 100)) : (m.completed > 0 ? 100 : 0)
  }))
})
</script>

