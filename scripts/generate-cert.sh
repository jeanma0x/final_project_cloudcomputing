#!/usr/bin/env bash
set -euo pipefail

CERT_DIR="$(cd "$(dirname "$0")/.." && pwd)/frontend/certs"
CERT_FILE="$CERT_DIR/selfsigned.crt"
KEY_FILE="$CERT_DIR/selfsigned.key"

mkdir -p "$CERT_DIR"

echo "[cert] Generando certificado para localhost (mkcert si está disponible)."
if command -v mkcert >/dev/null 2>&1; then
  mkcert -cert-file "$CERT_FILE" -key-file "$KEY_FILE" localhost 127.0.0.1 ::1
  echo "[cert] Certificado creado con mkcert. Importa el CA de mkcert para evitar advertencias."
else
  echo "[cert] mkcert no está instalado; usando OpenSSL como fallback (el navegador mostrará advertencia)."
  openssl req -x509 -nodes -days 365 \
    -newkey rsa:2048 \
    -keyout "$KEY_FILE" \
    -out "$CERT_FILE" \
    -subj "/CN=localhost" \
    -addext "subjectAltName=DNS:localhost,IP:127.0.0.1,IP:::1"
fi

chmod 600 "$KEY_FILE"
echo "[cert] Archivos generados en $CERT_DIR"
