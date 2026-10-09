<template>
  <div class="section filters-wrapper" ref="wrapperRef">
    <!-- Cabeçalho do Painel -->
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px; flex-wrap:wrap; gap:8px;">
      <div>
        <div class="title" style="font-size:1.05rem; font-weight:800; color:var(--purple); margin:0;">
          Painel de Filtros Multiseleção Integrado
        </div>
        <div class="sub" style="font-size:0.8rem; color:var(--muted); margin-top:2px;">
          Selecione múltiplos valores por filtro para recalcular os visuais e diagnósticos em tempo real.
        </div>
      </div>
      <div style="display:flex; align-items:center; gap:8px;">
        <span v-if="activeFiltersCount > 0" class="badge bpurple" style="font-size:0.75rem; font-weight:700;">
          {{ activeFiltersCount }} filtro(s) ativo(s)
        </span>
        <button
          class="btn secondary"
          @click="resetAllFilters"
          style="font-size:0.78rem; padding:4px 9px;"
          title="Limpar todos os filtros selecionados"
        >
          Resetar Filtros
        </button>
      </div>
    </div>

    <!-- Linha 1: Dropdowns Multiseleção -->
    <div class="filters-grid">
      <!-- 1. Área Requisitante -->
      <div class="ms-container" :class="{ open: openDropdown === 'areas' }">
        <label>Área Requisitante</label>
        <div class="ms-trigger" @click.stop="toggleDropdown('areas')">
          <span class="ms-text" :title="getTriggerText('areas', 'Todas')">
            {{ getTriggerText('areas', 'Todas') }}
            <span v-if="roadmapStore.filters.areas.length > 1" class="ms-count-badge">
              {{ roadmapStore.filters.areas.length }}
            </span>
          </span>
          <span class="ms-arrow">▼</span>
        </div>
        <div class="ms-dropdown" @click.stop>
          <input
            v-model="searchQueries.areas"
            type="text"
            class="ms-search"
            placeholder="Buscar área..."
          />
          <div class="ms-actions">
            <span class="ms-action-btn" @click="selectAll('areas', areaOptions)">Marcar Todos</span>
            <span class="ms-action-btn" @click="clearAll('areas')">Limpar</span>
          </div>
          <div class="ms-list">
            <div v-if="filteredAreaOptions.length === 0" class="ms-empty">Nenhuma área encontrada</div>
            <label
              v-for="opt in filteredAreaOptions"
              :key="opt"
              class="ms-item"
            >
              <input
                type="checkbox"
                :checked="roadmapStore.filters.areas.includes(opt)"
                @change="toggleItem('areas', opt)"
              />
              <span>{{ opt }}</span>
            </label>
          </div>
        </div>
      </div>

      <!-- 2. Situação do Projeto -->
      <div class="ms-container" :class="{ open: openDropdown === 'status' }">
        <label>Situação do Projeto</label>
        <div class="ms-trigger" @click.stop="toggleDropdown('status')">
          <span class="ms-text" :title="getTriggerText('status', 'Todos')">
            {{ getTriggerText('status', 'Todos') }}
            <span v-if="roadmapStore.filters.status.length > 1" class="ms-count-badge">
              {{ roadmapStore.filters.status.length }}
            </span>
          </span>
          <span class="ms-arrow">▼</span>
        </div>
        <div class="ms-dropdown" @click.stop>
          <input
            v-model="searchQueries.status"
            type="text"
            class="ms-search"
            placeholder="Buscar status..."
          />
          <div class="ms-actions">
            <span class="ms-action-btn" @click="selectAll('status', statusOptions)">Marcar Todos</span>
            <span class="ms-action-btn" @click="clearAll('status')">Limpar</span>
          </div>
          <div class="ms-list">
            <div v-if="filteredStatusOptions.length === 0" class="ms-empty">Nenhum status encontrado</div>
            <label
              v-for="opt in filteredStatusOptions"
              :key="opt"
              class="ms-item"
            >
              <input
                type="checkbox"
                :checked="roadmapStore.filters.status.includes(opt)"
                @change="toggleItem('status', opt)"
              />
              <span>{{ opt }}</span>
            </label>
          </div>
        </div>
      </div>

      <!-- 3. Owner do Projeto -->
      <div class="ms-container" :class="{ open: openDropdown === 'owners' }">
        <label>Owner do Projeto</label>
        <div class="ms-trigger" @click.stop="toggleDropdown('owners')">
          <span class="ms-text" :title="getTriggerText('owners', 'Todos')">
            {{ getTriggerText('owners', 'Todos') }}
            <span v-if="roadmapStore.filters.owners.length > 1" class="ms-count-badge">
              {{ roadmapStore.filters.owners.length }}
            </span>
          </span>
          <span class="ms-arrow">▼</span>
        </div>
        <div class="ms-dropdown" @click.stop>
          <input
            v-model="searchQueries.owners"
            type="text"
            class="ms-search"
            placeholder="Buscar owner..."
          />
          <div class="ms-actions">
            <span class="ms-action-btn" @click="selectAll('owners', ownerOptions)">Marcar Todos</span>
            <span class="ms-action-btn" @click="clearAll('owners')">Limpar</span>
          </div>
          <div class="ms-list">
            <div v-if="filteredOwnerOptions.length === 0" class="ms-empty">Nenhum owner encontrado</div>
            <label
              v-for="opt in filteredOwnerOptions"
              :key="opt"
              class="ms-item"
            >
              <input
                type="checkbox"
                :checked="roadmapStore.filters.owners.includes(opt)"
                @change="toggleItem('owners', opt)"
              />
              <span>{{ opt }}</span>
            </label>
          </div>
        </div>
      </div>

      <!-- 4. Prioridade -->
      <div class="ms-container" :class="{ open: openDropdown === 'priority' }">
        <label>Prioridade</label>
        <div class="ms-trigger" @click.stop="toggleDropdown('priority')">
          <span class="ms-text" :title="getTriggerText('priority', 'Todas')">
            {{ getTriggerText('priority', 'Todas') }}
            <span v-if="roadmapStore.filters.priority.length > 1" class="ms-count-badge">
              {{ roadmapStore.filters.priority.length }}
            </span>
          </span>
          <span class="ms-arrow">▼</span>
        </div>
        <div class="ms-dropdown" @click.stop>
          <input
            v-model="searchQueries.priority"
            type="text"
            class="ms-search"
            placeholder="Buscar prioridade..."
          />
          <div class="ms-actions">
            <span class="ms-action-btn" @click="selectAll('priority', priorityOptions)">Marcar Todos</span>
            <span class="ms-action-btn" @click="clearAll('priority')">Limpar</span>
          </div>
          <div class="ms-list">
            <div v-if="filteredPriorityOptions.length === 0" class="ms-empty">Nenhuma prioridade</div>
            <label
              v-for="opt in filteredPriorityOptions"
              :key="opt"
              class="ms-item"
            >
              <input
                type="checkbox"
                :checked="roadmapStore.filters.priority.includes(opt)"
                @change="toggleItem('priority', opt)"
              />
              <span>{{ opt }}</span>
            </label>
          </div>
        </div>
      </div>

      <!-- 5. Projetos Atrasados -->
      <div class="ms-container" :class="{ open: openDropdown === 'delays' }">
        <label>Projetos Atrasados</label>
        <div class="ms-trigger" @click.stop="toggleDropdown('delays')">
          <span class="ms-text">
            {{ delayTriggerText }}
          </span>
          <span class="ms-arrow">▼</span>
        </div>
        <div class="ms-dropdown" @click.stop>
          <div class="ms-list">
            <label
              class="ms-item"
              :class="{ active: roadmapStore.filters.delays === 'all' }"
              @click="setDelayFilter('all')"
            >
              <input type="radio" name="delayOpt" :checked="roadmapStore.filters.delays === 'all'" />
              <span>Todos</span>
            </label>
            <label
              class="ms-item"
              :class="{ active: roadmapStore.filters.delays === 'overdue' }"
              @click="setDelayFilter('overdue')"
            >
              <input type="radio" name="delayOpt" :checked="roadmapStore.filters.delays === 'overdue'" />
              <span style="color:var(--red); font-weight:700;">⚠️ Apenas Atrasados</span>
            </label>
            <label
              class="ms-item"
              :class="{ active: roadmapStore.filters.delays === 'ontime' }"
              @click="setDelayFilter('ontime')"
            >
              <input type="radio" name="delayOpt" :checked="roadmapStore.filters.delays === 'ontime'" />
              <span style="color:var(--green); font-weight:700;">✔ No Prazo</span>
            </label>
          </div>
        </div>
      </div>

      <!-- 6. Solicitante -->
      <div class="ms-container" :class="{ open: openDropdown === 'requesters' }">
        <label>Solicitante</label>
        <div class="ms-trigger" @click.stop="toggleDropdown('requesters')">
          <span class="ms-text" :title="getTriggerText('requesters', 'Todos')">
            {{ getTriggerText('requesters', 'Todos') }}
            <span v-if="roadmapStore.filters.requesters.length > 1" class="ms-count-badge">
              {{ roadmapStore.filters.requesters.length }}
            </span>
          </span>
          <span class="ms-arrow">▼</span>
        </div>
        <div class="ms-dropdown" @click.stop>
          <input
            v-model="searchQueries.requesters"
            type="text"
            class="ms-search"
            placeholder="Buscar solicitante..."
          />
          <div class="ms-actions">
            <span class="ms-action-btn" @click="selectAll('requesters', requesterOptions)">Marcar Todos</span>
            <span class="ms-action-btn" @click="clearAll('requesters')">Limpar</span>
          </div>
          <div class="ms-list">
            <div v-if="filteredRequesterOptions.length === 0" class="ms-empty">Nenhum solicitante cadastrado</div>
            <label
              v-for="opt in filteredRequesterOptions"
              :key="opt"
              class="ms-item"
            >
              <input
                type="checkbox"
                :checked="roadmapStore.filters.requesters.includes(opt)"
                @change="toggleItem('requesters', opt)"
              />
              <span>{{ opt }}</span>
            </label>
          </div>
        </div>
      </div>

      <!-- 7. Responsável Técnico -->
      <div class="ms-container" :class="{ open: openDropdown === 'technicalResponsibles' }">
        <label>Responsável Técnico</label>
        <div class="ms-trigger" @click.stop="toggleDropdown('technicalResponsibles')">
          <span class="ms-text" :title="getTriggerText('technicalResponsibles', 'Todos')">
            {{ getTriggerText('technicalResponsibles', 'Todos') }}
            <span v-if="roadmapStore.filters.technicalResponsibles.length > 1" class="ms-count-badge">
              {{ roadmapStore.filters.technicalResponsibles.length }}
            </span>
          </span>
          <span class="ms-arrow">▼</span>
        </div>
        <div class="ms-dropdown" @click.stop>
          <input
            v-model="searchQueries.technicalResponsibles"
            type="text"
            class="ms-search"
            placeholder="Buscar responsável..."
          />
          <div class="ms-actions">
            <span class="ms-action-btn" @click="selectAll('technicalResponsibles', techRespOptions)">Marcar Todos</span>
            <span class="ms-action-btn" @click="clearAll('technicalResponsibles')">Limpar</span>
          </div>
          <div class="ms-list">
            <div v-if="filteredTechRespOptions.length === 0" class="ms-empty">Nenhum responsável encontrado</div>
            <label
              v-for="opt in filteredTechRespOptions"
              :key="opt"
              class="ms-item"
            >
              <input
                type="checkbox"
                :checked="roadmapStore.filters.technicalResponsibles.includes(opt)"
                @change="toggleItem('technicalResponsibles', opt)"
              />
              <span>{{ opt }}</span>
            </label>
          </div>
        </div>
      </div>

      <!-- 8. Gestor Imediato (solicitado pelo usuário) -->
      <div class="ms-container" :class="{ open: openDropdown === 'managers' }">
        <label>Gestor</label>
        <div class="ms-trigger" @click.stop="toggleDropdown('managers')">
          <span class="ms-text" :title="getTriggerText('managers', 'Todos')">
            {{ getTriggerText('managers', 'Todos') }}
            <span v-if="roadmapStore.filters.managers.length > 1" class="ms-count-badge">
              {{ roadmapStore.filters.managers.length }}
            </span>
          </span>
          <span class="ms-arrow">▼</span>
        </div>
        <div class="ms-dropdown" @click.stop>
          <input
            v-model="searchQueries.managers"
            type="text"
            class="ms-search"
            placeholder="Buscar gestor..."
          />
          <div class="ms-actions">
            <span class="ms-action-btn" @click="selectAll('managers', managerOptions)">Marcar Todos</span>
            <span class="ms-action-btn" @click="clearAll('managers')">Limpar</span>
          </div>
          <div class="ms-list">
            <div v-if="filteredManagerOptions.length === 0" class="ms-empty">Nenhum gestor associado</div>
            <label
              v-for="opt in filteredManagerOptions"
              :key="opt"
              class="ms-item"
            >
              <input
                type="checkbox"
                :checked="roadmapStore.filters.managers.includes(opt)"
                @change="toggleItem('managers', opt)"
              />
              <span>{{ opt }}</span>
            </label>
          </div>
        </div>
      </div>
    </div>

    <!-- Linha 2: Intervalos Temporais (Caixa Única c/ Popover) + Busca Textual -->
    <div class="row2-filters-grid" style="margin-top:8px;">
      <!-- Período do Projeto -->
      <div class="ms-container date-range-container" :class="{ open: openDropdown === 'projectDate' }">
        <label>Período do Projeto</label>
        <div class="ms-trigger date-trigger" @click.stop="toggleDropdown('projectDate')">
          <div class="ms-text" :title="getDateTriggerText('project')">
            <span style="opacity:0.8;">📅</span>
            <span :style="{ fontWeight: (roadmapStore.filters.projectStart || roadmapStore.filters.projectEnd) ? '700' : '500', color: (roadmapStore.filters.projectStart || roadmapStore.filters.projectEnd) ? 'var(--purple)' : 'inherit' }">
              {{ getDateTriggerText('project') }}
            </span>
          </div>
          <div style="display:flex; align-items:center; gap:4px;">
            <span
              v-if="roadmapStore.filters.projectStart || roadmapStore.filters.projectEnd"
              class="date-clear-icon"
              @click.stop="clearDateFilter('project')"
              title="Limpar período do projeto"
            >
              ✕
            </span>
            <span class="ms-arrow">▼</span>
          </div>
        </div>

        <!-- Dropdown Popover do Período do Projeto -->
        <div class="dr-dropdown" @click.stop>
          <div class="dr-section-title">Atalhos de Período</div>
          <div class="dr-presets-grid">
            <button
              type="button"
              class="dr-preset-btn"
              :class="{ active: isPresetActive('project', 'today') }"
              @click="applyDatePreset('project', 'today')"
            >
              Hoje
            </button>
            <button
              type="button"
              class="dr-preset-btn"
              :class="{ active: isPresetActive('project', 'this_week') }"
              @click="applyDatePreset('project', 'this_week')"
            >
              Esta Semana
            </button>
            <button
              type="button"
              class="dr-preset-btn"
              :class="{ active: isPresetActive('project', 'this_month') }"
              @click="applyDatePreset('project', 'this_month')"
            >
              Mês Atual
            </button>
            <button
              type="button"
              class="dr-preset-btn"
              :class="{ active: isPresetActive('project', 'last_month') }"
              @click="applyDatePreset('project', 'last_month')"
            >
              Mês Anterior
            </button>
            <button
              type="button"
              class="dr-preset-btn"
              :class="{ active: isPresetActive('project', 'this_year') }"
              @click="applyDatePreset('project', 'this_year')"
            >
              Este Ano
            </button>
            <button
              type="button"
              class="dr-preset-btn"
              :class="{ active: isPresetActive('project', 'all') }"
              @click="applyDatePreset('project', 'all')"
            >
              Todo o Período
            </button>
          </div>

          <div class="dr-divider"></div>

          <div class="dr-section-title">Intervalo Personalizado</div>
          <div class="dr-inputs-row">
            <div class="dr-input-col">
              <label for="filterProjStart">De (Início)</label>
              <input
                id="filterProjStart"
                type="date"
                class="dr-date-input"
                v-model="roadmapStore.filters.projectStart"
              />
            </div>
            <div class="dr-input-col">
              <label for="filterProjEnd">Até (Término)</label>
              <input
                id="filterProjEnd"
                type="date"
                class="dr-date-input"
                v-model="roadmapStore.filters.projectEnd"
              />
            </div>
          </div>

          <div class="dr-footer">
            <button
              type="button"
              class="btn secondary"
              style="font-size:0.76rem; padding:3px 8px;"
              @click="clearDateFilter('project')"
            >
              Limpar
            </button>
            <button
              type="button"
              class="btn"
              style="font-size:0.76rem; padding:3px 10px;"
              @click="closeDropdowns"
            >
              Aplicar
            </button>
          </div>
        </div>
      </div>

      <!-- Período da Atividade -->
      <div class="ms-container date-range-container" :class="{ open: openDropdown === 'activityDate' }">
        <label>Período da Atividade</label>
        <div class="ms-trigger date-trigger" @click.stop="toggleDropdown('activityDate')">
          <div class="ms-text" :title="getDateTriggerText('activity')">
            <span style="opacity:0.8;">📅</span>
            <span :style="{ fontWeight: (roadmapStore.filters.activityStart || roadmapStore.filters.activityEnd) ? '700' : '500', color: (roadmapStore.filters.activityStart || roadmapStore.filters.activityEnd) ? 'var(--purple)' : 'inherit' }">
              {{ getDateTriggerText('activity') }}
            </span>
          </div>
          <div style="display:flex; align-items:center; gap:4px;">
            <span
              v-if="roadmapStore.filters.activityStart || roadmapStore.filters.activityEnd"
              class="date-clear-icon"
              @click.stop="clearDateFilter('activity')"
              title="Limpar período da atividade"
            >
              ✕
            </span>
            <span class="ms-arrow">▼</span>
          </div>
        </div>

        <!-- Dropdown Popover do Período da Atividade -->
        <div class="dr-dropdown" @click.stop>
          <div class="dr-section-title">Atalhos de Período</div>
          <div class="dr-presets-grid">
            <button
              type="button"
              class="dr-preset-btn"
              :class="{ active: isPresetActive('activity', 'today') }"
              @click="applyDatePreset('activity', 'today')"
            >
              Hoje
            </button>
            <button
              type="button"
              class="dr-preset-btn"
              :class="{ active: isPresetActive('activity', 'this_week') }"
              @click="applyDatePreset('activity', 'this_week')"
            >
              Esta Semana
            </button>
            <button
              type="button"
              class="dr-preset-btn"
              :class="{ active: isPresetActive('activity', 'this_month') }"
              @click="applyDatePreset('activity', 'this_month')"
            >
              Mês Atual
            </button>
            <button
              type="button"
              class="dr-preset-btn"
              :class="{ active: isPresetActive('activity', 'last_month') }"
              @click="applyDatePreset('activity', 'last_month')"
            >
              Mês Anterior
            </button>
            <button
              type="button"
              class="dr-preset-btn"
              :class="{ active: isPresetActive('activity', 'this_year') }"
              @click="applyDatePreset('activity', 'this_year')"
            >
              Este Ano
            </button>
            <button
              type="button"
              class="dr-preset-btn"
              :class="{ active: isPresetActive('activity', 'all') }"
              @click="applyDatePreset('activity', 'all')"
            >
              Todo o Período
            </button>
          </div>

          <div class="dr-divider"></div>

          <div class="dr-section-title">Intervalo Personalizado</div>
          <div class="dr-inputs-row">
            <div class="dr-input-col">
              <label for="filterActStart">De (Início)</label>
              <input
                id="filterActStart"
                type="date"
                class="dr-date-input"
                v-model="roadmapStore.filters.activityStart"
              />
            </div>
            <div class="dr-input-col">
              <label for="filterActEnd">Até (Término)</label>
              <input
                id="filterActEnd"
                type="date"
                class="dr-date-input"
                v-model="roadmapStore.filters.activityEnd"
              />
            </div>
          </div>

          <div class="dr-footer">
            <button
              type="button"
              class="btn secondary"
              style="font-size:0.76rem; padding:3px 8px;"
              @click="clearDateFilter('activity')"
            >
              Limpar
            </button>
            <button
              type="button"
              class="btn"
              style="font-size:0.76rem; padding:3px 10px;"
              @click="closeDropdowns"
            >
              Aplicar
            </button>
          </div>
        </div>
      </div>

      <!-- Busca Textual -->
      <div class="search-box-container">
        <label for="filterSearchText">Busca Textual</label>
        <div style="position:relative;">
          <input
            id="filterSearchText"
            type="text"
            class="form-control"
            v-model="roadmapStore.filters.search"
            placeholder="Nome do projeto, chamado ou solicitante..."
            style="height:32px; font-size:0.84rem; padding-left:28px; padding-right:26px;"
          />
          <span style="position:absolute; left:8px; top:8px; font-size:0.85rem; opacity:0.6;">🔍</span>
          <span
            v-if="roadmapStore.filters.search"
            class="date-clear-icon search-clear"
            @click="roadmapStore.filters.search = ''"
            title="Limpar busca"
          >
            ✕
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted, onBeforeUnmount } from 'vue'
import { useRoadmapStore } from '@/stores/roadmap'

