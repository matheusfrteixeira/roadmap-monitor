<template>
  <div>
    <div class="title">Visão Executiva por Área</div>
    <div class="sub">Desempenho, volume, entregas e riscos de prazo segmentados por diretoria / área corporativa.</div>

    <GlobalFilters />

    <!-- 5 KPIs Executivos por Área -->
    <div class="kpis" style="margin-top:10px;">
      <div class="kpi primary">
        <div class="v">{{ topAreaInfo.name }}</div>
        <div class="l">Maior Portfólio</div>
        <div class="n">{{ topAreaInfo.total }} projetos ({{ topAreaInfo.pct }}%)</div>
      </div>
      <div class="kpi">
        <div class="v" :style="{ color: topDelayedArea.delayed > 0 ? 'var(--red)' : 'var(--green)' }">
          {{ topDelayedArea.delayed }}
        </div>
        <div class="l">Maior Volume Atrasado</div>
        <div class="n">{{ topDelayedArea.name }}</div>
      </div>
      <div class="kpi">
        <div class="v" style="color:var(--green)">
          {{ topCompletedArea.rate }}%
        </div>
        <div class="l">Maior Conclusão</div>
        <div class="n">{{ topCompletedArea.name }}</div>
      </div>
      <div class="kpi">
        <div class="v">{{ areasList.length }}</div>
        <div class="l">Áreas Ativas</div>
        <div class="n">Com demandas cadastradas</div>
      </div>
      <div class="kpi">
        <div class="v" :style="{ color: criticalAreasCount > 0 ? 'var(--red)' : 'var(--green)' }">
          {{ criticalAreasCount }}
        </div>
        <div class="l">Áreas Críticas</div>
        <div class="n">Com projetos em atraso</div>
      </div>
    </div>

    <!-- GRID COM PARETO DE VOLUME E TAXA DE ATRASO -->
    <div class="section grid2" style="margin-top:12px;">
      <!-- 1. Pareto de Volume por Área -->
      <div class="card">
        <h3>Pareto de Volume por Área</h3>
        <div class="small">Curva 80/20 demonstrando a concentração de projetos corporativos por área.</div>

        <div style="margin-top: 8px;">
          <!-- Cabeçalho do Pareto -->
          <div style="display:grid; grid-template-columns: 130px 1fr 40px 50px 50px; gap:8px; font-weight:700; font-size:0.78rem; color:var(--purple); padding-bottom:5px; border-bottom:1px solid var(--line);">
            <div>Área</div>
            <div>Volume de Projetos</div>
            <div style="text-align:right;">Qtd</div>
            <div style="text-align:right;">% Rel.</div>
            <div style="text-align:right;">% Acum.</div>
          </div>

          <!-- Linhas do Pareto -->
          <div
            v-for="item in paretoData"
            :key="item.area"
            style="display:grid; grid-template-columns: 130px 1fr 40px 50px 50px; gap:8px; align-items:center; padding:5px 0; border-bottom:1px solid #FAF8FC; font-size:0.82rem;"
          >
            <div style="font-weight:700; color:var(--purple); white-space:nowrap; overflow:hidden; text-overflow:ellipsis;" :title="item.area">
              {{ item.area }}
            </div>

            <!-- Barra combinada: Relativa (Fill) + Marcador Acumulado -->
            <div style="position:relative; height:10px; background:#F3EFF9; border-radius:5px; overflow:hidden;">
              <div
                style="height:100%; background:var(--purple); border-radius:5px; transition:width 0.3s;"
                :style="{ width: item.pctRel + '%' }"
                :title="'Volume relativo: ' + item.pctRel + '%'"
              ></div>
              <!-- Linha acumulada -->
              <div
                style="position:absolute; top:0; bottom:0; width:2px; background:var(--pink); z-index:2;"
                :style="{ left: item.pctCum + '%' }"
                :title="'Acumulado: ' + item.pctCum + '%'"
              ></div>
            </div>

            <div style="text-align:right; font-weight:700;">{{ item.total }}</div>
            <div style="text-align:right; color:var(--purple)">{{ item.pctRel }}%</div>
            <div style="text-align:right; font-weight:700; color:var(--pink)">{{ item.pctCum }}%</div>
          </div>

          <div v-if="paretoData.length === 0" style="text-align:center; padding:16px; color:var(--muted)">
            Nenhuma área com projetos no filtro atual.
          </div>
        </div>
      </div>

      <!-- 2. Taxa de Atraso por Área -->
      <div class="card">
        <h3>Taxa de Atraso por Área</h3>
        <div class="small">Concentração de prazos críticos e projetos atrasados.</div>

        <div style="margin-top: 8px;">
          <div v-for="item in delayedAreasList" :key="item.area" style="margin: 6px 0;">
            <div style="display:flex; justify-content:space-between; font-size:0.82rem; margin-bottom:3px;">
              <span style="font-weight:700; color:var(--purple)">{{ item.area }}</span>
              <strong style="color:var(--red)">{{ item.delayed }} atrasados ({{ item.delayedRate }}% dos atrasos)</strong>
            </div>
            <div class="track">
              <div class="fill red" :style="{ width: item.delayedRate + '%' }"></div>
            </div>
          </div>

          <div v-if="delayedAreasList.length === 0" style="text-align:center; padding:25px 10px; color:var(--green)">
            <div style="font-size:24px; margin-bottom:4px;">🎉</div>
            <strong>Parabéns!</strong> Nenhuma área possui projetos em atraso no momento.
          </div>
        </div>
      </div>
    </div>

    <!-- TABELA CONSOLIDADA POR ÁREA REQUISITANTE -->
    <div class="card" style="margin-top:10px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
        <div>
          <h3>Tabela Consolidada por Área Requisitante</h3>
          <div class="small">Visão geral do volume, execução e riscos de cada departamento.</div>
        </div>
        <input
          v-model="areaSearch"
          class="form-control"
          placeholder="Buscar área..."
          style="max-width:180px; font-size:0.82rem; height:32px;"
        />
      </div>

      <div class="tw">
        <table>
          <thead>
            <tr>
              <th>Área Requisitante</th>
              <th style="text-align:center;">Projetos</th>
              <th style="text-align:center;">Atividades</th>
              <th style="text-align:center;">Concluídas</th>
              <th style="text-align:center;">% Conclusão</th>
              <th style="text-align:center;">Próxima Entrega</th>
              <th style="text-align:center;">Dias p/ Entrega</th>
              <th style="text-align:center;">Atrasados</th>
              <th style="text-align:center;">Sinal Executivo</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="area in filteredAreasList"
              :key="area.area"
              class="clickable-row"
              :class="{ selected: selectedAreaFilter === area.area }"
              @click="toggleAreaFilter(area.area)"
              :title="'Clique para filtrar por ' + area.area"
            >
              <td>
                <strong style="color:var(--purple)">🏢 {{ area.area }}</strong>
              </td>
              <td style="text-align:center;"><span class="badge bpurple">{{ area.projetos }}</span></td>
              <td style="text-align:center;">{{ area.atividades }}</td>
              <td style="text-align:center;"><span class="badge bgreen">{{ area.concluidas }}</span></td>
              <td style="text-align:center;">
                <div style="display:inline-flex; align-items:center; gap:6px;">
                  <div class="track" style="width:60px;">
                    <div class="fill green" :style="{ width: area.completionRate + '%' }"></div>
                  </div>
                  <strong>{{ area.completionRate }}%</strong>
                </div>
              </td>
              <td style="text-align:center;">{{ area.nextDelivery }}</td>
              <td style="text-align:center;">
                <span v-if="area.minDays !== '—'" :style="{ color: area.minDays < 0 ? 'var(--red)' : 'inherit', fontWeight: '700' }">
                  {{ area.minDays }}d
                </span>
                <span v-else>—</span>
              </td>
              <td style="text-align:center;" :style="{ color: area.atrasados > 0 ? 'var(--red)' : 'inherit', fontWeight: '800' }">
                {{ area.atrasados }}
              </td>
              <td style="text-align:center;">
                <span class="badge" :class="area.signalClass">{{ area.signal }}</span>
              </td>
            </tr>
            <tr v-if="filteredAreasList.length === 0">
              <td colspan="9" style="text-align:center; padding:20px; color:var(--muted)">
                Nenhuma área localizada com o filtro informado.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoadmapStore } from '@/stores/roadmap'
