<template>
  <div>
    <!-- Top Action Bar -->
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:8px;">
      <router-link to="/portfolio/roadmaps" class="btn secondary">
        ← Voltar para Roadmaps
      </router-link>

      <!-- Permissão aberta para todos os usuários conforme solicitado -->
      <div style="display:flex; gap:8px; flex-wrap:wrap;">
        <button class="btn secondary" @click="openEditProjectModal">
          ✏️ Editar Projeto
        </button>
        <button class="btn secondary" @click="openCreateDeliverableModal">
          📦 + Novo Entregável
        </button>
        <button class="btn" @click="openCreateActivityModal(null)">
          ⚡ + Nova Atividade
        </button>
      </div>
    </div>

    <!-- Cabeçalho do Projeto Detalhado -->
    <div class="card" v-if="project">
      <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:14px;">
        <div style="flex:1; min-width:300px;">
          <div style="display:flex; align-items:center; gap:6px; margin-bottom:6px; flex-wrap:wrap;">
            <span class="badge bpurple">PROJ-{{ String(project.id).padStart(3, '0') }}</span>
            <span class="badge bgray" v-if="project.ticket_number">🎫 Chamado: {{ project.ticket_number }}</span>
            <span class="badge bpink">🏢 Área/Cliente: {{ project.area_name || 'Geral' }}</span>
            <span class="badge" :class="getPriorityClass(project.priority)">Prioridade: {{ project.priority }}</span>
          </div>

          <h1 style="margin:4px 0 6px; font-size:1.25rem; color:var(--purple)">{{ project.name }}</h1>

          <!-- Grid de Informações com Horas Cadastradas do Projeto -->
          <div style="font-size:0.82rem; color:#595163; display:grid; grid-template-columns:repeat(auto-fit, minmax(170px, 1fr)); gap:6px; margin-top:6px;">
            <div>Solicitante: <strong>{{ project.requester || 'Não informado' }}</strong></div>
            <div>Owner (Líder): <strong>{{ project.owner_name || 'Não definido' }}</strong></div>
            <div>Início Calculado: <strong>{{ formatDate(project.start_date) }}</strong></div>
            <div>Término Calculado: <strong>{{ formatDate(project.end_date) }}</strong></div>
            <div>Horas no Projeto: <strong style="color:var(--pink)">⏱️ {{ projectTotalHours }}h ({{ projectTotalMinutes }} min)</strong></div>
          </div>

          <!-- Comentários do Projeto -->
          <div v-if="project.comments" class="callout" style="margin-top:10px;">
            <strong>💬 Comentários do Projeto:</strong><br>
            {{ project.comments }}
          </div>
        </div>

        <div style="text-align:right; min-width:200px;">
          <span class="badge" :class="getStatusClass(project.status)">
            {{ project.status }}
          </span>
          <div style="margin-top:10px; font-weight:800;">
            Progresso Geral: {{ project.progress || 0 }}%
          </div>
          <div class="track" style="width:200px; margin-top:4px;">
            <div class="fill" :style="{ width: (project.progress || 0) + '%' }"></div>
          </div>
          <div class="small" style="margin-top:4px; color:var(--muted)">
            {{ projectCompletedActivities }} de {{ projectTotalActivities }} atividades concluídas
            <span v-if="projectDeliverables.length > 0"> · {{ projectDeliverables.length }} entregáveis</span>
          </div>
          <!-- <div v-if="projectDelayedActivities > 0" class="small" style="margin-top:3px;">
            <span class="badge bred" style="font-weight:800;">
              ⚠️ {{ projectDelayedActivities }} atividade(s) atrasada(s)
            </span>
          </div> -->
          <!-- <div class="small" style="margin-top:2px; color:var(--pink); font-weight:700;">
            ⏱️ {{ projectTotalHours }} horas apontadas
          </div> -->
        </div>
      </div>
    </div>

    <!-- Navegação de Abas do Projeto -->
    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:14px; flex-wrap:wrap; gap:8px;">
      <div style="display:flex; gap:8px; flex-wrap:wrap;">
        <button
          class="btn"
          :class="activeViewTab === 'deliverables' ? '' : 'secondary'"
          @click="activeViewTab = 'deliverables'"
        >
          📦 Entregáveis & Atividades ({{ projectDeliverables.length }} ent., {{ projectActivities.length }} ativ.)
        </button>
        <button
          class="btn"
          :class="activeViewTab === 'gantt' ? '' : 'secondary'"
          @click="activeViewTab = 'gantt'"
        >
          📊 Cronograma Gantt
        </button>
        <!-- ABA SOLICITADA: HORAS & HISTÓRICO DA EQUIPE -->
        <button
          class="btn"
          :class="activeViewTab === 'team' ? '' : 'secondary'"
          @click="activeViewTab = 'team'"
        >
          ⏱️ Horas & Histórico da Equipe ({{ projectTotalHours }}h)
        </button>
      </div>

      <!-- Expandir / Recolher todos os entregáveis -->
      <div v-if="activeViewTab === 'deliverables' && projectDeliverables.length > 0" style="display:flex; gap:6px;">
        <button class="btn secondary" style="padding:5px 10px;" @click="setAllExpanded(true)">
          + Expandir Todos
        </button>
        <button class="btn secondary" style="padding:5px 10px;" @click="setAllExpanded(false)">
          − Recolher Todos
        </button>
      </div>
    </div>

    <!-- ABA 1: ESTRUTURA HIERÁRQUICA DE ENTREGÁVEIS E ATIVIDADES -->
    <div v-if="activeViewTab === 'deliverables'" class="section">
      <!-- Se não houver entregáveis nem atividades -->
      <div v-if="deliverableGroups.length === 0" class="card" style="text-align:center; padding:35px 20px; margin-top:10px;">
        <div style="font-size:32px; margin-bottom:8px;">📦</div>
        <h3 style="color:var(--purple); margin-bottom:4px;">Nenhum entregável cadastrado no projeto</h3>
        <p style="font-size:0.84rem; color:var(--muted); max-width:400px; margin:auto; margin-bottom:12px;">
          Estruture seu projeto dividindo-o em Entregáveis (marcos/fases), e dentro de cada entregável adicione as Atividades operacionais.
        </p>
        <div style="display:flex; justify-content:center; gap:8px;">
          <button class="btn" @click="openCreateDeliverableModal">+ Criar Primeiro Entregável</button>
          <button class="btn secondary" @click="openCreateActivityModal(null)">+ Criar Atividade Geral</button>
        </div>
      </div>

      <!-- Lista de Grupos de Entregáveis -->
      <div v-for="group in deliverableGroups" :key="group.id" class="card" style="margin-top:10px; padding:0; overflow:hidden;">
        <!-- Cabeçalho do Entregável (Accordion Toggle) -->
        <div
          style="background:#FAF8FC; border-bottom:1px solid var(--line); padding:8px 14px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; cursor:pointer;"
          @click="toggleGroup(group.id)"
        >
          <div style="display:flex; align-items:center; gap:8px;">
            <button
              class="btn secondary"
              style="width:20px; height:20px; padding:0; display:flex; align-items:center; justify-content:center; font-size:11px; font-weight:800;"
              @click.stop="toggleGroup(group.id)"
              :title="isExpanded(group.id) ? 'Recolher entregável' : 'Expandir entregável'"
            >
              {{ isExpanded(group.id) ? '−' : '+' }}
            </button>

            <div>
              <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap;">
                <span class="badge bpurple">ENTREGÁVEL</span>
                <strong style="color:var(--purple); font-size:0.95rem;">{{ group.name }}</strong>
                <span class="badge" :class="getStatusClass(group.status)">{{ group.status }}</span>
                <!-- Horas do Entregável -->
                <span class="badge bpink" title="Horas apontadas neste entregável">
                  ⏱️ {{ group.trackedHours }}h
                </span>
                <!-- Atividades e Atrasadas do Entregável -->
                <span class="badge bgray" style="font-weight:700;" title="Atividades concluídas">
                  📋 {{ group.completedActivities }}/{{ group.totalActivities }} atividades
                </span>
                <span
                  v-if="group.delayedActivities > 0"
                  class="badge bred"
                  style="font-weight:800;"
                  title="Atividades com prazo vencido e não concluídas"
                >
                  ⚠️ {{ group.delayedActivities }} atrasada(s)
                </span>
                <span
                  v-else-if="group.totalActivities > 0"
                  class="badge bgreen"
                >
                  No prazo
                </span>
              </div>
              <div v-if="group.comments" class="small" style="color:var(--muted); margin-top:2px;">
                💬 {{ group.comments }}
              </div>
            </div>
          </div>

          <div style="display:flex; align-items:center; gap:14px;" @click.stop>
            <!-- Datas e Progresso do Entregável -->
            <div style="text-align:right;">
              <div class="small" style="color:var(--muted)">
                {{ formatDate(group.start_date) }} → {{ formatDate(group.end_date) }}
              </div>
              <div style="display:flex; align-items:center; gap:6px; margin-top:2px; justify-content:flex-end;">
                <div class="track" style="width:80px;">
                  <div class="fill green" :style="{ width: (group.progress || 0) + '%' }"></div>
                </div>
                <strong style="font-size:0.9rem;">{{ group.progress || 0 }}%</strong>
                <span class="small" style="color:var(--muted)">
                  ({{ group.completedActivities }}/{{ group.totalActivities }})
                </span>
                <span
                  v-if="group.delayedActivities > 0"
                  class="badge bred"
                  style="font-weight:800;"
                >
                  {{ group.delayedActivities }} atrasada(s)
                </span>
              </div>
            </div>

            <!-- Ações do Entregável -->
            <div style="display:flex; gap:6px;">
              <button
                v-if="group.id !== 'general'"
                class="btn"
                style="padding:5px 10px;"
                @click="openCreateActivityModal(group.id)"
                title="Adicionar atividade vinculada a este entregável"
              >
                + Atividade
              </button>
              <button
                v-if="group.id !== 'general'"
                class="btn secondary"
                style="padding:5px 10px;"
                @click="openEditDeliverableModal(group.raw)"
                title="Editar entregável"
              >
                Editar
              </button>
              <button
                v-if="group.id !== 'general'"
                class="btn secondary"
                style="padding:5px 10px; color:var(--red);"
                @click="confirmDeleteDeliverable(group.raw)"
                title="Excluir entregável"
              >
                Excluir
              </button>
            </div>
          </div>
        </div>

        <!-- Tabela de Atividades do Entregável (Colapsável) -->
        <div v-show="isExpanded(group.id)" style="padding:10px 16px;">
          <div class="tw">
            <table>
              <thead>
                <tr>
                  <th style="width:70px;">ID</th>
                  <th>Atividade / Tarefa</th>
                  <th>Responsável Técnico</th>
                  <th>Status</th>
                  <th>Início</th>
                  <th>Término</th>
                  <th>Progresso</th>
                  <th style="text-align:center;">Horas Logadas</th>
                  <th>Timetracker</th>
                  <th style="width:110px; text-align:right;">Ações</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="ativ in group.activities" :key="ativ.id" :style="isActivityDelayed(ativ) ? 'background:#FFF8F8;' : ''">
                  <td><strong>ATIV-{{ String(ativ.id).padStart(4, '0') }}</strong></td>
                  <td>
                    <strong style="color:var(--purple)">{{ ativ.name }}</strong>
                    <div v-if="ativ.description" class="small" style="color:var(--muted)">{{ ativ.description }}</div>
                    <div v-if="ativ.comments" class="small" style="color:var(--pink)">💬 {{ ativ.comments }}</div>
                  </td>
                  <td>
                    <span v-if="ativ.assignee_name" class="badge bpurple">
                      👤 {{ ativ.assignee_name }}
                    </span>
                    <span v-else class="small" style="color:var(--muted)">—</span>
                  </td>
                  <td>
                    <span class="badge" :class="getStatusClass(ativ.status)">
                      {{ ativ.status }}
                    </span>
                    <span
                      v-if="isActivityDelayed(ativ)"
                      class="badge bred"
                      style="margin-left:4px; font-weight:800;"
                    >
                      Atrasada
                    </span>
                  </td>
                  <td><span>{{ formatDate(ativ.start_date) }}</span></td>
                  <td>
                    <span
                      :style="{ color: isActivityDelayed(ativ) ? 'var(--red)' : 'inherit', fontWeight: isActivityDelayed(ativ) ? '800' : 'normal' }"
                    >
                      {{ formatDate(ativ.end_date) }}
                    </span>
                  </td>
                  <td style="min-width:95px;">
                    <div style="display:flex; align-items:center; gap:6px;">
                      <div class="track" style="flex:1;">
                        <div class="fill" :style="{ width: (ativ.progress || 0) + '%' }"></div>
                      </div>
                      <span style="font-weight:700;">{{ (ativ.progress || 0) }}%</span>
                    </div>
                  </td>
                  <!-- Horas Registradas na Atividade -->
                  <td style="text-align:center;">
                    <span class="badge bpink" style="font-weight:700;">
                      ⏱️ {{ ativ.total_tracked_hours || 0 }}h
                    </span>
                  </td>
                  <td>
                    <div style="display:flex; gap:5px;">
                      <button
                        v-if="timetrackerStore.activeTimer?.activityId === ativ.id"
                        class="btn danger"
                        style="padding:4px 8px;"
                        @click="handleStopTimer"
                      >
                        ⏹️ Parar ({{ timetrackerStore.formattedTimer }})
                      </button>
                      <button
                        v-else
                        class="btn pink"
                        style="padding:4px 8px;"
                        @click="handleStartTimer(ativ)"
                      >
                        ▶️ Iniciar
                      </button>

                      <button
                        class="btn secondary"
                        style="padding:4px 8px;"
                        @click="openManualTimeModal(ativ)"
                        title="Apontar horas manualmente"
                      >
                        + Horas
                      </button>
                    </div>
                  </td>
                  <td style="text-align:right;">
                    <div style="display:flex; justify-content:flex-end; gap:5px;">
                      <button
                        class="btn secondary"
                        style="padding:4px 8px;"
                        @click="openEditActivityModal(ativ)"
                      >
                        Editar
                      </button>
                      <button
                        class="btn secondary"
                        style="padding:4px 8px; color:var(--red);"
                        @click="confirmDeleteActivity(ativ)"
                      >
                        Excluir
                      </button>
                    </div>
                  </td>
                </tr>

                <tr v-if="group.activities.length === 0">
                  <td colspan="10" style="text-align:center; padding:20px; color:var(--muted)">
                    Nenhuma atividade cadastrada neste entregável ainda.
                    <button class="btn secondary" style="margin-left:8px;" @click="openCreateActivityModal(group.id)">
                      + Adicionar Atividade
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- ABA 2: GRÁFICO DE GANTT (ENTREGÁVEIS & ATIVIDADES) -->
    <div v-if="activeViewTab === 'gantt'" class="section">
      <div class="card" style="margin-top:10px;">
        <div style="margin-bottom:8px;">
          <h3>Cronograma de Entregas do Projeto (Gantt)</h3>
          <div class="small">Visualize a cadência temporal dos entregáveis e atividades ao longo dos dias.</div>
        </div>
        <GanttChart :items="ganttItems" />
      </div>
    </div>

    <!-- ABA 3: HORAS & HISTÓRICO DA EQUIPE -->
    <div v-if="activeViewTab === 'team'" class="section">
      <!-- Mini Indicadores de Esforço -->
      <div class="kpis" style="margin-top:10px;">
        <div class="kpi primary">
          <div class="v">{{ projectTimeSummary.total_hours }}h</div>
          <div class="l">Total de Horas Investidas</div>
          <div class="n">{{ projectTimeSummary.total_minutes }} minutos apontados</div>
        </div>
        <div class="kpi">
          <div class="v" style="color:var(--purple2)">{{ projectTimeSummary.team_members?.length || 0 }}</div>
          <div class="l">Membros da Equipe</div>
          <div class="n">Trabalharam nesta demanda</div>
        </div>
        <div class="kpi">
          <div class="v" style="color:var(--pink)">{{ projectTimeSummary.entries_count || 0 }}</div>
          <div class="l">Apontamentos Realizados</div>
          <div class="n">Lançamentos no timetracker</div>
        </div>
        <div class="kpi">
          <div class="v" style="color:var(--green)">
            {{ projectTimeSummary.team_members?.length ? (projectTimeSummary.total_hours / projectTimeSummary.team_members.length).toFixed(1) : 0 }}h
          </div>
          <div class="l">Média por Membro</div>
          <div class="n">Carga média por participante</div>
        </div>
      </div>

      <!-- CARD 1: EQUIPE E DISTRIBUIÇÃO DE ESFORÇO -->
      <div class="card" style="margin-top:12px;">
        <h3>Equipe & Distribuição de Horas no Projeto</h3>
        <div class="small">Lista de todos os profissionais que já registraram tempo de dedicação nesta demanda.</div>

        <div class="tw" style="margin-top:10px;">
          <table>
            <thead>
              <tr>
                <th>Profissional / Membro</th>
                <th>Papel / Perfil</th>
                <th style="text-align:center;">Lançamentos</th>
                <th style="text-align:center;">Horas Apontadas</th>
                <th>Participação no Esforço</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="member in projectTimeSummary.team_members" :key="member.user_id">
                <td>
                  <div style="display:flex; align-items:center; gap:6px;">
                    <div class="brand-icon" style="width:24px; height:24px; font-size:0.75rem; background:var(--purple);">
                      {{ member.user_name.charAt(0) }}
                    </div>
                    <div>
                      <strong style="color:var(--purple)">{{ member.user_name }}</strong>
                      <div class="small" style="color:var(--muted)">{{ member.user_email }}</div>
                    </div>
                  </div>
                </td>
                <td>
                  <span class="badge bpurple">{{ member.user_role }}</span>
                </td>
                <td style="text-align:center;">
                  <span class="badge bgray">{{ member.entries_count }}</span>
                </td>
                <td style="text-align:center;">
                  <strong style="color:var(--pink); font-size:0.86rem;">{{ member.total_hours }}h</strong>
                  <span class="small" style="color:var(--muted); margin-left:2px;">({{ member.total_minutes }}m)</span>
                </td>
                <td style="min-width:130px;">
                  <div style="display:flex; align-items:center; gap:6px;">
                    <div class="track" style="flex:1;">
                      <div class="fill" style="background:var(--pink);" :style="{ width: member.percentage + '%' }"></div>
                    </div>
                    <strong style="font-size:0.78rem;">{{ member.percentage }}%</strong>
                  </div>
                </td>
              </tr>

              <tr v-if="!projectTimeSummary.team_members || projectTimeSummary.team_members.length === 0">
                <td colspan="5" style="text-align:center; padding:25px; color:var(--muted)">
                  Nenhum registro de horas efetuado para este projeto ainda. Inicie o timetracker ou aponte horas em uma atividade!
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- CARD 2: HISTÓRICO COMPLETO DE APONTAMENTOS -->
      <div class="card" style="margin-top:14px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <div>
            <h3>Histórico Completo de Apontamentos da Demanda</h3>
            <div class="small">Log cronológico de cada sessão de trabalho e descrição do esforço executado.</div>
          </div>
          <span class="badge bpurple">{{ projectTimeSummary.entries?.length || 0 }} registros</span>
        </div>

        <div class="tw" style="max-height:420px;">
          <table>
            <thead>
              <tr>
                <th style="width:90px;">Data</th>
                <th>Profissional</th>
                <th>Entregável</th>
                <th>Atividade</th>
                <th style="text-align:center;">Tempo</th>
                <th>Descrição / Notas</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="entry in projectTimeSummary.entries" :key="entry.id">
                <td><span style="font-weight:700;">{{ formatDateTime(entry.date_recorded) }}</span></td>
                <td>
                  <strong style="color:var(--purple)">👤 {{ entry.user_name }}</strong>
                </td>
                <td>
                  <span class="badge bpurple">{{ entry.deliverable_name }}</span>
                </td>
                <td>
                  <strong>{{ entry.activity_name }}</strong>
                </td>
                <td style="text-align:center;">
                  <span class="badge bpink" style="font-weight:800;">
                    ⏱️ {{ entry.time_spent_hours }}h ({{ entry.time_spent_minutes }}m)
                  </span>
                </td>
                <td>
                  <span style="color:#493E54;">{{ entry.description }}</span>
                </td>
              </tr>

              <tr v-if="!projectTimeSummary.entries || projectTimeSummary.entries.length === 0">
                <td colspan="6" style="text-align:center; padding:25px; color:var(--muted)">
                  Nenhum apontamento registrado nesta demanda.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- MODAL 1: EDITAR PROJETO -->
    <div v-if="showEditProjectModal" class="modal-backdrop" @click.self="showEditProjectModal = false">
      <div class="modal-content" style="max-width:560px;">
        <div class="modal-header">
          <h2>Editar Detalhes do Projeto</h2>
          <button class="modal-close" @click="showEditProjectModal = false">×</button>
        </div>
        <form @submit.prevent="handleSaveProject">
          <div class="form-group">
            <label>Nome do Projeto *</label>
            <input v-model="projectForm.name" required class="form-control" />
          </div>

          <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
            <div class="form-group">
              <label>Área / Cliente</label>
              <select v-model="projectForm.area_id" class="form-control">
                <option :value="null">Selecione uma área...</option>
                <option v-for="a in areasList" :key="a.id" :value="a.id">
                  🏢 {{ a.name }}
                </option>
              </select>
            </div>
            <div class="form-group">
              <label>Owner (Líder / Condutor)</label>
              <select v-model="projectForm.owner_id" class="form-control">
                <option :value="null">Selecione o owner...</option>
                <option v-for="u in usersList" :key="u.id" :value="u.id">
                  👤 {{ u.name }}
                </option>
              </select>
            </div>
          </div>

          <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
            <div class="form-group">
              <label>Número do Chamado / Ticket</label>
              <input v-model="projectForm.ticket_number" class="form-control" placeholder="ex: CH-4589" />
            </div>
            <div class="form-group">
              <label>Solicitante</label>
              <input v-model="projectForm.requester" class="form-control" placeholder="ex: João Silva" />
            </div>
          </div>

          <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
            <div class="form-group">
              <label>Status</label>
              <select v-model="projectForm.status" class="form-control">
                <option value="Não Iniciado">Não Iniciado</option>
                <option value="Em Andamento">Em Andamento</option>
                <option value="Concluído">Concluído</option>
                <option value="StandBy">StandBy</option>
                <option value="Em Espera">Em Espera</option>
                <option value="Cancelado">Cancelado</option>
              </select>
            </div>
            <div class="form-group">
              <label>Prioridade</label>
              <select v-model="projectForm.priority" class="form-control">
                <option value="Normal">Normal</option>
                <option value="Alta">Alta</option>
                <option value="Crítica">Crítica</option>
                <option value="Média">Média</option>
                <option value="Baixa">Baixa</option>
                <option value="🎯 Executivo">🎯 Executivo</option>
              </select>
            </div>
          </div>

          <div class="form-group">
            <label>Comentários do Projeto</label>
            <textarea v-model="projectForm.comments" class="form-control" placeholder="Observações gerais..."></textarea>
          </div>

          <div style="display:flex; justify-content:flex-end; gap:8px; margin-top:14px;">
            <button type="button" class="btn secondary" @click="showEditProjectModal = false">Cancelar</button>
            <button type="submit" class="btn">Salvar Projeto</button>
          </div>
        </form>
      </div>
    </div>

    <!-- MODAL 2: CRIAR / EDITAR ENTREGÁVEL -->
    <div v-if="showDeliverableModal" class="modal-backdrop" @click.self="showDeliverableModal = false">
      <div class="modal-content" style="max-width:500px;">
        <div class="modal-header">
          <h2>{{ editingDeliverableId ? 'Editar Entregável' : 'Novo Entregável' }}</h2>
          <button class="modal-close" @click="showDeliverableModal = false">×</button>
        </div>
        <form @submit.prevent="handleSaveDeliverable">
          <div class="form-group">
            <label>Nome do Entregável *</label>
            <input v-model="deliverableForm.name" required class="form-control" placeholder="ex: Fase 1 - Levantamento & Arquitetura" />
          </div>

          <div class="form-group">
            <label>Status</label>
            <select v-model="deliverableForm.status" class="form-control">
              <option value="Não Iniciado">Não Iniciado</option>
              <option value="Em Andamento">Em Andamento</option>
              <option value="Concluído">Concluído</option>
              <option value="StandBy">StandBy</option>
              <option value="Em Espera">Em Espera</option>
              <option value="Cancelado">Cancelado</option>
            </select>
          </div>

          <div class="form-group">
            <label>Descrição / Comentários do Entregável</label>
            <textarea v-model="deliverableForm.comments" class="form-control" placeholder="Objetivo e escopo desta entrega..."></textarea>
          </div>

          <div style="display:flex; justify-content:flex-end; gap:8px; margin-top:14px;">
            <button type="button" class="btn secondary" @click="showDeliverableModal = false">Cancelar</button>
            <button type="submit" class="btn">{{ editingDeliverableId ? 'Atualizar' : 'Criar Entregável' }}</button>
          </div>
        </form>
      </div>
    </div>

    <!-- MODAL 3: CRIAR / EDITAR ATIVIDADE -->
    <div v-if="showActivityModal" class="modal-backdrop" @click.self="showActivityModal = false">
      <div class="modal-content" style="max-width:540px;">
        <div class="modal-header">
          <h2>{{ editingActivityId ? 'Editar Atividade' : 'Nova Atividade' }}</h2>
          <button class="modal-close" @click="showActivityModal = false">×</button>
        </div>
        <form @submit.prevent="handleSaveActivity">
          <div class="form-group">
            <label>Nome da Atividade *</label>
            <input v-model="activityForm.name" required class="form-control" placeholder="ex: Criar fluxos de ETL e APIs" />
          </div>

          <div class="form-group">
            <label>Vincular ao Entregável</label>
            <select v-model="activityForm.deliverable_id" class="form-control">
              <option :value="null">Sem entregável (Atividade Geral)</option>
              <option v-for="d in projectDeliverables" :key="d.id" :value="d.id">
                📦 {{ d.name }}
              </option>
            </select>
          </div>

          <div class="form-group">
            <label>Responsável Técnico da Demanda (Lista)</label>
            <select v-model="activityForm.assignee_id" class="form-control">
              <option :value="null">Selecione o responsável técnico...</option>
              <option v-for="u in usersList" :key="u.id" :value="u.id">
                👤 {{ u.name }} ({{ u.role }})
              </option>
            </select>
          </div>

          <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
            <div class="form-group">
              <label>Status</label>
              <select v-model="activityForm.status" class="form-control">
                <option value="Não Iniciado">Não Iniciado</option>
                <option value="Em Andamento">Em Andamento</option>
                <option value="Concluído">Concluído</option>
                <option value="StandBy">StandBy</option>
                <option value="Em Espera">Em Espera</option>
                <option value="Cancelado">Cancelado</option>
              </select>
            </div>
            <div class="form-group">
              <label>Progresso (%)</label>
              <input v-model.number="activityForm.progress" type="number" min="0" max="100" class="form-control" />
            </div>
          </div>

          <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
            <div class="form-group">
              <label>Data de Início Prevista</label>
              <input v-model="activityForm.start_date" type="date" class="form-control" />
            </div>
            <div class="form-group">
              <label>Data de Término Prevista</label>
              <input v-model="activityForm.end_date" type="date" class="form-control" />
            </div>
          </div>

          <div class="form-group">
            <label>Descrição do Entregável / Atividade</label>
            <input v-model="activityForm.description" class="form-control" placeholder="Resumo do escopo..." />
          </div>

          <div class="form-group">
            <label>Área de Comentários / Observações da Atividade</label>
            <textarea v-model="activityForm.comments" class="form-control" placeholder="Comentários sobre execução, dependências ou impedimentos..."></textarea>
          </div>

          <div style="display:flex; justify-content:flex-end; gap:8px; margin-top:14px;">
            <button type="button" class="btn secondary" @click="showActivityModal = false">Cancelar</button>
            <button type="submit" class="btn">{{ editingActivityId ? 'Salvar Alterações' : 'Criar Atividade' }}</button>
          </div>
        </form>
      </div>
    </div>

    <!-- MODAL 4: APONTAMENTO MANUAL DE HORAS -->
    <div v-if="showManualModal" class="modal-backdrop" @click.self="showManualModal = false">
      <div class="modal-content">
        <div class="modal-header">
          <h2>Apontar Horas na Atividade</h2>
          <button class="modal-close" @click="showManualModal = false">×</button>
        </div>
        <div>
          <p style="margin:0 0 8px; font-size:0.82rem; color:var(--muted)">
            Atividade: <strong>{{ selectedActivity?.name }}</strong>
          </p>
          <div class="form-group">
            <label>Tempo Trabalhado (Minutos) *</label>
            <input v-model.number="manualMinutes" type="number" min="1" class="form-control" placeholder="ex: 60" />
          </div>
          <div class="form-group">
            <label>Descrição do que foi realizado</label>
            <textarea v-model="manualDescription" class="form-control" placeholder="Notas sobre o que foi executado..."></textarea>
          </div>
          <div style="display:flex; justify-content:flex-end; gap:8px; margin-top:14px;">
            <button class="btn secondary" @click="showManualModal = false">Cancelar</button>
            <button class="btn pink" @click="confirmManualLog">Registrar Horas</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useRoadmapStore } from '@/stores/roadmap'