const roadmapStore = useRoadmapStore()
const wrapperRef = ref(null)

// Controle de dropdown aberto
const openDropdown = ref(null)

// Buscas internas em cada dropdown
const searchQueries = reactive({
  areas: '',
  status: '',
  owners: '',
  priority: '',
  delays: '',
  requesters: '',
  technicalResponsibles: '',
  managers: ''
})

function toggleDropdown(name) {
  openDropdown.value = openDropdown.value === name ? null : name
}

function closeDropdowns() {
  openDropdown.value = null
}

function handleClickOutside(e) {
  if (wrapperRef.value && !wrapperRef.value.contains(e.target)) {
    closeDropdowns()
  }
}

onMounted(() => {
  window.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  window.removeEventListener('click', handleClickOutside)
})

// OPÇÕES DISPONÍVEIS
const areaOptions = computed(() => {
  const set = new Set()
  if (roadmapStore.areas) roadmapStore.areas.forEach(a => { if (a.name) set.add(a.name) })
  if (roadmapStore.projects) roadmapStore.projects.forEach(p => { if (p.area_name) set.add(p.area_name) })
  return Array.from(set).sort()
})

const filteredAreaOptions = computed(() => {
  const q = searchQueries.areas.toLowerCase().trim()
  return areaOptions.value.filter(o => !q || o.toLowerCase().includes(q))
})

