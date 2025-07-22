# Reglas de Desarrollo y Estándares - Microservicio de Inteligencia de Negocios

## 2.1. Prácticas de Código

### 2.1.1. Clean Code & SOLID Principles

* **Single Responsibility**: Una clase = una responsabilidad específica
  * ✅ Implementado: Cada entidad en su propio archivo (`marca_ganado_bovino.py`, `logo_marca_bovina.py`, etc.)
  * ✅ Implementado: Cada interfaz de repositorio en su propio archivo
* **Open/Closed**: Extensible para nuevas funcionalidades sin modificar código existente
  * ✅ Implementado: Interfaces de repositorios permiten nuevas implementaciones
* **Liskov Substitution**: Interfaces bien definidas y consistentes
  * ✅ Implementado: Repositorios concretos implementan interfaces abstractas
* **Interface Segregation**: Interfaces pequeñas y específicas
  * ✅ Implementado: Cada repositorio tiene su interfaz específica
* **Dependency Inversion**: Inyección de dependencias, no dependencias directas
  * ✅ Implementado: Container de dependencias y adapters para compatibilidad

**Ejemplo de implementación actual:**
```python
# ✅ Correcto - Clean Code (implementado en Fase 1)
from apps.analytics.domain.entities.marca_ganado_bovino import MarcaGanadoBovino
from apps.analytics.domain.repositories.marca_repository import MarcaGanadoBovinoRepository

class MarcaGanadoBovino:
    """Entidad de dominio - Single Responsibility"""
    def __init__(self, numero_marca: str, nombre_productor: str, ...):
        self.numero_marca = numero_marca
        self.nombre_productor = nombre_productor
        # Validaciones específicas de la entidad
    
    def validar_estado(self) -> bool:
        """Responsabilidad única: validar estado"""
        pass

# ✅ Correcto - Interface Segregation
class MarcaGanadoBovinoRepository(ABC):
    """Interfaz específica para operaciones de marcas"""
    @abstractmethod
    def get_by_id(self, marca_id: int) -> Optional[MarcaGanadoBovino]:
        pass
    
    @abstractmethod
    def save(self, marca: MarcaGanadoBovino) -> MarcaGanadoBovino:
        pass

# ✅ Correcto - Dependency Inversion
class DjangoMarcaRepository(MarcaGanadoBovinoRepository):
    """Implementación concreta usando Django ORM"""
    def get_by_id(self, marca_id: int) -> Optional[MarcaGanadoBovino]:
        # Conversión entre modelo Django y entidad de dominio
        pass
```

### 2.1.2. Formateo y Estilo (PEP8 / Black)

* **Formateo automático**: Black con configuración estándar
* **Líneas máximas**: 88 caracteres
* **Nomenclatura**: snake_case para variables y funciones
* **Imports**: Organizados y agrupados
* **Docstrings**: Google style para documentación

**Configuración Black:**
```toml
# pyproject.toml
[tool.black]
line-length = 88
target-version = ['py39']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''
```

### 2.1.3. DRY (Don't Repeat Yourself)

* **Reutilización**: Lógica común en `services.py` o `use_cases/`
* **Helpers**: Funciones utilitarias en módulos específicos
* **Templates**: Para reportes y visualizaciones
* **Constants**: Valores constantes centralizados

**Ejemplo de implementación:**
```python
# ✅ Correcto - DRY
class ReportGenerator:
    def __init__(self, template_service: TemplateService):
        self.template_service = template_service
    
    def generate_monthly_report(self, data: dict) -> str:
        template = self.template_service.get_template('monthly_report')
        return template.render(data)
    
    def generate_annual_report(self, data: dict) -> str:
        template = self.template_service.get_template('annual_report')
        return template.render(data)

# ❌ Incorrecto - Repetición
class ReportGenerator:
    def generate_monthly_report(self, data: dict) -> str:
        # Código duplicado para renderizado
        pass
    
    def generate_annual_report(self, data: dict) -> str:
        # Código duplicado para renderizado
        pass
```

### 2.1.4. Type Hints y MyPy

* **Type hints**: Obligatorios en Python 3.9+
* **MyPy**: Chequeo estático de tipos
* **Strict mode**: Configuración estricta para calidad
* **Generic types**: Uso apropiado de genéricos

**Configuración MyPy:**
```toml
# pyproject.toml
[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true
```

## 2.2. Estructura de Repositorio

### 2.2.1. Estructura Principal

