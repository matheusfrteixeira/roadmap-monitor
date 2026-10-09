<template>
  <div>
    <div class="title">👥 Stakeholders & Gestão do Trabalho</div>
    <div class="sub">Visão consolidada do volume por Solicitantes, Owners condutores, Responsáveis Técnicos e Detalhamento por Projeto.</div>

    <GlobalFilters />

    <!-- Mini KPIs -->
    <div class="kpis" style="margin-top: 10px;">
      <div class="kpi primary">
        <div class="v">{{ requestersSummary.length }}</div>
        <div class="l">Solicitantes Ativos</div>
        <div class="n">Clientes / Solicitantes</div>
      </div>
      <div class="kpi">
        <div class="v" style="color:var(--purple2)">{{ ownersSummary.length }}</div>
        <div class="l">Owners de Projetos</div>
        <div class="n">Líderes de iniciativas</div>
      </div>
      <div class="kpi">
        <div class="v" style="color:var(--pink)">{{ assigneesSummary.length }}</div>
        <div class="l">Responsáveis Técnicos</div>
        <div class="n">Membros executores</div>
      </div>
      <div class="kpi">
        <div class="v" style="color:var(--green)">{{ roadmapStore.kpis.completedProjects }}</div>
        <div class="l">Projetos Concluídos</div>
        <div class="n">Entregas finalizadas</div>
      </div>
      <div class="kpi">
        <div class="v" style="color:var(--yellow)">{{ roadmapStore.kpis.totalProjects - roadmapStore.kpis.completedProjects }}</div>
        <div class="l">Projetos em Fila</div>
        <div class="n">Demandas abertas</div>
      </div>
    </div>

    <!-- GRID 1: SOLICITANTES & OWNERS -->
    <div class="section grid2" style="margin-top:14px;">
      <!-- 1. Visão por Solicitante -->
      <div class="card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <div>
            <h3>Visão por Solicitante</h3>
            <div class="small">Volume de projetos solicitados e taxa de entrega.</div>
          </div>
          <input
            v-model="requesterSearch"
            class="form-control"
            placeholder="Filtrar solicitante..."
            style="max-width:200px;"
          />
        </div>

        <div class="tw" style="max-height:360px;">
          <table>
            <thead>
              <tr>
                <th>Solicitante</th>
                <th style="text-align:center;">Projetos</th>
                <th style="text-align:center;">Concluídos</th>
                <th style="text-align:center;">Pendentes</th>
                <th style="text-align:center;">Taxa (%)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="r in filteredRequesters" :key="r.name">
                <td><strong style="color:var(--purple)">{{ r.name }}</strong></td>
                <td style="text-align:center;"><span class="badge bpurple">{{ r.total }}</span></td>
                <td style="text-align:center;"><span class="badge bgreen">{{ r.completed }}</span></td>
                <td style="text-align:center;"><span class="badge byellow">{{ r.pending }}</span></td>
                <td style="text-align:center;">
                  <div style="display:inline-flex; align-items:center; gap:5px;">
                    <div class="track" style="width:50px;">
                      <div class="fill green" :style="{ width: r.rate + '%' }"></div>
                    </div>
                    <span>{{ r.rate }}%</span>
                  </div>
                </td>
              </tr>
              <tr v-if="filteredRequesters.length === 0">
                <td colspan="5" style="text-align:center; padding:15px; color:var(--muted)">Nenhum solicitante localizado.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 2. Visão por Owner -->
      <div class="card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <div>
            <h3>Visão por Owner</h3>
            <div class="small">Carga de trabalho por Owner (líder do projeto).</div>
          </div>
          <input
            v-model="ownerSearch"
            class="form-control"
            placeholder="Filtrar owner..."
            style="max-width:170px; font-size:0.82rem; height:30px;"
          />
        </div>

        <div class="tw" style="max-height:360px;">
          <table>
            <thead>
              <tr>
                <th>Owner (Líder)</th>
                <th style="text-align:center;">Projetos</th>
                <th style="text-align:center;">Concluídos</th>
                <th style="text-align:center;">Pendentes</th>
                <th style="text-align:center;">Taxa (%)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="o in filteredOwners" :key="o.name">
                <td>
                  <div style="display:flex; align-items:center; gap:6px;">
                    <div class="brand-icon" style="width:24px; height:24px; font-size:0.76rem;">{{ o.name.charAt(0) }}</div>
                    <strong style="color:var(--purple)">{{ o.name }}</strong>
                  </div>
                </td>
                <td style="text-align:center;"><span class="badge bpurple">{{ o.total }}</span></td>
                <td style="text-align:center;"><span class="badge bgreen">{{ o.completed }}</span></td>
                <td style="text-align:center;"><span class="badge byellow">{{ o.pending }}</span></td>
                <td style="text-align:center;">
                  <div style="display:inline-flex; align-items:center; gap:5px;">
                    <div class="track" style="width:50px;">
                      <div class="fill green" :style="{ width: o.rate + '%' }"></div>
                    </div>
                    <span>{{ o.rate }}%</span>
                  </div>
                </td>
              </tr>
              <tr v-if="filteredOwners.length === 0">
                <td colspan="5" style="text-align:center; padding:15px; color:var(--muted)">Nenhum owner localizado.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- GRID 2: RESPONSÁVEIS TÉCNICOS & VISÃO POR PROJETO -->
    <div class="section grid2" style="margin-top:14px;">
      <!-- 3. Visão por Responsável Técnico -->
      <div class="card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <div>
            <h3>Visão por Responsável Técnico</h3>
            <div class="small">Carga de trabalho de atividades por membro técnico executor.</div>
          </div>
          <input
            v-model="assigneeSearch"
            class="form-control"
            placeholder="Filtrar responsável..."
            style="max-width:200px;"
          />
        </div>

        <div class="tw" style="max-height:360px;">
          <table>
            <thead>
              <tr>
                <th>Responsável Técnico</th>
                <th style="text-align:center;">Atividades</th>
                <th style="text-align:center;">Concluídas</th>
                <th style="text-align:center;">Pendentes</th>
                <th style="text-align:center;">Taxa (%)</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="s in filteredAssignees" :key="s.name">
                <td>
                  <div style="display:flex; align-items:center; gap:6px;">
                    <div class="brand-icon" style="width:24px; height:24px; font-size:0.76rem; background:var(--pink);">{{ s.name.charAt(0) }}</div>
                    <strong style="color:var(--purple)">{{ s.name }}</strong>
                  </div>
                </td>
                <td style="text-align:center;"><span class="badge bpurple">{{ s.total }}</span></td>
                <td style="text-align:center;"><span class="badge bgreen">{{ s.completed }}</span></td>
                <td style="text-align:center;"><span class="badge byellow">{{ s.pending }}</span></td>
                <td style="text-align:center;">
                  <div style="display:inline-flex; align-items:center; gap:5px;">
                    <div class="track" style="width:50px;">
                      <div class="fill green" :style="{ width: s.rate + '%' }"></div>
                    </div>
                    <span>{{ s.rate }}%</span>
                  </div>
                </td>
              </tr>
              <tr v-if="filteredAssignees.length === 0">
                <td colspan="5" style="text-align:center; padding:15px; color:var(--muted)">Nenhum responsável localizado.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 4. Visão por Projeto (com Entregáveis e Atividades) -->
      <div class="card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <div>
            <h3>Visão por Projeto</h3>
            <div class="small">Resumo quantitativo de entregáveis, atividades e atrasos.</div>
          </div>
          <input
            v-model="projectSearch"
            class="form-control"
            placeholder="Filtrar projeto..."
            style="max-width:170px; font-size:0.82rem; height:30px;"
          />
        </div>

        <div class="tw" style="max-height:360px;">
          <table>
            <thead>
              <tr>
                <th>Projeto</th>
                <th style="text-align:center;">Entregáveis</th>
                <th style="text-align:center;">Atividades</th>
                <th style="text-align:center;">% Conclusão</th>
                <th style="text-align:center;">Atrasado</th>
                <th style="text-align:center;">Status</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="p in filteredProjectsScope"
                :key="p.id"
                class="clickable-row"
                @click="$router.push(`/portfolio/projeto/${p.id}`)"
                :title="'Abrir detalhes do projeto ' + p.name"
              >
                <td>
                  <strong style="color:var(--purple)">{{ p.name }}</strong>
                </td>
                <td style="text-align:center;"><span class="badge bpurple">{{ p.deliverablesCount }}</span></td>
                <td style="text-align:center;">{{ p.activitiesCount }}</td>
                <td style="text-align:center;">
                  <div style="display:inline-flex; align-items:center; gap:5px;">
                    <div class="track" style="width:45px;">
                      <div class="fill green" :style="{ width: p.progress + '%' }"></div>
                    </div>
                    <span>{{ p.progress }}%</span>
                  </div>
                </td>
                <td style="text-align:center;">
                  <span v-if="p.isDelayed" class="badge bred">Sim</span>
                  <span v-else style="color:var(--muted)">Não</span>
                </td>
                <td style="text-align:center;">
                  <span class="badge" :class="p.status === 'Concluído' ? 'bgreen' : (p.status === 'Em Andamento' ? 'bpurple' : 'bgray')">
                    {{ p.status }}
                  </span>
                </td>
              </tr>
              <tr v-if="filteredProjectsScope.length === 0">
                <td colspan="6" style="text-align:center; padding:15px; color:var(--muted)">Nenhum projeto localizado.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoadmapStore } from '@/stores/roadmap'
