# 🐄 Ganadería BI - Microservicio de Inteligencia de Negocios

## 📋 Descripción

Microservicio encargado de procesar datos del ecosistema ganadero bovino y exponer indicadores, reportes y dashboards para la toma de decisiones estratégicas. Forma parte de la arquitectura de microservicios de la plataforma ganadera.

## 🎯 Estado Actual: Fase 2 - Clean Architecture Implementada ✅

### ✅ **IMPLEMENTADO Y FUNCIONAL**
- **App Legacy**: `business_intelligence` (mantener compatibilidad)
- **App Clean Architecture**: `apps.analytics` IMPLEMENTADA
- **Endpoints API**: Operativos en `/api/bi/v1/`
- **Base de Datos**: MySQL con PyMySQL
- **Clean Architecture**: Domain e Infrastructure Layers implementadas
- **Dependency Injection**: Container configurado
- **Testing**: pytest configurado
- **Linting**: black, flake8, mypy
- **Servicios Avanzados**: Celery, Redis, JWT configurados

### ⏳ **PENDIENTE: Fase 3 - Use Cases y Presentation**
- Use Cases Layer (lógica de aplicación)
- Presentation Layer (APIs REST con Clean Architecture)
- Testing completo para Clean Architecture
- Documentación avanzada

## 🎯 Funcionalidades Principales

### 📊 Dashboard y KPIs
* `/api/bi/v1/dashboard/` → Dashboard principal con métricas en tiempo real
* `/api/bi/v1/kpis/` → Indicadores clave de rendimiento (KPIs)
* `/api/bi/v1/estadisticas/` → Análisis estadísticos avanzados

### 📈 Reportes y Análisis
* `/api/bi/v1/reportes/` → Generación y descarga de reportes PDF/Excel
* `/api/bi/v1/tendencias/` → Análisis de tendencias temporales
* `/api/bi/v1/predicciones/` → Análisis predictivo y forecasting

### 🏷️ Gestión de Marcas Bovinas
* `/api/bi/v1/marcas-bovinas/` → CRUD completo de marcas de ganado
* `/api/bi/v1/logos-bovinos/` → Generación y gestión de logos IA
* `/api/bi/v1/historial-estados/` → Auditoría de cambios de estado

## 🏗️ Arquitectura del Proyecto

### Estructura Actual (Fase 2)
```
ganaderia_bi/
├── settings.py                        # ✅ Configuración con Clean Architecture
├── requirements.txt                   # ✅ Dependencias con Clean Architecture
├── manage.py                         # ✅ Django management
├── wsgi.py                           # ✅ WSGI application
├── urls.py                           # ✅ URL routing
├── business_intelligence/             # ✅ App legacy - MANTENER COMPATIBILIDAD
│   ├── models.py                      # Modelos Django
│   ├── views/                         # Views completos
│   ├── serializers.py                 # Serializers
│   └── urls.py                        # URLs activas
├── apps/analytics/                    # ✅ Clean Architecture IMPLEMENTADA
│   ├── domain/                        # ✅ Entidades y repositorios
│   ├── infrastructure/                # ✅ Implementaciones con Django ORM
│   ├── use_cases/                     # ⏳ Lógica de aplicación (PENDIENTE)
│   └── presentation/                  # ⏳ APIs REST (PENDIENTE)
├── logs/                              # ✅ Directorio de logs
├── Makefile                           # ✅ Comandos con Clean Architecture
└── ESTADO_IMPLEMENTACION.md           # ✅ Documentación de estado
```

### Estado de Implementación
* **✅ Fase 1 Completada**: Funcionalidad básica con `business_intelligence`
* **✅ Fase 2 Completada**: Clean Architecture con `apps.analytics`
* **⏳ Fase 3 Pendiente**: Use Cases y Presentation Layers
* **⏳ Fase 4 Pendiente**: Testing completo y documentación avanzada

## 🚀 Instalación y Configuración

### Prerrequisitos
```bash
Python 3.9+
Django 4.2.7
MySQL 8.0+
Redis 6.0+ (para Clean Architecture)
```

### Instalación Local
```bash
# Clonar repositorio
git clone <repository-url>
cd bi-service

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno (opcional)
# Las variables se configuran automáticamente desde settings.py

# Migraciones
python manage.py makemigrations
python manage.py migrate

# Generar datos de prueba
python manage.py generar_datos --marcas 100 --logos 80

# Ejecutar servidor
python manage.py runserver

# Comandos de desarrollo (Makefile)
make install          # Instalar dependencias
make test            # Ejecutar tests
make lint            # Verificar calidad de código
make format          # Formatear código
make setup-dev       # Configurar entorno completo
make security        # Análisis de seguridad
make celery-worker   # Ejecutar worker de Celery
make celery-beat     # Ejecutar beat de Celery
```

