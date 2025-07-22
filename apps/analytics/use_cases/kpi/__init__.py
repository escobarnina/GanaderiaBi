"""
Use Cases para gestión de KPIs de ganado bovino
"""

from .calcular_kpis_use_case import CalcularKPIsUseCase
from .obtener_kpis_use_case import ObtenerKPIsUseCase
from .generar_reporte_kpis_use_case import GenerarReporteKPIsUseCase

__all__ = [
    "CalcularKPIsUseCase",
    "ObtenerKPIsUseCase",
    "GenerarReporteKPIsUseCase",
]
