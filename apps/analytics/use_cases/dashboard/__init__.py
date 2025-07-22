"""
Use Cases para gestión de dashboard
"""

from .obtener_dashboard_data_use_case import ObtenerDashboardDataUseCase
from .generar_reporte_dashboard_use_case import GenerarReporteDashboardUseCase

__all__ = [
    "ObtenerDashboardDataUseCase",
    "GenerarReporteDashboardUseCase",
]
