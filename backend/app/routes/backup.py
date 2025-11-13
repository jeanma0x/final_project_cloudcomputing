from __future__ import annotations

import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from subprocess import CalledProcessError, run

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import desc
from sqlalchemy.orm import Session

from ..auth import get_current_user
from ..audit import record_audit_log
from ..config import settings
from ..db import get_db
from ..models import AuditLog, User
from ..schemas import AuditLogOut, BackupResponse

router = APIRouter(prefix="/backup", tags=["backup"])


@router.post("", response_model=BackupResponse, status_code=201)
def trigger_backup(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    mysqldump_bin = shutil.which("mysqldump")
    if not mysqldump_bin:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="mysqldump no está instalado en el contenedor de la API",
        )

    backup_dir = Path(settings.BACKUP_DIR)
    backup_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    dump_file = backup_dir / f"manual_{timestamp}.sql"

    cmd = [
        mysqldump_bin,
        f"-h{settings.DB_HOST}",
        f"-P{settings.DB_PORT}",
        f"-u{settings.DB_USER}",
        "--single-transaction",
        "--quick",
        "--no-tablespaces",
        settings.DB_NAME,
    ]

    env = os.environ.copy()
    env["MYSQL_PWD"] = settings.DB_PASSWORD

    try:
        with open(dump_file, "w", encoding="utf-8") as fh:
            run(cmd, check=True, env=env, stdout=fh, stderr=None)
    except CalledProcessError as exc:
        record_audit_log(
            db,
            action="BACKUP_ERROR",
            actor_email=current_user.email,
            payload={"code": exc.returncode, "file": str(dump_file)},
        )
        raise HTTPException(status_code=500, detail="Error al ejecutar mysqldump")

    size_bytes = dump_file.stat().st_size
    log = record_audit_log(
        db,
        action="BACKUP_OK",
        actor_email=current_user.email,
        payload={"file": str(dump_file), "size_bytes": size_bytes},
    )

    created_at = log.created_at if log else datetime.now(timezone.utc)

    return BackupResponse(
        file=str(dump_file),
        size_bytes=size_bytes,
        created_at=created_at,
        triggered_by=current_user.email,
    )


@router.get("/logs", response_model=list[AuditLogOut])
def backup_logs(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    logs = (
        db.query(AuditLog)
        .filter(AuditLog.action.like("BACKUP%"))
        .order_by(desc(AuditLog.created_at))
        .limit(20)
        .all()
    )
    return logs
