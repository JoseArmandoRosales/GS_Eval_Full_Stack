# Instrucciones de Ejecución - Sistema de Solicitud de Crédito

## Inicio Rápido (5 minutos)

### Requisitos
- Docker Desktop instalado y corriendo
- Puertos disponibles: 3000, 8000, 5432

### Pasos para Ejecutar

1. **Abrir terminal en la carpeta del proyecto**
```bash
cd GS_Ejercicio
```

2. **Iniciar todos los servicios con Docker Compose**
```bash
docker-compose up -d
```

3. **Esperar a que los servicios inicien** (aproximadamente 30-60 segundos)
```bash
# Ver el estado de los contenedores
docker-compose ps

# Ver logs para confirmar que todo está corriendo
docker-compose logs -f
```

4. **Acceder a las aplicaciones**
- **Frontend (Clientes)**: http://localhost:3000
- **Backend API Docs**: http://localhost:8000/api/docs
- **Dashboard Admin**: http://localhost:3000/admin

### Credenciales de Administrador

```
Usuario: admin
Contraseña: admin123
```

---

## Guía de Uso del Sistema

### Para Clientes (Solicitar Crédito)

1. Abrir navegador en http://localhost:3000
2. Verás el formulario de solicitud de crédito
3. Llenar todos los campos:
   - **Datos Personales**: Nombre, apellido, email, teléfono, fecha de nacimiento
   - **Información Financiera**: Ingreso mensual, score crediticio (300-850), checkboxes de productos crediticios
   - **Detalles del Crédito**: Monto solicitado, plazo en meses, sucursal
4. Hacer clic en "Enviar Solicitud"
5. Se mostrará un modal con el resultado:
   - ✅ **APROBADO**: Con detalles de la solicitud
   - ❌ **RECHAZADO**: Con motivo específico del rechazo

### Para Administradores (Ver Indicadores)

1. Hacer clic en "Admin" en la barra superior o ir a http://localhost:3000/admin
2. Iniciar sesión:
   - Usuario: `admin`
   - Contraseña: `admin123`
3. Serás redirigido al dashboard con:
   - Tarjetas con total de solicitudes, aprobadas, rechazadas y monto aprobado
   - Gráfico de pie con distribución aprobados vs rechazados
   - Gráfico de barras con solicitudes por sucursal
   - Tabla detallada con estadísticas por sucursal
4. Para cerrar sesión, hacer clic en "Cerrar Sesión" en la barra superior

---

## Casos de Prueba Recomendados

### Solicitud APROBADA (Caso Ideal)

```
Nombre: Juan
Apellido: Pérez
Email: juan.perez@ejemplo.com
Teléfono: 55-1234-5678
Fecha de Nacimiento: 1990-01-15
Ingreso Mensual: $30,000
Score Crediticio: 720
Tiene tarjeta de crédito: ✓ Sí
Tiene crédito automotriz: ✓ Sí
Monto Solicitado: $100,000
Plazo: 36 meses
Sucursal: Cualquiera

Resultado Esperado: ✅ APROBADO
```

### Solicitud RECHAZADA (Score bajo)

```
Nombre: María
Apellido: López
Email: maria.lopez@ejemplo.com
Edad: 28
Ingreso Mensual: $20,000
Score Crediticio: 550 (< 600 mínimo)
Tiene tarjeta de crédito: ☐ No
Tiene crédito automotriz: ☐ No
Monto Solicitado: $50,000
Plazo: 24 meses
Sucursal: Cualquiera

Resultado Esperado: ❌ RECHAZADO - "Score crediticio insuficiente"
```

### Solicitud RECHAZADA (Cuota muy alta)

```
Nombre: Carlos
Apellido: Ramírez
Email: carlos.ramirez@ejemplo.com
Edad: 35
Ingreso Mensual: $10,000
Score Crediticio: 700
Tiene tarjeta de crédito: ✓ Sí
Tiene crédito automotriz: ☐ No
Monto Solicitado: $100,000
Plazo: 12 meses (cuota: $8,333)
Sucursal: Cualquiera

Resultado Esperado: ❌ RECHAZADO - "Cuota excede el 40% del ingreso"
```

