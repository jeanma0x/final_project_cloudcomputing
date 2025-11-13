FROM alpine:3.20

# Instalamos cliente de MySQL y cron (busybox)
RUN apk add --no-cache mysql-client busybox-suid

# Crear directorio donde se montará el volumen de backups
RUN mkdir -p /backups

# Copiar script de backup
COPY backup.sh /usr/local/bin/backup.sh
RUN chmod +x /usr/local/bin/backup.sh

# Copiar configuración de cron para el usuario root
COPY crontab /etc/crontabs/root

# Ejecutar cron en primer plano (para que el contenedor viva)
CMD ["crond", "-f", "-l", "2"]
