<template>
  <div>
    <div style="display:flex; justify-content:space-between; align-items:center;">
      <div>
        <div class="title">⚙️ Painel de Configurações Administrativas</div>
        <div class="sub">Gerencie Áreas/Clientes corporativos, usuários, níveis de acesso e a cadeia de gestão hierárquica.</div>
      </div>
    </div>

    <!-- Abas de Navegação das Configurações -->
    <div style="display:flex; gap:8px; margin-top:10px;">
      <button
        class="btn"
        :class="activeTab === 'areas' ? '' : 'secondary'"
        @click="activeTab = 'areas'"
      >
        🏢 Áreas & Clientes ({{ areas.length }})
      </button>
      <button
        class="btn"
        :class="activeTab === 'users' ? '' : 'secondary'"
        @click="activeTab = 'users'"
      >
        👥 Usuários & Gestores ({{ users.length }})
      </button>
    </div>

    <!-- ABA 1: ÁREAS & CLIENTES -->
    <div v-if="activeTab === 'areas'" class="card" style="margin-top:10px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
        <div>
          <h3>Cadastro de Áreas & Clientes</h3>
          <div class="small">Cadastre os clientes ou diretorias que solicitam demandas (ex: RH - DHO, Operações, Cliente XPTO).</div>
        </div>
        <button class="btn" @click="openNewAreaModal">+ Nova Área / Cliente</button>
      </div>

      <div class="tw">
        <table>
          <thead>
            <tr>
              <th style="width: 80px;">ID</th>
              <th>Nome da Área / Cliente</th>
              <th style="width: 140px; text-align:right;">Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="area in areas" :key="area.id">
              <td><strong>#{{ area.id }}</strong></td>
              <td><strong style="color:var(--purple)">{{ area.name }}</strong></td>
              <td style="text-align:right;">
                <button class="btn secondary" style="padding:4px 9px; margin-right:4px;" @click="openEditAreaModal(area)">
                  Editar
                </button>
                <button class="btn danger" style="padding:4px 9px;" @click="handleDeleteArea(area.id)">
                  Excluir
                </button>
              </td>
            </tr>
            <tr v-if="areas.length === 0">
              <td colspan="3" style="text-align:center; padding:20px; color:var(--muted)">Nenhuma área/cliente cadastrada.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- ABA 2: USUÁRIOS & HIERARQUIA -->
    <div v-if="activeTab === 'users'" class="card" style="margin-top:10px;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
        <div>
          <h3>Usuários, Cargos & Gestor Imediato</h3>
          <div class="small">Configure as permissões de acesso e associe cada analista ao seu gestor imediato responsável.</div>
        </div>
        <button class="btn" @click="openNewUserModal">+ Novo Usuário</button>
      </div>

      <div class="tw">
        <table>
          <thead>
            <tr>
              <th style="width: 70px;">ID</th>
              <th>Nome</th>
              <th>Email</th>
              <th>Nível de Acesso (Cargo)</th>
              <th>Gestor Imediato</th>
              <th style="width: 100px; text-align:right;">Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in users" :key="u.id">
              <td><strong>#{{ u.id }}</strong></td>
              <td><strong style="color:var(--purple)">{{ u.name }}</strong></td>
              <td>{{ u.email }}</td>
              <td>
                <span class="badge" :class="getRoleBadgeClass(u.role)">
                  {{ getRoleLabel(u.role) }}
                </span>
              </td>
              <td>
                <span v-if="u.manager_name" class="badge bpurple">
                  👤 {{ u.manager_name }}
                </span>
                <span v-else class="small" style="color:var(--muted)">
                  — Sem gestor direto
                </span>
              </td>
              <td style="text-align:right;">
                <button class="btn secondary" style="padding:4px 9px;" @click="openEditUserModal(u)">
                  Editar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- MODAL ÁREA / CLIENTE -->
    <div v-if="showAreaModal" class="modal-backdrop" @click.self="showAreaModal = false">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ editingAreaId ? 'Editar Área / Cliente' : 'Nova Área / Cliente' }}</h2>
          <button class="modal-close" @click="showAreaModal = false">×</button>
        </div>
        <form @submit.prevent="saveArea">
          <div class="form-group">
            <label>Nome da Área ou Cliente</label>
            <input
              v-model="areaFormName"
              required
              class="form-control"
              placeholder="ex: RH - DHO ou Cliente XPTO"
            />
          </div>
          <div style="display:flex; justify-content:flex-end; gap:8px; margin-top:14px;">
            <button type="button" class="btn secondary" @click="showAreaModal = false">Cancelar</button>
            <button type="submit" class="btn">Salvar</button>
          </div>
        </form>
      </div>
    </div>

    <!-- MODAL USUÁRIO / GESTOR -->
    <div v-if="showUserModal" class="modal-backdrop" @click.self="showUserModal = false">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ editingUserId ? 'Editar Usuário & Gestão' : 'Cadastrar Novo Usuário' }}</h2>
          <button class="modal-close" @click="showUserModal = false">×</button>
        </div>
        <form @submit.prevent="saveUser">
          <div class="form-group">
            <label>Nome Completo</label>
            <input v-model="userForm.name" required class="form-control" placeholder="ex: João Silva" />
          </div>
          <div class="form-group">
            <label>Email Corporativo</label>
            <input v-model="userForm.email" type="email" required class="form-control" placeholder="ex: joao@empresa.com" />
          </div>
          <div class="form-group" v-if="!editingUserId">
            <label>Senha Inicial</label>
            <input v-model="userForm.password" type="password" required class="form-control" placeholder="••••••••" />
          </div>
          <div class="form-group" v-else>
            <label>Nova Senha (deixe em branco para manter a atual)</label>
            <input v-model="userForm.password" type="password" class="form-control" placeholder="Opcional" />
          </div>

          <div class="form-group">
            <label>Nível de Permissão (Cargo)</label>
            <select v-model="userForm.role" class="form-control">
              <option value="analista">Analista (Execução & Apontamento)</option>
              <option value="gestor">Gestor (Visão de Equipe & Gestão)</option>
              <option value="admin">Administrador (Controle Total)</option>
            </select>
          </div>

          <div class="form-group">
            <label>Gestor Imediato</label>
            <select v-model="userForm.manager_id" class="form-control">
              <option :value="null">Nenhum (Topo da Hierarquia / Admin)</option>
              <option
                v-for="mgr in availableManagers"
                :key="mgr.id"
                :value="mgr.id"
              >
                {{ mgr.name }} ({{ getRoleLabel(mgr.role) }})
              </option>
            </select>
            <div class="small" style="margin-top:3px; color:var(--muted)">
              O gestor imediato terá visão do calendário de apontamentos deste usuário.
            </div>
          </div>

          <div style="display:flex; justify-content:flex-end; gap:8px; margin-top:14px;">
            <button type="button" class="btn secondary" @click="showUserModal = false">Cancelar</button>
            <button type="submit" class="btn">Salvar Usuário</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'