```
ganaderia_bi/
├── settings.py           # Configuración Django
├── urls.py              # URLs principales
├── wsgi.py              # WSGI application
├── apps/
│   └── analytics/        # ✅ Nueva arquitectura Clean Architecture
│       ├── domain/       # ✅ FASE 1 COMPLETADA
│       │   ├── enums.py                  # Enumeraciones del dominio
│       │   ├── entities/                  # Entidades separadas por responsabilidad
│       │   │   ├── marca_ganado_bovino.py
│       │   │   ├── logo_marca_bovina.py
│       │   │   ├── kpi_ganado_bovino.py
│       │   │   ├── historial_estado_marca.py
│       │   │   ├── dashboard_data.py
│       │   │   └── reporte_data.py
│       │   └── repositories/              # Interfaces de repositorios
│       │       ├── marca_repository.py
│       │       ├── logo_repository.py
│       │       ├── kpi_repository.py
│       │       ├── historial_repository.py
│       │       ├── dashboard_repository.py
│       │       └── reporte_repository.py
│       ├── infrastructure/                # ✅ FASE 1 COMPLETADA
│       │   ├── repositories/              # Implementaciones con Django ORM
│       │   │   └── django_repositories.py
│       │   └── adapters.py               # Adapters para compatibilidad
│       ├── use_cases/                     # 🔄 FASE 2 (en desarrollo)
│       └── presentation/                  # 🔄 FASE 3 (pendiente)
├── business_intelligence/ # 🏛️ Código legacy (mantener compatibilidad)
│   ├── models.py         # Modelos Django originales
│   ├── views/            # Views existentes
│   ├── serializers.py    # Serializers existentes
│   └── urls.py           # URLs existentes
├── scripts/              # Scripts ETL y utilidades
├── docker/               # Archivos Docker
├── k8s/                  # Manifiestos Kubernetes
├── docs/                 # Documentación
├── requirements.txt      # Dependencias
├── .env.example          # Variables de entorno ejemplo
├── .gitignore
├── pyproject.toml        # Configuración de herramientas
├── README.md
├── Makefile              # Comandos de desarrollo
├── .pre-commit-config.yaml # Pre-commit hooks
└── arquitectura.md       # Documento de arquitectura
```

### 2.2.2. Convenciones de Nomenclatura

* **Archivos Python**: snake_case (ej: `kpi_calculator.py`)
* **Clases**: PascalCase (ej: `KPICalculator`)
* **Funciones y variables**: snake_case (ej: `calculate_monthly_kpis`)
* **Constantes**: UPPER_SNAKE_CASE (ej: `MAX_RETRY_ATTEMPTS`)
* **Módulos**: snake_case (ej: `analytics/use_cases/`)

### 2.2.3. Organización de Tests

```
tests/
├── unit/                 # Tests unitarios
│   ├── test_kpi_calculator.py
│   ├── test_report_generator.py
│   └── test_trend_analyzer.py
├── integration/          # Tests de integración
│   ├── test_api_endpoints.py
│   ├── test_database_operations.py
│   └── test_external_services.py
├── factories/            # Factories para tests
│   ├── kpi_factory.py
│   ├── report_factory.py
│   └── user_factory.py
├── conftest.py          # Configuración pytest
└── fixtures/            # Datos de prueba
    ├── sample_data.json
    └── test_reports/
```

## 2.3. Calidad y Testing

### 2.3.1. Testing Strategy

* **Unit Tests**: 80%+ coverage obligatorio
* **Integration Tests**: APIs y base de datos
* **E2E Tests**: Flujos completos críticos
* **Performance Tests**: Carga y stress testing

### 2.3.2. Herramientas de Testing

```python
# requirements/test.txt
pytest==7.4.0
pytest-django==4.5.2
pytest-cov==4.1.0
factory-boy==3.3.0
faker==19.12.0
responses==0.23.3
pytest-mock==3.11.1
pytest-xdist==3.3.1
```

### 2.3.3. Configuración Pytest

```python
# pytest.ini
[tool:pytest]
DJANGO_SETTINGS_MODULE = bi.settings.test
python_files = tests.py test_*.py *_tests.py
addopts = 
    --strict-markers
    --strict-config
    --cov=apps
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
testpaths = apps/tests
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
    api: API tests
```

### 2.3.4. CI/CD Pipeline

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install -r requirements/test.txt
      
      - name: Run linting
        run: |
          flake8 apps/
          black --check apps/
          mypy apps/
      
      - name: Run tests
        run: |
          pytest --cov=apps --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
```

### 2.3.5. Code Review Checklist

**Funcionalidad:**
- [ ] El código cumple con los requerimientos
- [ ] No hay regresiones en funcionalidad existente
- [ ] Los tests cubren los casos edge

**Calidad:**
- [ ] Sigue los principios SOLID
- [ ] No hay código duplicado (DRY)
- [ ] Nomenclatura clara y consistente
- [ ] Documentación actualizada

**Seguridad:**
- [ ] Validación de inputs
- [ ] Sanitización de datos
- [ ] No hay vulnerabilidades conocidas
- [ ] Manejo seguro de secretos

**Performance:**
- [ ] Consultas optimizadas
- [ ] Uso apropiado de cache
- [ ] No hay memory leaks
- [ ] Response times aceptables

## 2.4. Seguridad

### 2.4.1. Autenticación y Autorización

* **JWT**: Tokens con expiración configurable
* **OAuth2**: Integración con proveedores externos
* **RBAC**: Roles basados en acceso
* **Rate Limiting**: Protección contra abuso

### 2.4.2. Validación de Datos

```python
# ✅ Correcto - Validación robusta
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError

