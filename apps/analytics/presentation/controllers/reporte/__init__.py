"""
Controllers de Clean Architecture para Reportes de ganado bovino
Organizados por responsabilidad siguiendo principios SOLID
"""

# Ejecutivo Controllers
from .ejecutivo_controller import (
    reporte_ejecutivo_mensual,
    reporte_anual,
)

# Comparativo Controllers
from .comparativo_controller import (
    reporte_comparativo_departamentos,
    analisis_competitividad_departamental,
)

# Personalizado Controllers
from .personalizado_controller import (
    reporte_personalizado,
    generar_reporte_personalizado_avanzado,
    exportar_excel,
)

# Especializado Controllers
from .especializado_controller import (
    reporte_productor_individual,
    reporte_impacto_economico,
    reporte_innovacion_tecnologica,
    reporte_sostenibilidad_sectorial,
)

__all__ = [
    # Ejecutivo
    "reporte_ejecutivo_mensual",
    "reporte_anual",
    # Comparativo
    "reporte_comparativo_departamentos",
    "analisis_competitividad_departamental",
    # Personalizado
    "reporte_personalizado",
    "generar_reporte_personalizado_avanzado",
    "exportar_excel",
    # Especializado
    "reporte_productor_individual",
    "reporte_impacto_economico",
    "reporte_innovacion_tecnologica",
    "reporte_sostenibilidad_sectorial",
]
