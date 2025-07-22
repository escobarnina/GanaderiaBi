# Documento de Arquitectura: Microservicio de Inteligencia de Negocios

## 1.1. Visión General

El Microservicio de Inteligencia de Negocios (BI Service) forma parte de la plataforma ganadera microservicios. Su responsabilidad es consumir datos de afiliados, ganado y certificados, procesarlos en un modelo analítico y exponer:

* Dashboards con KPIs clave del sector ganadero bovino
* Endpoints REST para consumo de reportes y tendencias
* Jobs programados para generación de informes ejecutivos
* Análisis estadísticos por raza, departamento y propósito ganadero

La arquitectura se basa en Clean Architecture y microservicios, con las siguientes capas:

```
[ API Gateway ]
       ↓ REST/v1
[ BI Service ]
    ┌──────────────┐    ┌───────────────┐
    │ Presentation │ →  │ Use Cases     │
    ├──────────────┤    ├───────────────┤
    │ Infrastructure│ ← │ Domain Models │
    └──────────────┘    └───────────────┘
         │                     │
      Django               Python Classes
         │                     │
      MySQL Cluster      Pandas / NumPy
```

### 1.1.1. Responsabilidades del Microservicio

* **Procesamiento de Datos**: Consumir y transformar datos de otros microservicios
* **Análisis Estadístico**: Calcular KPIs y métricas del sector ganadero
* **Generación de Reportes**: Crear informes ejecutivos y dashboards
* **Visualización**: Exponer datos para interfaces de usuario
* **Predicciones**: Análisis de tendencias y forecasting

## 1.2. Componentes Principales

### 1.2.1. API Gateway
* **Responsable**: Ingeniero de Integración
* **Funciones**: JWT, enrouting a `/api/bi/v1/*`
* **Tecnologías**: Spring Cloud Gateway / Kong

### 1.2.2. Presentation Layer (Django REST Framework)
* **Responsable**: Equipo de Desarrollo
* **Componentes**: Serializers, ViewSets, Swagger/OpenAPI
* **Endpoints principales**:
  * `/api/bi/v1/dashboard/` - Dashboard principal
  * `/api/bi/v1/kpis/` - Indicadores clave
  * `/api/bi/v1/estadisticas/` - Análisis estadísticos
  * `/api/bi/v1/reportes/` - Generación de reportes

### 1.2.3. Use Cases Layer
* **Responsable**: Analista de BI
* **Clases principales**:
  * `CalcularKPIs` - Procesamiento de indicadores
  * `GenerarReporte` - Creación de informes
  * `ObtenerTendencias` - Análisis temporal
  * `AnalizarRendimiento` - Métricas de eficiencia

### 1.2.4. Domain Models Layer
* **Responsable**: Analista de Requerimientos + Expertos de Dominio
* **Estructura implementada**:
  ```
  apps/analytics/domain/
  ├── enums.py                    # ✅ Enumeraciones del dominio (fuente única de verdad)
  ├── entities/                   # ✅ Entidades separadas por responsabilidad
  │   ├── marca_ganado_bovino.py # Gestión de marcas bovinas
  │   ├── logo_marca_bovina.py   # Generación de logos IA
  │   ├── kpi_ganado_bovino.py   # Indicadores clave
  │   ├── historial_estado_marca.py # Auditoría de cambios
  │   ├── dashboard_data.py       # Datos del dashboard
  │   └── reporte_data.py         # Datos de reportes
  └── repositories/               # ✅ Interfaces de repositorios
      ├── marca_repository.py     # Operaciones de marcas
      ├── logo_repository.py      # Operaciones de logos
      ├── kpi_repository.py       # Operaciones de KPIs
      ├── historial_repository.py # Operaciones de historial
      ├── dashboard_repository.py # Operaciones de dashboard
      └── reporte_repository.py   # Operaciones de reportes
  ```
* **Principios aplicados**:
  * **Single Responsibility**: ✅ Cada entidad en su propio archivo
  * **Open/Closed**: ✅ Extensible sin modificar código existente
  * **Dependency Inversion**: ✅ Interfaces independientes de implementación
  * **Clean Architecture**: ✅ Dominio independiente de frameworks
  * **Single Source of Truth**: ✅ Enumeraciones centralizadas


