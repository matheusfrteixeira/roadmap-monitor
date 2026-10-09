from typing import Optional
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.time_entry_repo import TimeEntryRepository
from app.repositories.activity_repo import ActivityRepository
from app.schemas.time_entry import TimeEntryCreate
from app.models.time_entry import TimeEntry
from app.models.active_timer import ActiveTimer
from app.models.user import User, RoleEnum

class TimeEntryService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = TimeEntryRepository(db)
        self.activity_repo = ActivityRepository(db)

    def log_time(self, time_in: TimeEntryCreate, current_user: User):
        activity = self.activity_repo.get_by_id(time_in.activity_id)
        if not activity:
            raise HTTPException(status_code=404, detail="Atividade não encontrada.")

        time_entry_obj = TimeEntry(
            **time_in.model_dump(),
            user_id=current_user.id
        )
        return self.repo.create(time_entry_obj)

    def get_my_time_entries(self, user_id: int):
        return self.repo.get_by_user_id(user_id)

    def get_activity_time_entries(self, activity_id: int):
        return self.repo.get_by_activity_id(activity_id)

    def get_activity_total_time(self, activity_id: int):
        raw_total = self.repo.get_total_minutes_by_activity(activity_id)
        total_minutes = int(raw_total or 0)
        return {
            "activity_id": activity_id,
            "total_minutes": total_minutes,
            "total_hours": round(total_minutes / 60.0, 2)
        }

    def get_project_time_summary(self, project_id: int):
        """Retorna histórico completo e resumo por membro de equipe do projeto."""
        entries = self.repo.get_by_project_id(project_id)
        total_minutes = sum(e.time_spent_minutes for e in entries)

        user_map = {}
        for e in entries:
            uid = e.user_id
            if uid not in user_map:
                u = e.user
                user_map[uid] = {
                    "user_id": uid,
                    "user_name": u.name if u else "Desconhecido",
                    "user_role": u.role.value if (u and hasattr(u.role, 'value')) else (str(u.role) if u else "analista"),
                    "total_minutes": 0,
                    "total_hours": 0.0,
                    "percentage": 0.0,
                    "entries_count": 0
                }
            user_map[uid]["total_minutes"] += e.time_spent_minutes
            user_map[uid]["entries_count"] += 1

        team_members = list(user_map.values())
        for tm in team_members:
            tm["total_hours"] = round(tm["total_minutes"] / 60.0, 1)
            tm["percentage"] = round((tm["total_minutes"] / total_minutes * 100), 1) if total_minutes > 0 else 0.0
        team_members.sort(key=lambda x: x["total_minutes"], reverse=True)

        formatted_entries = []
        for e in entries:
            formatted_entries.append({
                "id": e.id,
                "user_id": e.user_id,
                "user_name": e.user.name if e.user else "Usuário Desconhecido",
                "activity_id": e.activity_id,
                "activity_name": e.activity.name if e.activity else "Atividade",
                "deliverable_name": e.activity.deliverable.name if (e.activity and e.activity.deliverable) else "Etapas Gerais",
                "time_spent_minutes": e.time_spent_minutes,
                "time_spent_hours": round(e.time_spent_minutes / 60.0, 2),
                "description": e.description or "Sem observações",
                "date_recorded": e.date_recorded.isoformat() if e.date_recorded else None
            })

        return {
            "project_id": project_id,
            "total_minutes": total_minutes,
            "total_hours": round(total_minutes / 60.0, 1),
            "entries_count": len(entries),
            "team_members": team_members,
            "entries": formatted_entries
        }

    def get_calendar_entries(self, current_user: User, target_user_id: Optional[int] = None):
        """Retorna histórico diário respeitando a hierarquia de gestão."""
        query = self.db.query(TimeEntry).join(User, TimeEntry.user_id == User.id)
        
        if current_user.role == RoleEnum.admin:
            if target_user_id:
                query = query.filter(TimeEntry.user_id == target_user_id)
        elif current_user.role == RoleEnum.gestor:
            subordinate_ids = [u.id for u in self.db.query(User).filter(User.manager_id == current_user.id).all()]
            allowed_ids = subordinate_ids + [current_user.id]
            if target_user_id:
                if target_user_id not in allowed_ids:
                    raise HTTPException(
                        status_code=403, 
                        detail="Você só pode visualizar apontamentos seus ou de seus subordinados diretos."
                    )
                query = query.filter(TimeEntry.user_id == target_user_id)
            else:
                query = query.filter(TimeEntry.user_id.in_(allowed_ids))
        else:  # Analista
            query = query.filter(TimeEntry.user_id == current_user.id)
            
        entries = query.order_by(TimeEntry.date_recorded.desc()).all()
        
        result = []
        for e in entries:
            date_iso = e.date_recorded.isoformat() if e.date_recorded else None
            if date_iso and not date_iso.endswith('Z') and '+' not in date_iso:
                date_iso += 'Z'
            result.append({
                "id": e.id,
                "time_spent_minutes": e.time_spent_minutes,
                "description": e.description,
                "date_recorded": date_iso,
                "user_id": e.user_id,
                "user_name": e.user.name if e.user else "Usuário Desconhecido",
                "activity_id": e.activity_id,
                "activity_name": e.activity.name if e.activity else "Atividade Não Informada",
                "project_id": e.activity.project_id if e.activity else None,
                "project_name": e.activity.project.name if (e.activity and e.activity.project) else "Sem Projeto"
            })
        return result

    def _format_active_timer(self, active: Optional[ActiveTimer]):
        if not active:
            return None
        activity = active.activity
        project = activity.project if activity else None
        elapsed = int((datetime.utcnow() - active.start_time).total_seconds()) if active.start_time else 0
        
        start_iso = ""
        if active.start_time:
            start_iso = active.start_time.isoformat()
            if not start_iso.endswith('Z') and '+' not in start_iso:
                start_iso += 'Z'

        return {
            "id": active.id,
            "user_id": active.user_id,
            "activity_id": active.activity_id,
            "activity_name": activity.name if activity else None,
            "project_id": project.id if project else None,
            "project_name": project.name if project else None,
            "start_time": start_iso,
            "elapsed_seconds": max(0, elapsed)
        }

    def get_active_timer(self, current_user: User):
        active = self.repo.get_active_timer_by_user(current_user.id)
        return self._format_active_timer(active)

    def start_active_timer(self, activity_id: int, current_user: User):
        activity = self.activity_repo.get_by_id(activity_id)
        if not activity:
            raise HTTPException(status_code=404, detail="Atividade não encontrada.")

        active = self.repo.get_active_timer_by_user(current_user.id)
        if active:
            if active.activity_id == activity_id:
                return self._format_active_timer(active)
            
            # Finaliza automaticamente o timer da atividade anterior
            elapsed_secs = max(1, int((datetime.utcnow() - active.start_time).total_seconds()))
            minutes = max(1, round(elapsed_secs / 60))
            prev_act_name = active.activity.name if active.activity else "tarefa anterior"
            desc = f"Finalizado automaticamente ao alternar para: {activity.name}"
            self.repo.create(TimeEntry(
                time_spent_minutes=minutes,
                description=desc,
                activity_id=active.activity_id,
                user_id=current_user.id
            ))
            self.repo.delete_active_timer(active)

        new_timer = ActiveTimer(
            user_id=current_user.id,
            activity_id=activity_id,
            start_time=datetime.utcnow()
        )
        saved = self.repo.create_active_timer(new_timer)
        return self._format_active_timer(saved)

    def stop_active_timer(self, description: Optional[str], current_user: User):
        active = self.repo.get_active_timer_by_user(current_user.id)
        if not active:
            raise HTTPException(status_code=400, detail="Nenhum cronômetro ativo encontrado para este usuário.")

        elapsed_secs = max(1, int((datetime.utcnow() - active.start_time).total_seconds()))
        minutes = max(1, round(elapsed_secs / 60))
        act_name = active.activity.name if active.activity else "atividade"
        desc = description or f"Sessão cronometrada em {act_name}"
        
        entry = self.repo.create(TimeEntry(
            time_spent_minutes=minutes,
            description=desc,
            activity_id=active.activity_id,
            user_id=current_user.id
        ))
        self.repo.delete_active_timer(active)
        return entry
