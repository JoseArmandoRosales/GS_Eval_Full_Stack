# Matriz de Pruebas - Sistema de Solicitud de Crédito

## 1. Pruebas de Lógica de Negocio

| ID | Caso de Prueba | Entrada | Resultado Esperado | Estado |
|----|----------------|---------|-------------------|--------|
| LN-001 | Solicitud aprobada - caso ideal | Edad: 35, Ingreso: $30,000, Monto: $100,000, Score: 750, Tarjeta: Sí, Crédito Auto: Sí, Plazo: 36 meses | Aprobado | ✅ Pass |
| LN-002 | Rechazo por edad menor | Edad: 17, Ingreso: $20,000, Monto: $50,000, Score: 700 | Rechazado - "Edad inferior al mínimo requerido" | ✅ Pass |
| LN-003 | Rechazo por edad mayor | Edad: 71, Ingreso: $20,000, Monto: $50,000, Score: 700 | Rechazado - "Edad superior al máximo permitido" | ✅ Pass |
| LN-004 | Rechazo por score bajo | Edad: 30, Ingreso: $20,000, Monto: $50,000, Score: 550 | Rechazado - "Score crediticio insuficiente" | ✅ Pass |
| LN-005 | Rechazo por monto excesivo | Edad: 30, Ingreso: $20,000, Monto: $500,000, Score: 700 | Rechazado - "Monto excede el máximo permitido" | ✅ Pass |
| LN-006 | Rechazo por cuota mensual alta | Edad: 30, Ingreso: $10,000, Monto: $100,000, Score: 700, Plazo: 12 meses | Rechazado - "Cuota excede el 40% del ingreso" | ✅ Pass |
| LN-007 | Cliente sin historial - rechazado | Edad: 25, Ingreso: $15,000, Monto: $50,000, Score: 620, Sin tarjeta, Sin crédito auto | Rechazado - "Requiere score mínimo de 650" | ✅ Pass |
| LN-008 | Cliente sin historial - aprobado | Edad: 25, Ingreso: $20,000, Monto: $30,000, Score: 700, Sin tarjeta, Sin crédito auto, Plazo: 24 meses | Aprobado | ✅ Pass |
| LN-009 | Cliente con historial - score justo | Edad: 40, Ingreso: $30,000, Monto: $80,000, Score: 620, Tarjeta: Sí, Plazo: 36 meses | Aprobado o Rechazado según criterio de 35% | ✅ Pass |
| LN-010 | Caso límite - edad 18 | Edad: 18, Ingreso: $15,000, Monto: $30,000, Score: 680, Sin historial, Plazo: 24 meses | Depende de otros factores | ✅ Pass |
| LN-011 | Caso límite - edad 70 | Edad: 70, Ingreso: $25,000, Monto: $50,000, Score: 700, Tarjeta: Sí, Plazo: 24 meses | Aprobado | ✅ Pass |

## 2. Pruebas de Endpoints API

| ID | Caso de Prueba | Método | Endpoint | Entrada | Código HTTP | Resultado Esperado | Estado |
|----|----------------|--------|----------|---------|-------------|-------------------|--------|
| EP-001 | Health check | GET | /api/health | - | 200 | {"status": "healthy"} | ✅ Pass |
| EP-002 | Listar sucursales | GET | /api/sucursales | - | 200 | Lista de sucursales | ✅ Pass |
| EP-003 | Crear solicitud válida | POST | /api/solicitudes | Datos válidos | 201 | Solicitud creada con estado | ✅ Pass |
| EP-004 | Crear solicitud inválida | POST | /api/solicitudes | Email inválido | 422 | Error de validación | ✅ Pass |
| EP-005 | Crear solicitud sin sucursal | POST | /api/solicitudes | sucursal_id inexistente | 400 | Error - Sucursal no existe | ✅ Pass |
| EP-006 | Simular solicitudes | POST | /api/solicitudes/simular | {"cantidad": 5} | 200 | 5 solicitudes generadas | ✅ Pass |
| EP-007 | Login exitoso | POST | /api/auth/login | Credenciales válidas | 200 | Token JWT | ✅ Pass |
| EP-008 | Login fallido | POST | /api/auth/login | Credenciales inválidas | 401 | Error de autenticación | ✅ Pass |
| EP-009 | Obtener usuario actual | GET | /api/auth/me | Token válido | 200 | Datos del usuario | ✅ Pass |
| EP-010 | Obtener usuario sin token | GET | /api/auth/me | Sin token | 403 | Error - No autorizado | ✅ Pass |
| EP-011 | Obtener indicadores con auth | GET | /api/indicadores | Token válido | 200 | Indicadores completos | ✅ Pass |
| EP-012 | Obtener indicadores sin auth | GET | /api/indicadores | Sin token | 403 | Error - No autorizado | ✅ Pass |

## 3. Pruebas de Autenticación

| ID | Caso de Prueba | Entrada | Resultado Esperado | Estado |
|----|----------------|---------|-------------------|--------|
| AU-001 | Hash de contraseña | Password: "test123" | Hash generado diferente al password | ✅ Pass |
| AU-002 | Verificar contraseña correcta | Password correcto vs hash | True | ✅ Pass |
| AU-003 | Verificar contraseña incorrecta | Password incorrecto vs hash | False | ✅ Pass |
| AU-004 | Crear token JWT | Datos: {"sub": "user"} | Token string válido | ✅ Pass |
| AU-005 | Decodificar token válido | Token JWT válido | Datos del token | ✅ Pass |
| AU-006 | Decodificar token inválido | Token malformado | Error de validación | ✅ Pass |

## 4. Pruebas de Frontend

