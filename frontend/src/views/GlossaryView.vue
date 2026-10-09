<template>
  <div>
    <div class="title">Glossário & Regras de Negócio</div>
    <div class="sub">Documentação das fórmulas, métricas e convenções de farol adotadas no sistema.</div>

    <div class="grid2" style="margin-top:10px;">
      <div class="card">
        <h3>Total de Projetos</h3>
        <div class="callout">
          <strong>Fórmula:</strong> Contagem única de projetos cadastrados no portfólio.<br>
          Representa a carteira global monitorada.
        </div>
      </div>

      <div class="card">
        <h3>Conclusão de Projetos (%)</h3>
        <div class="callout">
          <strong>Fórmula:</strong> (Projetos com status 'Concluído' ou progresso = 100%) / Total de Projetos * 100.
        </div>
      </div>

      <div class="card">
        <h3>Projetos Atrasados</h3>
        <div class="callout warning">
          <strong>Regra:</strong> Projetos com Data de Término menor que a data de Hoje e cujo status não seja 'Concluído'.
        </div>
      </div>

      <div class="card">
        <h3>Timetracker & Apontamentos</h3>
        <div class="callout">
          <strong>Regra de Negócio:</strong> Analistas registram o tempo gasto em cada atividade atribuída. O sistema acumula as horas e fornece transparência de produtividade e esforço real vs planejado.
        </div>
      </div>
    </div>
  </div>
</template>

