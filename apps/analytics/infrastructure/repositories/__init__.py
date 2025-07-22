"""
Repositorios de infraestructura para la aplicación de analytics
Implementaciones concretas de los repositorios de dominio usando Django ORM
"""

from .marca_repository import DjangoMarcaRepository
from .logo_repository import DjangoLogoRepository
from .kpi_repository import DjangoKpiRepository
from .historial_repository import DjangoHistorialRepository
from .dashboard_repository import DjangoDashboardRepository
from .reporte_repository import DjangoReporteRepository

__all__ = [
    "DjangoMarcaRepository",
    "DjangoLogoRepository",
    "DjangoKpiRepository",
    "DjangoHistorialRepository",
    "DjangoDashboardRepository",
    "DjangoReporteRepository",
]