const statusOptions = computed(() => {
  const defaults = ['Não Iniciado', 'Em Andamento', 'Concluído', 'StandBy', 'Em Espera', 'Cancelado']
  const set = new Set(defaults)
  if (roadmapStore.projects) roadmapStore.projects.forEach(p => { if (p.status) set.add(p.status) })
  return Array.from(set)
})

const filteredStatusOptions = computed(() => {
  const q = searchQueries.status.toLowerCase().trim()
  return statusOptions.value.filter(o => !q || o.toLowerCase().includes(q))
})

const ownerOptions = computed(() => {
  const set = new Set()
  if (roadmapStore.users) roadmapStore.users.forEach(u => { if (u.name) set.add(u.name) })
  if (roadmapStore.projects) roadmapStore.projects.forEach(p => { if (p.owner_name) set.add(p.owner_name) })
  return Array.from(set).sort()
})

const filteredOwnerOptions = computed(() => {
  const q = searchQueries.owners.toLowerCase().trim()
  return ownerOptions.value.filter(o => !q || o.toLowerCase().includes(q))
})

const priorityOptions = computed(() => {
  return ['Crítica', 'Alta', 'Normal', 'Média', 'Baixa', '🎯 Executivo']
})

const filteredPriorityOptions = computed(() => {
  const q = searchQueries.priority.toLowerCase().trim()
  return priorityOptions.value.filter(o => !q || o.toLowerCase().includes(q))
})

