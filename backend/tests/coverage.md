# 📊 Reporte de Cobertura de Pruebas

**Plataforma:** Linux, Python 3.11.14  
**Fecha:** 16/10/2025  
**Comando:** `pytest --cov=app --cov-report=term-missing --cov-report=html`

## 📈 Resumen General

| Métrica | Valor | Estado |
|---------|-------|--------|
| **Cobertura Total** | **90%** | ✅ Excelente |
| **Líneas Totales** | 494 | - |
| **Líneas Cubiertas** | 444 | - |
| **Líneas No Cubiertas** | 50 | - |

## 📋 Cobertura por Módulo

| Módulo | Líneas | No Cubiertas | Cobertura | Líneas Faltantes |
|--------|--------|--------------|-----------|------------------|
| `app/__init__.py` | 0 | 0 | **100%** | - |
| `app/config.py` | 22 | 0 | **100%** | - |
| `app/database.py` | 12 | 0 | **100%** | - |
| `app/models.py` | 49 | 0 | **100%** | - |
| `app/crud.py` | 93 | 5 | **95%** | 143, 184-186, 284 |
| `app/schemas.py` | 132 | 6 | **95%** | 46-51 |
| `app/auth.py` | 60 | 11 | **82%** | 41, 62, 65-66, 94, 113-122 |
| `app/main.py` | 77 | 14 | **82%** | 45-46, 135-136, 152-155, 167-168, 191-192, 212-213 |
| `app/business_logic.py` | 49 | 14 | **71%** | 73, 82, 85, 127-142 |
