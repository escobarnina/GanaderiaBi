# business_intelligence/urls.py - Actualizado para estructura modular
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MarcaGanadoBovinoViewSet,
    LogoMarcaBovinaViewSet,
    DashboardBovinoViewSet,
    KPIGanadoBovinoViewSet,
    HistorialEstadoMarcaViewSet,
    EstadisticasBovinoViewSet,
    ReportesBovinoViewSet,
)

# Router principal para los ViewSets
router = DefaultRouter()

# Registro de ViewSets con los nuevos modelos bovinos
router.register(r"marcas-bovinas", MarcaGanadoBovinoViewSet, basename="marcas-bovinas")
router.register(r"logos-bovinos", LogoMarcaBovinaViewSet, basename="logos-bovinos")
router.register(
    r"dashboard-bovino", DashboardBovinoViewSet, basename="dashboard-bovino"
)
router.register(r"kpis-bovinos", KPIGanadoBovinoViewSet, basename="kpis-bovinos")
router.register(
    r"historial-estados", HistorialEstadoMarcaViewSet, basename="historial-estados"
)
router.register(
    r"estadisticas-bovinos", EstadisticasBovinoViewSet, basename="estadisticas-bovinos"
)
router.register(r"reportes-bovinos", ReportesBovinoViewSet, basename="reportes-bovinos")

