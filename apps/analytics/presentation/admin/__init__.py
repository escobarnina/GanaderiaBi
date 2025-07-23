"""
Configuración del Admin de Django para Clean Architecture.

Este módulo contiene las configuraciones del admin que son específicas
de la implementación de Django, siguiendo los principios de Clean Architecture.

Admins disponibles:
- MarcaGanadoBovinoAdmin: Gestión de marcas con acciones masivas
- LogoMarcaBovinaAdmin: Visualización de logos con indicadores de calidad
- KPIGanadoBovinoAdmin: Análisis de KPIs con métricas de eficiencia
- HistorialEstadoMarcaAdmin: Auditoría completa de cambios de estado
- DashboardDataAdmin: Dashboard con métricas en tiempo real
- ReporteDataAdmin: Gestión de reportes con análisis de datos

Estado: ✅ 6 admins completos siguiendo Clean Architecture y SOLID
"""

from django.contrib import admin
from django.apps import apps
from .dashboard_admin import DashboardDataAdmin
from .reporte_admin import ReporteDataAdmin
from .kpi_admin import KPIGanadoBovinoAdmin
from .historial_admin import HistorialEstadoMarcaAdmin
from .marca_admin import MarcaGanadoBovinoAdmin
from .logo_admin import LogoMarcaBovinaAdmin

__all__ = [
    "DashboardDataAdmin",
    "ReporteDataAdmin",
    "KPIGanadoBovinoAdmin",
    "HistorialEstadoMarcaAdmin",
    "MarcaGanadoBovinoAdmin",
    "LogoMarcaBovinaAdmin",
]

# Información del módulo admin
ADMIN_VERSION = "2.0.0"
ADMIN_STATUS = "✅ Completado con funcionalidades avanzadas"
TOTAL_ADMINS = 6


def get_admin_info():
    """Retorna información detallada del módulo admin"""
    return {
        "version": ADMIN_VERSION,
        "status": ADMIN_STATUS,
        "total_admins": TOTAL_ADMINS,
        "admins": __all__,
        "features": [
            "Acciones masivas inteligentes",
            "Visualización con colores dinámicos",
            "Dashboard en tiempo real",
            "Auditoría completa",
            "Exportación múltiple formato",
            "Filtros avanzados en cascada",
        ],
    }


def get_admin_statistics():
    """Obtiene estadísticas de uso de los admins"""
    try:
        # Obtener modelos registrados
        analytics_app = apps.get_app_config("analytics")
        models = analytics_app.get_models()

        stats = {}
        for model in models:
            stats[model.__name__] = {
                "total_records": model.objects.count(),
                "admin_registered": model in admin.site._registry,
            }

        return stats
    except Exception as e:
        return {"error": str(e)}


# Configuración personalizada del sitio admin
def customize_admin_site():
    """Personaliza el sitio de administración"""
    admin.site.site_header = "🐄 Sistema BI Ganado Bovino"
    admin.site.site_title = "BI Ganado Admin"
    admin.site.index_title = "Panel de Control - Inteligencia de Negocios"
    admin.site.site_url = "/dashboard/"
    admin.site.enable_nav_sidebar = True


# Ejecutar personalización
customize_admin_site()