### 1.2.5. Infrastructure Layer
* **Django ORM para MySQL** (Responsable: DBA)
  * ✅ Implementación de repositorios concretos en `apps/analytics/infrastructure/repositories/`
  * ✅ Conversión entre modelos Django y entidades del dominio
  * ✅ **Modelos Django separados por responsabilidad** en `apps/analytics/infrastructure/models/`
  * ✅ **Uso de enumeraciones del dominio** como fuente única de verdad
  * ✅ Mantenimiento de compatibilidad con código legacy
* **Celery + Redis** para jobs programados (Responsable: DevOps)
* **Pipelines ETL** (Airflow o scripts Python) (Responsable: Ingeniero de Datos)
* **Dependency Injection** (Responsable: Equipo de Desarrollo)
  * ✅ Container para inyección de dependencias
  * ✅ Adapters para compatibilidad con código legacy

## 1.3. Integraciones con Otros Microservicios

### 1.3.1. Microservicio Afiliados
* **Endpoint**: `/api/afiliados/v1/ganaderos/`
* **Datos**: Información de productores, propiedades, ubicaciones
* **Frecuencia**: Sincronización diaria

### 1.3.2. Microservicio Ganado
* **Endpoint**: `/api/ganado/v1/produccion/`
* **Datos**: Producción de leche, cabezas de ganado, rendimientos
* **Frecuencia**: Actualización en tiempo real

### 1.3.3. Microservicio Certificados
* **Endpoint**: `/api/certificados/v1/estados/`
* **Datos**: Estados de certificación, tiempos de procesamiento
* **Frecuencia**: Sincronización cada 4 horas

### 1.3.4. Microservicio IA
* **Endpoint**: `/api/ia/v1/logos/`
* **Datos**: Logos generados, métricas de IA
* **Frecuencia**: On-demand

## 1.4. Infraestructura Cloud

### 1.4.1. Despliegue
* **Plataforma**: AWS EKS (Elastic Kubernetes Service)
* **Contenedores**: Docker con multi-stage builds
* **Orquestación**: Kubernetes con Helm charts

### 1.4.2. Configuración
* **ConfigMaps**: Variables de entorno no sensibles
* **Secrets**: Claves de API, credenciales de BD
* **Volumes**: Almacenamiento persistente para logs y cache

### 1.4.3. Escalabilidad
* **Auto-scaling**: Basado en CPU (70%) y latencia de respuestas (<200ms)
* **HPA**: Horizontal Pod Autoscaler
* **VPA**: Vertical Pod Autoscaler (en desarrollo)

### 1.4.4. Monitoreo y Observabilidad
* **Métricas**: Prometheus + Grafana
* **Logs**: ELK Stack (Elasticsearch, Logstash, Kibana)
* **Tracing**: Jaeger para distributed tracing
* **Alertas**: PagerDuty / Slack

### 1.4.5. Base de Datos
* **MySQL Cluster**: Master-Slave con replicación
* **Backup**: Automático diario con retención de 30 días
* **Performance**: Query optimization y indexing

### 1.4.6. Cache y Performance
* **Redis**: Cache de KPIs y datos frecuentemente consultados
* **CDN**: CloudFront para assets estáticos
* **Load Balancer**: ALB con health checks

## 1.5. Patrones de Diseño

### 1.5.1. Clean Architecture
* **Independencia de frameworks**: Django como herramienta, no como dependencia
* **Testabilidad**: Inyección de dependencias para testing
* **Independencia de UI**: APIs REST independientes de la interfaz
* **Independencia de BD**: ORM como abstracción
* **Estructura implementada**:
  * **Domain Layer**: Entidades y reglas de negocio puras
  * **Infrastructure Layer**: Implementaciones concretas con Django ORM
  * **Use Cases Layer**: Lógica de aplicación (en desarrollo)
  * **Presentation Layer**: APIs y serializers (en desarrollo)
* **Migración incremental**: Mantenimiento de compatibilidad con código legacy