import GlobalFilters from '@/components/GlobalFilters.vue'

const roadmapStore = useRoadmapStore()
const areaSearch = ref('')
const selectedAreaFilter = ref('')

function toggleAreaFilter(areaName) {
  if (selectedAreaFilter.value === areaName) {
    selectedAreaFilter.value = ''
    roadmapStore.filters.search = ''
  } else {
    selectedAreaFilter.value = areaName
    roadmapStore.filters.search = areaName
  }
}

// Mapeamento e Agrupamento Consolidado por Área
const areasList = computed(() => {
  const map = {}
  const today = new Date()
  today.setHours(0, 0, 0, 0)

  // Mapear projetos
  roadmapStore.filteredProjects.forEach(p => {
    const area = p.area_name || 'Geral'
    if (!map[area]) {
      map[area] = {
        area,
        projetos: 0,
        atividades: 0,
        concluidas: 0,
        atrasados: 0,
        nextDeliveryDate: null,
        minDays: 99999
      }
    }
    map[area].projetos++

    const isDelayed = p.status !== 'Concluído' && p.end_date && new Date(p.end_date) < today
    if (isDelayed) {
      map[area].atrasados++
    }

    if (p.end_date && p.status !== 'Concluído') {
      const dt = new Date(p.end_date)
      const diffDays = Math.ceil((dt - today) / (1000 * 60 * 60 * 24))
      if (diffDays < map[area].minDays) {
        map[area].minDays = diffDays
        map[area].nextDeliveryDate = dt
      }
    }
  })

  // Mapear atividades por área
  const projAreaMap = {}
  roadmapStore.filteredProjects.forEach(p => {
    projAreaMap[p.id] = p.area_name || 'Geral'
  })

  roadmapStore.filteredActivities.forEach(a => {
    const area = projAreaMap[a.project_id] || 'Geral'
    if (!map[area]) {
      map[area] = {
        area,
        projetos: 0,
        atividades: 0,
        concluidas: 0,
        atrasados: 0,
        nextDeliveryDate: null,
        minDays: 99999
      }
    }
    map[area].atividades++
    if (a.status === 'Concluído' || a.progress >= 100) {
      map[area].concluidas++
    }
  })

  return Object.values(map).map(a => {
    const completionRate = a.atividades > 0 ? ((a.concluidas / a.atividades) * 100).toFixed(0) : (a.projetos > 0 ? '0' : '0')
    let signalClass = 'bgreen'
    let signal = 'Sob controle'

    if (a.atrasados > 0) {
      signalClass = 'bred'
      signal = 'Prazo crítico'
    } else if (parseFloat(completionRate) < 50 && a.atividades > 0) {
      signalClass = 'byellow'
      signal = 'Baixa execução'
    }

    const nextDelivery = a.nextDeliveryDate ? a.nextDeliveryDate.toLocaleDateString('pt-BR') : '—'
    const minDays = a.minDays !== 99999 ? a.minDays : '—'

    return {
      ...a,
      completionRate,
      signalClass,
      signal,
      nextDelivery,
      minDays
    }
  }).sort((a, b) => b.projetos - a.projetos)
})

