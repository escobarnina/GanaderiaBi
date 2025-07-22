# business_intelligence/views/__init__.py
"""
Estructura modular de views para el sistema de ganado bovino
"""

from .marca_bovino_views import MarcaGanadoBovinoViewSet
from .logo_bovino_views import LogoMarcaBovinaViewSet
from .dashboard_views import DashboardBovinoViewSet
from .kpi_views import KPIGanadoBovinoViewSet
from .historial_views import HistorialEstadoMarcaViewSet
from .estadisticas_views import EstadisticasBovinoViewSet
from .reportes_views import ReportesBovinoViewSet

__all__ = [
    "MarcaGanadoBovinoViewSet",
    "LogoMarcaBovinaViewSet",
    "DashboardBovinoViewSet",
    "KPIGanadoBovinoViewSet",
    "HistorialEstadoMarcaViewSet",
    "EstadisticasBovinoViewSet",
    "ReportesBovinoViewSet",
]
