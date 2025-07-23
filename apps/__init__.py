"""
Paquete principal de aplicaciones - Clean Architecture

Este paquete contiene todas las aplicaciones del sistema de inteligencia de negocios ganadero,
implementadas siguiendo los principios de Clean Architecture.

Aplicaciones disponibles:
- analytics: Sistema principal de analytics con Clean Architecture
  - Domain Layer: Entidades, repositorios, enums
  - Application Layer: Use cases del negocio
  - Infrastructure Layer: Modelos Django, implementaciones de repositorios
  - Presentation Layer: Controllers, serializers, URLs

Estructura:
apps/
├── analytics/                 # ✅ Sistema principal de analytics
│   ├── domain/              # Lógica de negocio pura
│   ├── use_cases/           # Casos de uso del negocio
│   ├── infrastructure/      # Implementaciones concretas
│   └── presentation/        # Interfaces de usuario y APIs
└── __init__.py             # Este archivo

Estado de la migración:
✅ Domain Layer: 100% completado
✅ Application Layer: 100% completado (35 use cases)
✅ Infrastructure Layer: 100% completado
✅ Presentation Layer: 100% completado (71 controllers, 8 serializers)

Versión del proyecto: Sincronizada con apps.analytics.__version__
"""

__author__ = "GanaderiaBi Team"

# Aplicaciones disponibles
AVAILABLE_APPS = [
    "analytics",
]

# Estado de migración por aplicación
MIGRATION_STATUS = {
    "analytics": {
        "domain": "✅ Completado",
        "application": "✅ Completado",
        "infrastructure": "✅ Completado",
        "presentation": "✅ Completado",
        "overall": "✅ 100% Migrado a Clean Architecture",
    }
}


def get_migration_status():
    """Retorna el estado de migración de todas las aplicaciones"""
    return MIGRATION_STATUS


def get_available_apps():
    """Retorna la lista de aplicaciones disponibles"""
    return AVAILABLE_APPS


def get_project_version():
    """Retorna la versión del proyecto desde analytics"""
    try:
        from apps.analytics import __version__ as analytics_version

        return analytics_version
    except ImportError:
        return "No disponible"
