"""
URLs globales para la aplicación de analytics
Agrupa todas las URLs específicas por dominio
"""

from django.urls import path, include

app_name = "analytics"

urlpatterns = [
    # ============================================================================
    # URLs POR DOMINIO
    # ============================================================================
    path("marcas/", include("apps.analytics.presentation.urls.marca_urls")),
    path("logos/", include("apps.analytics.presentation.urls.logo_urls")),
    path("kpis/", include("apps.analytics.presentation.urls.kpi_urls")),
    path("dashboard/", include("apps.analytics.presentation.urls.dashboard_urls")),
    path("historial/", include("apps.analytics.presentation.urls.historial_urls")),
    path("reportes/", include("apps.analytics.presentation.urls.reporte_urls")),
]