const requesterOptions = computed(() => {
  const set = new Set()
  if (roadmapStore.projects) roadmapStore.projects.forEach(p => { if (p.requester) set.add(p.requester) })
  return Array.from(set).sort()
})

const filteredRequesterOptions = computed(() => {
  const q = searchQueries.requesters.toLowerCase().trim()
  return requesterOptions.value.filter(o => !q || o.toLowerCase().includes(q))
})

const techRespOptions = computed(() => {
  const set = new Set()
  if (roadmapStore.activities) roadmapStore.activities.forEach(a => { if (a.assignee_name) set.add(a.assignee_name) })
  if (roadmapStore.users) roadmapStore.users.forEach(u => { if (u.name) set.add(u.name) })
  return Array.from(set).sort()
})

const filteredTechRespOptions = computed(() => {
  const q = searchQueries.technicalResponsibles.toLowerCase().trim()
  return techRespOptions.value.filter(o => !q || o.toLowerCase().includes(q))
})

const managerOptions = computed(() => {
  const set = new Set()
  if (roadmapStore.projects) roadmapStore.projects.forEach(p => { if (p.manager_name) set.add(p.manager_name) })
  if (roadmapStore.users) {
    roadmapStore.users.forEach(u => {
      if (u.manager_name) set.add(u.manager_name)
      if (u.role === 'gestor' || u.role === 'admin') set.add(u.name)
    })
  }
  return Array.from(set).sort()
})

