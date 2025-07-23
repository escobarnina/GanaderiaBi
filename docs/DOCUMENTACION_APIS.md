# 📚 Documentación de APIs - Sistema de Inteligencia de Negocios Ganadero

## 🎯 **Descripción General**

Este documento describe las APIs del sistema de inteligencia de negocios ganadero, implementado con **Clean Architecture** y preparado para microservicios.

## 🚀 **Acceso a la Documentación**

### **Endpoints de Documentación**
- **Swagger UI**: `http://localhost:8000/api/docs/`
- **ReDoc**: `http://localhost:8000/api/redoc/`
- **Schema OpenAPI**: `http://localhost:8000/api/schema/`

## 📊 **Estructura de APIs**

### **Base URL**
```
http://localhost:8000/api/analytics/
```

### **Dominios Disponibles**

#### **🏷️ Marcas de Ganado** (`/marcas/`)
- **CRUD Básico**: Crear, leer, actualizar, eliminar marcas
- **Gestión de Estado**: Aprobar, rechazar marcas
- **Consultas Especializadas**: Pendientes, por procesar, procesadas hoy
- **Estadísticas**: Por raza, por departamento
- **Procesamiento Masivo**: Operaciones en lote

#### **🎨 Logos con IA** (`/logos/`)
- **Generación**: Crear logos automáticamente
- **Gestión**: Listar, obtener, actualizar logos
- **Calidad**: Análisis de calidad de logos
- **Estadísticas**: Rendimiento de IA
- **Rendimiento**: Métricas de generación

#### **📊 Dashboard** (`/dashboard/`)
- **Datos Ejecutivos**: Métricas principales
- **KPIs**: Indicadores clave
- **Tendencias**: Análisis temporal
- **Reportes**: Generación de reportes

#### **📈 KPIs** (`/kpis/`)
- **Cálculo**: Calcular KPIs automáticamente
- **Consulta**: Obtener KPIs específicos
- **Reportes**: Generar reportes de KPIs
- **Comparativos**: Análisis comparativo
- **Temporales**: Análisis por períodos

#### **📋 Historial** (`/historial/`)
- **Auditoría**: Trazabilidad de cambios
- **Actividad**: Actividad reciente
- **Patrones**: Análisis de patrones
- **Eficiencia**: Métricas de evaluadores
- **CRUD**: Gestión de historial

#### **📊 Reportes** (`/reportes/`)
- **Mensuales**: Reportes mensuales
- **Anuales**: Reportes anuales
- **Comparativos**: Por departamentos
- **Personalizados**: Reportes a medida
- **Especializados**: Impacto económico, innovación, sostenibilidad

#### **📈 Estadísticas** (`/estadisticas/`)
- **Análisis**: Análisis estadístico
- **Tecnología**: Métricas tecnológicas
- **Tendencias**: Análisis de tendencias
- **Comparativos**: Comparaciones

#### **🔧 Data Generation** (`/data-generation/`)
- **Mockaroo**: Generación de datos de prueba
- **Descripciones**: Generar descripciones de marcas
- **Prompts**: Generar prompts para logos

## 🔧 **Ejemplos de Uso**

### **🏷️ Gestión de Marcas**

#### **Listar Marcas**
```bash
GET /api/analytics/marcas/
```

#### **Crear Marca**
```bash
POST /api/analytics/marcas/crear/
Content-Type: application/json

{
    "numero_marca": "M001",
    "nombre_productor": "Juan Pérez",
    "monto_certificacion": 1500.00,
    "raza_bovino": "HOLSTEIN",
    "proposito_ganado": "LECHE",
    "cantidad_cabezas": 50,
    "departamento": "SANTA_CRUZ",
    "municipio": "Santa Cruz de la Sierra",
    "ci_productor": "12345678",
    "telefono_productor": "70012345"
}
```

#### **Aprobar Marca**
```bash
POST /api/analytics/marcas/{marca_id}/aprobar/
```

#### **Obtener Estadísticas por Raza**
```bash
GET /api/analytics/marcas/estadisticas/por-raza/
```

### **🎨 Generación de Logos**

#### **Generar Logo**
```bash
POST /api/analytics/logos/generar/
Content-Type: application/json

{
    "marca_id": 1,
    "modelo_ia": "DALL_E_3",
    "prompt": "Logo moderno para marca de ganado bovino"
}
```

#### **Listar Logos**
```bash
GET /api/analytics/logos/
```

#### **Obtener Estadísticas de IA**
```bash
GET /api/analytics/logos/estadisticas/
```

### **📊 Dashboard**