# URLs principales
urlpatterns = [
    # URLs del router
    path("", include(router.urls)),
    # URLs para dashboard (acceso directo)
    path(
        "dashboard/",
        include(
            [
                path(
                    "kpis-principales/",
                    DashboardBovinoViewSet.as_view({"get": "kpis_principales"}),
                    name="dashboard-kpis",
                ),
                path(
                    "tendencias-mensuales/",
                    DashboardBovinoViewSet.as_view({"get": "tendencias_mensuales"}),
                    name="dashboard-tendencias",
                ),
                path(
                    "metricas-tiempo-real/",
                    DashboardBovinoViewSet.as_view({"get": "metricas_tiempo_real"}),
                    name="dashboard-tiempo-real",
                ),
                path(
                    "resumen-ejecutivo/",
                    DashboardBovinoViewSet.as_view({"get": "resumen_ejecutivo"}),
                    name="dashboard-resumen",
                ),
            ]
        ),
    ),
    # URLs para estadísticas específicas
    path(
        "estadisticas/",
        include(
            [
                path(
                    "por-raza/",
                    EstadisticasBovinoViewSet.as_view({"get": "estadisticas_por_raza"}),
                    name="stats-raza",
                ),
                path(
                    "por-departamento/",
                    EstadisticasBovinoViewSet.as_view(
                        {"get": "estadisticas_por_departamento"}
                    ),
                    name="stats-departamento",
                ),
                path(
                    "por-proposito/",
                    EstadisticasBovinoViewSet.as_view(
                        {"get": "estadisticas_por_proposito"}
                    ),
                    name="stats-proposito",
                ),
                path(
                    "rendimiento-ia/",
                    EstadisticasBovinoViewSet.as_view(
                        {"get": "rendimiento_modelos_ia"}
                    ),
                    name="stats-ia",
                ),
                path(
                    "comparativa-temporal/",
                    EstadisticasBovinoViewSet.as_view({"get": "comparativa_temporal"}),
                    name="stats-temporal",
                ),
                path(
                    "predicciones/",
                    EstadisticasBovinoViewSet.as_view({"get": "predicciones_demanda"}),
                    name="stats-predicciones",
                ),
                path(
                    "eficiencia/",
                    EstadisticasBovinoViewSet.as_view({"get": "analisis_eficiencia"}),
                    name="stats-eficiencia",
                ),
                path(
                    "tendencias-geograficas/",
                    EstadisticasBovinoViewSet.as_view(
                        {"get": "tendencias_geograficas"}
                    ),
                    name="stats-geografico",
                ),
                path(
                    "distribucion-razas/",
                    EstadisticasBovinoViewSet.as_view({"get": "distribucion_razas"}),
                    name="stats-razas",
                ),
            ]
        ),
    ),
    # URLs para reportes ejecutivos
    path(
        "reportes/",
        include(
            [
                path(
                    "ejecutivo-mensual/",
                    ReportesBovinoViewSet.as_view({"get": "reporte_ejecutivo_mensual"}),
                    name="reporte-mensual",
                ),
                path(
                    "anual/",
                    ReportesBovinoViewSet.as_view({"get": "reporte_anual"}),
                    name="reporte-anual",
                ),
                path(
                    "comparativo-departamentos/",
                    ReportesBovinoViewSet.as_view(
                        {"get": "reporte_comparativo_departamentos"}
                    ),
                    name="reporte-departamentos",
                ),
                path(
                    "personalizado/",
                    ReportesBovinoViewSet.as_view({"post": "reporte_personalizado"}),
                    name="reporte-personalizado",
                ),
                path(
                    "exportar/excel/",
                    ReportesBovinoViewSet.as_view({"get": "exportar_excel"}),
                    name="exportar-excel",
                ),
            ]
        ),
    ),
    # URLs para gestión de marcas bovinas
    path(
        "marcas/",
        include(
            [
                path(
                    "pendientes/",
                    MarcaGanadoBovinoViewSet.as_view({"get": "marcas_pendientes"}),
                    name="marcas-pendientes",
                ),
                path(
                    "por-procesar/",
                    MarcaGanadoBovinoViewSet.as_view({"get": "marcas_por_procesar"}),
                    name="marcas-procesar",
                ),
                path(
                    "procesadas-hoy/",
                    MarcaGanadoBovinoViewSet.as_view({"get": "marcas_procesadas_hoy"}),
                    name="marcas-hoy",
                ),
                path(
                    "alertas-tiempo/",
                    MarcaGanadoBovinoViewSet.as_view(
                        {"get": "alertas_tiempo_procesamiento"}
                    ),
                    name="marcas-alertas",
                ),
                path(
                    "estadisticas-raza/",
                    MarcaGanadoBovinoViewSet.as_view({"get": "estadisticas_por_raza"}),
                    name="marcas-stats-raza",
                ),
                path(
                    "estadisticas-departamento/",
                    MarcaGanadoBovinoViewSet.as_view(
                        {"get": "estadisticas_por_departamento"}
                    ),
                    name="marcas-stats-dept",
                ),
                path(
                    "procesamiento-masivo/",
                    MarcaGanadoBovinoViewSet.as_view({"post": "procesamiento_masivo"}),
                    name="marcas-masivo",
                ),
                path(
                    "<int:pk>/aprobar/",
                    MarcaGanadoBovinoViewSet.as_view({"post": "aprobar_marca"}),
                    name="aprobar-marca",
                ),
                path(
                    "<int:pk>/rechazar/",
                    MarcaGanadoBovinoViewSet.as_view({"post": "rechazar_marca"}),
                    name="rechazar-marca",
                ),
                path(
                    "<int:pk>/historial/",
                    MarcaGanadoBovinoViewSet.as_view({"get": "ver_historial"}),
                    name="marca-historial",
                ),
            ]
        ),
    ),
    # URLs para gestión de logos bovinos
    path(
        "logos/",
        include(
            [
                path(
                    "pendientes-generacion/",
                    LogoMarcaBovinaViewSet.as_view({"get": "logos_pendientes"}),
                    name="logos-pendientes",
                ),
                path(
                    "fallidos/",
                    LogoMarcaBovinaViewSet.as_view({"get": "logos_fallidos"}),
                    name="logos-fallidos",
                ),
                path(
                    "por-calidad/",
                    LogoMarcaBovinaViewSet.as_view({"get": "logos_por_calidad"}),
                    name="logos-calidad",
                ),
                path(
                    "rendimiento-modelos/",
                    LogoMarcaBovinaViewSet.as_view({"get": "rendimiento_modelos_ia"}),
                    name="logos-rendimiento",
                ),
                path(
                    "analisis-prompts/",
                    LogoMarcaBovinaViewSet.as_view({"get": "analisis_prompts"}),
                    name="logos-prompts",
                ),
                path(
                    "generar-masivo/",
                    LogoMarcaBovinaViewSet.as_view({"post": "generar_logos_masivo"}),
                    name="logos-masivo",
                ),
                path(
                    "evaluar-calidad-masiva/",
                    LogoMarcaBovinaViewSet.as_view({"post": "evaluar_calidad_masiva"}),
                    name="logos-evaluar",
                ),
                path(
                    "<int:pk>/regenerar/",
                    LogoMarcaBovinaViewSet.as_view({"post": "regenerar_logo"}),
                    name="regenerar-logo",
                ),
            ]
        ),
    ),
    # URLs para KPIs bovinos
    path(
        "kpis/",
        include(
            [
                path(
                    "ultimos-12-meses/",
                    KPIGanadoBovinoViewSet.as_view({"get": "ultimos_12_meses"}),
                    name="kpis-12-meses",
                ),
                path(
                    "comparativa-trimestral/",
                    KPIGanadoBovinoViewSet.as_view({"get": "comparativa_trimestral"}),
                    name="kpis-trimestral",
                ),
                path(
                    "analisis-estacional/",
                    KPIGanadoBovinoViewSet.as_view({"get": "analisis_estacional"}),
                    name="kpis-estacional",
                ),
                path(
                    "actuales/",
                    KPIGanadoBovinoViewSet.as_view({"get": "kpis_actuales"}),
                    name="kpis-actuales",
                ),
            ]
        ),
    ),
    # URLs para historial y auditoría
    path(
        "historial/",
        include(
            [
                path(
                    "actividad-reciente/",
                    HistorialEstadoMarcaViewSet.as_view({"get": "actividad_reciente"}),
                    name="historial-reciente",
                ),
                path(
                    "auditoria-usuario/",
                    HistorialEstadoMarcaViewSet.as_view({"get": "auditoria_usuario"}),
                    name="historial-usuario",
                ),
                path(
                    "patrones-cambio/",
                    HistorialEstadoMarcaViewSet.as_view(
                        {"get": "patrones_cambio_estado"}
                    ),
                    name="historial-patrones",
                ),
                path(
                    "eficiencia-evaluadores/",
                    HistorialEstadoMarcaViewSet.as_view(
                        {"get": "eficiencia_evaluadores"}
                    ),
                    name="historial-evaluadores",
                ),
            ]
        ),
    ),
]

