"""
Controllers de Clean Architecture para la aplicación de analytics
Implementan la lógica de presentación usando use cases
"""

from .marca_controller import MarcaController
from .logo_controller import LogoController
from .kpi_controller import KPIController
from .dashboard_controller import DashboardController
from .historial_controller import HistorialController
from .reporte_controller import ReporteController

__all__ = [
    "MarcaController",
    "LogoController",
    "KPIController",
    "DashboardController",
    "HistorialController",
    "ReporteController",
]
