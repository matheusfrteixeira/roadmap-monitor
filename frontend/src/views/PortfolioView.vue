<template>
  <div>
    <div style="display:flex; justify-content:space-between; align-items:flex-end; gap:10px;">
      <div>
        <div class="title">Portfólio Completo de Projetos</div>
        <div class="sub">
          Visão holística de demandas. O início, término e progresso do projeto são sincronizados automaticamente com as atividades.
        </div>
      </div>
      <button class="btn" @click="openCreateModal">
        + Novo Projeto
      </button>
    </div>

    <!-- Filtros -->
    <GlobalFilters />

    <div class="card" style="margin-top: 10px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
        <span class="small">Exibindo <strong>{{ roadmapStore.filteredProjects.length }}</strong> projetos</span>
      </div>

      <div class="tw">
        <table>
          <thead>
            <tr>
              <th style="width: 80px;">ID</th>
              <th>Nome do Projeto</th>
              <th>Área / Cliente</th>
              <th>Chamado / Solicit.</th>
              <th>Solicitante</th>
              <th>Owner (Líder)</th>
              <th style="text-align:center;">Entregáveis / Ativ.</th>
              <th>Status</th>
              <th>Período Automático</th>
              <th>Progresso</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="proj in roadmapStore.filteredProjects"
              :key="proj.id"
              class="clickable-row"
              @click="$router.push(`/projeto/${proj.id}`)"
            >
              <td><strong>PROJ-{{ String(proj.id).padStart(3, '0') }}</strong></td>
              <td>
                <strong style="color: var(--purple)">{{ proj.name }}</strong>
                <div v-if="proj.comments" class="small" style="color:var(--muted); max-width:220px; overflow:hidden; text-overflow:ellipsis;">
                  💬 {{ proj.comments }}
                </div>
              </td>
              <td>
                <span class="badge bpurple">
                  🏢 {{ proj.area_name || 'Geral' }}
                </span>
              </td>
              <td>
                <span v-if="proj.ticket_number" class="badge bgray">
                  🎫 {{ proj.ticket_number }}
                </span>
                <span v-else class="small" style="color:var(--muted)">—</span>
              </td>
              <td>{{ proj.requester || '—' }}</td>
              <td>
                <span v-if="proj.owner_name">👤 {{ proj.owner_name }}</span>
                <span v-else class="small" style="color:var(--muted)">—</span>
              </td>
              <td style="text-align:center;">
                <div style="display:flex; flex-direction:column; align-items:center; gap:4px;">
                  <div style="display:inline-flex; align-items:center; gap:4px; flex-wrap:wrap; justify-content:center;">
                    <span v-if="proj.total_deliverables > 0" class="badge bpurple">
                      {{ proj.total_deliverables }} ent.
                    </span>
                    <span class="badge" :class="proj.total_activities > 0 ? 'bpink' : 'bgray'">
                      {{ proj.completed_activities || 0 }}/{{ proj.total_activities || 0 }} ativ.
                    </span>
                  </div>
                  <!-- Indicador de Atividades Atrasadas -->
                  <span
                    v-if="getProjectDelayedActivities(proj) > 0"
                    class="badge bred"
                    style="font-weight:800;"
                    title="Quantidade de atividades atrasadas neste projeto"
                  >
                    ⚠️ {{ getProjectDelayedActivities(proj) }} ativ. atrasada(s)
                  </span>
                </div>
              </td>
              <td>
                <span class="badge" :class="getStatusClass(proj.status)">
                  {{ proj.status }}
                </span>
              </td>
              <td>
                <span :style="{ color: isOverdue(proj) ? 'var(--red)' : 'inherit', fontWeight: isOverdue(proj) ? 'bold' : 'normal' }">
                  {{ formatDate(proj.start_date) }} → {{ formatDate(proj.end_date) }}
                  <span v-if="isOverdue(proj)" class="badge bred" style="margin-left:4px;">Atrasado</span>
                </span>
              </td>
              <td style="min-width: 110px;">
                <div style="display:flex; align-items:center; gap:6px;">
                  <div class="track" style="flex:1;">
                    <div class="fill" :style="{ width: (proj.progress || 0) + '%' }"></div>
                  </div>
                  <span style="font-weight:700;">{{ (proj.progress || 0) }}%</span>
                </div>
              </td>
              <td>
                <button class="btn secondary" style="padding:4px 9px;">
                  Abrir →
                </button>
              </td>
            </tr>
            <tr v-if="roadmapStore.filteredProjects.length === 0">
              <td colspan="11" style="text-align:center; padding: 25px; color: var(--muted)">
                Nenhum projeto encontrado com os filtros atuais.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal Novo Projeto -->
    <div v-if="showNewModal" class="modal-backdrop" @click.self="showNewModal = false">
      <div class="modal-content" style="max-width:560px;">
        <div class="modal-header">
          <h2>Cadastrar Novo Projeto de Roadmap</h2>
          <button class="modal-close" @click="showNewModal = false">×</button>
        </div>
        <form @submit.prevent="handleCreateProject">
          <div class="form-group">
            <label>Nome do Projeto *</label>
            <input v-model="newProject.name" required class="form-control" placeholder="ex: Implantação CRM" />
          </div>

          <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
            <div class="form-group">
              <label>Área / Cliente Corporativo *</label>
              <select v-model="newProject.area_id" class="form-control">
                <option v-for="area in areasList" :key="area.id" :value="area.id">
                  {{ area.name }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label>Número do Chamado / Solicitação (Se houver)</label>
              <input v-model="newProject.ticket_number" class="form-control" placeholder="ex: TCK-99482 ou JIRA-120" />
            </div>
          </div>

          <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
            <div class="form-group">
              <label>Solicitante (Preenchimento manual)</label>
              <input v-model="newProject.requester" class="form-control" placeholder="ex: Maria Silva (Diretoria RH)" />
            </div>

            <div class="form-group">
              <label>Owner (Líder que conduzirá o projeto)</label>
              <select v-model="newProject.owner_id" class="form-control">
                <option v-for="u in usersList" :key="u.id" :value="u.id">
                  {{ u.name }}
                </option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label>Prioridade</label>
            <select v-model="newProject.priority" class="form-control">
              <option value="Crítica">Crítica</option>
              <option value="Alta">Alta</option>
              <option value="Normal">Normal</option>
              <option value="Média">Média</option>
              <option value="Baixa">Baixa</option>
            </select>
          </div>

          <div class="form-group">
            <label>Comentários / Observações do Projeto</label>
            <textarea
              v-model="newProject.comments"
              class="form-control"
              placeholder="Descreva o objetivo macro, escopo ou comentários relevantes deste projeto..."
            ></textarea>
          </div>

          <div class="callout" style="margin-top:8px;">
            ℹ️ <strong>Datas e Progresso:</strong> Serão calculados de forma 100% automática a partir das atividades inseridas neste projeto.
          </div>

          <div style="display:flex; justify-content:flex-end; gap:8px; margin-top:14px;">
            <button type="button" class="btn secondary" @click="showNewModal = false">Cancelar</button>
            <button type="submit" class="btn" :disabled="saving">
              {{ saving ? 'Salvando...' : 'Criar Projeto' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoadmapStore } from '@/stores/roadmap'
import { useAuthStore } from '@/stores/auth'
import GlobalFilters from '@/components/GlobalFilters.vue'
import api from '@/services/api'

const roadmapStore = useRoadmapStore()
const authStore = useAuthStore()

const showNewModal = ref(false)
const saving = ref(false)
const areasList = ref([])
const usersList = ref([])

const newProject = ref({
  name: '',
  priority: 'Normal',
  status: 'Não Iniciado',
  area_id: 1,
  owner_id: 1,
  ticket_number: '',
  requester: '',
  comments: ''
})

onMounted(async () => {
  await loadLookups()
})

async function loadLookups() {
  try {
    const [areasRes, usersRes] = await Promise.all([
      api.get('/areas/'),
      api.get('/users/')
    ])
    areasList.value = areasRes.data
    usersList.value = usersRes.data
    if (areasList.value.length > 0) newProject.value.area_id = areasList.value[0].id
    if (usersList.value.length > 0) newProject.value.owner_id = usersList.value[0].id
  } catch (err) {
    console.error('Erro ao carregar lookups:', err)
  }
}

function openCreateModal() {
  newProject.value.name = ''
  newProject.value.ticket_number = ''
  newProject.value.requester = ''
  newProject.value.comments = ''
  showNewModal.value = true
}

function formatDate(d) {
  if (!d) return '—'
  return new Date(d + 'T00:00:00').toLocaleDateString('pt-BR')
}

function isOverdue(proj) {
  if (!proj.end_date || proj.status === 'Concluído') return false
  const today = new Date()
  today.setHours(0,0,0,0)
  return new Date(proj.end_date + 'T00:00:00') < today
}

function getProjectDelayedActivities(proj) {
  if (proj.delayed_activities !== undefined && proj.delayed_activities !== null) {
    return proj.delayed_activities
  }
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return roadmapStore.activities.filter(a => {
    return a.project_id === proj.id && a.status !== 'Concluído' && (a.progress === null || a.progress < 100) && a.end_date && new Date(a.end_date + 'T00:00:00') < today
  }).length
}

function getStatusClass(s) {
  if (s === 'Concluído') return 'bgreen'
  if (s === 'Em Andamento') return 'bpurple'
  if (s === 'Em Espera') return 'byellow'
  return 'bgray'
}

async function handleCreateProject() {
  saving.value = true
  try {
    await roadmapStore.createProject(newProject.value)
    showNewModal.value = false
    await roadmapStore.fetchAll()
  } catch (err) {
    alert(err.response?.data?.detail || 'Erro ao criar projeto.')
  } finally {
    saving.value = false
  }
}
</script>