import GlobalFilters from '@/components/GlobalFilters.vue'
import api from '@/services/api'

const roadmapStore = useRoadmapStore()
const usersList = ref([])

const requesterSearch = ref('')
const ownerSearch = ref('')
const assigneeSearch = ref('')
const projectSearch = ref('')

onMounted(async () => {
  try {
    const res = await api.get('/users/')
    usersList.value = res.data
  } catch (err) {
    console.error('Erro ao buscar usuários:', err)
  }
})

const userMap = computed(() => {
  const map = {}
  usersList.value.forEach(u => {
    map[u.id] = u.name
  })
  return map
})

// 1. Agrupamento por Solicitante
const requestersSummary = computed(() => {
  const map = {}
  roadmapStore.filteredProjects.forEach(p => {
    const req = (p.requester || '').trim() || 'Não Informado / Interno'
    if (!map[req]) {
      map[req] = { name: req, total: 0, completed: 0, pending: 0 }
    }
    map[req].total++
    if (p.status === 'Concluído' || p.progress >= 100) {
      map[req].completed++
    } else {
      map[req].pending++
    }
  })

  return Object.values(map).map(r => ({
    ...r,
    rate: r.total > 0 ? ((r.completed / r.total) * 100).toFixed(0) : 0
  })).sort((a, b) => b.total - a.total)
})

