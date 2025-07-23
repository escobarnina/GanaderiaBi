"""
Controllers de Clean Architecture para Dashboard de ganado bovino
Organizados por responsabilidad siguiendo principios SOLID
"""

# KPIs Controllers
from .kpis_controller import (
    kpis_principales,
    metricas_tiempo_real,
)

# Tendencias Controllers
from .tendencias_controller import (
    tendencias_mensuales,
    analisis_tendencias,
)

# Ejecutivo Controllers
from .ejecutivo_controller import (
    resumen_ejecutivo,
    generar_reporte_ejecutivo,
    metricas_eficiencia_regional,
)

__all__ = [
    # KPIs
    "kpis_principales",
    "metricas_tiempo_real",
    # Tendencias
    "tendencias_mensuales",
    "analisis_tendencias",
    # Ejecutivo
    "resumen_ejecutivo",
    "generar_reporte_ejecutivo",
    "metricas_eficiencia_regional",
]