import { useAuthStore } from '@/stores/auth'
import { useTimetrackerStore } from '@/stores/timetracker'
import GanttChart from '@/components/GanttChart.vue'
import api from '@/services/api'

const route = useRoute()
const roadmapStore = useRoadmapStore()
const authStore = useAuthStore()
const timetrackerStore = useTimetrackerStore()

const projectId = parseInt(route.params.id)
const activeViewTab = ref('deliverables')
const usersList = ref([])
const areasList = ref([])

// Controle de Accordion (quais entregáveis estão expandidos)
const expandedGroups = ref(new Set(['general']))

// Histórico e Resumo de Horas do Projeto
const projectTimeSummary = ref({
  project_id: projectId,
  total_minutes: 0,
  total_hours: 0,
  entries_count: 0,
  team_members: [],
  entries: []
})

async function loadProjectTimeSummary() {
  try {
    const res = await api.get(`/timetracker/project/${projectId}`)
    projectTimeSummary.value = res.data
  } catch (err) {
    console.error('Erro ao carregar resumo de horas do projeto:', err)
  }
}

onMounted(async () => {
  try {
    const [uRes, aRes] = await Promise.all([
      api.get('/users/'),
      api.get('/areas/'),
      loadProjectTimeSummary()
    ])
    usersList.value = uRes.data
    areasList.value = aRes.data
  } catch (err) {
    console.error('Erro ao buscar dados auxiliares:', err)
  }
})

