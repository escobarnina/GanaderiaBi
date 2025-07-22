# apps/analytics/infrastructure/models/__init__.py
"""
Modelos Django separados por responsabilidad - Clean Architecture
Cada modelo en su propio archivo siguiendo Single Responsibility Principle
"""

from .marca_ganado_bovino_model import MarcaGanadoBovinoModel
from .logo_marca_bovina_model import LogoMarcaBovinaModel
from .kpi_ganado_bovino_model import KPIGanadoBovinoModel
from .historial_estado_marca_model import HistorialEstadoMarcaModel
from .dashboard_data_model import DashboardDataModel
from .reporte_data_model import ReporteDataModel

__all__ = [
    "MarcaGanadoBovinoModel",
    "LogoMarcaBovinaModel",
    "KPIGanadoBovinoModel",
    "HistorialEstadoMarcaModel",
    "DashboardDataModel",
    "ReporteDataModel",
]
