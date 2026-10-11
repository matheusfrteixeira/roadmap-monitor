# 📘 Documentação Técnica do Backend - RoadMap Corporate Monitor

Esta documentação fornece uma visão aprofundada da arquitetura, modelagem de dados, regras de negócio, camada de serviços, segurança e o catálogo completo de endpoints da API do **RoadMap Corporate Monitor**.

---

## 1. Visão Geral & Tecnologias

A API do **RoadMap Corporate Monitor** é construída em Python utilizando o framework **FastAPI**, oferecendo alta performance assíncrona, documentação OpenAPI/Swagger automática e validação tipada de contratos através do **Pydantic v2**. O armazenamento relacional é gerenciado pelo **SQLAlchemy 2.0 ORM** com migrações via **Alembic** e banco de dados **MySQL 8.0**.

### 🛠️ Stack Tecnológica

| Componente | Tecnologia / Biblioteca | Função Principal |
| :--- | :--- | :--- |
| **Framework Web** | [FastAPI](https://fastapi.tiangolo.com/) (v0.109+) | Roteamento, validação de requisições e injeção de dependências |
| **ORM** | [SQLAlchemy 2.0](https://www.sqlalchemy.org/) | Modelagem relacional e abstração de consultas SQL |
| **Driver MySQL** | `PyMySQL` | Driver de conexão pura Python para MySQL 8.0 |
| **Validação / Schemas**| [Pydantic v2](https://docs.pydantic.dev/) | Schemas de entrada/saída e validações de tipos |
| **Autenticação & JWT** | `python-jose` + `passlib[bcrypt]` | Criptografia de senhas (bcrypt) e tokens JWT (Bearer) |
| **Migrações de Banco** | [Alembic](https://alembic.sqlalchemy.org/) | Controle de versão do esquema do banco de dados |
| **Servidor ASGI** | [Uvicorn](https://www.uvicorn.org/) | Servidor de aplicação assíncrono para execução da API |
| **Containerização** | [Docker Compose](https://docs.docker.com/compose/) | Orquestração do MySQL 8.0 e interface phpMyAdmin |

---

## 2. Arquitetura em Camadas

A aplicação adota o padrão em camadas com separação clara de responsabilidades (*Separation of Concerns*), permitindo fácil manutenção, desacoplamento e testabilidade:

```mermaid
flowchart TD
    Client["Cliente Frontend (Vue 3 / PrimeVue)"] -->|HTTP / JSON com Bearer Token| CORS["FastAPI App & Middlewares (CORS)"]
    
    subgraph Routing ["Camada de Controladores (app/api/routes)"]
        CORS --> Routers["API Routers (/api/auth, /api/projects, etc.)"]
        Routers --> Deps["Dependências (app/api/deps.py)"]
        Deps -.->|Verificação JWT & RBAC| Security["Segurança & Token"]
        Deps -.->|Sessão do Banco| DB_Session["SessionLocal"]
    end
    
    subgraph Business ["Camada de Regras de Negócio (app/services)"]
        Routers --> Services["Services (ProjectService, TimeEntryService, etc.)"]
        Services --> BusinessRules["Regras: Recálculo de Datas, Timers, Validações"]
    end
    
    subgraph Persistence ["Camada de Persistência (app/repositories)"]
        Services --> Repos["Repositories (ProjectRepo, ActivityRepo, etc.)"]
        Repos --> ORMModels["Modelos SQLAlchemy (app/models)"]
    end
    
    subgraph Database ["Infraestrutura de Banco de Dados"]
        ORMModels --> MySQL[("MySQL 8.0 Database")]
        ORMModels -.->|Event Listeners before_flush| Audit["app/db/audit.py (Auditoria Automática)"]
        Audit -->|Registra deltas JSON| AuditTable[("Tabela audit_logs")]
    end
```

### Divisão das Pastas do Backend

```text
backend/
├── alembic/              # Scripts e versões de migração do banco de dados
├── app/
│   ├── api/              # Camada de controle HTTP e dependências
│   │   ├── routes/       # Módulos de rotas organizados por recurso
│   │   └── deps.py       # Injeção de dependências (get_db, get_current_user, require_role)
│   ├── core/             # Configurações globais e segurança
│   │   ├── config.py     # Variáveis de ambiente Pydantic Settings
│   │   └── security.py   # Funções de hash bcrypt e criação/verificação de JWT
│   ├── db/               # Infraestrutura de banco de dados
│   │   ├── audit.py      # SQLAlchemy listeners para auditoria automática
│   │   ├── base_class.py # Classe base declarativa SQLAlchemy
│   │   └── session.py    # Factory SessionLocal e Engine
│   ├── models/           # Modelos de entidades ORM (SQLAlchemy)
│   ├── repositories/     # Consultas e persistência direta no banco de dados
│   ├── schemas/          # Contratos de DTO (Data Transfer Objects) Pydantic
│   ├── services/         # Camada de regras de negócio e orquestração
│   └── main.py           # Ponto de entrada da aplicação FastAPI
├── create_admin.py       # Script utilitário para criar usuário administrador
├── docker-compose.yml    # Configuração de containers Docker (MySQL e phpMyAdmin)
├── requirements.txt      # Dependências Python do projeto
├── reset_database.py     # Script para reset seguro dos dados de teste
└── test_all_endpoints.py # Suíte de testes de integração via TestClient
```

---

## 3. Modelagem de Dados & Banco Relacional

O esquema do banco de dados foi projetado para garantir integridade referencial, rastreabilidade e flexibilidade na gestão de projetos hierárquicos:

```mermaid
erDiagram
    users ||--o{ users : "possui subordinados (manager_id)"
    users ||--o{ projects : "gerencia / é responsável (owner_id)"
    users ||--o{ activities : "é encarregado (assignee_id)"
    users ||--o{ time_entries : "lança horas (user_id)"
    users ||--o| active_timers : "possui no máximo 1 timer ativo (user_id)"
    users ||--o{ audit_logs : "autor da alteração (user_id)"

    areas ||--o{ projects : "pertence à área/cliente (area_id)"

    projects ||--o{ deliverables : "contém (project_id)"
    projects ||--o{ activities : "contém (project_id)"

    deliverables ||--o{ activities : "agrupa tarefas (deliverable_id)"

    activities ||--o{ time_entries : "recebe apontamentos (activity_id)"
    activities ||--o{ active_timers : "alvo do cronômetro (activity_id)"

    users {
        int id PK
        string name
        string email UK
        string hashed_password
        enum role "admin | gestor | analista"
        int manager_id FK "auto-relacionamento"
    }

    areas {
        int id PK
        string name UK
    }

    projects {
        int id PK
        string name
        string priority
        string status
        date start_date
        date end_date
        float progress
        string ticket_number
        string requester
        text comments
        int owner_id FK
        int area_id FK
    }

    deliverables {
        int id PK
        int project_id FK
        string name
        text description
        text comments
        string status
        date start_date
        date end_date
        float progress
        datetime created_at
        datetime updated_at
    }

    activities {
        int id PK
        string name
        text description
        text comments
        string status
        date start_date
        date end_date
        float progress
        int project_id FK
        int deliverable_id FK
        int assignee_id FK
    }

    time_entries {
        int id PK
        int time_spent_minutes
        text description
        datetime date_recorded
        int activity_id FK
        int user_id FK
    }

    active_timers {
        int id PK
        int user_id FK "UK (1 por usuário)"
        int activity_id FK
        datetime start_time
    }

    audit_logs {
        int id PK
        string table_name
        int record_id
        string action "INSERT | UPDATE | DELETE"
        json old_data
        json new_data
        datetime created_at
        int user_id FK
    }
```

---

## 4. Autenticação, Autorização e Segurança (RBAC)

O sistema implementa autenticação via **OAuth2 Password Bearer com Tokens JWT (JSON Web Tokens)** e autorização baseada em papéis (**Role-Based Access Control - RBAC**).

### Perfis de Usuário (`RoleEnum`)

1. **`admin` (Administrador)**:
   - Acesso irrestrito a todas as funcionalidades do sistema.
   - Permissão exclusiva para gerenciar usuários (`POST /api/users/`, `PUT /api/users/{id}`).
   - Permissão exclusiva para cadastrar, editar e excluir Áreas/Clientes (`/api/areas`).
   - Visibilidade completa de acompanhamento e apontamentos de qualquer colaborador.

2. **`gestor` (Gestor de Projetos / Equipe)**:
   - Criação e manutenção de Projetos, Entregáveis e Atividades.
   - Acompanhamento diário e semanal dos apontamentos de horas da sua equipe e subordinados diretos.
   - Atribuição de demandas aos analistas.

3. **`analista` (Colaborador / Executor)**:
   - Visualização de demandas e atividades sob sua responsabilidade.
   - Apontamento manual de horas e uso do cronômetro em tempo real.
   - Acompanhamento dos seus próprios lançamentos de horas.
   - Atualização de status e progresso das suas atividades.

### Dependências de Segurança (`app/api/deps.py`)

- `get_db()`: Gerador de sessão SQLAlchemy com fechamento automático no bloco `finally`.
- `get_current_user()`: Decodifica o JWT no cabeçalho `Authorization: Bearer <token>`, valida a expiração e busca o usuário no banco de dados.
- `require_role(roles: List[RoleEnum])`: Decorator/dependência que restringe o endpoint apenas aos perfis autorizados, disparando `403 Forbidden` caso o perfil do usuário não conste na lista permitida.

---

## 5. Sistema de Auditoria Automática

O backend conta com um mecanismo automático de auditoria implementado via listeners de eventos do SQLAlchemy (`app/db/audit.py`), desacoplado dos serviços e controladores.

### Funcionamento do Event Listener

O listener intercepta o evento `before_flush` da sessão SQLAlchemy:

```python
@event.listens_for(Session, 'before_flush')
def receive_before_flush(session: Session, flush_context, instances):
    ...
```

- **Operações INSERT**: O novo registro é serializado e inserido na tabela `audit_logs` com `action="INSERT"`, `old_data=None` e `new_data={campos e valores}`.
- **Operações UPDATE**: Utiliza `get_history(obj, column.name)` para identificar exatamente quais colunas sofreram alteração. Grava apenas as propriedades modificadas com os valores anteriores em `old_data` e os novos em `new_data`.
- **Operações DELETE**: Grava o estado final do objeto antes da remoção definitiva com `action="DELETE"` e `new_data=None`.
- **Serialização Robusta**: A função `serialize_value()` converte tipos como `datetime.date`, `datetime.datetime`, `Enum`, `Decimal` e objetos aninhados para formatos primitivos nativos de JSON.
- **Isolamento**: A própria tabela `audit_logs` é ignorada pelo listener para evitar loops de recursão.

---

## 6. Camada de Serviços (`app/services`) - Regras de Negócio

A camada de serviços encapsula todas as regras operacionais da aplicação, garantindo consistência e consistência de dados em operações complexas:

### 1. `UserService` (`app/services/user_service.py`)
- **Criação de Usuários**: Valida unicidade do e-mail; criptografa a senha com `bcrypt` antes da persistência.
- **Atualização**: Permite alteração de perfil (`role`), vínculo de gestor imediato (`manager_id`) e redefinição de senha opcional.
- **Enriquecimento (`_enrich_user`)**: Resolve dinamicamente o nome do gestor responsável para facilitar a renderização nas interfaces de listagem.

### 2. `AreaService` (`app/services/area_service.py`)
- **Validação de Nomes Únicos**: Impede o cadastro de áreas ou clientes homônimos, retornando erro descritivo `400 Bad Request`.
- **Gestão Cadastral**: CRUD restrito para administradores; fornece listagem para preenchimento de seletores no frontend.

### 3. `ProjectService` (`app/services/project_service.py`)
- **Métricas Agregadas (`_enrich_project`)**:
  - Calcula a contagem total de entregáveis e atividades.
  - Computa atividades concluídas (`status == 'Concluído'` ou `progress >= 100`).
  - Calcula atividades em atraso (`is_delayed`), comparando a data prevista de término com a data corrente (`date.today()`).
  - Totaliza horas e minutos apontados em todas as atividades do projeto.
  - Preenche nomes resolvidos de área, gestor e responsável.
- **Recálculo Dinâmico (`recalculate_project_metrics`)**:
  - Ajusta automaticamente a **data de início** do projeto para a menor data inicial entre suas atividades.
  - Ajusta a **data de término** para a maior data final entre suas atividades.
  - Calcula o **progresso percentual** baseado na proporção de atividades finalizadas.

### 4. `DeliverableService` (`app/services/deliverable_service.py`)
- **Gestão de Entregáveis / Marcos**: Agrupa tarefas intermediárias dentro de um projeto.
- **Recálculo de Entregáveis (`recalculate_deliverable_metrics`)**:
  - Calcula data de início e fim baseando-se nas atividades filhas.
  - Atualiza o progresso percentual ponderado do entregável.
  - Ajusta o status automaticamente para `"Em Andamento"` ou `"Concluído"`.
- **Cascateamento de Exclusão**: Ao remover um entregável, dispara automaticamente o recálculo das métricas do projeto pai.

### 5. `ActivityService` (`app/services/activity_service.py`)
- **Cálculo de Atraso em Tempo Real**: Define o atributo `is_delayed=True` quando a atividade não está concluída e sua `end_date` é anterior ao dia atual.
- **Efeito Dominó no Recálculo**:
  - A criação, edição ou exclusão de uma atividade recalcula imediatamente os marcos do entregável vinculado (`DeliverableService.recalculate_deliverable_metrics`).
  - Dispara o recálculo das datas e progresso geral do projeto pai (`ProjectService.recalculate_project_metrics`).
  - Ao transferir uma atividade de um entregável para outro, ambos os entregáveis têm suas métricas reajustadas.

### 6. `TimeEntryService` (`app/services/time_entry_service.py`)
- **Apontamento Manual (`log_time`)**: Registra horas gastas com validação da atividade existente.
- **Cronômetro Ativo (`ActiveTimer`)**:
  - **Unicidade de Sessão**: Cada colaborador pode ter no máximo 1 cronômetro rodando simultaneamente (chave única em `user_id`).
  - **Troca Inteligente de Tarefa (`start_active_timer`)**: Se o usuário iniciar o cronômetro em uma nova atividade enquanto outra já estava ativa, o serviço calcula automaticamente o tempo decorrido da anterior, salva como um apontamento com a observação *"Finalizado automaticamente ao alternar para: [Nome]"*, remove o timer antigo e inicia o novo.
  - **Fuso Horário UTC e Formatação**: Gera datas ISO com sufixo `Z` garantindo que o frontend exiba a contagem regressiva/progressiva perfeitamente sincronizada em qualquer timezone.
- **Resumo Financeiro e de Equipe (`get_project_time_summary`)**:
  - Agrupa horas por colaborador no projeto, calculando a porcentagem de dedicação de cada membro em relação ao total.
- **Visão de Calendário / Acompanhamento (`get_calendar_entries`)**:
  - Fornece a linha do tempo diária para o calendário semanal/mensal de acompanhamento, com suporte a filtros por colaborador.

---

## 7. Catálogo Completo de Endpoints da API

Todas as rotas (exceto o login e a rota raiz) exigem o envio do cabeçalho de autenticação:
`Authorization: Bearer <access_token>`

---

### 🔑 Autenticação (`/api/auth`)

#### `POST /api/auth/login`
- **Descrição**: Autentica o usuário e retorna o token de acesso JWT.
- **Content-Type**: `application/x-www-form-urlencoded` (Padrão OAuth2).
- **Parâmetros do Formulário**:
  - `username` (string): E-mail do usuário cadastrado.
  - `password` (string): Senha do usuário.
- **Resposta de Sucesso (`200 OK`)**:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
    "token_type": "bearer"
  }
  ```
- **Erros**: `400 Bad Request` ("Incorrect email or password").

---

### 👤 Usuários (`/api/users`)

#### `GET /api/users/me`
- **Descrição**: Retorna o perfil completo do usuário autenticado no token.
- **Permissão**: Qualquer usuário autenticado.
- **Resposta de Sucesso (`200 OK`)**:
  ```json
  {
    "id": 1,
    "name": "Administrador do Sistema",
    "email": "admin@roadmap.com",
    "role": "admin",
    "manager_id": null,
    "manager_name": null
  }
  ```

#### `GET /api/users/`
- **Descrição**: Lista todos os usuários ativos no sistema (utilizado para popular seletores de responsáveis e gestores).
- **Permissão**: Qualquer usuário autenticado.
- **Resposta de Sucesso (`200 OK`)**: Lista de `UserResponse`.

#### `POST /api/users/`
- **Descrição**: Cadastra um novo usuário no sistema com senha criptografada.
- **Permissão**: Exclusivo para perfil `admin`.
- **Payload (`application/json`)**:
  ```json
  {
    "name": "Carlos Silva",
    "email": "carlos.silva@empresa.com",
    "role": "analista",
    "manager_id": 2,
    "password": "senhaSegura123"
  }
  ```
- **Resposta de Sucesso (`200 OK`)**: `UserResponse` do usuário criado.
- **Erros**: `400 Bad Request` ("O email já está registrado.").

#### `PUT /api/users/{user_id}`
- **Descrição**: Atualiza dados cadastrais, cargo, gestor responsável e/ou senha de um usuário existente.
- **Permissão**: Exclusivo para perfil `admin`.
- **Payload (`application/json`)**:
  ```json
  {
    "name": "Carlos Silva Junior",
    "role": "gestor",
    "manager_id": 1,
    "password": "novaSenhaOpcional"
  }
  ```
- **Resposta de Sucesso (`200 OK`)**: `UserResponse` atualizado.

---

### 🏢 Áreas e Clientes (`/api/areas`)

#### `GET /api/areas/`
- **Descrição**: Retorna todas as áreas/clientes cadastradas.
- **Permissão**: Qualquer usuário autenticado.
- **Resposta de Sucesso (`200 OK`)**:
  ```json
  [
    { "id": 1, "name": "Recursos Humanos" },
    { "id": 2, "name": "Financeiro & Controladoria" }
  ]
  ```

#### `POST /api/areas/`
- **Descrição**: Cadastra uma nova área/cliente no sistema.
- **Permissão**: Exclusivo para perfil `admin`.
- **Payload**:
  ```json
  { "name": "Logística e Suprimentos" }
  ```
- **Resposta de Sucesso (`200 OK`)**: Objeto da área criada com `id` e `name`.

#### `PUT /api/areas/{area_id}`
- **Descrição**: Atualiza o nome de uma área existente.
- **Permissão**: Exclusivo para perfil `admin`.
- **Payload**:
  ```json
  { "name": "Supply Chain & Logística" }
  ```

#### `DELETE /api/areas/{area_id}`
- **Descrição**: Exclui uma área/cliente.
- **Permissão**: Exclusivo para perfil `admin`.
- **Resposta de Sucesso (`200 OK`)**:
  ```json
  { "message": "Área/Cliente excluída com sucesso." }
  ```

---

### 🚀 Projetos e Demandas (`/api/projects`)

#### `GET /api/projects/`
- **Descrição**: Retorna a lista de todos os projetos cadastrados com métricas consolidadas em tempo real.
- **Permissão**: Qualquer usuário autenticado.
- **Resposta de Sucesso (`200 OK`)**:
  ```json
  [
    {
      "id": 10,
      "name": "Implantação ERP Fiscal",
      "priority": "Alta",
      "status": "Em Andamento",
      "start_date": "2026-10-01",
      "end_date": "2026-12-15",
      "progress": 45.5,
      "ticket_number": "PRJ-2026-089",
      "requester": "Diretoria Financeira",
      "comments": "Fase de testes de integração com a SEFAZ",
      "area_id": 2,
      "owner_id": 3,
      "total_deliverables": 4,
      "total_activities": 12,
      "completed_activities": 5,
      "delayed_activities": 1,
      "total_tracked_minutes": 2740,
      "total_tracked_hours": 45.7,
      "area_name": "Financeiro & Controladoria",
      "owner_name": "Mariana Santos",
      "manager_id": 1,
      "manager_name": "Administrador do Sistema"
    }
  ]
  ```

#### `POST /api/projects/`
- **Descrição**: Cadastra um novo projeto/demanda.
- **Permissão**: Usuários autenticados.
- **Payload**:
  ```json
  {
    "name": "Portal do Colaborador 2.0",
    "priority": "Normal",
    "status": "Não Iniciado",
    "start_date": "2026-11-01",
    "end_date": "2026-12-30",
    "progress": 0.0,
    "ticket_number": "TICK-4421",
    "requester": "Departamento Pessoal",
    "comments": "Modernização da interface e autosserviço",
    "area_id": 1,
    "owner_id": 2
  }
  ```

#### `PUT /api/projects/{project_id}`
- **Descrição**: Atualiza dados cadastrais, datas ou status de um projeto existente.
- **Permissão**: Usuários autenticados.
- **Payload**: Campos opcionais de atualização conforme `ProjectUpdate`.

---

### 📦 Entregáveis / Marcos (`/api/deliverables`)

#### `GET /api/deliverables/`
- **Descrição**: Retorna todos os entregáveis do sistema com indicadores de atividades associadas.
- **Permissão**: Qualquer usuário autenticado.

#### `GET /api/deliverables/project/{project_id}`
- **Descrição**: Retorna os entregáveis vinculados a um projeto específico.
- **Permissão**: Qualquer usuário autenticado.

#### `GET /api/deliverables/{deliverable_id}`
- **Descrição**: Busca os dados de um entregável específico pelo seu ID.

#### `POST /api/deliverables/`
- **Descrição**: Cria um novo entregável vinculado a um projeto.
- **Payload**:
  ```json
  {
    "name": "Módulo de Segurança e Perfis",
    "description": "Configuração de RBAC e auditoria de acessos",
    "comments": "Seguir padrões OWASP",
    "status": "Não Iniciado",
    "start_date": "2026-10-15",
    "end_date": "2026-10-25",
    "progress": 0.0,
    "project_id": 10
  }
  ```

#### `PUT /api/deliverables/{deliverable_id}`
- **Descrição**: Atualiza um entregável existente.

#### `DELETE /api/deliverables/{deliverable_id}`
- **Descrição**: Exclui um entregável e recalcula as métricas do projeto pai.

---

### 📋 Atividades e Tarefas (`/api/activities`)

#### `GET /api/activities/`
- **Descrição**: Retorna todas as atividades cadastradas com resolução de responsável, entregável e verificação de atraso.
- **Resposta de Sucesso (`200 OK`)**:
  ```json
  [
    {
      "id": 54,
      "name": "Desenvolver tela de login PrimeVue",
      "description": "Criar componente com formulário reativo e feedback",
      "comments": "Aguardando validação do designer",
      "status": "Em Andamento",
      "start_date": "2026-10-10",
      "end_date": "2026-10-14",
      "progress": 70.0,
      "project_id": 10,
      "deliverable_id": 3,
      "assignee_id": 4,
      "assignee_name": "Lucas Pereira",
      "deliverable_name": "Módulo de Segurança e Perfis",
      "is_delayed": false,
      "total_tracked_minutes": 420,
      "total_tracked_hours": 7.0
    }
  ]
  ```

#### `POST /api/activities/`
- **Descrição**: Cria uma nova atividade, recalculando automaticamente os prazos e progresso do entregável e do projeto pai.
- **Payload**:
  ```json
  {
    "name": "Configurar migrations Alembic",
    "description": "Criar tabelas no banco de dados",
    "status": "Não Iniciado",
    "start_date": "2026-10-12",
    "end_date": "2026-10-13",
    "progress": 0.0,
    "project_id": 10,
    "deliverable_id": 3,
    "assignee_id": 4
  }
  ```

#### `PUT /api/activities/{activity_id}`
- **Descrição**: Atualiza percentual de progresso, status, prazos ou responsável da atividade. Dispara recálculo automático em cascata.

#### `DELETE /api/activities/{activity_id}`
- **Descrição**: Exclui a atividade e recalcula as métricas do projeto e entregável afetados.

---

### ⏱️ Timetracker & Gestão de Horas (`/api/timetracker`)

#### `GET /api/timetracker/active`
- **Descrição**: Retorna o cronômetro atualmente em execução do usuário logado, caso exista.
- **Resposta de Sucesso (`200 OK`)**:
  ```json
  {
    "id": 8,
    "user_id": 4,
    "activity_id": 54,
    "activity_name": "Desenvolver tela de login PrimeVue",
    "project_id": 10,
    "project_name": "Implantação ERP Fiscal",
    "start_time": "2026-10-11T13:45:00.000000Z",
    "elapsed_seconds": 1845
  }
  ```
  *(Se não houver cronômetro rodando, retorna `null`).*

#### `POST /api/timetracker/start`
- **Descrição**: Inicia o cronômetro do usuário logado na atividade especificada. Se o usuário já possuía um cronômetro rodando em outra atividade, a anterior é encerrada e registrada automaticamente no histórico.
- **Payload**:
  ```json
  { "activity_id": 54 }
  ```
- **Resposta de Sucesso (`200 OK`)**: Objeto `ActiveTimerResponse`.

#### `POST /api/timetracker/stop`
- **Descrição**: Para o cronômetro ativo, calcula o tempo em minutos e salva permanentemente como um apontamento (`TimeEntry`).
- **Payload**:
  ```json
  { "description": "Concluída integração da API com o formulário" }
  ```
- **Resposta de Sucesso (`200 OK`)**: Objeto `TimeEntryResponse` com o total de minutos gravados.

#### `POST /api/timetracker/`
- **Descrição**: Lançamento manual retroativo de horas gastas em uma atividade.
- **Payload**:
  ```json
  {
    "time_spent_minutes": 120,
    "description": "Reunião de alinhamento técnico e modelagem",
    "activity_id": 54
  }
  ```

#### `GET /api/timetracker/me`
- **Descrição**: Retorna o histórico de todos os apontamentos manuais e cronometrados do usuário autenticado.

#### `GET /api/timetracker/activity/{activity_id}`
- **Descrição**: Lista todos os apontamentos de horas realizados em uma atividade específica.

#### `GET /api/timetracker/activity/{activity_id}/total`
- **Descrição**: Retorna o resumo consolidado de tempo gasto na atividade.
- **Resposta de Sucesso (`200 OK`)**:
  ```json
  {
    "activity_id": 54,
    "total_minutes": 540,
    "total_hours": 9.0
  }
  ```

#### `GET /api/timetracker/calendar`
- **Descrição**: Visão diária/semanal para acompanhamento de apontamentos.
- **Parâmetros de Consulta (Query Params)**:
  - `user_id` (opcional, int): Permite filtrar por um usuário específico quando permitido pelo perfil.
- **Regra de Acesso**:
  - `analista`: Enxerga apenas seus próprios apontamentos.
  - `gestor`: Enxerga seus apontamentos e de todos os colaboradores sob sua gestão.
  - `admin`: Enxerga os apontamentos de todos os colaboradores do sistema.

#### `GET /api/timetracker/project/{project_id}`
- **Descrição**: Retorna o sumário completo de alocação de tempo na demanda, com detalhamento individual por membro da equipe (percentual de horas dedicadas, contagem de apontamentos e lista analítica de entradas).
- **Resposta de Sucesso (`200 OK`)**:
  ```json
  {
    "project_id": 10,
    "total_minutes": 2740,
    "total_hours": 45.7,
    "entries_count": 18,
    "team_members": [
      {
        "user_id": 4,
        "user_name": "Lucas Pereira",
        "user_role": "analista",
        "total_minutes": 1800,
        "total_hours": 30.0,
        "percentage": 65.7,
        "entries_count": 12
      },
      {
        "user_id": 3,
        "user_name": "Mariana Santos",
        "user_role": "gestor",
        "total_minutes": 940,
        "total_hours": 15.7,
        "percentage": 34.3,
        "entries_count": 6
      }
    ],
    "entries": [ ... ]
  }
  ```

---

## 8. Configuração e Variáveis de Ambiente

As configurações são gerenciadas pela classe `Settings` em `app/core/config.py` e podem ser customizadas criando um arquivo `.env` na raiz da pasta `backend/`:

| Variável | Valor Padrão | Descrição |
| :--- | :--- | :--- |
| `PROJECT_NAME` | `"RoadMap Corporate Monitor"` | Nome exibido na documentação Swagger |
| `DATABASE_URL` | `mysql+pymysql://root:password@127.0.0.1/roadmap` | String de conexão SQLAlchemy com MySQL |
| `SECRET_KEY` | `"sua_chave_secreta_aqui"` | Chave secreta de assinatura dos tokens JWT |
| `ALGORITHM` | `"HS256"` | Algoritmo criptográfico utilizado no token JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `10080` (7 dias) | Tempo de vida dos tokens de acesso emitidos |

---

## 9. Como Rodar o Backend Localmente

### Pré-requisitos
- Python 3.10+ instalado.
- Docker e Docker Compose instalados.

### Passo 1: Subir o Banco de Dados MySQL
Na pasta `backend/`, inicie os containers do MySQL e phpMyAdmin:
```bash
docker compose up -d
```
> O MySQL estará disponível na porta `3306` e o phpMyAdmin no navegador em `http://localhost:8080` (usuário: `root`, senha: `password`).

### Passo 2: Criar e Ativar o Ambiente Virtual Python
```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente (Linux/macOS)
source venv/bin/activate

# Ativar ambiente (Windows PowerShell)
.\venv\Scripts\Activate.ps1
```

### Passo 3: Instalar as Dependências
```bash
pip install -r requirements.txt
```

### Passo 4: Executar as Migrações do Banco (Alembic)
```bash
alembic upgrade head
```

### Passo 5: Criar o Usuário Administrador Inicial
Execute o script utilitário para criar o primeiro usuário do sistema:
```bash
python create_admin.py
```
> Credenciais padrão:
> - **E-mail**: `admin@roadmap.com`
> - **Senha**: `admin123`

### Passo 6: Iniciar o Servidor FastAPI (Uvicorn)
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
A API estará ativa em `http://localhost:8000`.

- **Swagger UI Interativo**: `http://localhost:8000/docs`
- **Documentação ReDoc**: `http://localhost:8000/redoc`

---

## 10. Scripts Utilitários

Na raiz da pasta `backend/` constam três scripts de suporte ao desenvolvimento:

1. **`python create_admin.py`**:
   Verifica se o usuário `admin@roadmap.com` existe e, se não existir, cria o cadastro com perfil `admin` e senha segura hasheada.
2. **`python reset_database.py`**:
   Limpa com segurança todas as tabelas transacionais de teste (`active_timers`, `time_entries`, `audit_logs`, `activities`, `deliverables`, `projects`, `areas`), resetando os auto-increments para 1 mas **mantendo intactos todos os usuários** e o histórico de migrações `alembic_version`. Para preservar também as áreas cadastradas, execute:
   ```bash
   python reset_database.py --keep-areas
   ```
3. **`python test_all_endpoints.py`**:
   Bateria completa de testes automatizados via `TestClient`, autenticando como admin e validando chamadas HTTP ponta a ponta em todos os 7 módulos da API.