const filteredManagerOptions = computed(() => {
  const q = searchQueries.managers.toLowerCase().trim()
  return managerOptions.value.filter(o => !q || o.toLowerCase().includes(q))
})

// Ações de Seleção
function toggleItem(key, val) {
  const list = [...roadmapStore.filters[key]]
  const idx = list.indexOf(val)
  if (idx !== -1) {
    list.splice(idx, 1)
  } else {
    list.push(val)
  }
  roadmapStore.filters[key] = list
}

function selectAll(key, allOptions) {
  roadmapStore.filters[key] = [...allOptions]
}

function clearAll(key) {
  roadmapStore.filters[key] = []
}

function setDelayFilter(val) {
  roadmapStore.filters.delays = val
  roadmapStore.filters.deadline = val
  closeDropdowns()
}

const delayTriggerText = computed(() => {
  const d = roadmapStore.filters.delays || 'all'
  if (d === 'overdue') return '⚠️ Apenas Atrasados'
  if (d === 'ontime') return '✔ No Prazo'
  return 'Todos'
})

function getTriggerText(key, defaultLabel) {
  const arr = roadmapStore.filters[key] || []
  if (arr.length === 0) return defaultLabel
  if (arr.length === 1) return arr[0]
  return `${arr.length} selecionados`
}