# URLs de compatibilidad (mantienen las URLs anteriores funcionando)
compatibility_urls = [
    # Redirecciones para mantener compatibilidad con versiones anteriores
    path(
        "marcas/",
        MarcaGanadoBovinoViewSet.as_view({"get": "list", "post": "create"}),
        name="marcas-compat",
    ),
    path(
        "marcas/<int:pk>/",
        MarcaGanadoBovinoViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="marca-detail-compat",
    ),
    path(
        "logos/",
        LogoMarcaBovinaViewSet.as_view({"get": "list", "post": "create"}),
        name="logos-compat",
    ),
    path(
        "logos/<int:pk>/",
        LogoMarcaBovinaViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="logo-detail-compat",
    ),
    # Dashboard compatibility
    path(
        "dashboard/kpis_principales/",
        DashboardBovinoViewSet.as_view({"get": "kpis_principales"}),
        name="dashboard-kpis-compat",
    ),
    path(
        "dashboard/tendencias_mensuales/",
        DashboardBovinoViewSet.as_view({"get": "tendencias_mensuales"}),
        name="dashboard-tendencias-compat",
    ),
    path(
        "dashboard/metricas_tiempo_real/",
        DashboardBovinoViewSet.as_view({"get": "metricas_tiempo_real"}),
        name="dashboard-tiempo-real-compat",
    ),
]

# Agregar URLs de compatibilidad
urlpatterns += compatibility_urls
