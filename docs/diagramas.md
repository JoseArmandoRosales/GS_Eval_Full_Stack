# Diagramas del Sistema - Sistema de Solicitud de Crédito

## 1. Diagrama de Casos de Uso

```
┌─────────────────────────────────────────────────────────────┐
│         Sistema de Solicitud de Crédito                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────┐                                                │
│  │ Cliente │                                                │
│  └────┬────┘                                                │
│       │                                                      │
│       ├──► (Solicitar Crédito)                             │
│       │         │                                           │
│       │         ├─► <include> (Llenar Formulario)         │
│       │         ├─► <include> (Seleccionar Sucursal)      │
│       │         └─► <include> (Ver Resultado)             │
│       │                                                      │
│       └──► (Consultar Sucursales)                          │
│                                                              │
│  ┌──────────────┐                                           │
│  │ Administrador│                                           │
│  └──────┬───────┘                                           │
│         │                                                    │
│         ├──► (Iniciar Sesión)                              │
│         │         └─► <extend> (Autenticación JWT)        │
│         │                                                    │
│         ├──► (Ver Dashboard)                               │
│         │         ├─► <include> (Ver Gráficos)            │
│         │         ├─► <include> (Ver Estadísticas)        │
│         │         └─► <include> (Ver Tabla Sucursales)    │
│         │                                                    │
│         ├──► (Simular Solicitudes)                         │
│         │         └─► <include> (Generar Datos Aleatorios)│
│         │                                                    │
│         └──► (Cerrar Sesión)                               │
│                                                              │
│  ┌─────────┐                                                │
│  │ Sistema │                                                │
│  └────┬────┘                                                │
│       │                                                      │
│       ├──► (Evaluar Solicitud)                             │
│       │         ├─► <include> (Validar Edad)              │
│       │         ├─► <include> (Validar Score)             │
│       │         ├─► <include> (Calcular Capacidad Pago)   │
│       │         └─► <include> (Determinar Aprobación)     │
│       │                                                      │
│       └──► (Persistir Datos)                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## 2. Diagrama de Secuencia - Solicitud de Crédito

```
Cliente          Frontend         Backend         Lógica          DB
  │                 │                │            Negocio          │
  │──Llenar form───>│                │              │              │
  │                 │                │              │              │
  │──Submit────────>│                │              │              │
  │                 │                │              │              │
  │                 │──POST /api/────>│              │              │
  │                 │   solicitudes  │              │              │
  │                 │                │              │              │
  │                 │                │──Validar────>│              │
  │                 │                │   Pydantic   │              │
  │                 │                │<─────────────│              │
  │                 │                │              │              │
  │                 │                │──Buscar──────────────────>│
  │                 │                │   Cliente    │              │
  │                 │                │<──────────────────────────│
  │                 │                │              │              │
  │                 │                │──Evaluar────>│              │
  │                 │                │   Solicitud  │              │
  │                 │                │   (Reglas)   │              │
  │                 │                │<─Aprobado/───│              │
  │                 │                │   Rechazado  │              │
  │                 │                │              │              │
  │                 │                │──Guardar──────────────────>│
  │                 │                │   Solicitud  │              │
  │                 │                │<──────────────────────────│
  │                 │                │              │              │
  │                 │<──Response─────│              │              │
  │                 │   (Resultado)  │              │              │
  │                 │                │              │              │
  │<──Modal────────│                │              │              │
  │   Resultado    │                │              │              │
  │                 │                │              │              │
```

## 3. Diagrama de Secuencia - Autenticación Admin

```
Admin         Frontend         Backend         Auth          DB
  │               │                │           Module         │
  │──Ir a login──>│                │             │            │
  │               │                │             │            │
  │──Ingresar─────>│                │             │            │
  │   credenciales│                │             │            │
  │               │                │             │            │
  │──Submit──────>│                │             │            │
  │               │                │             │            │
  │               │──POST /api/────>│             │            │
  │               │   auth/login   │             │            │
  │               │                │             │            │
  │               │                │──Buscar─────────────────>│
  │               │                │   usuario   │            │
  │               │                │<────────────────────────│
  │               │                │             │            │
  │               │                │──Verify────>│            │
  │               │                │   Password  │            │
  │               │                │<────────────│            │
  │               │                │             │            │
  │               │                │──Create────>│            │
  │               │                │   JWT Token │            │
  │               │                │<────────────│            │
  │               │                │             │            │
  │               │<──Token────────│             │            │
  │               │                │             │            │
  │<──Guardar─────│                │             │            │
  │   token local │                │             │            │
  │               │                │             │            │
  │──Redirect────>│                │             │            │
  │   Dashboard   │                │             │            │
  │               │                │             │            │
  │               │──GET /api/─────>│             │            │
  │               │   indicadores  │             │            │
  │               │   +Bearer Token│             │            │
  │               │                │             │            │
  │               │                │──Validate──>│            │
  │               │                │   Token     │            │
  │               │                │<────────────│            │
  │               │                │             │            │
  │               │                │──Query──────────────────>│
  │               │                │<────────────────────────│
  │               │                │             │            │
  │               │<──Indicadores──│             │            │
  │               │                │             │            │
  │<──Dashboard───│                │             │            │
  │   con datos   │                │             │            │
  │               │                │             │            │