### Solicitud RECHAZADA (Cliente nuevo)

```
Nombre: Ana
Apellido: García
Email: ana.garcia@ejemplo.com
Edad: 25
Ingreso Mensual: $15,000
Score Crediticio: 620
Tiene tarjeta de crédito: ☐ No (sin historial)
Tiene crédito automotriz: ☐ No (sin historial)
Monto Solicitado: $50,000
Plazo: 24 meses
Sucursal: Cualquiera

Resultado Esperado: ❌ RECHAZADO - "Para clientes sin historial crediticio se requiere score mínimo de 650"
```

---

## Probar la API Directamente

### Ver Documentación Interactiva (Swagger)
http://localhost:8000/api/docs

### Ejemplos de Requests con curl

#### 1. Crear Solicitud
```bash
curl -X POST "http://localhost:8000/api/solicitudes" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Pedro",
    "apellido": "Martínez",
    "email": "pedro.martinez@ejemplo.com",
    "telefono": "55-9876-5432",
    "fecha_nacimiento": "1988-05-20",
    "edad": 35,
    "monto_solicitado": 80000,
    "ingreso_mensual": 25000,
    "score_crediticio": 680,
    "tiene_tarjeta_credito": true,
    "tiene_credito_automotriz": false,
    "plazo_meses": 36,
    "sucursal_id": 1
  }'
```

#### 2. Simular 10 Solicitudes
```bash
curl -X POST "http://localhost:8000/api/solicitudes/simular" \
  -H "Content-Type: application/json" \
  -d '{"cantidad": 10}'
```

#### 3. Login Admin
```bash
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

#### 4. Obtener Indicadores (requiere token del paso 3)
```bash
TOKEN="<token_obtenido_del_login>"

curl -X GET "http://localhost:8000/api/indicadores" \
  -H "Authorization: Bearer $TOKEN"
```

---

## Generar Datos de Prueba

Para poblar el sistema con solicitudes de prueba:

### Opción 1: Desde el navegador
1. Login como admin
2. Abrir consola del navegador (F12)
3. Ejecutar:
```javascript
fetch('http://localhost:8000/api/solicitudes/simular', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({cantidad: 20})
})
.then(r => r.json())
.then(data => console.log('Solicitudes creadas:', data));
```

### Opción 2: Desde terminal
```bash
curl -X POST "http://localhost:8000/api/solicitudes/simular" \
  -H "Content-Type: application/json" \
  -d '{"cantidad": 20}'
```

---

## Verificar Base de Datos

### Conectarse a PostgreSQL
```bash
docker-compose exec db psql -U credituser -d credit_system
```

### Consultas Útiles
```sql
-- Ver todas las solicitudes
SELECT id, estado, monto_solicitado, score_crediticio, fecha_solicitud 
FROM solicitudes 
ORDER BY fecha_solicitud DESC 
LIMIT 10;

-- Ver estadísticas
SELECT 
    COUNT(*) as total,
    SUM(CASE WHEN estado = 'aprobado' THEN 1 ELSE 0 END) as aprobadas,
    SUM(CASE WHEN estado = 'rechazado' THEN 1 ELSE 0 END) as rechazadas
FROM solicitudes;

-- Ver vista de estadísticas por sucursal
SELECT * FROM vista_estadisticas_solicitudes;

-- Ver solicitudes completas con info de cliente
SELECT * FROM vista_solicitudes_completas LIMIT 5;

-- Salir
\q
```

---

## Ejecutar Pruebas Unitarias

### Dentro del contenedor de backend
```bash
docker-compose exec backend pytest
```

### Con cobertura
```bash
docker-compose exec backend pytest --cov=app --cov-report=term-missing
```

### Pruebas específicas
```bash
# Solo lógica de negocio
docker-compose exec backend pytest tests/test_business_logic.py -v

# Solo endpoints
docker-compose exec backend pytest tests/test_endpoints.py -v

