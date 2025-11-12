-- Este script se ejecuta automáticamente al primer arranque del contenedor
-- porque lo montamos en /docker-entrypoint-initdb.d/

-- Tabla principal de usuarios
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,            -- Identificador único
  email VARCHAR(190) NOT NULL UNIQUE,           -- Email único (index natural)
  password_hash VARCHAR(255) NOT NULL,          -- Hash de contraseña (bcrypt, etc.)
  full_name VARCHAR(190),                       -- Nombre opcional
  is_active TINYINT(1) DEFAULT 1,               -- Bandera de usuario activo
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Fecha de creación
) ENGINE=InnoDB;

-- Tabla simple de auditoría para registrar acciones clave (login, backup, etc.)
CREATE TABLE IF NOT EXISTS audit_logs (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  action VARCHAR(100) NOT NULL,                 -- Tipo de acción (REGISTER, LOGIN, BACKUP_OK, etc.)
  actor_email VARCHAR(190),                     -- Quién lo realizó (si aplica)
  payload JSON,                                 -- Datos adicionales (opcional)
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;