#### **Obtener Datos del Dashboard**
```bash
GET /api/analytics/dashboard/
```

#### **Generar Reporte Ejecutivo**
```bash
POST /api/analytics/dashboard/reporte/
```

### **📈 KPIs**

#### **Calcular KPIs**
```bash
POST /api/analytics/kpis/calcular/
```

#### **Obtener KPIs**
```bash
GET /api/analytics/kpis/
```

### **📋 Historial**

#### **Obtener Actividad Reciente**
```bash
GET /api/analytics/historial/actividad-reciente/
```

#### **Obtener Auditoría por Usuario**
```bash
GET /api/analytics/historial/auditoria-usuario/{usuario_id}/
```

### **📊 Reportes**

#### **Generar Reporte Mensual**
```bash
POST /api/analytics/reportes/mensual/
Content-Type: application/json

{
    "mes": 12,
    "anio": 2024,
    "formato": "excel"
}
```

#### **Exportar a Excel**
```bash
POST /api/analytics/reportes/exportar-excel/
```

## 🔐 **Autenticación y Permisos**

### **Configuración Actual**
- **Autenticación**: SessionAuthentication
- **Permisos**: AllowAny (para desarrollo)
- **CORS**: Configurado para desarrollo

### **Para Producción**
```python
# Configurar en settings.py
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}
```

## 📊 **Respuestas de API**

### **Formato Estándar**
```json
{
    "success": true,
    "data": {
        // Datos de la respuesta
    },
    "message": "Operación exitosa",
    "timestamp": "2024-12-19T10:30:00Z"
}
```

### **Respuesta de Error**
```json
{
    "success": false,
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "Datos inválidos",
        "details": {
            "numero_marca": ["Este campo es requerido"]
        }
    },
    "timestamp": "2024-12-19T10:30:00Z"
}
```

## 🧪 **Testing de APIs**

### **Ejecutar Tests**
```bash
# Tests de APIs
python manage.py test apps.analytics.presentation

# Tests específicos
python manage.py test apps.analytics.presentation.controllers.marca
```

### **Ejemplos de Tests**
```python
# Test de creación de marca
def test_crear_marca_api():
    data = {
        "numero_marca": "M001",
        "nombre_productor": "Juan Pérez",
        # ... otros campos
    }
    response = client.post('/api/analytics/marcas/crear/', data)
    assert response.status_code == 201
```

## 📈 **Métricas y Monitoreo**

### **Endpoints de Salud**
- **Health Check**: `/api/health/`
- **Status**: `/api/status/`

### **Logs**
- **Nivel**: DEBUG en desarrollo
- **Formato**: Verbose con timestamp
- **Archivo**: Console (desarrollo)

## 🚀 **Despliegue**

### **Variables de Entorno**
```env
# Django
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com

# Database
DATABASE_URL=postgresql://user:password@host:port/db

# APIs Externas
AFILIADOS_API_URL=https://api.afiliados.com/v1/
GANADO_API_URL=https://api.ganado.com/v1/
IA_API_URL=https://api.ai-service.com/v1/
```

### **Comandos de Despliegue**
```bash
# Migrar base de datos
python manage.py migrate

# Recolectar archivos estáticos
python manage.py collectstatic

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver 0.0.0.0:8000
```

## 📚 **Recursos Adicionales**

### **Documentación Técnica**
- **[ARQUITECTURA.md](ARQUITECTURA.md)**: Detalles de Clean Architecture
- **[REGLAS_DESARROLLO.md](REGLAS_DESARROLLO.md)**: Estándares de desarrollo
- **[README.md](README.md)**: Descripción general del proyecto

### **Herramientas de Desarrollo**
- **Swagger UI**: Interfaz interactiva para probar APIs
- **ReDoc**: Documentación alternativa más limpia
- **Postman**: Colección de APIs para testing

## ✅ **Estado de Implementación**

### **✅ APIs Implementadas**
- **71 controllers** organizados por dominio
- **8 serializers** siguiendo Clean Architecture
- **URLs modulares** por dominio
- **Documentación automática** con drf-spectacular

### **✅ Funcionalidades**
- **CRUD completo** para todos los dominios
- **Operaciones especializadas** por dominio
- **Estadísticas y métricas** implementadas
- **Reportes ejecutivos** funcionales
- **Auditoría y trazabilidad** completa

### **✅ Calidad**
- **Clean Architecture** aplicada
- **Principios SOLID** cumplidos
- **Testing** implementado
- **Documentación** completa

---

**Desarrollado con ❤️ para el sector ganadero**
**Versión**: 2.0.0 - APIs documentadas y funcionales 