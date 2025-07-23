"""
Controllers de Clean Architecture para KPIs de ganado bovino
Organizados por responsabilidad siguiendo principios SOLID
"""

# CRUD Controllers
from .crud_controller import (
    listar_kpis,
    obtener_kpi,
    calcular_kpis,
)

# Temporal Controllers
from .temporal_controller import (
    ultimos_12_meses,
    kpis_actuales,
)

# Comparativo Controllers
from .comparativo_controller import (
    comparativa_trimestral,
)

# Estacional Controllers
from .estacional_controller import (
    analisis_estacional,
)

__all__ = [
    # CRUD
    "listar_kpis",
    "obtener_kpi",
    "calcular_kpis",
    # Temporal
    "ultimos_12_meses",
    "kpis_actuales",
    # Comparativo
    "comparativa_trimestral",
    # Estacional
    "analisis_estacional",
]
