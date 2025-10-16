-- =============================================
-- Sistema de Solicitud de Crédito
-- Script de Inicialización de Base de Datos
-- =============================================

-- Crear extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================
-- Tabla: sucursales
-- =============================================
CREATE TABLE IF NOT EXISTS sucursales (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ciudad VARCHAR(100) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- Tabla: clientes
-- =============================================
CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    fecha_nacimiento DATE NOT NULL,
    edad INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_edad CHECK (edad >= 0 AND edad <= 150)
);

-- =============================================
-- Tabla: solicitudes
-- =============================================
CREATE TABLE IF NOT EXISTS solicitudes (
    id SERIAL PRIMARY KEY,
    cliente_id INTEGER NOT NULL,
    sucursal_id INTEGER NOT NULL,
    monto_solicitado DECIMAL(15, 2) NOT NULL,
    ingreso_mensual DECIMAL(15, 2) NOT NULL,
    score_crediticio INTEGER NOT NULL,
    tiene_tarjeta_credito BOOLEAN DEFAULT FALSE,
    tiene_credito_automotriz BOOLEAN DEFAULT FALSE,
    plazo_meses INTEGER NOT NULL,
    estado VARCHAR(20) NOT NULL CHECK (estado IN ('aprobado', 'rechazado')),
    motivo_rechazo TEXT,
    fecha_solicitud TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE,
    FOREIGN KEY (sucursal_id) REFERENCES sucursales(id) ON DELETE RESTRICT,
    CONSTRAINT chk_monto_positivo CHECK (monto_solicitado > 0),
    CONSTRAINT chk_ingreso_positivo CHECK (ingreso_mensual > 0),
    CONSTRAINT chk_score_range CHECK (score_crediticio >= 300 AND score_crediticio <= 850),
    CONSTRAINT chk_plazo_positivo CHECK (plazo_meses > 0 AND plazo_meses <= 360)
);

-- =============================================
-- Tabla: usuarios_admin
-- =============================================
CREATE TABLE IF NOT EXISTS usuarios_admin (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- Índices para mejorar performance
-- =============================================
CREATE INDEX IF NOT EXISTS idx_solicitudes_cliente ON solicitudes(cliente_id);
CREATE INDEX IF NOT EXISTS idx_solicitudes_sucursal ON solicitudes(sucursal_id);
CREATE INDEX IF NOT EXISTS idx_solicitudes_estado ON solicitudes(estado);
CREATE INDEX IF NOT EXISTS idx_solicitudes_fecha ON solicitudes(fecha_solicitud);
CREATE INDEX IF NOT EXISTS idx_clientes_email ON clientes(email);
CREATE INDEX IF NOT EXISTS idx_usuarios_admin_username ON usuarios_admin(username);

-- =============================================
-- Datos de ejemplo para sucursales
-- =============================================
INSERT INTO sucursales (nombre, ciudad, direccion, telefono) VALUES
('Sucursal Centro', 'Ciudad de México', 'Av. Juárez 123, Col. Centro', '55-1234-5678'),
('Sucursal Norte', 'Monterrey', 'Blvd. Díaz Ordaz 456, Col. Santa María', '81-8765-4321'),
('Sucursal Occidente', 'Guadalajara', 'Av. Chapultepec 789, Col. Americana', '33-9876-5432'),
('Sucursal Bajío', 'León', 'Blvd. Adolfo López Mateos 321, Col. Jardines del Moral', '477-123-4567'),
('Sucursal Sureste', 'Mérida', 'Calle 60 No. 234, Col. Centro', '999-987-6543')
ON CONFLICT DO NOTHING;

-- =============================================
-- Usuario admin por defecto
-- Contraseña: admin123 (hash bcrypt)
-- =============================================
-- Nota: Este hash debe ser generado por el backend al iniciar
-- Este es solo un placeholder, el backend creará el usuario real

-- =============================================
-- Vistas útiles para reportes
-- =============================================
CREATE OR REPLACE VIEW vista_estadisticas_solicitudes AS
SELECT 
    s.id as sucursal_id,
    s.nombre as sucursal_nombre,
    s.ciudad,
    COUNT(sol.id) as total_solicitudes,
    SUM(CASE WHEN sol.estado = 'aprobado' THEN 1 ELSE 0 END) as aprobadas,
    SUM(CASE WHEN sol.estado = 'rechazado' THEN 1 ELSE 0 END) as rechazadas,
    ROUND(AVG(sol.monto_solicitado), 2) as monto_promedio,
    ROUND(SUM(CASE WHEN sol.estado = 'aprobado' THEN sol.monto_solicitado ELSE 0 END), 2) as monto_aprobado_total
FROM sucursales s
LEFT JOIN solicitudes sol ON s.id = sol.sucursal_id
GROUP BY s.id, s.nombre, s.ciudad;

CREATE OR REPLACE VIEW vista_solicitudes_completas AS
SELECT 
    sol.id,
    sol.monto_solicitado,
    sol.ingreso_mensual,
    sol.score_crediticio,
    sol.tiene_tarjeta_credito,
    sol.tiene_credito_automotriz,
    sol.plazo_meses,
    sol.estado,
    sol.motivo_rechazo,
    sol.fecha_solicitud,
    c.nombre || ' ' || c.apellido as cliente_nombre,
    c.email as cliente_email,
    c.edad as cliente_edad,
    suc.nombre as sucursal_nombre,
    suc.ciudad as sucursal_ciudad
FROM solicitudes sol
INNER JOIN clientes c ON sol.cliente_id = c.id
INNER JOIN sucursales suc ON sol.sucursal_id = suc.id
ORDER BY sol.fecha_solicitud DESC;

-- =============================================
-- Comentarios en las tablas
-- =============================================
COMMENT ON TABLE clientes IS 'Almacena la información de los clientes que solicitan crédito';
COMMENT ON TABLE sucursales IS 'Catálogo de sucursales donde se pueden realizar solicitudes';
COMMENT ON TABLE solicitudes IS 'Registro de todas las solicitudes de crédito realizadas';
COMMENT ON TABLE usuarios_admin IS 'Usuarios administradores del sistema';
COMMENT ON VIEW vista_estadisticas_solicitudes IS 'Estadísticas agregadas por sucursal';
COMMENT ON VIEW vista_solicitudes_completas IS 'Vista completa de solicitudes con información del cliente y sucursal';