class KPIModel(models.Model):
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0, message="El valor debe ser positivo"),
            MaxValueValidator(999999.99, message="El valor excede el límite")
        ]
    )
    
    def clean(self):
        if self.value < 0:
            raise ValidationError("Los KPIs no pueden ser negativos")

# ❌ Incorrecto - Sin validación
class KPIModel(models.Model):
    value = models.DecimalField(max_digits=10, decimal_places=2)
```

### 2.4.3. Sanitización de Inputs

```python
# ✅ Correcto - Sanitización
import bleach
from django.utils.html import strip_tags

def sanitize_input(text: str) -> str:
    """Sanitiza input de usuario"""
    # Remover HTML tags
    clean_text = strip_tags(text)
    # Sanitizar contenido
    clean_text = bleach.clean(clean_text, strip=True)
    return clean_text

# ❌ Incorrecto - Sin sanitización
def process_input(text: str) -> str:
    return text  # Vulnerable a XSS
```

### 2.4.4. Manejo de Secretos

```python
# ✅ Correcto - Variables de entorno
from decouple import config

DATABASE_URL = config('DATABASE_URL', default='sqlite:///db.sqlite3')
SECRET_KEY = config('SECRET_KEY', default='dev-secret-key')
API_KEY = config('API_KEY', default='')

# ❌ Incorrecto - Hardcoded secrets
DATABASE_URL = 'mysql://user:password@localhost/db'
SECRET_KEY = 'my-secret-key-123'
```

### 2.4.5. Logging y Auditoría

```python
import logging
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION

logger = logging.getLogger(__name__)

class AuditMixin:
    def log_action(self, action_flag, message):
        LogEntry.objects.log_action(
            user_id=self.request.user.id,
            content_type_id=self.content_type.id,
            object_id=self.object.id,
            object_repr=str(self.object),
            action_flag=action_flag,
            change_message=message
        )
        logger.info(f"Audit: {action_flag} - {message}")
```

### 2.4.6. Escaneo de Vulnerabilidades

* **Dependabot**: Actualizaciones automáticas de dependencias
* **Snyk**: Escaneo de vulnerabilidades
* **Bandit**: Análisis estático de seguridad Python
* **Safety**: Verificación de vulnerabilidades conocidas

```bash
# Comandos de seguridad
bandit -r apps/
safety check
pip-audit
```

## 2.9. Estado de Implementación de Reglas

### 2.9.1. Fase 1 Completada ✅
* **SOLID Principles**: Implementados en Domain Layer
  * ✅ Single Responsibility: Entidades separadas por archivo
  * ✅ Open/Closed: Interfaces extensibles
  * ✅ Liskov Substitution: Repositorios concretos
  * ✅ Interface Segregation: Interfaces específicas
  * ✅ Dependency Inversion: Container y adapters
* **Clean Architecture**: Estructura implementada
  * ✅ Domain Layer: Entidades y reglas de negocio puras
  * ✅ Infrastructure Layer: Implementaciones con Django ORM
  * ✅ **Modelos Django separados por responsabilidad** (corregido)
  * ✅ **Single Source of Truth en enumeraciones** (corregido)
* **Type Hints**: Implementados en todas las entidades
* **Documentación**: Docstrings en todas las clases

### 2.9.2. Fase 2 Completada ✅
* **Configuración Simplificada**: Principio KISS aplicado
  * Una sola configuración en `settings.py`
  * Un solo archivo `requirements.txt`
  * Comandos simplificados en `Makefile`
* **Compatibilidad Preservada**: Variables de entorno y comandos legacy
* **Dependency Injection**: Container configurado en `apps/analytics/infrastructure/container.py`
* **Estructura Optimizada**: Eliminación de archivos redundantes

### 2.9.3. Próximas Implementaciones
* **Use Cases Layer**: Aplicar reglas en lógica de aplicación
* **Presentation Layer**: Aplicar reglas en APIs y serializers
* **Testing**: Implementar tests unitarios y de integración
* **CI/CD**: Automatizar verificaciones de calidad

---

**Reglas de Desarrollo y Estándares - Microservicio de Inteligencia de Negocios**
*Versión: 1.3*
*Fecha: 2025*
*Equipo: BI/AI/Agentes*
*Estado: Fase 1 Completada + Correcciones SOLID Aplicadas* 