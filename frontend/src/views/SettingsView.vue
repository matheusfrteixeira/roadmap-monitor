<template>
  <div>
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
      <div>
        <div class="title">⚙️ Painel de Configurações Administrativas</div>
        <div class="sub">Gerencie Áreas/Clientes corporativos, usuários, níveis de acesso e a cadeia de gestão hierárquica.</div>
      </div>
    </div>

    <!-- Abas de Navegação das Configurações -->
    <div style="display:flex; gap:8px; margin-top:10px;">
      <Button
        :label="'🏢 Áreas & Clientes (' + areas.length + ')'"
        :severity="activeTab === 'areas' ? 'primary' : 'secondary'"
        :outlined="activeTab !== 'areas'"
        size="small"
        @click="activeTab = 'areas'"
      />
      <Button
        :label="'👥 Usuários & Gestores (' + users.length + ')'"
        :severity="activeTab === 'users' ? 'primary' : 'secondary'"
        :outlined="activeTab !== 'users'"
        size="small"
        @click="activeTab = 'users'"
      />
    </div>

    <!-- ABA 1: ÁREAS & CLIENTES -->
    <div v-if="activeTab === 'areas'" class="card" style="margin-top:10px; padding:14px;">
      <DataTable
        :value="areas"
        v-model:filters="areaFilters"
        dataKey="id"
        paginator
        :rows="10"
        :rowsPerPageOptions="[5, 10, 20]"
        removableSort
        stripedRows
        class="p-datatable-sm"
      >
        <template #header>
          <div style="display:flex; justify-content:space-between; align-items:center; gap:10px; flex-wrap:wrap;">
            <div>
              <h3 style="margin:0 0 2px 0;">Cadastro de Áreas & Clientes</h3>
              <div class="small" style="color:var(--muted)">Clientes ou diretorias solicitantes de demandas.</div>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
              <InputText
                v-model="areaFilters['global'].value"
                placeholder="Buscar área..."
                style="font-size:0.85rem; height:32px;"
              />
              <Button
                label="Nova Área / Cliente"
                icon="pi pi-plus"
                size="small"
                @click="openNewAreaModal"
              />
            </div>
          </div>
        </template>

        <template #empty>
          <div style="text-align:center; padding:25px; color:var(--muted)">
            Nenhuma área/cliente cadastrada.
          </div>
        </template>

        <Column field="id" header="ID" sortable style="width: 80px;">
          <template #body="{ data }">
            <strong>#{{ data.id }}</strong>
          </template>
        </Column>

        <Column field="name" header="Nome da Área / Cliente" sortable>
          <template #body="{ data }">
            <strong style="color:var(--purple); font-size:0.95rem;">🏢 {{ data.name }}</strong>
          </template>
        </Column>

        <Column header="Ações" style="width: 140px; text-align:right;">
          <template #body="{ data }">
            <div style="display:flex; justify-content:flex-end; gap:6px;">
              <Button
                icon="pi pi-pencil"
                severity="secondary"
                size="small"
                text
                title="Editar Área"
                @click="openEditAreaModal(data)"
              />
              <Button
                icon="pi pi-trash"
                severity="danger"
                size="small"
                text
                title="Excluir Área"
                @click="confirmDeleteArea(data)"
              />
            </div>
          </template>
        </Column>
      </DataTable>
    </div>

    <!-- ABA 2: USUÁRIOS & HIERARQUIA -->
    <div v-if="activeTab === 'users'" class="card" style="margin-top:10px; padding:14px;">
      <DataTable
        :value="users"
        v-model:filters="userFilters"
        dataKey="id"
        paginator
        :rows="10"
        :rowsPerPageOptions="[5, 10, 20]"
        removableSort
        stripedRows
        class="p-datatable-sm"
      >
        <template #header>
          <div style="display:flex; justify-content:space-between; align-items:center; gap:10px; flex-wrap:wrap;">
            <div>
              <h3 style="margin:0 0 2px 0;">Usuários, Cargos & Gestor Imediato</h3>
              <div class="small" style="color:var(--muted)">Configuração de permissões de acesso e estrutura de gestão.</div>
            </div>
            <div style="display:flex; align-items:center; gap:8px;">
              <InputText
                v-model="userFilters['global'].value"
                placeholder="Buscar usuário..."
                style="font-size:0.85rem; height:32px;"
              />
              <Button
                label="Novo Usuário"
                icon="pi pi-user-plus"
                size="small"
                @click="openNewUserModal"
              />
            </div>
          </div>
        </template>

        <template #empty>
          <div style="text-align:center; padding:25px; color:var(--muted)">
            Nenhum usuário cadastrado.
          </div>
        </template>

        <Column field="id" header="ID" sortable style="width: 80px;">
          <template #body="{ data }">
            <strong>#{{ data.id }}</strong>
          </template>
        </Column>

        <Column field="name" header="Nome" sortable>
          <template #body="{ data }">
            <strong style="color:var(--purple); font-size:0.95rem;">👤 {{ data.name }}</strong>
          </template>
        </Column>

        <Column field="email" header="Email" sortable />

        <Column field="role" header="Cargo / Nível" sortable style="width: 160px;">
          <template #body="{ data }">
            <Tag
              :value="getRoleLabel(data.role)"
              :severity="getRoleSeverity(data.role)"
              style="font-weight:700;"
            />
          </template>
        </Column>

        <Column field="manager_name" header="Gestor Imediato" sortable style="width: 200px;">
          <template #body="{ data }">
            <span v-if="data.manager_name" class="badge bpurple">
              👤 {{ data.manager_name }}
            </span>
            <span v-else class="small" style="color:var(--muted)">
              — Sem gestor direto
            </span>
          </template>
        </Column>

        <Column header="Ações" style="width: 90px; text-align:right;">
          <template #body="{ data }">
            <Button
              icon="pi pi-pencil"
              severity="secondary"
              size="small"
              text
              title="Editar Usuário"
              @click="openEditUserModal(data)"
            />
          </template>
        </Column>
      </DataTable>
    </div>

    <!-- DIALOG ÁREA / CLIENTE (PrimeVue) -->
    <Dialog
      v-model:visible="showAreaModal"
      modal
      :header="editingAreaId ? 'Editar Área / Cliente' : 'Nova Área / Cliente'"
      :style="{ width: '450px' }"
    >
      <div style="display:flex; flex-direction:column; gap:12px; margin-top:8px;">
        <div class="form-group" style="margin-bottom:0;">
          <label style="font-size:0.85rem; font-weight:700; color:var(--muted); display:block; margin-bottom:4px;">
            Nome da Área / Cliente *
          </label>
          <InputText
            v-model="areaFormName"
            placeholder="Ex: Recursos Humanos, Financeiro, Operações..."
            style="width:100%;"
            @keyup.enter="saveArea"
          />
        </div>
      </div>
      <template #footer>
        <Button label="Cancelar" severity="secondary" text @click="showAreaModal = false" />
        <Button label="Salvar Área" icon="pi pi-check" @click="saveArea" />
      </template>
    </Dialog>

    <!-- DIALOG USUÁRIO (PrimeVue) -->
    <Dialog
      v-model:visible="showUserModal"
      modal
      :header="editingUserId ? 'Editar Usuário' : 'Novo Usuário'"
      :style="{ width: '500px' }"
    >
      <div style="display:flex; flex-direction:column; gap:12px; margin-top:8px;">
        <div class="form-group" style="margin-bottom:0;">
          <label style="font-size:0.85rem; font-weight:700; color:var(--muted); display:block; margin-bottom:4px;">Nome Completo *</label>
          <InputText v-model="userForm.name" placeholder="Ex: João da Silva" style="width:100%;" />
        </div>

        <div class="form-group" style="margin-bottom:0;">
          <label style="font-size:0.85rem; font-weight:700; color:var(--muted); display:block; margin-bottom:4px;">Email Corporativo *</label>
          <InputText v-model="userForm.email" type="email" placeholder="joao@empresa.com" style="width:100%;" />
        </div>

        <div class="form-group" style="margin-bottom:0;">
          <label style="font-size:0.85rem; font-weight:700; color:var(--muted); display:block; margin-bottom:4px;">
            {{ editingUserId ? 'Nova Senha (deixe em branco para manter a atual)' : 'Senha de Acesso *' }}
          </label>
          <InputText v-model="userForm.password" type="password" placeholder="••••••••" style="width:100%;" />
        </div>

        <div class="form-group" style="margin-bottom:0;">
          <label style="font-size:0.85rem; font-weight:700; color:var(--muted); display:block; margin-bottom:4px;">Perfil de Acesso *</label>
          <Select
            v-model="userForm.role"
            :options="roleOptions"
            optionLabel="label"
            optionValue="value"
            style="width:100%;"
          />
        </div>

        <div class="form-group" style="margin-bottom:0;">
          <label style="font-size:0.85rem; font-weight:700; color:var(--muted); display:block; margin-bottom:4px;">Gestor Imediato Responsável</label>
          <Select
            v-model="userForm.manager_id"
            :options="managerSelectOptions"
            optionLabel="name"
            optionValue="id"
            placeholder="Nenhum (Sem gestor direto)"
            showClear
            style="width:100%;"
          />
        </div>
      </div>
      <template #footer>
        <Button label="Cancelar" severity="secondary" text @click="showUserModal = false" />
        <Button label="Salvar Usuário" icon="pi pi-check" @click="saveUser" />
      </template>
    </Dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { FilterMatchMode } from '@primevue/core/api'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import api from '@/services/api'