const project = computed(() => {
  return roadmapStore.projects.find(p => p.id === projectId)
})

const projectDeliverables = computed(() => {
  return roadmapStore.deliverables.filter(d => d.project_id === projectId)
})

const projectActivities = computed(() => {
  return roadmapStore.activities.filter(a => a.project_id === projectId)
})

function isActivityDelayed(ativ) {
  if (!ativ) return false
  if (ativ.is_delayed !== undefined && ativ.is_delayed !== null) {
    return Boolean(ativ.is_delayed)
  }
  if (!ativ.end_date || ativ.status === 'Concluído' || (ativ.progress !== null && ativ.progress >= 100)) {
    return false
  }
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return new Date(ativ.end_date + 'T00:00:00') < today
}

const projectTotalActivities = computed(() => projectActivities.value.length)
const projectCompletedActivities = computed(() => {
  return projectActivities.value.filter(a => a.status === 'Concluído' || a.progress >= 100).length
})
const projectDelayedActivities = computed(() => {
  return projectActivities.value.filter(a => isActivityDelayed(a)).length
})

const projectTotalHours = computed(() => {
  return projectTimeSummary.value.total_hours || project.value?.total_tracked_hours || 0
})

const projectTotalMinutes = computed(() => {
  return projectTimeSummary.value.total_minutes || project.value?.total_tracked_minutes || 0
})

