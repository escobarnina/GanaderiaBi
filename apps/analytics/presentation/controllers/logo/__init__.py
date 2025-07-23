"""
Controllers de Clean Architecture para logos de marcas bovinas
Organizados por responsabilidad siguiendo principios SOLID
"""

# CRUD Controllers
from .crud_controller import (
    listar_logos,
    obtener_logo,
    generar_logo,
)

# Consulta Controllers
from .consulta_controller import (
    logos_pendientes,
    logos_fallidos,
)

# Calidad Controllers
from .calidad_controller import (
    logos_por_calidad,
    evaluar_calidad_masiva,
)

# Rendimiento Controllers
from .rendimiento_controller import (
    rendimiento_modelos_ia,
    analisis_prompts,
)

# Generación Controllers
from .generacion_controller import (
    regenerar_logo,
    generar_logos_masivo,
)

__all__ = [
    # CRUD
    "listar_logos",
    "obtener_logo",
    "generar_logo",
    # Consulta
    "logos_pendientes",
    "logos_fallidos",
    # Calidad
    "logos_por_calidad",
    "evaluar_calidad_masiva",
    # Rendimiento
    "rendimiento_modelos_ia",
    "analisis_prompts",
    # Generación
    "regenerar_logo",
    "generar_logos_masivo",
]