// Helpers para Filtros de Período / Data
function toDateStr(d) {
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

function formatShortDate(dateStr) {
  if (!dateStr) return ''
  const parts = dateStr.split('-')
  if (parts.length === 3) {
    return `${parts[2]}/${parts[1]}/${parts[0]}`
  }
  return dateStr
}

function getPresetRange(presetKey) {
  const now = new Date()
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())

  if (presetKey === 'today') {
    const s = toDateStr(today)
    return { start: s, end: s }
  }

  if (presetKey === 'this_week') {
    const dayOfWeek = today.getDay()
    const diffToMonday = dayOfWeek === 0 ? -6 : 1 - dayOfWeek
    const monday = new Date(today)
    monday.setDate(today.getDate() + diffToMonday)
    const sunday = new Date(monday)
    sunday.setDate(monday.getDate() + 6)
    return { start: toDateStr(monday), end: toDateStr(sunday) }
  }

  if (presetKey === 'this_month') {
    const start = new Date(today.getFullYear(), today.getMonth(), 1)
    const end = new Date(today.getFullYear(), today.getMonth() + 1, 0)
    return { start: toDateStr(start), end: toDateStr(end) }
  }

  if (presetKey === 'last_month') {
    const start = new Date(today.getFullYear(), today.getMonth() - 1, 1)
    const end = new Date(today.getFullYear(), today.getMonth(), 0)
    return { start: toDateStr(start), end: toDateStr(end) }
  }

  if (presetKey === 'this_year') {
    const start = new Date(today.getFullYear(), 0, 1)
    const end = new Date(today.getFullYear(), 11, 31)
    return { start: toDateStr(start), end: toDateStr(end) }
  }

  return { start: '', end: '' }
}

