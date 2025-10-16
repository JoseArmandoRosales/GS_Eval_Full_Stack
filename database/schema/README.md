# Esquema de Base de Datos

## Descripción General

Base de datos PostgreSQL para el sistema de solicitud de crédito.

## Tablas Principales

### 1. clientes
Almacena la información de los clientes que solicitan crédito.

**Campos:**
- `id`: Identificador único (SERIAL PRIMARY KEY)
- `nombre`: Nombre del cliente (VARCHAR 100)
- `apellido`: Apellido del cliente (VARCHAR 100)
- `email`: Email único del cliente (VARCHAR 150, UNIQUE)
- `telefono`: Teléfono de contacto (VARCHAR 20)
- `fecha_nacimiento`: Fecha de nacimiento (DATE)
- `edad`: Edad calculada (INTEGER)
- `created_at`: Fecha de registro (TIMESTAMP)

### 2. sucursales
Catálogo de sucursales donde se pueden realizar solicitudes.

**Campos:**
- `id`: Identificador único (SERIAL PRIMARY KEY)
- `nombre`: Nombre de la sucursal (VARCHAR 100)
- `ciudad`: Ciudad donde se ubica (VARCHAR 100)
- `direccion`: Dirección completa (VARCHAR 255)
- `telefono`: Teléfono de contacto (VARCHAR 20)
- `created_at`: Fecha de registro (TIMESTAMP)

### 3. solicitudes
Registro de todas las solicitudes de crédito realizadas.

**Campos:**
- `id`: Identificador único (SERIAL PRIMARY KEY)
- `cliente_id`: Referencia al cliente (FK a clientes)
- `sucursal_id`: Referencia a la sucursal (FK a sucursales)
- `monto_solicitado`: Monto del crédito solicitado (DECIMAL 15,2)
- `ingreso_mensual`: Ingreso mensual declarado (DECIMAL 15,2)
- `score_crediticio`: Score crediticio (INTEGER, 300-850)
- `tiene_tarjeta_credito`: Indicador de tarjeta de crédito (BOOLEAN)
- `tiene_credito_automotriz`: Indicador de crédito automotriz (BOOLEAN)
- `plazo_meses`: Plazo en meses (INTEGER, 1-360)
- `estado`: Estado de la solicitud ('aprobado' o 'rechazado')
- `motivo_rechazo`: Motivo del rechazo si aplica (TEXT)
- `fecha_solicitud`: Fecha y hora de la solicitud (TIMESTAMP)

### 4. usuarios_admin
Usuarios administradores del sistema.

**Campos:**
- `id`: Identificador único (SERIAL PRIMARY KEY)
- `username`: Nombre de usuario único (VARCHAR 50, UNIQUE)
- `password_hash`: Hash de la contraseña (VARCHAR 255)
- `email`: Email único (VARCHAR 150, UNIQUE)
- `created_at`: Fecha de registro (TIMESTAMP)

## Vistas

### vista_estadisticas_solicitudes
Proporciona estadísticas agregadas por sucursal incluyendo total de solicitudes, aprobadas, rechazadas y montos.

### vista_solicitudes_completas
Vista desnormalizada con toda la información de solicitudes, clientes y sucursales para consultas rápidas.

## Índices

Los índices están creados para optimizar las consultas más frecuentes:
- Búsquedas por cliente en solicitudes
- Búsquedas por sucursal en solicitudes
- Filtros por estado de solicitud
- Ordenamiento por fecha
- Búsquedas por email de cliente
- Autenticación de usuarios admin

## Constraints

- Verificación de rangos válidos (edad, score crediticio, montos positivos)
- Claves foráneas con políticas de eliminación apropiadas
- Unicidad en emails y usernames
- Validación de estados permitidos