```

## 4. Diagrama de Arquitectura

```
┌────────────────────────────────────────────────────────────────┐
│                         CAPA DE PRESENTACIÓN                    │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │          Frontend (React + TypeScript)                   │  │
│  │  ┌────────────┐  ┌──────────────┐  ┌────────────────┐ │  │
│  │  │   Home     │  │    Login     │  │   Dashboard    │ │  │
│  │  │  Página    │  │    Página    │  │     Página     │ │  │
│  │  └────────────┘  └──────────────┘  └────────────────┘ │  │
│  │                                                          │  │
│  │  ┌────────────────────────────────────────────────────┐│  │
│  │  │          Componentes                                ││  │
│  │  │  - CreditApplicationForm                           ││  │
│  │  │  - ResultModal                                     ││  │
│  │  │  - Navbar                                          ││  │
│  │  │  - ProtectedRoute                                  ││  │
│  │  └────────────────────────────────────────────────────┘│  │
│  │                                                          │  │
│  │  ┌────────────┐  ┌──────────────┐  ┌────────────────┐ │  │
│  │  │  API Client│  │  Auth Store  │  │     Types      │ │  │
│  │  │   (Axios)  │  │  (Zustand)   │  │  (TypeScript)  │ │  │
│  │  └────────────┘  └──────────────┘  └────────────────┘ │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              │ HTTP/REST API (JSON)
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                       CAPA DE APLICACIÓN                         │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │          Backend (FastAPI + Python)                      │  │
│  │                                                          │  │
│  │  ┌────────────────────────────────────────────────────┐│  │
│  │  │             API Endpoints                           ││  │
│  │  │  /api/solicitudes    /api/auth/login              ││  │
│  │  │  /api/sucursales     /api/indicadores             ││  │
│  │  └────────────────────────────────────────────────────┘│  │
│  │                                                          │  │
│  │  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐ │  │
│  │  │   Schemas   │  │    Auth      │  │   Business   │ │  │
│  │  │  (Pydantic) │  │    (JWT)     │  │    Logic     │ │  │
│  │  └─────────────┘  └──────────────┘  └──────────────┘ │  │
│  │                                                          │  │
│  │  ┌─────────────┐  ┌──────────────┐                    │  │
│  │  │    CRUD     │  │   Middleware │                    │  │
│  │  │ Operations  │  │    (CORS)    │                    │  │
│  │  └─────────────┘  └──────────────┘                    │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              │ SQLAlchemy ORM
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                        CAPA DE DATOS                             │
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │         Base de Datos (PostgreSQL)                       │  │
│  │                                                          │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │  │
│  │  │   clientes   │  │  solicitudes │  │  sucursales  │ │  │
│  │  └──────────────┘  └──────────────┘  └──────────────┘ │  │
│  │                                                          │  │
│  │  ┌──────────────┐                                       │  │
│  │  │usuarios_admin│                                       │  │
│  │  └──────────────┘                                       │  │
│  │                                                          │  │
│  │  ┌────────────────────────────────────────────────────┐│  │
│  │  │               Vistas                                ││  │
│  │  │  - vista_estadisticas_solicitudes                  ││  │
│  │  │  - vista_solicitudes_completas                     ││  │
│  │  └────────────────────────────────────────────────────┘│  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                     INFRAESTRUCTURA (Docker)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────┐    ┌────────────┐    ┌─────────────┐          │
│  │ Container  │    │ Container  │    │  Container  │          │
│  │  Frontend  │    │  Backend   │    │   Database  │          │
│  │  (Nginx)   │◄───┤  (Uvicorn) │◄───┤ (PostgreSQL)│          │
│  │  :3000     │    │   :8000    │    │   :5432     │          │
│  └────────────┘    └────────────┘    └─────────────┘          │
│                                                                  │
│         └──────────────┬──────────────┘                         │
│                   credit_network                                │
│                  (Docker Network)                               │
└─────────────────────────────────────────────────────────────────┘
```

## 5. Diagrama Entidad-Relación (ER)

```
┌──────────────────────┐         ┌──────────────────────┐
│      clientes        │         │     sucursales       │
├──────────────────────┤         ├──────────────────────┤
│ PK  id (INT)         │         │ PK  id (INT)         │
│     nombre (VARCHAR) │         │     nombre (VARCHAR) │
│     apellido (VAR)   │         │     ciudad (VARCHAR) │
│     email (VARCHAR)  │         │     direccion (VAR)  │
│     telefono (VAR)   │         │     telefono (VAR)   │
│     fecha_nac (DATE) │         │     created_at (TS)  │
│     edad (INT)       │         └──────────┬───────────┘
│     created_at (TS)  │                    │
└──────────┬───────────┘                    │
           │                                 │
           │                                 │
           │ 1                               │ 1
           │                                 │
           │                                 │
           │              N                  │
           └────────────────┐   N ┌──────────┘
                            │     │
                    ┌───────▼─────▼───────────┐
                    │     solicitudes         │
                    ├─────────────────────────┤
                    │ PK  id (INT)            │
                    │ FK  cliente_id (INT)    │
                    │ FK  sucursal_id (INT)   │
                    │     monto_solicitado ($)│
                    │     ingreso_mensual ($) │
                    │     score_crediticio    │
                    │     tiene_tarjeta (BOOL)│
                    │     tiene_credito (BOOL)│
                    │     plazo_meses (INT)   │
                    │     estado (VARCHAR)    │
                    │     motivo_rechazo (TXT)│
                    │     fecha_solicitud (TS)│
                    └─────────────────────────┘


