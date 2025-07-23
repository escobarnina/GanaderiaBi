"""
URLs de business_intelligence - Migrado a Clean Architecture
Redirige a los nuevos controllers de Clean Architecture
"""

from django.urls import path, include
from django.http import HttpResponseRedirect
from django.urls import reverse

# ============================================================================
# FUNCIONES DE REDIRECCIÓN PARA MIGRACIÓN GRADUAL
# ============================================================================

def redirect_to_clean_architecture(request, new_path):
    """Redirige a la nueva estructura de Clean Architecture"""
    return HttpResponseRedirect(f"/api/analytics/{new_path}")

# ============================================================================
# URLS PRINCIPALES - REDIRIGEN A CLEAN ARCHITECTURE
# ============================================================================

urlpatterns = [
    # ============================================================================
    # REDIRECCIONES A MARCAS (Clean Architecture)
    # ============================================================================
    path("marcas-bovinas/", lambda request: redirect_to_clean_architecture(request, "marcas/"), name="marcas-bovinas-legacy"),
    path("marcas-bovinas/<int:pk>/", lambda request, pk: redirect_to_clean_architecture(request, f"marcas/{pk}/"), name="marca-detail-legacy"),
    
    # ============================================================================
    # REDIRECCIONES A LOGOS (Clean Architecture)
    # ============================================================================
    path("logos-bovinos/", lambda request: redirect_to_clean_architecture(request, "logos/"), name="logos-bovinos-legacy"),
    path("logos-bovinos/<int:pk>/", lambda request, pk: redirect_to_clean_architecture(request, f"logos/{pk}/"), name="logo-detail-legacy"),
    
    # ============================================================================
    # REDIRECCIONES A DASHBOARD (Clean Architecture)
    # ============================================================================
    path("dashboard-bovino/", lambda request: redirect_to_clean_architecture(request, "dashboard/"), name="dashboard-bovino-legacy"),
    path("dashboard/kpis-principales/", lambda request: redirect_to_clean_architecture(request, "dashboard/kpis/"), name="dashboard-kpis-legacy"),
    path("dashboard/tendencias-mensuales/", lambda request: redirect_to_clean_architecture(request, "dashboard/tendencias/"), name="dashboard-tendencias-legacy"),
    path("dashboard/metricas-tiempo-real/", lambda request: redirect_to_clean_architecture(request, "dashboard/tiempo-real/"), name="dashboard-tiempo-real-legacy"),
    path("dashboard/resumen-ejecutivo/", lambda request: redirect_to_clean_architecture(request, "dashboard/ejecutivo/"), name="dashboard-resumen-legacy"),
    
    # ============================================================================
    # REDIRECCIONES A KPIS (Clean Architecture)
    # ============================================================================
    path("kpis-bovinos/", lambda request: redirect_to_clean_architecture(request, "kpis/"), name="kpis-bovinos-legacy"),
    path("kpis/ultimos-12-meses/", lambda request: redirect_to_clean_architecture(request, "kpis/12-meses/"), name="kpis-12-meses-legacy"),
    path("kpis/comparativa-trimestral/", lambda request: redirect_to_clean_architecture(request, "kpis/trimestral/"), name="kpis-trimestral-legacy"),
    path("kpis/analisis-estacional/", lambda request: redirect_to_clean_architecture(request, "kpis/estacional/"), name="kpis-estacional-legacy"),
    path("kpis/actuales/", lambda request: redirect_to_clean_architecture(request, "kpis/actuales/"), name="kpis-actuales-legacy"),
    
    # ============================================================================
    # REDIRECCIONES A HISTORIAL (Clean Architecture)
    # ============================================================================
    path("historial-estados/", lambda request: redirect_to_clean_architecture(request, "historial/"), name="historial-estados-legacy"),
    path("historial/actividad-reciente/", lambda request: redirect_to_clean_architecture(request, "historial/actividad/"), name="historial-reciente-legacy"),
    path("historial/auditoria-usuario/", lambda request: redirect_to_clean_architecture(request, "historial/auditoria/"), name="historial-usuario-legacy"),
    path("historial/patrones-cambio/", lambda request: redirect_to_clean_architecture(request, "historial/patrones/"), name="historial-patrones-legacy"),
    path("historial/eficiencia-evaluadores/", lambda request: redirect_to_clean_architecture(request, "historial/eficiencia/"), name="historial-evaluadores-legacy"),
    
    # ============================================================================
    # REDIRECCIONES A ESTADÍSTICAS (Clean Architecture)
    # ============================================================================
    path("estadisticas-bovinos/", lambda request: redirect_to_clean_architecture(request, "estadisticas/"), name="estadisticas-bovinos-legacy"),
    path("estadisticas/por-raza/", lambda request: redirect_to_clean_architecture(request, "estadisticas/por-raza/"), name="stats-raza-legacy"),
    path("estadisticas/por-departamento/", lambda request: redirect_to_clean_architecture(request, "estadisticas/por-departamento/"), name="stats-departamento-legacy"),
    path("estadisticas/por-proposito/", lambda request: redirect_to_clean_architecture(request, "estadisticas/por-proposito/"), name="stats-proposito-legacy"),
    path("estadisticas/rendimiento-ia/", lambda request: redirect_to_clean_architecture(request, "estadisticas/rendimiento-modelos-ia/"), name="stats-ia-legacy"),
    path("estadisticas/comparativa-temporal/", lambda request: redirect_to_clean_architecture(request, "estadisticas/comparativa-temporal/"), name="stats-temporal-legacy"),
    path("estadisticas/predicciones/", lambda request: redirect_to_clean_architecture(request, "estadisticas/predicciones-demanda/"), name="stats-predicciones-legacy"),
    path("estadisticas/eficiencia/", lambda request: redirect_to_clean_architecture(request, "estadisticas/analisis-eficiencia/"), name="stats-eficiencia-legacy"),
    path("estadisticas/tendencias-geograficas/", lambda request: redirect_to_clean_architecture(request, "estadisticas/tendencias-geograficas/"), name="stats-geografico-legacy"),
    path("estadisticas/distribucion-razas/", lambda request: redirect_to_clean_architecture(request, "estadisticas/distribucion-razas/"), name="stats-razas-legacy"),
    
    # ============================================================================
    # REDIRECCIONES A REPORTES (Clean Architecture)
    # ============================================================================
    path("reportes-bovinos/", lambda request: redirect_to_clean_architecture(request, "reportes/"), name="reportes-bovinos-legacy"),
    path("reportes/ejecutivo-mensual/", lambda request: redirect_to_clean_architecture(request, "reportes/ejecutivo/mensual/"), name="reporte-mensual-legacy"),
    path("reportes/anual/", lambda request: redirect_to_clean_architecture(request, "reportes/ejecutivo/anual/"), name="reporte-anual-legacy"),
    path("reportes/comparativo-departamentos/", lambda request: redirect_to_clean_architecture(request, "reportes/comparativo/departamentos/"), name="reporte-departamentos-legacy"),
    path("reportes/personalizado/", lambda request: redirect_to_clean_architecture(request, "reportes/personalizado/"), name="reporte-personalizado-legacy"),
    path("reportes/exportar/excel/", lambda request: redirect_to_clean_architecture(request, "reportes/personalizado/exportar/"), name="exportar-excel-legacy"),
    
    # ============================================================================
    # REDIRECCIONES A DATA GENERATION (Clean Architecture)
    # ============================================================================
    path("data-generation/generar-datos-mockaroo/", lambda request: redirect_to_clean_architecture(request, "data-generation/generar-datos-mockaroo/"), name="data-generation-mockaroo-legacy"),
    path("data-generation/generar-descripcion-marca/", lambda request: redirect_to_clean_architecture(request, "data-generation/generar-descripcion-marca/"), name="data-generation-descripcion-legacy"),
    path("data-generation/generar-prompts-logo/", lambda request: redirect_to_clean_architecture(request, "data-generation/generar-prompts-logo/"), name="data-generation-prompts-legacy"),
]

# ============================================================================
# MENSAJE DE MIGRACIÓN
# ============================================================================

def migration_notice(request):
    """Muestra un mensaje sobre la migración a Clean Architecture"""
    return HttpResponseRedirect("/api/analytics/")
