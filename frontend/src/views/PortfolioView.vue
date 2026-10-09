<template>
  <div>
    <div style="display:flex; justify-content:space-between; align-items:flex-end; gap:10px; flex-wrap:wrap;">
      <div>
        <div class="title">Portfólio Completo de Projetos</div>
        <div class="sub">
          Visão holística de demandas corporativas. Início, término e progresso sincronizados com as atividades.
        </div>
      </div>
      <Button
        label="Novo Projeto"
        icon="pi pi-plus"
        @click="openCreateModal"
      />
    </div>

    <!-- Filtros Globais Integrados -->
    <GlobalFilters />

    <div class="card" style="margin-top: 10px; padding: 14px;">
      <DataTable
        :value="roadmapStore.filteredProjects"
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
            <span style="font-weight:700; color:var(--purple); font-size:0.95rem;">
              Projetos no Portfólio ({{ roadmapStore.filteredProjects.length }})
            </span>
            <span class="p-input-icon-left">
              <InputText
                v-model="tableFilters['global'].value"
                placeholder="Filtrar projetos..."
                style="font-size:0.85rem; height:32px;"
              />
            </span>
          </div>
        </template>

        <template #empty>
          <div style="text-align:center; padding:30px; color:var(--muted)">
            Nenhum projeto encontrado para os filtros selecionados.
          </div>
        </template>

        <!-- ID -->
        <Column field="id" header="ID" sortable style="width: 90px;">
          <template #body="{ data }">
            <strong>PROJ-{{ String(data.id).padStart(3, '0') }}</strong>
          </template>
        </Column>

        <!-- Nome do Projeto -->
        <Column field="name" header="Nome do Projeto" sortable style="min-width: 220px;">
          <template #body="{ data }">
            <strong style="color:var(--purple); font-size:0.95rem; cursor:pointer;" @click="$router.push(`/projeto/${data.id}`)">
              {{ data.name }}
            </strong>
            <div v-if="data.comments" class="small" style="color:var(--muted); max-width:240px; overflow:hidden; text-overflow:ellipsis; margin-top:2px;">
              💬 {{ data.comments }}
            </div>
          </template>
        </Column>

        <!-- Área / Cliente -->
        <Column field="area_name" header="Área / Cliente" sortable style="width: 140px;">
          <template #body="{ data }">
            <Tag
              :value="'🏢 ' + (data.area_name || 'Geral')"
              severity="secondary"
              style="font-size:0.75rem;"
            />
          </template>
        </Column>

        <!-- Chamado / Ticket -->
        <Column field="ticket_number" header="Chamado" sortable style="width: 120px;">
          <template #body="{ data }">
            <Tag
              v-if="data.ticket_number"
              :value="data.ticket_number"
              severity="info"
              style="font-size:0.75rem;"
            />
            <span v-else class="small" style="color:var(--muted)">—</span>
          </template>
        </Column>

        <!-- Solicitante -->
        <Column field="requester" header="Solicitante" sortable style="width: 140px;">
          <template #body="{ data }">
            <span style="font-size:0.85rem;">{{ data.requester || '—' }}</span>
          </template>
        </Column>

        <!-- Owner -->
        <Column field="owner_name" header="Owner" sortable style="width: 150px;">
          <template #body="{ data }">
            <span style="font-size:0.85rem; font-weight:600;">👤 {{ data.owner_name || '—' }}</span>
          </template>
        </Column>

        <!-- Entregáveis / Atividades -->
        <Column header="Entregáveis / Ativ." style="width: 130px; text-align:center;">
          <template #body="{ data }">
            <div style="font-size:0.82rem;">
              <strong>{{ data.deliverables?.length || 0 }}</strong> ent. /
              <strong style="color:var(--pink)">{{ countActivities(data) }}</strong> ativ.
            </div>
          </template>
        </Column>

        <!-- Status -->
        <Column field="status" header="Status" sortable style="width: 130px;">
          <template #body="{ data }">
            <Tag
              :value="data.status"
              :severity="getStatusSeverity(data.status)"
              style="font-weight:700;"
            />
          </template>
        </Column>

        <!-- Período -->
        <Column header="Período" style="width: 160px;">
          <template #body="{ data }">
            <div style="font-size:0.78rem; line-height:1.3;">
              <div>Início: <strong>{{ formatDate(data.start_date) }}</strong></div>
              <div>Fim: <strong>{{ formatDate(data.end_date) }}</strong></div>
            </div>
          </template>
        </Column>

        <!-- Progresso -->
        <Column field="progress" header="Progresso" sortable style="width: 130px;">
          <template #body="{ data }">
            <div style="display:flex; align-items:center; gap:6px;">
              <ProgressBar
                :value="data.progress || 0"
                :showValue="false"
                style="height: 8px; flex: 1;"
              />
              <span style="font-weight:700; font-size:0.8rem; min-width:32px; text-align:right;">
                {{ data.progress || 0 }}%
              </span>
            </div>
          </template>
        </Column>

        <!-- Ações -->
        <Column header="Ação" style="width: 90px; text-align:center;">
          <template #body="{ data }">
            <Button
              icon="pi pi-arrow-right"
              severity="secondary"
              size="small"
              text
              title="Abrir Detalhes do Projeto"
              @click="$router.push(`/projeto/${data.id}`)"
            />
          </template>
        </Column>
      </DataTable>
    </div>

    <!-- DIALOG NOVO PROJETO (PrimeVue) -->
    <Dialog
      v-model:visible="showNewModal"
      modal
      header="Cadastrar Novo Projeto de Roadmap"
      :style="{ width: '560px' }"
    >
      <form @submit.prevent="handleCreateProject" style="display:flex; flex-direction:column; gap:12px; margin-top:8px;">
        <div class="form-group" style="margin-bottom:0;">
          <label style="font-size:0.85rem; font-weight:700; color:var(--muted); display:block; margin-bottom:4px;">Nome do Projeto *</label>
          <InputText v-model="newProject.name" required placeholder="ex: Implantação CRM" style="width:100%;" />
        </div>

        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
          <div class="form-group" style="margin-bottom:0;">
            <label style="font-size:0.85rem; font-weight:700; color:var(--muted); display:block; margin-bottom:4px;">Área / Cliente Corporativo *</label>
            <Select
              v-model="newProject.area_id"
              :options="areasList"
              optionLabel="name"
              optionValue="id"
              placeholder="Selecione a área"
              style="width:100%;"
            />
          </div>

          <div class="form-group" style="margin-bottom:0;">
            <label style="font-size:0.85rem; font-weight:700; color:var(--muted); display:block; margin-bottom:4px;">Número do Chamado / Solicitação</label>
            <InputText v-model="newProject.ticket_number" placeholder="ex: TCK-99482" style="width:100%;" />
          </div>
        </div>

        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
          <div class="form-group" style="margin-bottom:0;">
            <label style="font-size:0.85rem; font-weight:700; color:var(--muted); display:block; margin-bottom:4px;">Solicitante</label>
            <InputText v-model="newProject.requester" placeholder="ex: Maria Silva (Diretoria RH)" style="width:100%;" />
          </div>

          <div class="form-group" style="margin-bottom:0;">
            <label style="font-size:0.85rem; font-weight:700; color:var(--muted); display:block; margin-bottom:4px;">Owner (Líder do Projeto)</label>
            <Select
              v-model="newProject.owner_id"
              :options="usersList"
              optionLabel="name"
              optionValue="id"
              placeholder="Selecione o líder"
              style="width:100%;"
            />
          </div>
        </div>

        <div class="form-group" style="margin-bottom:0;">
          <label style="font-size:0.85rem; font-weight:700; color:var(--muted); display:block; margin-bottom:4px;">Prioridade</label>
          <Select
            v-model="newProject.priority"
            :options="priorityOptions"
            optionLabel="label"
            optionValue="value"
            style="width:100%;"
          />
        </div>

        <div class="form-group" style="margin-bottom:0;">
          <label style="font-size:0.85rem; font-weight:700; color:var(--muted); display:block; margin-bottom:4px;">Comentários / Observações</label>
          <Textarea
            v-model="newProject.comments"
            rows="3"
            placeholder="Descreva o objetivo macro, escopo ou comentários relevantes..."
            style="width:100%; resize:vertical;"
          />
        </div>

        <div style="background:var(--purple4); border:1px solid var(--line); border-radius:8px; padding:10px; font-size:0.84rem; color:var(--purple);">
          ℹ️ <strong>Datas e Progresso:</strong> Serão calculados de forma 100% automática a partir das atividades cadastradas neste projeto.
        </div>

        <div style="display:flex; justify-content:flex-end; gap:8px; margin-top:10px;">
          <Button label="Cancelar" severity="secondary" text @click="showNewModal = false" />
          <Button type="submit" label="Criar Projeto" icon="pi pi-check" :loading="saving" />
        </div>
      </form>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { FilterMatchMode } from '@primevue/core/api'
