"""
URLs específicas para logos de marcas bovinas
"""

from django.urls import path
from ..controllers.logo import (
    # CRUD básicos
    listar_logos,
    obtener_logo,
    generar_logo,
    # Consultas especializadas
    logos_pendientes,
    logos_fallidos,
    # Análisis de calidad
    logos_por_calidad,
    evaluar_calidad_masiva,
    # Análisis de rendimiento
    rendimiento_modelos_ia,
    analisis_prompts,
    # Generación y regeneración
    regenerar_logo,
    generar_logos_masivo,
)

app_name = "logo"

urlpatterns = [
    # ============================================================================
    # ENDPOINTS CRUD BÁSICOS
    # ============================================================================
    path("", listar_logos, name="listar_logos"),
    path("<int:logo_id>/", obtener_logo, name="obtener_logo"),
    path("generar/", generar_logo, name="generar_logo"),
    # ============================================================================
    # ENDPOINTS DE CONSULTA ESPECIALIZADA
    # ============================================================================
    path("pendientes/", logos_pendientes, name="logos_pendientes"),
    path("fallidos/", logos_fallidos, name="logos_fallidos"),
    # ============================================================================
    # ENDPOINTS DE ANÁLISIS DE CALIDAD
    # ============================================================================
    path("por-calidad/", logos_por_calidad, name="logos_por_calidad"),
    path(
        "evaluar-calidad-masiva/", evaluar_calidad_masiva, name="evaluar_calidad_masiva"
    ),
    # ============================================================================
    # ENDPOINTS DE ANÁLISIS DE RENDIMIENTO
    # ============================================================================
    path(
        "rendimiento-modelos-ia/", rendimiento_modelos_ia, name="rendimiento_modelos_ia"
    ),
    path("analisis-prompts/", analisis_prompts, name="analisis_prompts"),
    # ============================================================================
    # ENDPOINTS DE GENERACIÓN Y REGENERACIÓN
    # ============================================================================
    path("<int:logo_id>/regenerar/", regenerar_logo, name="regenerar_logo"),
    path("generar-masivo/", generar_logos_masivo, name="generar_logos_masivo"),
]