### 1.5.2. Microservicios
* **Bounded Context**: Dominio específico del BI ganadero
* **API Gateway**: Punto único de entrada
* **Service Discovery**: Kubernetes DNS
* **Circuit Breaker**: Resiliencia ante fallos

### 1.5.3. Event-Driven Architecture
* **Event Sourcing**: Historial de cambios de estado
* **CQRS**: Separación de comandos y consultas
* **Message Queues**: Celery para jobs asíncronos

## 1.6. Seguridad

### 1.6.1. Autenticación y Autorización
* **JWT**: Tokens con expiración configurable
* **OAuth2**: Integración con proveedores externos
* **RBAC**: Roles basados en acceso (Admin, Analista, Viewer)

### 1.6.2. Protección de Datos
* **Encriptación**: TLS 1.3 en tránsito, AES-256 en reposo
* **PII**: Anonimización de datos personales
* **Auditoría**: Logs de acceso y cambios

### 1.6.3. Seguridad de Aplicación
* **OWASP Top 10**: Mitigaciones implementadas
* **Input Validation**: Sanitización de datos de entrada
* **SQL Injection**: ORM con parámetros preparados

## 1.7. Disaster Recovery

### 1.7.1. Backup Strategy
* **Base de Datos**: Backup automático cada 6 horas
* **Archivos**: S3 con versioning
* **Configuración**: Git con tags de releases

### 1.7.2. Recovery Procedures
* **RTO**: 4 horas (Recovery Time Objective)
* **RPO**: 6 horas (Recovery Point Objective)
* **Failover**: Multi-AZ deployment

## 1.8. Performance y Optimización

### 1.8.1. Métricas Clave
* **Response Time**: <200ms para 95% de requests
* **Throughput**: 1000 requests/segundo
* **Availability**: 99.9% uptime
* **Error Rate**: <0.1%

### 1.8.2. Optimizaciones
* **Database**: Indexing, query optimization, connection pooling
* **Cache**: Redis para datos frecuentemente consultados
* **CDN**: CloudFront para assets estáticos
* **Compression**: Gzip para responses

## 1.9. Estado de Implementación

### 1.9.1. Fase 1: Domain & Infrastructure ✅ COMPLETADA
* **Domain Layer**: Entidades y repositorios implementados
  * ✅ Separación de responsabilidades por archivo
  * ✅ Enumeraciones centralizadas como fuente única de verdad
  * ✅ Interfaces de repositorios definidas
* **Infrastructure Layer**: Implementaciones con Django ORM
  * ✅ Repositorios concretos implementados
  * ✅ Conversión entre modelos y entidades
  * ✅ **Modelos Django separados por responsabilidad** (corregido)
  * ✅ **Uso de enumeraciones del dominio** (corregido)
  * ✅ Adapters para compatibilidad legacy
* **Dependency Injection**: Container configurado
* **Testing**: Estructura preparada para tests unitarios

### 1.9.2. Fase 2: Configuración y Estructura ✅ COMPLETADA
* **Configuración Simplificada**: Una sola configuración en `settings.py`
* **Dependencias Únicas**: Un solo archivo `requirements.txt`
* **Comandos Simplificados**: Makefile actualizado
* **Compatibilidad Preservada**: Variables de entorno y comandos legacy
* **Principio KISS**: Keep It Simple, Stupid aplicado

### 1.9.3. Próximas Fases
* **Fase 3**: Use Cases Layer (en desarrollo)
* **Fase 4**: Presentation Layer (pendiente)
* **Fase 5**: Testing y Documentación (pendiente)

---

**Documento de Arquitectura - Microservicio de Inteligencia de Negocios**
*Versión: 1.2*
*Fecha: 2025*
*Equipo: BI/AI/Agentes*
*Estado: Fase 1 Completada + Correcciones SOLID Aplicadas*


**Documentos Relacionados:**
- `README.md` - Estado actual y funcionalidades
- `REGLAS_IMPLEMENTACION.md` - Reglas para próximas fases
- `REGLAS_DESARROLLO.md` - Estándares de desarrollo 