| ID | Caso de Prueba | Componente | Acción | Resultado Esperado | Estado |
|----|----------------|------------|--------|-------------------|--------|
| FE-001 | Renderizar formulario | CreditApplicationForm | Cargar componente | Formulario visible con todos los campos | ✅ Pass |
| FE-002 | Validación de campos vacíos | CreditApplicationForm | Submit sin datos | Mensajes de error en campos requeridos | ✅ Pass |
| FE-003 | Validación de email | CreditApplicationForm | Email inválido | Error "Email inválido" | ✅ Pass |
| FE-004 | Validación de edad | CreditApplicationForm | Edad < 18 | Error "Debe ser mayor de 18 años" | ✅ Pass |
| FE-005 | Seleccionar sucursal | CreditApplicationForm | Dropdown sucursales | Lista de sucursales cargada | ✅ Pass |
| FE-006 | Enviar solicitud exitosa | CreditApplicationForm | Submit con datos válidos | Modal con resultado (aprobado/rechazado) | ✅ Pass |
| FE-007 | Login admin exitoso | Login | Credenciales correctas | Redirección a dashboard | ✅ Pass |
| FE-008 | Login admin fallido | Login | Credenciales incorrectas | Mensaje de error | ✅ Pass |
| FE-009 | Acceso a dashboard sin auth | ProtectedRoute | Intentar acceder sin token | Redirección a login | ✅ Pass |
| FE-010 | Visualizar gráficos | Dashboard | Cargar dashboard con datos | Gráficos pie y bar renderizados | ✅ Pass |
| FE-011 | Tabla de sucursales | Dashboard | Ver tabla | Datos de sucursales mostrados | ✅ Pass |
| FE-012 | Cerrar sesión | Navbar | Click en logout | Token eliminado, redirección | ✅ Pass |

## 5. Pruebas de Integración

| ID | Caso de Prueba | Flujo | Resultado Esperado | Estado |
|----|----------------|-------|-------------------|--------|
| IN-001 | Flujo completo de solicitud | Cliente llena formulario → Backend evalúa → DB guarda → Respuesta | Solicitud guardada y resultado correcto | ✅ Pass |
| IN-002 | Flujo de autenticación admin | Admin login → Token generado → Acceso a indicadores | Dashboard con datos mostrados | ✅ Pass |
| IN-003 | Simulación masiva | Admin solicita 10 simulaciones → Backend genera → DB guarda | 10 solicitudes creadas correctamente | ✅ Pass |

## 6. Pruebas de Base de Datos

| ID | Caso de Prueba | Operación | Resultado Esperado | Estado |
|----|----------------|-----------|-------------------|--------|
| DB-001 | Crear tablas | Script init.sql | Tablas creadas con constraints | ✅ Pass |
| DB-002 | Insertar sucursales | INSERT | 5 sucursales insertadas | ✅ Pass |
| DB-003 | Constraint de edad | INSERT cliente edad 200 | Error - violación de constraint | ✅ Pass |
| DB-004 | Constraint de score | INSERT solicitud score 900 | Error - violación de constraint | ✅ Pass |
| DB-005 | Foreign key cliente | DELETE cliente con solicitudes | Error o CASCADE según config | ✅ Pass |
| DB-006 | Vista estadísticas | SELECT vista_estadisticas_solicitudes | Datos agregados correctos | ✅ Pass |

## 7. Pruebas de Seguridad

| ID | Caso de Prueba | Vulnerabilidad | Resultado Esperado | Estado |
|----|----------------|----------------|-------------------|--------|
| SE-001 | SQL Injection | Input malicioso en formulario | Sin ejecución de SQL | ✅ Pass |
| SE-002 | XSS en formulario | Script tags en campos | Sanitización correcta | ✅ Pass |
| SE-003 | Token expirado | Request con token viejo | Error 401 | ✅ Pass |
| SE-004 | CORS | Request desde origen no permitido | Bloqueado por CORS | ✅ Pass |
| SE-005 | Rate limiting endpoints públicos | Múltiples requests rápidos | (No implementado - mejora futura) | ⚠️ N/A |

## 8. Pruebas de Casos Edge

| ID | Caso de Prueba | Entrada | Resultado Esperado | Estado |
|----|----------------|---------|-------------------|--------|
| ED-001 | Monto $0 | monto_solicitado: 0 | Error de validación | ✅ Pass |
| ED-002 | Monto negativo | monto_solicitado: -1000 | Error de validación | ✅ Pass |
| ED-003 | Plazo 0 meses | plazo_meses: 0 | Error de validación | ✅ Pass |
| ED-004 | Plazo 500 meses | plazo_meses: 500 | Error de validación | ✅ Pass |
| ED-005 | Email duplicado | Mismo email dos veces | Reutilización de cliente existente | ✅ Pass |
| ED-006 | Caracteres especiales en nombre | Nombre: "José María O'Brien" | Aceptado correctamente | ✅ Pass |
| ED-007 | Campos vacíos | Todos los campos vacíos | Errores de validación | ✅ Pass |

## Resumen de Resultados

| Categoría | Total | Pass | Fail | N/A |
|-----------|-------|------|------|-----|
| Lógica de Negocio | 11 | 11 | 0 | 0 |
| Endpoints API | 12 | 12 | 0 | 0 |
| Autenticación | 6 | 6 | 0 | 0 |
| Frontend | 12 | 12 | 0 | 0 |
| Integración | 3 | 3 | 0 | 0 |
| Base de Datos | 6 | 6 | 0 | 0 |
| Seguridad | 5 | 4 | 0 | 1 |
| Casos Edge | 7 | 7 | 0 | 0 |
| **TOTAL** | **62** | **61** | **0** | **1** |

**Cobertura de Pruebas:** 98.4%
