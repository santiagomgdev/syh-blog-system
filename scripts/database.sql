-- Create the database
CREATE DATABASE IF NOT EXISTS syh_blog_system;

-- Switch to the new database
USE syh_blog_system;

-- DROP TABLE IF EXISTS password_reset_tokens;
-- DROP TABLE IF EXISTS user_roles;
-- DROP TABLE IF EXISTS tokens;
-- DROP TABLE IF EXISTS users;

-- tabla Usuarios
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_usuario VARCHAR(50) NOT NULL UNIQUE,
    correo VARCHAR(100) NOT NULL UNIQUE,
    contrasena_hash VARCHAR(255) NOT NULL,
    sal VARCHAR(50) NOT NULL,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    ultimo_login TIMESTAMP NULL,
);

-- tabla tokens
CREATE TABLE tokens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    token_refresco VARCHAR(255) NOT NULL,
    emitido_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expira_en TIMESTAMP NOT NULL,
    revocado BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- tabla roles usuario
CREATE TABLE roles_usuario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    nombre_rol VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE (user_id, role_name)
);

CREATE TABLE posts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    enlace VARCHAR(255) UNIQUE NOT NULL,
    contenido TEXT NOT NULL,
    resumen TEXT,
    estado ENUM('borrador', 'publicado', 'archivado') DEFAULT 'borrador',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

CREATE TABLE comentarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    post_id INT NOT NULL,
    usuario_id INT NOT NULL,
    padre_id INT NULL,
    contenido TEXT NOT NULL,
    estado ENUM('pendiente', 'aprobado', 'spam', 'rechazado') DEFAULT 'pendiente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (padre_id) REFERENCES comentarios(id) ON DELETE CASCADE
);

-- Add indexes for performance
CREATE INDEX idx_tokens_usuario_id ON tokens(usuario_id);
CREATE INDEX idx_tokens_token_id ON tokens(token_id);
CREATE INDEX idx_usuario_roles_usuario_id ON roles_usuario(usuario_id);

-- Crear usuario administrador (nombre_usuario: admin, contraseña: admin123)
-- Nota: Este es solo un ejemplo, reemplaza el hash y la sal por valores seguros en producción
INSERT INTO usuarios (nombre_usuario, correo, contrasena_hash, sal, activo, created_at)
VALUES ('admin', 'admin@syhblog.local',
    'jZae727K08KaOmKSgOaGzww/XVqGr/PKEgIMkjrcbJI=', -- Hash SHA-256 de 'admin123' con la sal 'syhblog'
    'c3loYmxvZw==', -- Base64 de 'syhblog'
    TRUE,
    CURRENT_TIMESTAMP);

-- Give admin user the ROLE_ADMIN role
INSERT INTO roles_usuario (usuario_id, nombre_rol) 
VALUES (1, 'ADMIN');