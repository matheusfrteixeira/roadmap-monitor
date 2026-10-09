<template>
  <div>
    <div class="title">📘 Documentação do Usuário & Manual de Utilização</div>
    <div class="sub">Guia operacional com regras de negócio, fluxos de demandas e boas práticas do RoadMap Corp.</div>

    <div class="grid2" style="margin-top:14px;">
      <!-- CARD 1: VISÃO GERAL E CONCEITOS -->
      <div class="card">
        <h3>1. Estrutura do Sistema & Papéis de Acesso (RBAC)</h3>
        <div class="callout" style="margin-top:8px;">
          O sistema separa as permissões em 3 níveis bem definidos:
          <ul style="margin:6px 0 0; padding-left:18px;">
            <li><strong>Administrador:</strong> Controle total. Gerencia áreas/clientes, usuários, atribui gestores imediatos e audita o sistema.</li>
            <li><strong>Gestor:</strong> Conduz projetos (Owner), acompanha o portfólio executivo e visualiza o calendário diário de toda a sua equipe direta.</li>
            <li><strong>Analista:</strong> Foco em execução. Atualiza o status e progresso de suas atividades e registra seu tempo no Timetracker.</li>
          </ul>
        </div>
      </div>

      <!-- CARD 2: CÁLCULOS AUTOMÁTICOS -->
      <div class="card">
        <h3>2. Automação de Prazos e Progresso do Projeto</h3>
        <div class="callout warning" style="margin-top:8px;">
          <strong>Regra de Cálculo Automático:</strong>
          <p style="margin:4px 0;">
            Você não precisa calcular o início, término ou progresso do projeto manualmente:
          </p>
          <ul style="margin:4px 0 0; padding-left:18px;">
            <li><strong>Início do Projeto:</strong> Menor data de início entre todas as atividades vinculadas.</li>
            <li><strong>Término do Projeto:</strong> Maior data de término entre todas as atividades vinculadas.</li>
            <li><strong>Progresso Geral (%):</strong> (Quantidade de atividades concluídas ÷ Total de atividades do projeto) × 100.</li>
          </ul>
        </div>
      </div>

      <!-- CARD 3: FLUXO DE DEMANDAS -->
      <div class="card">
        <h3>3. Fluxo de Criação de Projetos e Atividades</h3>
        <div class="callout" style="margin-top:8px;">
          <strong>Como cadastrar e conduzir uma demanda:</strong>
          <ol style="margin:6px 0 0; padding-left:18px; line-height:1.6;">
            <li>Na aba <strong>Portfólio de Projetos</strong>, clique em <strong>"+ Novo Projeto"</strong>.</li>
            <li>Selecione a <strong>Área/Cliente</strong> (ex: RH - DHO, Cliente XPTO).</li>
            <li>Informe o <strong>Chamado / Solicitação</strong> (se existir) e o <strong>Solicitante</strong>.</li>
            <li>Defina o <strong>Owner</strong> que liderará a entrega e comentários estratégicos.</li>
            <li>Entre no projeto para cadastrar as <strong>Atividades</strong> com seus respectivos responsáveis técnicos.</li>
          </ol>
        </div>
      </div>

      <!-- CARD 4: TIMETRACKER E CALENDÁRIO -->
      <div class="card">
        <h3>4. Como Utilizar o Timetracker & Acompanhamento</h3>
        <div class="callout" style="margin-top:8px;">
          <strong>Controle de Tempo e Produtividade:</strong>
          <ul style="margin:6px 0 0; padding-left:18px; line-height:1.6;">
            <li><strong>Cronômetro em Tempo Real:</strong> Clique em <strong>"▶️ Iniciar"</strong> na atividade que estiver executando. A barra no topo acompanhará o tempo mesmo se você trocar de tela.</li>
            <li><strong>Finalizar Sessão:</strong> Clique em <strong>"⏹️ Parar & Gravar"</strong> e descreva o que foi concluído.</li>
            <li><strong>Lançamento Manual:</strong> Use o botão <strong>"+ Horas"</strong> para apontamentos retroativos.</li>
            <li><strong>Acompanhamento Diário:</strong> Acesse a aba <strong>📅 Acompanhamento Diário</strong> para ver a produção do dia. Gestores têm visão consolidada de seus subordinados diretos.</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