import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import InputText from 'primevue/inputtext'
import Select from 'primevue/select'
import Tag from 'primevue/tag'
import Dialog from 'primevue/dialog'

const toast = useToast()
const confirm = useConfirm()

const activeTab = ref('areas')
const areas = ref([])
const users = ref([])

const areaFilters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS }
})

const userFilters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS }
})

// Area Modal
const showAreaModal = ref(false)
const editingAreaId = ref(null)
const areaFormName = ref('')

// User Modal
const showUserModal = ref(false)
const editingUserId = ref(null)
const userForm = ref({
  name: '',
  email: '',
  role: 'analista',
  manager_id: null,
  password: ''
})

const roleOptions = [
  { label: 'Analista (Acesso operacional básico)', value: 'analista' },
  { label: 'Gestor (Acesso a seus subordinados)', value: 'gestor' },
  { label: 'Administrador (Acesso global)', value: 'admin' }
]

const managerSelectOptions = computed(() => {
  return users.value.filter(u => u.id !== editingUserId.value)
})

onMounted(async () => {
  await loadData()
})

async function loadData() {
  try {
    const [areasRes, usersRes] = await Promise.all([
      api.get('/areas/'),
      api.get('/users/')
    ])
    areas.value = areasRes.data
    users.value = usersRes.data
  } catch (err) {
    console.error('Erro ao carregar configurações:', err)
  }
}