function applyDatePreset(type, presetKey) {
  const range = getPresetRange(presetKey)
  if (type === 'project') {
    roadmapStore.filters.projectStart = range.start
    roadmapStore.filters.projectEnd = range.end
  } else if (type === 'activity') {
    roadmapStore.filters.activityStart = range.start
    roadmapStore.filters.activityEnd = range.end
  }
  closeDropdowns()
}

function isPresetActive(type, presetKey) {
  const start = type === 'project' ? roadmapStore.filters.projectStart : roadmapStore.filters.activityStart
  const end = type === 'project' ? roadmapStore.filters.projectEnd : roadmapStore.filters.activityEnd

  if (presetKey === 'all') {
    return !start && !end
  }
  if (!start && !end) {
    return false
  }

  const range = getPresetRange(presetKey)
  return start === range.start && end === range.end
}

function clearDateFilter(type) {
  if (type === 'project') {
    roadmapStore.filters.projectStart = ''
    roadmapStore.filters.projectEnd = ''
  } else if (type === 'activity') {
    roadmapStore.filters.activityStart = ''
    roadmapStore.filters.activityEnd = ''
  }
}

function getDateTriggerText(type) {
  const start = type === 'project' ? roadmapStore.filters.projectStart : roadmapStore.filters.activityStart
  const end = type === 'project' ? roadmapStore.filters.projectEnd : roadmapStore.filters.activityEnd

  if (!start && !end) return 'Todos'

  if (isPresetActive(type, 'today')) return 'Hoje'
  if (isPresetActive(type, 'this_week')) return 'Esta Semana'
  if (isPresetActive(type, 'this_month')) {
    const parts = start.split('-')
    return `Mês Atual (${parts[1]}/${parts[0]})`
  }
  if (isPresetActive(type, 'last_month')) {
    const parts = start.split('-')
    return `Mês Anterior (${parts[1]}/${parts[0]})`
  }
  if (isPresetActive(type, 'this_year')) {
    const parts = start.split('-')
    return `Este Ano (${parts[0]})`
  }

  if (start && end) {
    return `${formatShortDate(start)} → ${formatShortDate(end)}`
  }
  if (start) {
    return `A partir de ${formatShortDate(start)}`
  }
  if (end) {
    return `Até ${formatShortDate(end)}`
  }

  return 'Todos'
}

const activeFiltersCount = computed(() => {
  let count = 0
  if (roadmapStore.filters.search) count++
  if (roadmapStore.filters.areas?.length > 0) count++
  if (roadmapStore.filters.status?.length > 0) count++
  if (roadmapStore.filters.owners?.length > 0) count++
  if (roadmapStore.filters.priority?.length > 0) count++
  if (roadmapStore.filters.delays && roadmapStore.filters.delays !== 'all') count++
  if (roadmapStore.filters.requesters?.length > 0) count++
  if (roadmapStore.filters.technicalResponsibles?.length > 0) count++
  if (roadmapStore.filters.managers?.length > 0) count++
  if (roadmapStore.filters.projectStart || roadmapStore.filters.projectEnd) count++
  if (roadmapStore.filters.activityStart || roadmapStore.filters.activityEnd) count++
  return count
})

function resetAllFilters() {
  roadmapStore.resetFilters()
  Object.keys(searchQueries).forEach(k => searchQueries[k] = '')
  closeDropdowns()
}
</script>

<style scoped>
.filters-wrapper {
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 14px 18px;
  margin-bottom: 14px;
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(8, minmax(130px, 1fr));
  gap: 10px;
}

.ms-container {
  position: relative;
  width: 100%;
}

