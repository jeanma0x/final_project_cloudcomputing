from sqlalchemy import Integer, String, TIMESTAMP, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

# Modelo ORM que mapea a la tabla users creada en init.sql
class User(Base):
    __tablename__ = "users"

    # Campos de la tabla con tipos y restricciones
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(190), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str | None] = mapped_column(String(190), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped = mapped_column(TIMESTAMP, server_default=func.current_timestamp())