### Variables de Entorno (Opcionales)
```env
# Django
SECRET_KEY=tu-clave-secreta-muy-segura
DEBUG=True

# Base de Datos
DB_NAME=ganaderia_bi
DB_USER=root
DB_PASSWORD=tu-password
DB_HOST=localhost
DB_PORT=3306

# Redis (para Clean Architecture)
REDIS_URL=redis://localhost:6379/0

# APIs Externas (para futuras integraciones)
AFILIADOS_API_URL=http://localhost:8001/api/afiliados/v1/
GANADO_API_URL=http://localhost:8002/api/ganado/v1/
CERTIFICADOS_API_URL=http://localhost:8003/api/certificados/v1/
IA_API_URL=http://localhost:8004/api/ia/v1/

# TODO: Variables para Fase 3
# JWT_PUBLIC_KEY=tu-jwt-public-key
# JWT_PRIVATE_KEY=tu-jwt-private-key
```

**Nota**: Todas las variables tienen valores por defecto en `settings.py`, por lo que no es necesario crear un archivo `.env` para desarrollo básico.

## 📡 Endpoints de la API

### Dashboard y KPIs

#### GET `/api/bi/v1/dashboard/kpis-principales/`
Retorna los KPIs principales del sistema.
```json
{
  "marcas_registradas_mes": 150,
  "tiempo_promedio_procesamiento": 24.5,
  "porcentaje_aprobacion": 85.2,
  "ingresos_mes": 125000.00,
  "total_cabezas_registradas": 25000,
  "promedio_cabezas_por_marca": 167.3
}
```

#### GET `/api/bi/v1/dashboard/tendencias-mensuales/`
Análisis de tendencias de los últimos 12 meses.
```json
{
  "tendencias": [
    {
      "mes": "2025-01",
      "marcas_registradas": 120,
      "ingresos": 98000.00,
      "tiempo_promedio": 22.1
    }
  ]
}
```

#### GET `/api/bi/v1/dashboard/metricas-tiempo-real/`
Métricas actualizadas en tiempo real.
```json
{
  "marcas_pendientes": 15,
  "marcas_procesando": 8,
  "marcas_aprobadas_hoy": 12,
  "tiempo_promedio_actual": 18.5
}
```

### Estadísticas Avanzadas

#### GET `/api/bi/v1/estadisticas/por-raza/`
Distribución de marcas por raza bovina.
```json
{
  "razas": [
    {
      "raza": "NELORE",
      "cantidad_marcas": 45,
      "porcentaje": 30.0,
      "promedio_cabezas": 180.5
    }
  ]
}
```

#### GET `/api/bi/v1/estadisticas/por-departamento/`
Análisis geográfico por departamentos.
```json
{
  "departamentos": [
    {
      "departamento": "SANTA_CRUZ",
      "marcas_registradas": 65,
      "ingresos": 52000.00,
      "promedio_tiempo": 20.3
    }
  ]
}
```

#### GET `/api/bi/v1/estadisticas/por-proposito/`
Distribución por propósito ganadero.
```json
{
  "propositos": [
    {
      "proposito": "CARNE",
      "marcas": 80,
      "porcentaje": 53.3,
      "total_cabezas": 15000
    }
  ]
}
```

### Reportes Ejecutivos

#### GET `/api/bi/v1/reportes/ejecutivo-mensual/`
Reporte ejecutivo del mes actual.
```json
{
  "periodo": "2025-01",
  "resumen": {
    "total_marcas": 150,
    "ingresos_totales": 125000.00,
    "tiempo_promedio": 24.5
  },
  "tendencias": {...},
  "recomendaciones": [...]
}
```

#### GET `/api/bi/v1/reportes/anual/`
Reporte anual completo.
```json
{
  "anio": 2025,
  "resumen_anual": {...},
  "comparativa_anterior": {...},
  "proyecciones": {...}
}
```

#### POST `/api/bi/v1/reportes/personalizado/`
Genera reporte personalizado según parámetros.
```json
{
  "fecha_inicio": "2025-01-01",
  "fecha_fin": "2025-01-31",
  "departamentos": ["SANTA_CRUZ", "BENI"],
  "razas": ["NELORE", "BRAHMAN"],
  "formato": "pdf"
}
```

### Gestión de Marcas Bovinas