.ms-container label {
  display: block;
  color: #756B7C;
  font-size: 0.78rem;
  font-weight: 700;
  margin: 0 0 3px 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.ms-trigger {
  width: 100%;
  height: 32px;
  border: 1px solid #DDD8E4;
  background: #fff;
  border-radius: 6px;
  padding: 0 8px;
  font-size: 0.82rem;
  color: #43394A;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  user-select: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.ms-trigger:hover,
.ms-container.open .ms-trigger {
  border-color: var(--purple);
  box-shadow: 0 0 0 1px rgba(109, 86, 160, 0.15);
}

.ms-trigger .ms-text {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 82%;
  display: flex;
  align-items: center;
  gap: 4px;
}

.ms-trigger .ms-arrow {
  font-size: 0.74rem;
  color: #857D8B;
  transition: transform 0.2s;
  flex-shrink: 0;
}

.ms-container.open .ms-arrow {
  transform: rotate(180deg);
}

.ms-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  min-width: 210px;
  width: 100%;
  margin-top: 4px;
  background: #fff;
  border: 1px solid var(--purple2);
  border-radius: 7px;
  box-shadow: 0 8px 20px rgba(62, 38, 102, 0.18);
  z-index: 1000;
  display: none;
  padding: 6px;
  max-height: 260px;
  overflow-y: auto;
}

.ms-container.open .ms-dropdown {
  display: block;
}

.ms-search {
  width: 100%;
  height: 28px;
  border: 1px solid #DDD8E4;
  border-radius: 5px;
  padding: 0 6px;
  font-size: 0.8rem;
  margin-bottom: 6px;
  outline: none;
  box-sizing: border-box;
}

.ms-search:focus {
  border-color: var(--purple);
}

.ms-actions {
  display: flex;
  justify-content: space-between;
  padding: 2px 4px 5px;
  border-bottom: 1px solid #F0ECF4;
  margin-bottom: 5px;
  font-size: 0.76rem;
}

.ms-action-btn {
  color: var(--purple);
  cursor: pointer;
  font-weight: 700;
}

.ms-action-btn:hover {
  text-decoration: underline;
}

.ms-list {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.ms-empty {
  font-size: 0.8rem;
  color: var(--muted);
  text-align: center;
  padding: 8px 4px;
}

.ms-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 5px 8px;
  border-radius: 5px;
  font-size: 0.82rem;
  color: #43394A;
  cursor: pointer;
  user-select: none;
  transition: background 0.15s ease;
}

.ms-item:hover {
  background: var(--purple4);
}

.ms-item input[type="checkbox"],
.ms-item input[type="radio"] {
  width: 14px;
  height: 14px;
  margin: 0;
  accent-color: var(--purple);
  cursor: pointer;
  flex-shrink: 0;
}

.ms-item span {
  line-height: 1.35;
}

.ms-count-badge {
  background: var(--purple);
  color: #fff;
  font-size: 0.72rem;
  font-weight: 800;
  border-radius: 8px;
  padding: 1.5px 5px;
  margin-left: 4px;
}

/* Linha 2 de datas e busca */
.row2-filters-grid {
  display: grid;
  grid-template-columns: minmax(220px, 1fr) minmax(220px, 1fr) minmax(260px, 1.4fr);
  gap: 10px;
}

.date-range-container {
  position: relative;
}

.date-trigger {
  padding-right: 6px;
}

.dr-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  width: 320px;
  margin-top: 4px;
  background: #fff;
  border: 1px solid var(--purple2);
  border-radius: 8px;
  box-shadow: 0 10px 24px rgba(62, 38, 102, 0.2);
  z-index: 1000;
  display: none;
  padding: 12px;
}

.ms-container.open .dr-dropdown {
  display: block;
}

.dr-section-title {
  font-size: 0.74rem;
  font-weight: 800;
  color: var(--purple);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 6px;
}

.dr-presets-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 6px;
}

.dr-preset-btn {
  padding: 5px 4px;
  font-size: 0.75rem;
  font-weight: 600;
  border: 1px solid #E2DCE9;
  background: #FAF8FC;
  color: #43394A;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
  transition: all 0.15s ease;
  white-space: nowrap;
}

.dr-preset-btn:hover {
  background: var(--purple4);
  border-color: var(--purple3);
  color: var(--purple);
}

.dr-preset-btn.active {
  background: var(--purple);
  border-color: var(--purple);
  color: #fff;
  font-weight: 700;
}

.dr-divider {
  height: 1px;
  background: #F0ECF4;
  margin: 10px 0;
}

.dr-inputs-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  margin-bottom: 10px;
}

.dr-input-col label {
  display: block;
  font-size: 0.72rem;
  font-weight: 700;
  color: #756B7C;
  margin-bottom: 3px;
}

.dr-date-input {
  width: 100%;
  height: 28px;
  border: 1px solid #DDD8E4;
  border-radius: 5px;
  background: #fff;
  padding: 0 6px;
  font-size: 0.78rem;
  color: #43394A;
  outline: none;
  box-sizing: border-box;
}

.dr-date-input:focus {
  border-color: var(--purple);
}

.dr-footer {
  display: flex;
  justify-content: flex-end;
  gap: 6px;
  border-top: 1px solid #F0ECF4;
  padding-top: 8px;
}

.date-clear-icon {
  font-size: 0.75rem;
  color: #857D8B;
  cursor: pointer;
  padding: 2px 5px;
  border-radius: 3px;
  line-height: 1;
  transition: all 0.15s;
}

.date-clear-icon:hover {
  color: #d32f2f;
  background: #FFEBEE;
}

.search-box-container {
  width: 100%;
}

.search-box-container label {
  display: block;
  color: #756B7C;
  font-size: 0.78rem;
  font-weight: 700;
  margin: 0 0 3px 2px;
}

.search-clear {
  position: absolute;
  right: 7px;
  top: 7px;
  font-size: 0.8rem;
}

@media (max-width: 1400px) {
  .filters-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 900px) {
  .filters-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .row2-filters-grid {
    grid-template-columns: 1fr;
  }
}
</style>