┌──────────────────────────────┐
│      usuarios_admin          │
├──────────────────────────────┤
│ PK  id (INT)                 │
│     username (VARCHAR) UNIQUE│
│     password_hash (VARCHAR)  │
│     email (VARCHAR) UNIQUE   │
│     created_at (TIMESTAMP)   │
└──────────────────────────────┘


Relaciones:
- clientes 1:N solicitudes (un cliente puede tener muchas solicitudes)
- sucursales 1:N solicitudes (una sucursal puede recibir muchas solicitudes)
- usuarios_admin: tabla independiente para administradores del sistema

Constraints:
- edad: CHECK (edad >= 0 AND edad <= 150)
- score_crediticio: CHECK (score >= 300 AND score <= 850)
- estado: CHECK (estado IN ('aprobado', 'rechazado'))
- monto_solicitado, ingreso_mensual: CHECK (> 0)
- plazo_meses: CHECK (> 0 AND <= 360)

Índices:
- idx_solicitudes_cliente ON solicitudes(cliente_id)
- idx_solicitudes_sucursal ON solicitudes(sucursal_id)
- idx_solicitudes_estado ON solicitudes(estado)
- idx_solicitudes_fecha ON solicitudes(fecha_solicitud)
- idx_clientes_email ON clientes(email)
- idx_usuarios_admin_username ON usuarios_admin(username)
```

## 6. Diagrama de Flujo - Evaluación de Crédito

```
                    ┌─────────────────┐
                    │   Solicitud     │
                    │   Recibida      │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Validar Edad    │
                    │  18 <= edad     │
                    │    <= 70 ?      │
                    └────┬───────┬────┘
                         │ No    │ Sí
                         ▼       │
                   [Rechazar]    │
                                 ▼
                    ┌─────────────────┐
                    │  Validar Score  │
                    │   >= 600 ?      │
                    └────┬───────┬────┘
                         │ No    │ Sí
                         ▼       │
                   [Rechazar]    │
                                 ▼
                    ┌─────────────────┐
                    │ Validar Monto   │
                    │ <= 10x ingreso? │
                    └────┬───────┬────┘
                         │ No    │ Sí
                         ▼       │
                   [Rechazar]    │
                                 ▼
                    ┌─────────────────┐
                    │  Calcular Cuota │
                    │  Cuota <= 40%   │
                    │   ingreso ?     │
                    └────┬───────┬────┘
                         │ No    │ Sí
                         ▼       │
                   [Rechazar]    │
                                 ▼
                    ┌─────────────────┐
                    │ ¿Tiene historial│
                    │  crediticio?    │
                    └────┬───────┬────┘
                   No    │       │ Sí
                         ▼       │
              ┌──────────────┐  │
              │Score >= 650? │  │
              │Cuota <= 30%? │  │
              │Monto <= 5x ? │  │
              └──┬────────┬──┘  │
           No    │ Sí     │     │
                 ▼        │     │
            [Rechazar]    │     │
                          │     │
                          ▼     ▼
                    ┌─────────────────┐
                    │   ¡APROBADO!    │
                    └─────────────────┘
```

## Notas Técnicas

- **Frontend**: React 18 con TypeScript, Material-UI para componentes, React Hook Form para formularios, Recharts para gráficos
- **Backend**: FastAPI con Python 3.11+, SQLAlchemy para ORM, Pydantic para validación
- **Base de Datos**: PostgreSQL 15 con constraints y vistas optimizadas
- **Autenticación**: JWT (JSON Web Tokens) con bcrypt para hashing de contraseñas
- **Contenedores**: Docker Compose para orquestación de los 3 servicios
- **API**: RESTful API con documentación automática (Swagger/OpenAPI)