#### GET `/api/bi/v1/marcas-bovinas/`
Lista todas las marcas con paginación.
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/bi/v1/marcas-bovinas/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "numero_marca": "MB-2025-001",
      "nombre_productor": "Juan Pérez",
      "raza_bovino": "NELORE",
      "proposito_ganado": "CARNE",
      "cantidad_cabezas": 200,
      "departamento": "SANTA_CRUZ",
      "estado": "APROBADO"
    }
  ]
}
```

#### POST `/api/bi/v1/marcas-bovinas/`
Crea una nueva marca de ganado.
```json
{
  "numero_marca": "MB-2025-002",
  "nombre_productor": "María González",
  "raza_bovino": "BRAHMAN",
  "proposito_ganado": "DOBLE_PROPOSITO",
  "cantidad_cabezas": 150,
  "departamento": "BENI",
  "municipio": "Trinidad",
  "ci_productor": "12345678",
  "telefono_productor": "591-70000000"
}
```

### Logos y IA

#### GET `/api/bi/v1/logos-bovinos/`
Lista logos generados por IA.
```json
{
  "count": 80,
  "results": [
    {
      "id": 1,
      "marca": "MB-2025-001",
      "url_logo": "https://storage.example.com/logos/logo_001.png",
      "modelo_ia_usado": "DALL-E-3",
      "calidad_logo": "ALTA",
      "tiempo_generacion_segundos": 15
    }
  ]
}
```

#### POST `/api/bi/v1/logos-bovinos/`
Genera un nuevo logo con IA.
```json
{
  "marca_id": 1,
  "modelo_ia_usado": "DALL-E-3",
  "prompt_usado": "Logo moderno para marca ganadera Nelore"
}
```

## 🔄 Jobs Programados (Celery)

### Jobs Automáticos
```python
# Jobs principales
generate_monthly_report    # Genera reporte mensual automático
update_kpi_cache          # Actualiza cache de KPIs
sync_external_data        # Sincroniza datos de otros microservicios
clean_old_logs            # Limpia logs antiguos
```

### Configuración de Celery
```python
# settings.py
CELERY_BROKER_URL = config('REDIS_URL')
CELERY_RESULT_BACKEND = config('REDIS_URL')
CELERY_TIMEZONE = 'America/La_Paz'

# Tareas programadas
CELERY_BEAT_SCHEDULE = {
    'generate-monthly-report': {
        'task': 'apps.analytics.tasks.generate_monthly_report',
        'schedule': crontab(day_of_month=1, hour=6),
    },
    'update-kpi-cache': {
        'task': 'apps.analytics.tasks.update_kpi_cache',
        'schedule': timedelta(hours=1),
    },
}
```

## 🐳 Despliegue con Docker

### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Exponer puerto
EXPOSE 8000

# Comando de inicio
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "bi.wsgi:application"]
```

### Docker Compose
```yaml
# docker-compose.yml
version: '3.8'

services:
  bi-service:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql://user:password@db:3306/ganaderia_bi
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: ganaderia_bi
    volumes:
      - mysql_data:/var/lib/mysql

  redis:
    image: redis:6.0-alpine
    volumes:
      - redis_data:/data

volumes:
  mysql_data:
  redis_data:
```

## ☸️ Despliegue en Kubernetes

### Deployment
```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bi-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: bi-service
  template:
    metadata:
      labels:
        app: bi-service
    spec:
      containers:
      - name: bi-service
        image: bi-service:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: bi-secrets
              key: database-url
        - name: REDIS_URL
          valueFrom:
            configMapKeyRef:
              name: bi-config
              key: redis-url
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### Service
```yaml
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: bi-service
spec:
  selector:
    app: bi-service
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
```

## 📊 Monitoreo y Observabilidad

### Métricas Clave
* **Response Time**: <200ms para 95% de requests
* **Throughput**: 1000 requests/segundo
* **Availability**: 99.9% uptime
* **Error Rate**: <0.1%

### Herramientas de Monitoreo
* **Prometheus + Grafana**: Métricas y dashboards
* **ELK Stack**: Logs centralizados
* **Jaeger**: Distributed tracing
* **Health Checks**: `/health/` endpoint

## 👥 Equipo y Roles

### Roles del Equipo
* **Product Owner**: Define prioridades de dashboard y KPIs
* **Data Scientist**: Valida fórmulas y calidad de datos
* **DevOps Engineer**: CI/CD y monitoreo
* **DBA**: Optimiza consultas y particiones
* **Backend Developer**: APIs y lógica de negocio
* **Frontend Developer**: Dashboards y visualizaciones

### Responsabilidades por Capa
* **API Gateway**: Ingeniero de Integración
* **Presentation**: Equipo de Desarrollo
* **Use Cases**: Analista de BI
* **Domain Models**: Analista de Requerimientos + Expertos de Dominio
  * ✅ Entidades y reglas de negocio implementadas
  * ✅ Interfaces de repositorios definidas
* **Infrastructure**: DBA + DevOps
  * ✅ Repositorios concretos con Django ORM
  * ✅ Adapters para compatibilidad legacy

## 🔧 Desarrollo Local

### Comandos Útiles
```bash
# Generar datos de prueba
python manage.py generar_datos --marcas 100 --logos 80

