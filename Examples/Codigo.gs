function doGet() {
  return HtmlService.createHtmlOutputFromFile('Index')
      .setTitle('Roadmap Corporate Monitor')
      .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

function getDashboardData() {
  // Lê a aba exata do seu Roadmap
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Road Map Completo');
  if (!sheet) return { error: "Aba 'Road Map Completo' não encontrada." };
  
  const data = sheet.getDataRange().getValues();

  const DB = {
    generated_at: new Date().toISOString().split('T')[0],
    projects: [],
    items: []
  };

  let projCount = 0;
  let itemCount = 0;
  let currentProject = null;
  const today = new Date();
  today.setHours(0,0,0,0);

  // O Excel "DemandasCopiaRoadmap" tem os cabeçalhos na linha 6 (índice 5) e os dados começam na 8 (índice 7)
  for (let i = 6; i < data.length; i++) {
    const row = data[i];
    const escopo = row[1]; // Coluna B: Escopo
    if (!escopo) continue;

    const nome = row[4] || ''; // Coluna E: Projeto / Nome da Tarefa
    if (!nome) continue;

    const area = row[2] || 'Não especificada'; // C
    const prioridade = row[3] || 'Não especificada'; // D
    const comentario = row[5] || ''; // F
    const solicitante = row[7] || 'Não especificado'; // H
    const responsavel = row[8] || 'Não especificado'; // I
    const owner = row[9] || 'Não especificado'; // J
    const status = row[10] || ''; // K
    const inicioDate = row[11]; // L
    const terminoDate = row[12]; // M
    const progresso = parseFloat(row[13]) || 0; // N

    let inicioStr = (inicioDate instanceof Date) ? inicioDate.toISOString().split('T')[0] : "";
    let terminoStr = (terminoDate instanceof Date) ? terminoDate.toISOString().split('T')[0] : "";

    if (escopo === 'Projeto Geral') {
      projCount++;
      let isAtrasado = 0;
      let diasAtraso = 0;
      if (terminoDate instanceof Date && status !== 'Concluído' && terminoDate < today) {
         isAtrasado = 1;
         diasAtraso = Math.ceil(Math.abs(today - terminoDate) / (1000 * 60 * 60 * 24));
      }

      currentProject = {
        id: "PROJ-" + String(projCount).padStart(3, '0'),
        rm_row: i + 1,
        nome: nome,
        area: area,
        prioridade: prioridade,
        owner: owner,
        status: status,
        situacao: (status === 'Concluído') ? 'Concluído' : 'Não concluído',
        progresso: progresso,
        inicio: inicioStr,
        termino: terminoStr,
        total_ativ: 0,
        concl_ativ: 0,
        is_atrasado: isAtrasado,
        dias_atraso: diasAtraso,
        solicitante: solicitante,
        responsavel: responsavel,
        activities: []
      };
      DB.projects.push(currentProject);
      
    } else {
      itemCount++;
      if (escopo === 'Atividade' && currentProject) {
         currentProject.total_ativ++;
         if (status === 'Concluído') currentProject.concl_ativ++;
      }

      const item = {
        id: "ITEM-" + String(itemCount).padStart(4, '0'),
        rm_row: i + 1,
        project_rm_row: currentProject ? currentProject.rm_row : null,
        escopo: escopo,
        projeto: currentProject ? currentProject.nome : '',
        item_nome: nome,
        area: currentProject ? currentProject.area : area,
        prioridade: currentProject ? currentProject.prioridade : prioridade,
        owner: currentProject ? currentProject.owner : owner,
        status_projeto: currentProject ? currentProject.status : '',
        situacao: currentProject ? currentProject.situacao : '',
        status_item: status || 'Não Iniciado',
        is_task: escopo === 'Atividade',
        inicio: inicioStr,
        termino: terminoStr,
        solicitante: solicitante,
        responsavel: responsavel,
        descricao: comentario
      };
      DB.items.push(item);
      
      if (currentProject) {
        currentProject.activities.push({
          rm_row: item.rm_row, escopo: item.escopo, nome: item.item_nome,
          status: item.status_item, inicio: item.inicio, termino: item.termino,
          progresso: progresso, solicitante: item.solicitante,
          responsavel: item.responsavel, descricao: item.descricao
        });
      }
    }
  }

  DB.total_projects = DB.projects.length;
  DB.total_items = DB.items.length;
  return DB;
}