"""
URLs específicas para Dashboard de ganado bovino
"""

from django.urls import path
from ..controllers.dashboard import (
    # KPIs principales
    kpis_principales,
    metricas_tiempo_real,
    # Tendencias
    tendencias_mensuales,
    analisis_tendencias,
    # Ejecutivo
    resumen_ejecutivo,
    generar_reporte_ejecutivo,
    metricas_eficiencia_regional,
)

app_name = "dashboard"

urlpatterns = [
    # ============================================================================
    # ENDPOINTS DE KPIs PRINCIPALES
    # ============================================================================
    path("kpis/", kpis_principales, name="kpis_principales"),
    path("metricas-tiempo-real/", metricas_tiempo_real, name="metricas_tiempo_real"),
    # ============================================================================
    # ENDPOINTS DE TENDENCIAS
    # ============================================================================
    path("tendencias-mensuales/", tendencias_mensuales, name="tendencias_mensuales"),
    path("analisis-tendencias/", analisis_tendencias, name="analisis_tendencias"),
    # ============================================================================
    # ENDPOINTS DE RESUMEN EJECUTIVO
    # ============================================================================
    path("resumen-ejecutivo/", resumen_ejecutivo, name="resumen_ejecutivo"),
    path(
        "generar-reporte-ejecutivo/",
        generar_reporte_ejecutivo,
        name="generar_reporte_ejecutivo",
    ),
    path(
        "eficiencia-regional/",
        metricas_eficiencia_regional,
        name="metricas_eficiencia_regional",
    ),
]
