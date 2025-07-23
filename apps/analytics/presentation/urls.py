"""
URLs principales para la app analytics siguiendo Clean Architecture.

Responsabilidades:
- Centralizar todas las URLs de los módulos de analytics
- Mantener separación de responsabilidades por módulo
- Proporcionar endpoints RESTful para cada funcionalidad
"""

from django.urls import path, include
from django.http import JsonResponse


def test_api(request):
    """Endpoint de prueba para verificar que la API funciona"""
    return JsonResponse(
        {
            "message": "API funcionando correctamente",
            "status": "success",
            "endpoints": {
                "marcas": "/api/analytics/marcas/",
                "logos": "/api/analytics/logos/",
                "kpis": "/api/analytics/kpis/",
                "dashboard": "/api/analytics/dashboard/",
                "reportes": "/api/analytics/reportes/",
            },
        }
    )


# URLs de los módulos específicos
urlpatterns = [
    # Endpoint de prueba
    path("test/", test_api, name="test_api"),
    # URLs de marcas
    path("marcas/", include("apps.analytics.presentation.urls.marca_urls")),
    # URLs de logos
    path("logos/", include("apps.analytics.presentation.urls.logo_urls")),
    # URLs de KPIs
    path("kpis/", include("apps.analytics.presentation.urls.kpi_urls")),
    # URLs de historial
    path("historial/", include("apps.analytics.presentation.urls.historial_urls")),
    # URLs de dashboard
    path("dashboard/", include("apps.analytics.presentation.urls.dashboard_urls")),
    # URLs de reportes
    path("reportes/", include("apps.analytics.presentation.urls.reporte_urls")),
    # URLs de estadísticas
    path(
        "estadisticas/", include("apps.analytics.presentation.urls.estadisticas_urls")
    ),
    # URLs de data generation
    path(
        "data-generation/",
        include("apps.analytics.presentation.urls.data_generation_urls"),
    ),
]
