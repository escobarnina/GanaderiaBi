# apps/analytics/domain/repositories/__init__.py
"""
Interfaces de repositorios para el dominio de Inteligencia de Negocios
"""

from .marca_repository import MarcaGanadoBovinoRepository
from .logo_repository import LogoMarcaBovinaRepository
from .kpi_repository import KPIGanadoBovinoRepository
from .historial_repository import HistorialEstadoMarcaRepository
from .dashboard_repository import DashboardRepository
from .reporte_repository import ReporteRepository

__all__ = [
    "MarcaGanadoBovinoRepository",
    "LogoMarcaBovinaRepository",
    "KPIGanadoBovinoRepository",
    "HistorialEstadoMarcaRepository",
    "DashboardRepository",
    "ReporteRepository",
]
