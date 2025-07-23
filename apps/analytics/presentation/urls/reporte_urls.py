"""
URLs específicas para Reportes de ganado bovino
"""

from django.urls import path
from ..controllers.reporte import (
    # Ejecutivo
    reporte_ejecutivo_mensual,
    reporte_anual,
    # Comparativo
    reporte_comparativo_departamentos,
    analisis_competitividad_departamental,
    # Personalizado
    reporte_personalizado,
    generar_reporte_personalizado_avanzado,
    exportar_excel,
    # Especializado
    reporte_productor_individual,
    reporte_impacto_economico,
    reporte_innovacion_tecnologica,
    reporte_sostenibilidad_sectorial,
)

app_name = "reporte"

urlpatterns = [
    # ============================================================================
    # ENDPOINTS DE REPORTES EJECUTIVOS
    # ============================================================================
    path(
        "ejecutivo-mensual/",
        reporte_ejecutivo_mensual,
        name="reporte_ejecutivo_mensual",
    ),
    path("ejecutivo-anual/", reporte_anual, name="reporte_anual"),
    # ============================================================================
    # ENDPOINTS DE REPORTES COMPARATIVOS
    # ============================================================================
    path(
        "comparativo-departamentos/",
        reporte_comparativo_departamentos,
        name="reporte_comparativo_departamentos",
    ),
    path(
        "competitividad-departamental/",
        analisis_competitividad_departamental,
        name="analisis_competitividad_departamental",
    ),
    # ============================================================================
    # ENDPOINTS DE REPORTES PERSONALIZADOS
    # ============================================================================
    path("personalizado/", reporte_personalizado, name="reporte_personalizado"),
    path(
        "personalizado-avanzado/",
        generar_reporte_personalizado_avanzado,
        name="generar_reporte_personalizado_avanzado",
    ),
    path("exportar-excel/", exportar_excel, name="exportar_excel"),
    # ============================================================================
    # ENDPOINTS DE REPORTES ESPECIALIZADOS
    # ============================================================================
    path(
        "productor-individual/",
        reporte_productor_individual,
        name="reporte_productor_individual",
    ),
    path(
        "impacto-economico/",
        reporte_impacto_economico,
        name="reporte_impacto_economico",
    ),
    path(
        "innovacion-tecnologica/",
        reporte_innovacion_tecnologica,
        name="reporte_innovacion_tecnologica",
    ),
    path(
        "sostenibilidad-sectorial/",
        reporte_sostenibilidad_sectorial,
        name="reporte_sostenibilidad_sectorial",
    ),
]
