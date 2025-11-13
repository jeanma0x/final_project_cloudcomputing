from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, func, JSON

from .db import Base

class User(Base):
    __tablename__ = "users"

    # Para que SQLAlchemy ignore cualquier anotación rara
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(190), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(190), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())


class AuditLog(Base):
    __tablename__ = "audit_logs"
    __allow_unmapped__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    action = Column(String(100), nullable=False)
    actor_email = Column(String(190), nullable=True)
    payload = Column(JSON, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