// Agrupamento Hierárquico: Entregáveis com suas Atividades
const deliverableGroups = computed(() => {
  const groups = []

  // 1. Entregáveis formais cadastrados
  projectDeliverables.value.forEach(d => {
    const ativs = projectActivities.value.filter(a => a.deliverable_id === d.id)
    const completed = ativs.filter(a => a.status === 'Concluído' || a.progress >= 100).length
    const delayed = ativs.filter(a => isActivityDelayed(a)).length
    const calcMin = ativs.reduce((sum, a) => sum + (a.total_tracked_minutes || 0), 0)
    const trackedHours = d.total_tracked_hours || (calcMin > 0 ? (calcMin / 60.0).toFixed(1) : 0)

    groups.push({
      id: d.id,
      name: d.name,
      status: d.status,
      comments: d.comments || d.description,
      start_date: d.start_date,
      end_date: d.end_date,
      progress: d.progress,
      totalActivities: ativs.length,
      completedActivities: completed,
      delayedActivities: delayed,
      trackedHours,
      activities: ativs,
      raw: d
    })
  })

  // 2. Atividades que ainda não têm entregável associado
  const unassignedAtivs = projectActivities.value.filter(a => !a.deliverable_id)
  if (unassignedAtivs.length > 0) {
    const completed = unassignedAtivs.filter(a => a.status === 'Concluído' || a.progress >= 100).length
    const delayed = unassignedAtivs.filter(a => isActivityDelayed(a)).length
    const prog = unassignedAtivs.length > 0 ? ((completed / unassignedAtivs.length) * 100).toFixed(0) : 0
    const calcMin = unassignedAtivs.reduce((sum, a) => sum + (a.total_tracked_minutes || 0), 0)
    const trackedHours = calcMin > 0 ? (calcMin / 60.0).toFixed(1) : 0

    groups.unshift({
      id: 'general',
      name: 'Entregáveis & Etapas Gerais',
      status: prog >= 100 ? 'Concluído' : 'Em Andamento',
      comments: 'Atividades e tarefas diretas do projeto',
      start_date: project.value?.start_date,
      end_date: project.value?.end_date,
      progress: prog,
      totalActivities: unassignedAtivs.length,
      completedActivities: completed,
      delayedActivities: delayed,
      trackedHours,
      activities: unassignedAtivs,
      raw: null
    })
  }

  return groups
})