function openNewAreaModal() {
  editingAreaId.value = null
  areaFormName.value = ''
  showAreaModal.value = true
}

function openEditAreaModal(area) {
  editingAreaId.value = area.id
  areaFormName.value = area.name
  showAreaModal.value = true
}

async function saveArea() {
  if (!areaFormName.value.trim()) {
    toast.add({ severity: 'warn', summary: 'Atenção', detail: 'Informe o nome da área.', life: 3000 })
    return
  }
  try {
    if (editingAreaId.value) {
      await api.put(`/areas/${editingAreaId.value}`, { name: areaFormName.value })
      toast.add({ severity: 'success', summary: 'Sucesso', detail: 'Área atualizada com sucesso!', life: 3000 })
    } else {
      await api.post('/areas/', { name: areaFormName.value })
      toast.add({ severity: 'success', summary: 'Sucesso', detail: 'Área cadastrada com sucesso!', life: 3000 })
    }
    showAreaModal.value = false
    await loadData()
  } catch (err) {
    toast.add({ severity: 'error', summary: 'Erro', detail: err.response?.data?.detail || 'Erro ao salvar Área.', life: 4000 })
  }
}

function confirmDeleteArea(area) {
  confirm.require({
    message: `Deseja realmente excluir a área "${area.name}"?`,
    header: 'Confirmação de Exclusão',
    icon: 'pi pi-exclamation-triangle',
    acceptLabel: 'Sim, excluir',
    rejectLabel: 'Cancelar',
    acceptClass: 'p-button-danger',
    accept: async () => {
      try {
        await api.delete(`/areas/${area.id}`)
        toast.add({ severity: 'success', summary: 'Sucesso', detail: 'Área excluída com sucesso!', life: 3000 })
        await loadData()
      } catch (err) {
        toast.add({ severity: 'error', summary: 'Erro', detail: err.response?.data?.detail || 'Erro ao excluir Área.', life: 4000 })
      }
    }
  })
}

function openNewUserModal() {
  editingUserId.value = null
  userForm.value = {
    name: '',
    email: '',
    role: 'analista',
    manager_id: null,
    password: ''
  }
  showUserModal.value = true
}

function openEditUserModal(u) {
  editingUserId.value = u.id
  userForm.value = {
    name: u.name,
    email: u.email,
    role: u.role,
    manager_id: u.manager_id,
    password: ''
  }
  showUserModal.value = true
}

async function saveUser() {
  if (!userForm.value.name.trim() || !userForm.value.email.trim()) {
    toast.add({ severity: 'warn', summary: 'Atenção', detail: 'Preencha nome e email.', life: 3000 })
    return
  }
  if (!editingUserId.value && !userForm.value.password) {
    toast.add({ severity: 'warn', summary: 'Atenção', detail: 'Defina uma senha para o novo usuário.', life: 3000 })
    return
  }
  try {
    if (editingUserId.value) {
      await api.put(`/users/${editingUserId.value}`, userForm.value)
      toast.add({ severity: 'success', summary: 'Sucesso', detail: 'Usuário atualizado com sucesso!', life: 3000 })
    } else {
      await api.post('/users/', userForm.value)
      toast.add({ severity: 'success', summary: 'Sucesso', detail: 'Usuário cadastrado com sucesso!', life: 3000 })
    }
    showUserModal.value = false
    await loadData()
  } catch (err) {
    toast.add({ severity: 'error', summary: 'Erro', detail: err.response?.data?.detail || 'Erro ao salvar Usuário.', life: 4000 })
  }
}

function getRoleLabel(role) {
  const map = { admin: 'Administrador', gestor: 'Gestor', analista: 'Analista' }
  return map[role] || role
}

function getRoleSeverity(role) {
  if (role === 'admin') return 'danger'
  if (role === 'gestor') return 'primary'
  return 'success'
}
</script>
