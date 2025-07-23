"""
URLs específicas para KPIs de ganado bovino
"""

from django.urls import path
from ..controllers.kpi import (
    # CRUD básicos
    listar_kpis,
    obtener_kpi,
    calcular_kpis,
    # Análisis temporal
    ultimos_12_meses,
    kpis_actuales,
    # Análisis comparativo
    comparativa_trimestral,
    # Análisis estacional
    analisis_estacional,
)

app_name = "kpi"

urlpatterns = [
    # ============================================================================
    # ENDPOINTS CRUD BÁSICOS
    # ============================================================================
    path("", listar_kpis, name="listar_kpis"),
    path("<int:kpi_id>/", obtener_kpi, name="obtener_kpi"),
    path("calcular/", calcular_kpis, name="calcular_kpis"),
    # ============================================================================
    # ENDPOINTS DE ANÁLISIS TEMPORAL
    # ============================================================================
    path("ultimos-12-meses/", ultimos_12_meses, name="ultimos_12_meses"),
    path("actuales/", kpis_actuales, name="kpis_actuales"),
    # ============================================================================
    # ENDPOINTS DE ANÁLISIS COMPARATIVO
    # ============================================================================
    path(
        "comparativa-trimestral/", comparativa_trimestral, name="comparativa_trimestral"
    ),
    # ============================================================================
    # ENDPOINTS DE ANÁLISIS ESTACIONAL
    # ============================================================================
    path("analisis-estacional/", analisis_estacional, name="analisis_estacional"),
]
