"""
Controllers de Clean Architecture para Estadísticas de ganado bovino
Organizados por responsabilidad siguiendo principios SOLID
"""

# Análisis Controllers
from .analisis_controller import (
    estadisticas_por_raza,
    estadisticas_por_departamento,
    estadisticas_por_proposito,
)

# Tendencias Controllers
from .tendencias_controller import (
    comparativa_temporal,
    predicciones_demanda,
    tendencias_geograficas,
)

# Tecnología Controllers
from .tecnologia_controller import (
    rendimiento_modelos_ia,
    analisis_eficiencia,
    distribucion_razas,
)

__all__ = [
    # Análisis
    "estadisticas_por_raza",
    "estadisticas_por_departamento",
    "estadisticas_por_proposito",
    # Tendencias
    "comparativa_temporal",
    "predicciones_demanda",
    "tendencias_geograficas",
    # Tecnología
    "rendimiento_modelos_ia",
    "analisis_eficiencia",
    "distribucion_razas",
]
