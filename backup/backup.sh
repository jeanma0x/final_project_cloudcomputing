#!/bin/sh

# Directorio donde guardar los backups
BACKUP_DIR="${BACKUP_DIR:-/backups}"

# Leer contraseña desde secret si existe
if [ -n "$MYSQL_PASSWORD_FILE" ] && [ -f "$MYSQL_PASSWORD_FILE" ]; then
  MYSQL_PASSWORD=$(cat "$MYSQL_PASSWORD_FILE")
fi

BACKUP_ACTOR="${BACKUP_ACTOR:-backup-cron}"

# Fecha actual para el nombre del archivo
DATE=$(date +"%Y-%m-%d_%H-%M")

# Nombre del archivo de respaldo
FILE="$BACKUP_DIR/backup_${DATE}.sql"

echo "=== Ejecutando backup: $FILE ==="

# Función auxiliar para registrar en audit_logs
log_audit() {
  local action="$1"
  local status_message="$2"
  local extra_json="$3"
  local escaped_file
  local escaped_message
  escaped_file=$(printf "%s" "$FILE" | sed "s/'/''/g")
  escaped_message=$(printf "%s" "$status_message" | sed "s/'/''/g")
  mysql \
    -h "$MYSQL_HOST" \
    -u "$MYSQL_USER" \
    -p"$MYSQL_PASSWORD" \
    "$MYSQL_DATABASE" \
    -e "INSERT INTO audit_logs(action, actor_email, payload) VALUES ('${action}', '${BACKUP_ACTOR}', JSON_OBJECT('file', '${escaped_file}', 'message', '${escaped_message}'${extra_json}));" >/dev/null 2>&1 || true
}

# Ejecutar mysqldump
if mysqldump \
  -h "$MYSQL_HOST" \
  -u "$MYSQL_USER" \
  -p"$MYSQL_PASSWORD" \
  --no-tablespaces \
  "$MYSQL_DATABASE" > "$FILE"; then
  echo "Backup completado."
  SIZE_BYTES=$(stat -c%s "$FILE" 2>/dev/null || stat -f%z "$FILE")
  log_audit "BACKUP_OK" "Backup desde cron" ", 'size_bytes', ${SIZE_BYTES}"
else
  echo "Error en el backup."
  log_audit "BACKUP_ERROR" "mysqldump devolvió error" ""
fi
