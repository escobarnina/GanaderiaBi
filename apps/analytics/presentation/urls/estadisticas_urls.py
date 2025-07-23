"""
URLs específicas para Estadísticas de ganado bovino
"""

from django.urls import path
from ..controllers.estadisticas import (
    # Análisis
    estadisticas_por_raza,
    estadisticas_por_departamento,
    estadisticas_por_proposito,
    # Tendencias
    comparativa_temporal,
    predicciones_demanda,
    tendencias_geograficas,
    # Tecnología
    rendimiento_modelos_ia,
    analisis_eficiencia,
    distribucion_razas,
)

app_name = "estadisticas"

urlpatterns = [
    # ============================================================================
    # ENDPOINTS DE ANÁLISIS DE ESTADÍSTICAS
    # ============================================================================
    path("por-raza/", estadisticas_por_raza, name="estadisticas_por_raza"),
    path(
        "por-departamento/",
        estadisticas_por_departamento,
        name="estadisticas_por_departamento",
    ),
    path(
        "por-proposito/", estadisticas_por_proposito, name="estadisticas_por_proposito"
    ),
    # ============================================================================
    # ENDPOINTS DE TENDENCIAS
    # ============================================================================
    path("comparativa-temporal/", comparativa_temporal, name="comparativa_temporal"),
    path("predicciones-demanda/", predicciones_demanda, name="predicciones_demanda"),
    path(
        "tendencias-geograficas/", tendencias_geograficas, name="tendencias_geograficas"
    ),
    # ============================================================================
    # ENDPOINTS DE TECNOLOGÍA
    # ============================================================================
    path(
        "rendimiento-modelos-ia/", rendimiento_modelos_ia, name="rendimiento_modelos_ia"
    ),
    path("analisis-eficiencia/", analisis_eficiencia, name="analisis_eficiencia"),
    path("distribucion-razas/", distribucion_razas, name="distribucion_razas"),
]