# Solo autenticación
docker-compose exec backend pytest tests/test_auth.py -v
```

---

## Detener y Limpiar

### Detener servicios (mantiene datos)
```bash
docker-compose down
```

### Detener y eliminar volúmenes (limpia BD)
```bash
docker-compose down -v
```

### Limpiar todo (imágenes, contenedores, volúmenes)
```bash
docker-compose down -v --rmi all
```

---

## Solución de Problemas Comunes

### Error: Puerto ya en uso

**Síntoma**: `Bind for 0.0.0.0:3000 failed: port is already allocated`

**Solución**:
```bash
# Ver qué está usando el puerto
# Windows:
netstat -ano | findstr :3000

# Linux/Mac:
lsof -ti:3000

# Matar el proceso o cambiar puertos en docker-compose.yml
```

### Error: Contenedor de backend no inicia

**Solución**:
```bash
# Ver logs
docker-compose logs backend

# Reconstruir imagen
docker-compose build backend
docker-compose up -d
```

### Error: No se puede conectar a la base de datos

**Solución**:
```bash
# Verificar que PostgreSQL esté corriendo
docker-compose ps db

# Reiniciar servicio
docker-compose restart db

# Ver logs de BD
docker-compose logs db
```

### Frontend muestra "Network Error"

**Solución**:
1. Verificar que backend esté corriendo: http://localhost:8000/api/health
2. Verificar CORS en backend
3. Limpiar caché del navegador
4. Revisar logs: `docker-compose logs frontend`

---

## Estructura de URLs

| URL | Descripción |
|-----|-------------|
| http://localhost:3000 | Frontend - Página de solicitud |
| http://localhost:3000/admin | Login de administrador |
| http://localhost:3000/admin/dashboard | Dashboard con indicadores |
| http://localhost:8000 | Backend - Información de la API |
| http://localhost:8000/api/docs | Documentación Swagger |
| http://localhost:8000/api/redoc | Documentación ReDoc |
| http://localhost:8000/api/health | Health check |

---

## Configuración Avanzada

### Cambiar Puerto del Frontend
Editar `docker-compose.yml`:
```yaml
services:
  frontend:
    ports:
      - "8080:80"  # Cambiar 3000 a 8080
```

### Cambiar Puerto del Backend
Editar `docker-compose.yml`:
```yaml
services:
  backend:
    ports:
      - "8001:8000"  # Cambiar 8000 a 8001
```

### Cambiar Credenciales de Admin
Editar archivo `.env`:
```env
ADMIN_USERNAME=miadmin
ADMIN_PASSWORD=mipassword123
```

---

## Características Adicionales

### Sucursales Precargadas
El sistema incluye 5 sucursales:
1. Sucursal Centro - Ciudad de México
2. Sucursal Norte - Monterrey
3. Sucursal Occidente - Guadalajara
4. Sucursal Bajío - León
5. Sucursal Sureste - Mérida

### Validaciones Automáticas
- Email válido
- Edad entre 18-70 años
- Score crediticio entre 300-850
- Plazo máximo 60 meses

### Seguridad Implementada
- JWT con expiración de 30 minutos
- Contraseñas hasheadas con bcrypt
- CORS configurado
- Validación de datos con Pydantic
- Protección contra SQL injection

---

## Recursos Adicionales

- **README.md**: Documentación completa del proyecto
- **docs/diagramas.md**: Diagramas de arquitectura y casos de uso
- **docs/matriz_pruebas.md**: 62 casos de prueba documentados
- **database/schema/README.md**: Esquema de base de datos detallado
- **http://localhost:8000/api/docs**: API interactiva

---

## Resumen de Comandos Esenciales

```bash
# Iniciar
docker-compose up -d

# Ver logs
docker-compose logs -f

# Estado
docker-compose ps

# Detener
docker-compose down

# Reiniciar un servicio
docker-compose restart backend

# Reconstruir
docker-compose build --no-cache
docker-compose up -d

# Pruebas
docker-compose exec backend pytest

# Base de datos
docker-compose exec db psql -U credituser -d credit_system
```

---