import { useToast } from 'primevue/usetoast'
import { useRoadmapStore } from '@/stores/roadmap'
import { useAuthStore } from '@/stores/auth'
import GlobalFilters from '@/components/GlobalFilters.vue'
import api from '@/services/api'

import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Select from 'primevue/select'
import Tag from 'primevue/tag'
import ProgressBar from 'primevue/progressbar'
import Dialog from 'primevue/dialog'
import Textarea from 'primevue/textarea'

const toast = useToast()
const roadmapStore = useRoadmapStore()
const authStore = useAuthStore()

const showNewModal = ref(false)
const saving = ref(false)
const areasList = ref([])
const usersList = ref([])

const tableFilters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS }
})

const priorityOptions = [
  { label: 'Crítica', value: 'Crítica' },
  { label: 'Alta', value: 'Alta' },
  { label: 'Normal', value: 'Normal' },
  { label: 'Média', value: 'Média' },
  { label: 'Baixa', value: 'Baixa' }
]

const newProject = ref({
  name: '',
  area_id: null,
  owner_id: null,
  ticket_number: '',
  requester: '',
  priority: 'Alta',
  comments: ''
})

onMounted(async () => {
  try {
    const [areasRes, usersRes] = await Promise.all([
      api.get('/areas/'),
      api.get('/users/')
    ])
    areasList.value = areasRes.data
    usersList.value = usersRes.data
    if (areasList.value.length > 0) newProject.value.area_id = areasList.value[0].id
    if (authStore.user?.id) newProject.value.owner_id = authStore.user.id
  } catch (err) {
    console.error('Erro ao carregar selects do projeto:', err)
  }
})