// Funções de Accordion
function isExpanded(groupId) {
  return expandedGroups.value.has(groupId)
}

function toggleGroup(groupId) {
  if (expandedGroups.value.has(groupId)) {
    expandedGroups.value.delete(groupId)
  } else {
    expandedGroups.value.add(groupId)
  }
}

function setAllExpanded(show) {
  if (show) {
    deliverableGroups.value.forEach(g => expandedGroups.value.add(g.id))
  } else {
    expandedGroups.value.clear()
  }
}

// Gantt Unificado
const ganttItems = computed(() => {
  const items = []
  projectDeliverables.value.forEach(d => {
    items.push({
      id: `deliv-${d.id}`,
      code: `ENT-${String(d.id).padStart(3, '0')}`,
      name: `📦 ${d.name}`,
      start_date: d.start_date,
      end_date: d.end_date,
      progress: d.progress,
      status: d.status
    })
  })
  projectActivities.value.forEach(a => {
    items.push({
      id: a.id,
      code: `ATIV-${String(a.id).padStart(4, '0')}`,
      name: a.name,
      start_date: a.start_date,
      end_date: a.end_date,
      progress: a.progress,
      status: a.status,
      is_delayed: isActivityDelayed(a)
    })
  })
  return items
})

// MODAL EDITAR PROJETO
const showEditProjectModal = ref(false)
const projectForm = ref({})

