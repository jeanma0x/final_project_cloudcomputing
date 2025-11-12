import os

# Encapsulamos la configuración para facilitar pruebas y cambiar según entorno
class Settings:
    # Config general de la app
    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))

    # Config de DB (inyectadas por docker-compose)
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_NAME: str = os.getenv("DB_NAME", "users_db")
    DB_USER: str = os.getenv("DB_USER", "app_user")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "app_password")

    # CORS para permitir peticiones desde el frontend
    CORS_ORIGINS: str = os.getenv("CORS_ORIGINS", "*")

settings = Settings()