# Ejecutar tests
pytest --cov=apps --cov-report=html

# Formatear código
black apps/
flake8 apps/

# Verificar tipos
mypy apps/

# Ejecutar Celery worker
celery -A bi worker -l info

# Ejecutar Celery beat
celery -A bi beat -l info
```

### Estructura de Desarrollo
```
ganaderia_bi/
├── apps/analytics/                    # ✅ Nueva arquitectura Clean Architecture
│   ├── domain/                        # ✅ FASE 1 COMPLETADA
│   │   ├── enums.py                  # Enumeraciones del dominio
│   │   ├── entities/                  # Entidades separadas por responsabilidad
│   │   └── repositories/              # Interfaces de repositorios
│   ├── infrastructure/                # ✅ FASE 1 COMPLETADA
│   │   ├── repositories/              # Implementaciones con Django ORM
│   │   └── adapters.py               # Adapters para compatibilidad
│   ├── use_cases/                     # 🔄 FASE 2 (en desarrollo)
│   └── presentation/                  # 🔄 FASE 3 (pendiente)
├── business_intelligence/             # 🏛️ Código legacy (mantener compatibilidad)
│   ├── models.py                      # Modelos Django originales
│   ├── views/                         # Views existentes
│   ├── serializers.py                 # Serializers existentes
│   └── urls.py                        # URLs existentes
├── scripts/                           # Scripts ETL
├── docker/                            # Configuración Docker
├── k8s/                               # Manifiestos Kubernetes
└── docs/                              # Documentación
```

## 📚 Documentación Adicional

* [Reglas de Implementación](REGLAS_IMPLEMENTACION.md) - Reglas para próximas fases
* [Documento de Arquitectura](ARQUITECTURA.md)
* [Reglas de Desarrollo](REGLAS_DESARROLLO.md)
* [API Documentation](docs/api/)
* [Deployment Guide](docs/deployment/)

## 🎯 Estado del Proyecto

### ✅ **Fase 1 - Completada**
- App `business_intelligence` completamente funcional
- Endpoints API operativos
- Testing y linting configurados
- Documentación básica

### ✅ **Fase 2 - Completada**
- Clean Architecture implementada con `apps.analytics`
- Domain e Infrastructure Layers funcionales
- Dependency Injection configurado
- Celery y Redis implementados
- Herramientas de seguridad activas

### ⏳ **Fase 3 - Pendiente**
- Use Cases Layer (lógica de aplicación)
- Presentation Layer (APIs REST con Clean Architecture)
- Testing completo para Clean Architecture
- Documentación avanzada

**Para más detalles sobre el estado de implementación, consulta la sección "Estado del Proyecto" en este README**

---

**Ganadería BI – Microservicio de Inteligencia de Negocios**
*Versión: 1.0*
*Equipo: BI/AI/Agentes*
*Tecnologías: Django, Python, MySQL, Redis, Celery*
*Estado: Fase 2 Completada - Clean Architecture Implementada* 

## 🏗️ Estado de Implementación y Buenas Prácticas

- Las **entidades del dominio** están separadas y encapsulan la lógica de negocio.
- Las **enumeraciones** están centralizadas y son la fuente única de verdad.
- Las **interfaces de repositorio** están en el dominio, desacopladas de la infraestructura.
- Los **modelos Django** están en la infraestructura, cada uno en su propio archivo.
- Los **repositorios de infraestructura** implementan las interfaces del dominio, con conversión clara entre modelos y entidades.
- Se han limpiado imports y eliminado dependencias innecesarias.
- No se expone código legacy ni detalles de Django fuera de la infraestructura.

**Estado actual:**
- Dominio, modelos, interfaces y repositorios de infraestructura cumplen Clean Architecture y SOLID.
- Cohesión fuerte y acoplamiento débil entre capas.

--- 