function openEditProjectModal() {
  projectForm.value = {
    name: project.value.name,
    area_id: project.value.area_id,
    owner_id: project.value.owner_id,
    ticket_number: project.value.ticket_number || '',
    requester: project.value.requester || '',
    status: project.value.status || 'Não Iniciado',
    priority: project.value.priority || 'Normal',
    comments: project.value.comments || ''
  }
  showEditProjectModal.value = true
}

async function handleSaveProject() {
  try {
    await roadmapStore.updateProject(projectId, projectForm.value)
    showEditProjectModal.value = false
    await Promise.all([roadmapStore.fetchAll(), loadProjectTimeSummary()])
  } catch (err) {
    alert(err.response?.data?.detail || 'Erro ao atualizar projeto.')
  }
}

// MODAL ENTREGÁVEIS
const showDeliverableModal = ref(false)
const editingDeliverableId = ref(null)
const deliverableForm = ref({
  name: '',
  comments: '',
  status: 'Não Iniciado'
})

function openCreateDeliverableModal() {
  editingDeliverableId.value = null
  deliverableForm.value = {
    name: '',
    comments: '',
    status: 'Não Iniciado',
    project_id: projectId
  }
  showDeliverableModal.value = true
}

function openEditDeliverableModal(d) {
  editingDeliverableId.value = d.id
  deliverableForm.value = {
    name: d.name,
    comments: d.comments || d.description || '',
    status: d.status || 'Não Iniciado'
  }
  showDeliverableModal.value = true
}

