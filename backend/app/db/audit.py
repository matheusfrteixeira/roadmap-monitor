import datetime
from enum import Enum
from decimal import Decimal
from typing import Dict, Any

from sqlalchemy import event
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import get_history

from app.models.audit_log import AuditLog

def serialize_value(val: Any) -> Any:
    """Converte qualquer tipo de dado Python para tipo primitivo compatível com JSON."""
    if val is None:
        return None
    if isinstance(val, (datetime.date, datetime.datetime)):
        return val.isoformat()
    if isinstance(val, Enum):
        return val.value
    if isinstance(val, Decimal):
        return float(val)
    if isinstance(val, (int, float, str, bool)):
        return val
    if isinstance(val, (list, tuple)):
        return [serialize_value(x) for x in val]
    if isinstance(val, dict):
        return {str(k): serialize_value(v) for k, v in val.items()}
    return str(val)

def get_state_dict(obj) -> Dict[str, Any]:
    """Helper para transformar objeto SQLAlchemy em dict seguro para JSON."""
    state = {}
    for column in obj.__table__.columns:
        raw_val = getattr(obj, column.name, None)
        state[column.name] = serialize_value(raw_val)
    return state

@event.listens_for(Session, 'before_flush')
def receive_before_flush(session: Session, flush_context, instances):
    for obj in session.new:
        if isinstance(obj, AuditLog):
            continue  # Não audita a própria tabela de auditoria
        
        table_name = obj.__tablename__ if hasattr(obj, '__tablename__') else obj.__class__.__name__
        new_data = get_state_dict(obj)
        
        log = AuditLog(
            table_name=table_name,
            record_id=obj.id if hasattr(obj, 'id') and obj.id else 0,
            action="INSERT",
            old_data=None,
            new_data=new_data,
        )
        session.add(log)

    for obj in session.dirty:
        if isinstance(obj, AuditLog):
            continue
            
        table_name = obj.__tablename__ if hasattr(obj, '__tablename__') else obj.__class__.__name__
        old_data = {}
        new_data = {}
        changed = False
        
        for column in obj.__table__.columns:
            history = get_history(obj, column.name)
            
            if history.has_changes():
                changed = True
                old_val = history.deleted[0] if history.deleted else None
                new_val = history.added[0] if history.added else None
                
                old_data[column.name] = serialize_value(old_val)
                new_data[column.name] = serialize_value(new_val)
        
        if changed:
            log = AuditLog(
                table_name=table_name,
                record_id=obj.id if hasattr(obj, 'id') else 0,
                action="UPDATE",
                old_data=old_data,
                new_data=new_data,
            )
            session.add(log)

    for obj in session.deleted:
        if isinstance(obj, AuditLog):
            continue
            
        table_name = obj.__tablename__ if hasattr(obj, '__tablename__') else obj.__class__.__name__
        old_data = get_state_dict(obj)
        
        log = AuditLog(
            table_name=table_name,
            record_id=obj.id if hasattr(obj, 'id') else 0,
            action="DELETE",
            old_data=old_data,
            new_data=None,
        )
        session.add(log)