function openCreateModal() {
  newProject.value = {
    name: '',
    area_id: areasList.value[0]?.id || null,
    owner_id: authStore.user?.id || usersList.value[0]?.id || null,
    ticket_number: '',
    requester: '',
    priority: 'Alta',
    comments: ''
  }
  showNewModal.value = true
}

async function handleCreateProject() {
  if (!newProject.value.name.trim()) {
    toast.add({ severity: 'warn', summary: 'Atenção', detail: 'Informe o nome do projeto.', life: 3000 })
    return
  }
  saving.value = true
  try {
    const res = await api.post('/projects/', newProject.value)
    showNewModal.value = false
    await roadmapStore.fetchAll()
    toast.add({
      severity: 'success',
      summary: 'Projeto Criado',
      detail: `Projeto "${res.data.name}" criado com sucesso!`,
      life: 3500
    })
  } catch (err) {
    toast.add({
      severity: 'error',
      summary: 'Erro',
      detail: err.response?.data?.detail || 'Erro ao cadastrar projeto.',
      life: 4000
    })
  } finally {
    saving.value = false
  }
}

function countActivities(proj) {
  if (!proj.deliverables) return 0
  return proj.deliverables.reduce((sum, d) => sum + (d.activities?.length || 0), 0)
}

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
</script>