const filteredAreasList = computed(() => {
  if (!areaSearch.value) return areasList.value
  const s = areaSearch.value.toLowerCase()
  return areasList.value.filter(a => a.area.toLowerCase().includes(s))
})

// Pareto de Volume por Área
const paretoData = computed(() => {
  const list = [...areasList.value].sort((a, b) => b.projetos - a.projetos)
  const totalProjs = list.reduce((acc, item) => acc + item.projetos, 0) || 1
  let cum = 0

  return list.slice(0, 10).map(item => {
    cum += item.projetos
    const pctRel = ((item.projetos / totalProjs) * 100).toFixed(1)
    const pctCum = ((cum / totalProjs) * 100).toFixed(1)
    return {
      area: item.area,
      total: item.projetos,
      pctRel,
      pctCum
    }
  })
})

// Taxa de Atraso por Área
const delayedAreasList = computed(() => {
  const delayed = areasList.value.filter(a => a.atrasados > 0).sort((a, b) => b.atrasados - a.atrasados)
  const totalDelays = delayed.reduce((acc, a) => acc + a.atrasados, 0) || 1

  return delayed.map(item => ({
    area: item.area,
    delayed: item.atrasados,
    delayedRate: ((item.atrasados / totalDelays) * 100).toFixed(1)
  }))
})

// Top KPIs
const topAreaInfo = computed(() => {
  if (areasList.value.length === 0) return { name: '—', total: 0, pct: 0 }
  const top = areasList.value[0]
  const tot = areasList.value.reduce((acc, a) => acc + a.projetos, 0) || 1
  return {
    name: top.area,
    total: top.projetos,
    pct: ((top.projetos / tot) * 100).toFixed(0)
  }
})

const topDelayedArea = computed(() => {
  if (delayedAreasList.value.length === 0) return { name: 'Nenhuma', delayed: 0 }
  return {
    name: delayedAreasList.value[0].area,
    delayed: delayedAreasList.value[0].delayed
  }
})

const topCompletedArea = computed(() => {
  const sorted = [...areasList.value].filter(a => a.atividades > 0).sort((a, b) => b.completionRate - a.completionRate)
  if (sorted.length === 0) return { name: '—', rate: 0 }
  return {
    name: sorted[0].area,
    rate: sorted[0].completionRate
  }
})

const criticalAreasCount = computed(() => {
  return areasList.value.filter(a => a.atrasados > 0).length
})
</script>