async function handleSaveDeliverable() {
  try {
    if (editingDeliverableId.value) {
      await roadmapStore.updateDeliverable(editingDeliverableId.value, deliverableForm.value)
    } else {
      deliverableForm.value.project_id = projectId
      const created = await roadmapStore.createDeliverable(deliverableForm.value)
      expandedGroups.value.add(created.id)
    }
    showDeliverableModal.value = false
    await Promise.all([roadmapStore.fetchAll(), loadProjectTimeSummary()])
  } catch (err) {
    alert(err.response?.data?.detail || 'Erro ao salvar entregável.')
  }
}

async function confirmDeleteDeliverable(d) {
  if (confirm(`Tem certeza que deseja excluir o entregável "${d.name}"? As atividades vinculadas a ele ficarão sem entregável.`)) {
    try {
      await roadmapStore.deleteDeliverable(d.id)
      await Promise.all([roadmapStore.fetchAll(), loadProjectTimeSummary()])
    } catch (err) {
      alert('Erro ao excluir entregável.')
    }
  }
}

// MODAL ATIVIDADES
const showActivityModal = ref(false)
const editingActivityId = ref(null)
const activityForm = ref({
  name: '',
  deliverable_id: null,
  assignee_id: null,
  status: 'Não Iniciado',
  progress: 0,
  start_date: '',
  end_date: '',
  description: '',
  comments: ''
})

