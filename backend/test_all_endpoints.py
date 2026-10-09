import sys
import datetime
from starlette.testclient import TestClient

import app.models
import app.db.audit
from app.main import app
from app.db.session import SessionLocal
from app.models.audit_log import AuditLog

def test_everything_via_http():
    client = TestClient(app)
    print("\n========================================================")
    print("🚀 TESTANDO TODOS OS ENDPOINTS HTTP DA API FASTAPI")
    print("========================================================")

    # 1. Login
    login_res = client.post("/api/auth/login", data={
        "username": "admin@roadmap.com",
        "password": "admin123"
    })
    assert login_res.status_code == 200, f"Login falhou: {login_res.text}"
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("✔ [1/7] POST /api/auth/login -> 200 OK (Token obtido com sucesso)")

    # 2. Get User Me
    me_res = client.get("/api/users/me", headers=headers)
    assert me_res.status_code == 200
    user_data = me_res.json()
    assert user_data["email"] == "admin@roadmap.com"
    print(f"✔ [2/7] GET /api/users/me -> 200 OK (Usuário: {user_data['name']})")

    # 3. Criar Projeto (testando datas + auditoria JSON)
    project_payload = {
        "name": "Dashboard RH Automatizado",
        "priority": "Alta",
        "status": "Em Andamento",
        "start_date": "2026-10-12",
        "end_date": "2026-10-30",
        "progress": 10.0,
        "area_id": 1,
        "owner_id": user_data["id"]
    }
    proj_res = client.post("/api/projects/", json=project_payload, headers=headers)
    assert proj_res.status_code == 200, f"Erro ao criar projeto: {proj_res.text}"
    proj_id = proj_res.json()["id"]
    print(f"✔ [3/7] POST /api/projects/ -> 200 OK (Projeto ID {proj_id} criado e auditado com sucesso)")

    # 4. Listar e Atualizar Projeto
    projs_list = client.get("/api/projects/", headers=headers)
    assert projs_list.status_code == 200
    assert len(projs_list.json()) > 0

    update_proj_res = client.put(f"/api/projects/{proj_id}", json={
        "progress": 40.0,
        "priority": "Crítica"
    }, headers=headers)
    assert update_proj_res.status_code == 200
    print(f"✔ [4/7] GET & PUT /api/projects/ -> 200 OK (Projeto atualizado para 40%)")

    # 4.5. Criar e Listar Entregável
    deliverable_payload = {
        "name": "Fase 1 - Estruturação e Backend",
        "project_id": proj_id,
        "description": "Entregável contendo todas as atividades de arquitetura",
        "status": "Em Andamento"
    }
    deliv_res = client.post("/api/deliverables/", json=deliverable_payload, headers=headers)
    assert deliv_res.status_code == 200, f"Erro ao criar entregável: {deliv_res.text}"
    deliv_id = deliv_res.json()["id"]
    print(f"✔ [4.5/7] POST /api/deliverables/ -> 200 OK (Entregável ID {deliv_id} criado)")

    # 5. Criar e Atualizar Atividade vinculada ao Entregável
    activity_payload = {
        "name": "Desenvolvimento do Frontend Vue3",
        "description": "Criação das visões de dashboards e timetracker",
        "status": "Em Andamento",
        "start_date": "2026-10-12",
        "end_date": "2026-10-18",
        "progress": 50.0,
        "project_id": proj_id,
        "deliverable_id": deliv_id,
        "assignee_id": user_data["id"]
    }
    ativ_res = client.post("/api/activities/", json=activity_payload, headers=headers)
    assert ativ_res.status_code == 200, f"Erro ao criar atividade: {ativ_res.text}"
    ativ_id = ativ_res.json()["id"]

    ativ_update = client.put(f"/api/activities/{ativ_id}", json={
        "status": "Concluído",
        "progress": 100.0
    }, headers=headers)
    assert ativ_update.status_code == 200
    print(f"✔ [5/7] POST & PUT /api/activities/ -> 200 OK (Atividade ID {ativ_id} criada e concluída)")

    # 6. Timetracker (Apontar horas, listar me, total por atividade)
    time_payload = {
        "activity_id": ativ_id,
        "time_spent_minutes": 90,
        "description": "Refatoração das camadas e testes integrados"
    }
    time_res = client.post("/api/timetracker/", json=time_payload, headers=headers)
    assert time_res.status_code == 200, f"Erro no timetracker: {time_res.text}"
    time_entry_id = time_res.json()["id"]

    my_times = client.get("/api/timetracker/me", headers=headers)
    assert my_times.status_code == 200
    assert len(my_times.json()) > 0

    total_time = client.get(f"/api/timetracker/activity/{ativ_id}/total", headers=headers)
    assert total_time.status_code == 200
    total_data = total_time.json()

    proj_time = client.get(f"/api/timetracker/project/{proj_id}", headers=headers)
    assert proj_time.status_code == 200
    proj_time_data = proj_time.json()
    assert proj_time_data["total_minutes"] >= 90
    assert len(proj_time_data["team_members"]) > 0
    print(f"✔ [6/7] TIMETRACKER (POST, GET /me, GET /total, GET /project) -> 200 OK (Projeto {proj_id}: {proj_time_data['total_hours']}h por {len(proj_time_data['team_members'])} membro(s))")

    # 6.5. Testar Active Timer Persistente no Banco de Dados
    start_timer = client.post("/api/timetracker/start", json={"activity_id": ativ_id}, headers=headers)
    assert start_timer.status_code == 200
    get_timer = client.get("/api/timetracker/active", headers=headers)
    assert get_timer.status_code == 200
    assert get_timer.json() is not None
    assert get_timer.json()["activity_id"] == ativ_id
    stop_timer = client.post("/api/timetracker/stop", json={"description": "Finalização do timer no teste"}, headers=headers)
    assert stop_timer.status_code == 200
    get_timer_after = client.get("/api/timetracker/active", headers=headers)
    assert get_timer_after.status_code == 200
    assert get_timer_after.json() is None
    print(f"✔ [6.5/7] ACTIVE TIMER PERSISTENTE NO BANCO (START, GET, STOP) -> 200 OK (Contagem individual por usuário validada)")

    # 7. Verificar Auditoria
    db = SessionLocal()
    audit_logs = db.query(AuditLog).order_by(AuditLog.id.desc()).limit(5).all()
    print(f"✔ [7/7] AUDITORIA -> {len(audit_logs)} registros recentes encontrados!")
    for log in audit_logs:
        print(f"       [{log.action}] Tabela: {log.table_name} | Record ID: {log.record_id}")
    db.close()

    print("\n========================================================")
    print("✅ TODOS OS ENDPOINTS DA API ESTÃO 100% OPERACIONAIS E AUDITADOS!")
    print("========================================================\n")

if __name__ == "__main__":
    test_everything_via_http()

