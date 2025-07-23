"""
URLs específicas para Generación de Datos
"""

from django.urls import path
from ..controllers.data_generation import (
    generar_datos_mockaroo,
    generar_descripcion_marca,
    generar_prompts_logo,
)

app_name = "data_generation"

urlpatterns = [
    # ============================================================================
    # ENDPOINTS DE GENERACIÓN DE DATOS
    # ============================================================================
    path(
        "generar-datos-mockaroo/", generar_datos_mockaroo, name="generar_datos_mockaroo"
    ),
    path(
        "generar-descripcion-marca/",
        generar_descripcion_marca,
        name="generar_descripcion_marca",
    ),
    path("generar-prompts-logo/", generar_prompts_logo, name="generar_prompts_logo"),
]