const activeTab = ref('areas')
const areas = ref([])
const users = ref([])

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

const availableManagers = computed(() => {
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
  try {
    if (editingAreaId.value) {
      await api.put(`/areas/${editingAreaId.value}`, { name: areaFormName.value })
    } else {
      await api.post('/areas/', { name: areaFormName.value })
    }
    showAreaModal.value = false
    await loadData()
  } catch (err) {
    alert(err.response?.data?.detail || 'Erro ao salvar Área.')
  }
}

async function handleDeleteArea(id) {
  if (!confirm('Deseja realmente excluir esta Área/Cliente?')) return
  try {
    await api.delete(`/areas/${id}`)
    await loadData()
  } catch (err) {
    alert(err.response?.data?.detail || 'Erro ao excluir Área.')
  }
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
  try {
    if (editingUserId.value) {
      await api.put(`/users/${editingUserId.value}`, userForm.value)
    } else {
      await api.post('/users/', userForm.value)
    }
    showUserModal.value = false
    await loadData()
  } catch (err) {
    alert(err.response?.data?.detail || 'Erro ao salvar Usuário.')
  }
}

function getRoleLabel(role) {
  const map = { admin: 'Administrador', gestor: 'Gestor', analista: 'Analista' }
  return map[role] || role
}

function getRoleBadgeClass(role) {
  if (role === 'admin') return 'bred'
  if (role === 'gestor') return 'bpurple'
  return 'bgreen'
}
</script>

