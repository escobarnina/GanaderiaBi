# apps/analytics/domain/entities/__init__.py
"""
Entidades del dominio de Inteligencia de Negocios
"""

from .marca_ganado_bovino import MarcaGanadoBovino
from .logo_marca_bovina import LogoMarcaBovina
from .kpi_ganado_bovino import KPIGanadoBovino
from .historial_estado_marca import HistorialEstadoMarca
from .dashboard_data import DashboardData
from .reporte_data import ReporteData

__all__ = [
    "MarcaGanadoBovino",
    "LogoMarcaBovina",
    "KPIGanadoBovino",
    "HistorialEstadoMarca",
    "DashboardData",
    "ReporteData",
]