const filteredRequesters = computed(() => {
  if (!requesterSearch.value) return requestersSummary.value
  const s = requesterSearch.value.toLowerCase()
  return requestersSummary.value.filter(r => r.name.toLowerCase().includes(s))
})

// 2. Agrupamento por Owner
const ownersSummary = computed(() => {
  const map = {}
  roadmapStore.filteredProjects.forEach(p => {
    const ownerName = p.owner_name || (p.owner_id && userMap.value[p.owner_id]) || 'Não Definido'
    if (!map[ownerName]) {
      map[ownerName] = { name: ownerName, total: 0, completed: 0, pending: 0 }
    }
    map[ownerName].total++
    if (p.status === 'Concluído' || p.progress >= 100) {
      map[ownerName].completed++
    } else {
      map[ownerName].pending++
    }
  })

  return Object.values(map).map(o => ({
    ...o,
    rate: o.total > 0 ? ((o.completed / o.total) * 100).toFixed(0) : 0
  })).sort((a, b) => b.total - a.total)
})

const filteredOwners = computed(() => {
  if (!ownerSearch.value) return ownersSummary.value
  const s = ownerSearch.value.toLowerCase()
  return ownersSummary.value.filter(o => o.name.toLowerCase().includes(s))
})

// 3. Agrupamento por Responsável Técnico
const assigneesSummary = computed(() => {
  const map = {}
  roadmapStore.filteredActivities.forEach(a => {
    const name = a.assignee_name || (a.assignee_id && userMap.value[a.assignee_id]) || 'Não Atribuído'
    if (!map[name]) {
      map[name] = { name, total: 0, completed: 0, pending: 0 }
    }
    map[name].total++
    if (a.status === 'Concluído' || a.progress >= 100) {
      map[name].completed++
    } else {
      map[name].pending++
    }
  })

  return Object.values(map).map(item => ({
    ...item,
    rate: item.total > 0 ? ((item.completed / item.total) * 100).toFixed(0) : 0
  })).sort((a, b) => b.total - a.total)
})

const filteredAssignees = computed(() => {
  if (!assigneeSearch.value) return assigneesSummary.value
  const s = assigneeSearch.value.toLowerCase()
  return assigneesSummary.value.filter(a => a.name.toLowerCase().includes(s))
})

// 4. Visão por Projeto com Entregáveis e Atividades
const projectsScopeList = computed(() => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)

  return roadmapStore.filteredProjects.map(p => {
    const delivs = roadmapStore.filteredDeliverables.filter(d => d.project_id === p.id).length
    const ativs = roadmapStore.filteredActivities.filter(a => a.project_id === p.id).length
    const isDelayed = p.status !== 'Concluído' && p.end_date && new Date(p.end_date) < today

    return {
      id: p.id,
      name: p.name,
      deliverablesCount: delivs,
      activitiesCount: ativs,
      progress: p.progress || 0,
      isDelayed,
      status: p.status
    }
  })
})

const filteredProjectsScope = computed(() => {
  if (!projectSearch.value) return projectsScopeList.value
  const s = projectSearch.value.toLowerCase()
  return projectsScopeList.value.filter(p => p.name.toLowerCase().includes(s))
})
</script>
