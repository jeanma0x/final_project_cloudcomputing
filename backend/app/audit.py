from __future__ import annotations

from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from .models import AuditLog


def record_audit_log(
    db: Session,
    action: str,
    actor_email: Optional[str] = None,
    payload: Optional[Dict[str, Any]] = None,
) -> Optional[AuditLog]:
    """Guarda una entrada básica en la tabla audit_logs.

    Los errores nunca deben tumbar la petición principal, por lo que se
    silencian devolviendo None.
    """
    try:
        log = AuditLog(action=action, actor_email=actor_email, payload=payload)
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    except Exception:
        db.rollback()
        return None
