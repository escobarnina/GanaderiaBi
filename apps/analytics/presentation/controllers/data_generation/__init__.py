"""
Controllers de Clean Architecture para Generación de Datos
Organizados por responsabilidad siguiendo principios SOLID
"""

# Generación Controllers
from .generacion_controller import (
    generar_datos_mockaroo,
    generar_descripcion_marca,
    generar_prompts_logo,
)

__all__ = [
    # Generación
    "generar_datos_mockaroo",
    "generar_descripcion_marca",
    "generar_prompts_logo",
]
