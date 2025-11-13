#!/bin/bash
set -euo pipefail

if [[ -z "${BACKUP_USER:-}" ]]; then
  echo "[init_backup_user] BACKUP_USER no definido; se omite creación."
  exit 0
fi

if [[ -n "${MYSQL_ROOT_PASSWORD_FILE:-}" && -f "${MYSQL_ROOT_PASSWORD_FILE}" ]]; then
  MYSQL_ROOT_PASSWORD=$(cat "$MYSQL_ROOT_PASSWORD_FILE")
fi

if [[ -n "${BACKUP_PASSWORD_FILE:-}" && -f "${BACKUP_PASSWORD_FILE}" ]]; then
  BACKUP_PASS_VALUE=$(cat "$BACKUP_PASSWORD_FILE")
elif [[ -n "${BACKUP_PASSWORD:-}" ]]; then
  BACKUP_PASS_VALUE="$BACKUP_PASSWORD"
else
  echo "[init_backup_user] No se proporcionó contraseña para el usuario de backup."
  exit 0
fi

cat <<SQL | mysql -uroot -p"${MYSQL_ROOT_PASSWORD}"
CREATE USER IF NOT EXISTS '${BACKUP_USER}'@'%' IDENTIFIED WITH mysql_native_password BY '${BACKUP_PASS_VALUE}';
GRANT SELECT, LOCK TABLES, SHOW VIEW, EVENT, TRIGGER ON \`${MYSQL_DATABASE}\`.* TO '${BACKUP_USER}'@'%';
GRANT INSERT ON \`${MYSQL_DATABASE}\`.audit_logs TO '${BACKUP_USER}'@'%';
GRANT PROCESS ON *.* TO '${BACKUP_USER}'@'%';
FLUSH PRIVILEGES;
SQL

echo "[init_backup_user] Usuario ${BACKUP_USER} configurado."
