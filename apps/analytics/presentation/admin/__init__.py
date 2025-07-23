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

from .marca_admin import MarcaGanadoBovinoAdmin
from .logo_admin import LogoMarcaBovinaAdmin
from .kpi_admin import KPIGanadoBovinoAdmin
from .historial_admin import HistorialEstadoMarcaAdmin
from .dashboard_admin import DashboardDataAdmin
from .reporte_admin import ReporteDataAdmin

__all__ = [
    "MarcaGanadoBovinoAdmin",
    "LogoMarcaBovinaAdmin",
    "KPIGanadoBovinoAdmin",
    "HistorialEstadoMarcaAdmin",
    "DashboardDataAdmin",
    "ReporteDataAdmin",
]

# Información del módulo admin
ADMIN_VERSION = "1.0.0"
ADMIN_STATUS = "✅ Completado"
TOTAL_ADMINS = 6


def get_admin_info():
    """Retorna información del módulo admin"""
    return {
        "version": ADMIN_VERSION,
        "status": ADMIN_STATUS,
        "total_admins": TOTAL_ADMINS,
        "admins": __all__,
    }