function openCreateActivityModal(targetDeliverableId = null) {
  editingActivityId.value = null
  activityForm.value = {
    name: '',
    deliverable_id: targetDeliverableId === 'general' ? null : targetDeliverableId,
    assignee_id: authStore.user?.id || null,
    status: 'Não Iniciado',
    progress: 0,
    start_date: '',
    end_date: '',
    description: '',
    comments: '',
    project_id: projectId
  }
  showActivityModal.value = true
}

function openEditActivityModal(ativ) {
  editingActivityId.value = ativ.id
  activityForm.value = {
    name: ativ.name,
    deliverable_id: ativ.deliverable_id || null,
    assignee_id: ativ.assignee_id || null,
    status: ativ.status || 'Não Iniciado',
    progress: ativ.progress || 0,
    start_date: ativ.start_date || '',
    end_date: ativ.end_date || '',
    description: ativ.description || '',
    comments: ativ.comments || ''
  }
  showActivityModal.value = true
}

async function handleSaveActivity() {
  try {
    if (editingActivityId.value) {
      await roadmapStore.updateActivity(editingActivityId.value, activityForm.value)
    } else {
      activityForm.value.project_id = projectId
      await roadmapStore.createActivity(activityForm.value)
      if (activityForm.value.deliverable_id) {
        expandedGroups.value.add(activityForm.value.deliverable_id)
      }
    }
    showActivityModal.value = false
    await Promise.all([roadmapStore.fetchAll(), loadProjectTimeSummary()])
  } catch (err) {
    alert(err.response?.data?.detail || 'Erro ao salvar atividade.')
  }
}

async function confirmDeleteActivity(ativ) {
  if (confirm(`Tem certeza que deseja excluir a atividade "${ativ.name}"?`)) {
    try {
      await roadmapStore.deleteActivity(ativ.id)
      await Promise.all([roadmapStore.fetchAll(), loadProjectTimeSummary()])
    } catch (err) {
      alert('Erro ao excluir atividade.')
    }
  }
}

// TIMETRACKER MANUAL & REALTIME
const showManualModal = ref(false)
const selectedActivity = ref(null)
const manualMinutes = ref(60)
const manualDescription = ref('')

function openManualTimeModal(ativ) {
  selectedActivity.value = ativ
  manualMinutes.value = 60
  manualDescription.value = ''
  showManualModal.value = true
}

async function confirmManualLog() {
  if (!selectedActivity.value) return
  await timetrackerStore.logTime(
    selectedActivity.value.id,
    manualMinutes.value,
    manualDescription.value
  )
  showManualModal.value = false
  await Promise.all([roadmapStore.fetchAll(), loadProjectTimeSummary()])
  alert('Horas apontadas com sucesso!')
}

async function handleStartTimer(ativ) {
  const hadOtherTimer = timetrackerStore.activeTimer && timetrackerStore.activeTimer.activityId !== ativ.id
  await timetrackerStore.startTimer(ativ)
  if (hadOtherTimer) {
    await Promise.all([roadmapStore.fetchAll(), loadProjectTimeSummary()])
  }
}

async function handleStopTimer() {
  await timetrackerStore.stopTimer()
  await Promise.all([roadmapStore.fetchAll(), loadProjectTimeSummary()])
}

function formatDate(d) {
  if (!d) return '—'
  return new Date(d + 'T00:00:00').toLocaleDateString('pt-BR')
}

function formatDateTime(dtStr) {
  if (!dtStr) return '—'
  const d = new Date(dtStr)
  return d.toLocaleDateString('pt-BR') + ' ' + d.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
}

function getStatusClass(s) {
  if (s === 'Concluído') return 'bgreen'
  if (s === 'Em Andamento') return 'bpurple'
  if (s === 'Em Espera' || s === 'StandBy') return 'byellow'
  if (s === 'Cancelado') return 'bred'
  return 'bgray'
}

function getPriorityClass(p) {
  if (p === 'Crítica') return 'bred'
  if (p === 'Alta') return 'bpink'
  if (p === '🎯 Executivo') return 'bpurple'
  return 'bgray'
}
</script>
