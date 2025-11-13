import os
from pathlib import Path
from typing import Optional


def _read_secret(var_name: str, default: Optional[str] = None) -> Optional[str]:
    """Lee primero VAR_NAME_FILE (si existe) y si no, el valor directo del env."""
    file_path = os.getenv(f"{var_name}_FILE")
    if file_path and Path(file_path).exists():
        return Path(file_path).read_text().strip()
    return os.getenv(var_name, default)


# Encapsulamos la configuración para facilitar pruebas y cambiar según entorno
class Settings:
    # Config general de la app
    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
    BACKUP_DIR: str = os.getenv("BACKUP_DIR", "/backups")
    BACKUP_ACTOR: str = os.getenv("BACKUP_ACTOR", "backup-cron")

    # Config de DB (inyectadas por docker-compose)
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_NAME: str = os.getenv("DB_NAME", "users_db")
    DB_USER: str = os.getenv("DB_USER", "app_user")
    DB_PASSWORD: str = _read_secret("DB_PASSWORD", "app_password") or "app_password"

    # CORS para permitir peticiones desde el frontend
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")

    # JWT
    JWT_SECRET: str = _read_secret("JWT_SECRET", "change_this_in_prod") or "change_this_in_prod"
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_EXPIRES_MIN: int = int(os.getenv("JWT_EXPIRES_MIN", "60"))

settings = Settings()
