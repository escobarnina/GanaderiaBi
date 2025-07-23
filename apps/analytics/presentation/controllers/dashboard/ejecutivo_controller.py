"""
Controller para resumen ejecutivo del dashboard
Responsabilidad única: Análisis para alta dirección
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, Any

from apps.analytics.infrastructure.container.main_container import Container


class DashboardEjecutivoController:
    """Controller para resumen ejecutivo del dashboard"""

    def __init__(self):
        """Inicializa el controller con inyección de dependencias"""
        self.container = Container()

        # Use cases de resumen ejecutivo
        self.obtener_dashboard_data_use_case = (
            self.container.get_obtener_dashboard_data_use_case()
        )
        self.generar_reporte_dashboard_use_case = (
            self.container.get_generar_reporte_dashboard_use_case()
        )


# ============================================================================
# ENDPOINTS DE RESUMEN EJECUTIVO
# ============================================================================


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def resumen_ejecutivo(request):
    """Resumen ejecutivo para la alta dirección"""
    try:
        controller = DashboardEjecutivoController()

        # Ejecutar use case para obtener resumen ejecutivo
        resumen = controller.obtener_dashboard_data_use_case.execute(
            {
                "tipo": "resumen_ejecutivo",
                "periodo_dias": 30,
                "incluir_predicciones": True,
                "incluir_recomendaciones": True,
            }
        )

        return Response(
            {
                "periodo_analisis": resumen.periodo_analisis,
                "fecha_generacion": resumen.fecha_generacion,
                "metricas_clave": {
                    "marcas_registradas": resumen.marcas_registradas,
                    "cabezas_bovinas": resumen.cabezas_bovinas,
                    "crecimiento_vs_mes_anterior": resumen.crecimiento_vs_mes_anterior,
                    "eficiencia_promedio_sistema": resumen.eficiencia_promedio_sistema,
                },
                "region_mas_eficiente": {
                    "departamento": resumen.region_mas_eficiente.departamento,
                    "score_eficiencia": resumen.region_mas_eficiente.score_eficiencia,
                    "tasa_aprobacion": resumen.region_mas_eficiente.tasa_aprobacion,
                },
                "predicciones_proximo_mes": {
                    "marcas_estimadas": resumen.predicciones.marcas_estimadas,
                    "cabezas_estimadas": resumen.predicciones.cabezas_estimadas,
                    "ingresos_estimados": resumen.predicciones.ingresos_estimados,
                    "confianza_prediccion": resumen.predicciones.confianza_prediccion,
                },
                "top_departamentos_ganaderos": resumen.top_departamentos_ganaderos,
                "rendimiento_tecnologia": {
                    "logos_generados": resumen.rendimiento_tecnologia.logos_generados,
                    "tasa_exito_ia": resumen.rendimiento_tecnologia.tasa_exito_ia,
                    "estado": resumen.rendimiento_tecnologia.estado,
                },
                "recomendaciones": resumen.recomendaciones,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener resumen ejecutivo: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generar_reporte_ejecutivo(request):
    """Genera reporte ejecutivo personalizado"""
    try:
        controller = DashboardEjecutivoController()

        # Validar parámetros de entrada
        periodo_dias = request.data.get("periodo_dias", 30)
        incluir_predicciones = request.data.get("incluir_predicciones", True)
        formato_reporte = request.data.get("formato_reporte", "json")

        # Ejecutar use case para generar reporte
        reporte = controller.generar_reporte_dashboard_use_case.execute(
            {
                "tipo": "reporte_ejecutivo",
                "periodo_dias": periodo_dias,
                "incluir_predicciones": incluir_predicciones,
                "formato": formato_reporte,
                "incluir_graficos": request.data.get("incluir_graficos", True),
                "incluir_alertas": request.data.get("incluir_alertas", True),
            }
        )

        return Response(
            {
                "mensaje": f"Reporte ejecutivo generado para {periodo_dias} días",
                "reporte": reporte.contenido,
                "formato": reporte.formato,
                "fecha_generacion": reporte.fecha_generacion,
                "tamaño_bytes": reporte.tamaño_bytes,
            },
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        return Response(
            {"error": f"Error al generar reporte ejecutivo: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def metricas_eficiencia_regional(request):
    """Métricas de eficiencia por región"""
    try:
        controller = DashboardEjecutivoController()

        # Ejecutar use case para obtener métricas de eficiencia
        eficiencia = controller.obtener_dashboard_data_use_case.execute(
            {"tipo": "eficiencia_regional", "incluir_ranking": True}
        )

        return Response(
            {
                "ranking_eficiencia": eficiencia.ranking_eficiencia,
                "promedio_eficiencia": eficiencia.promedio_eficiencia,
                "region_mas_eficiente": eficiencia.region_mas_eficiente,
                "region_menos_eficiente": eficiencia.region_menos_eficiente,
                "factores_eficiencia": eficiencia.factores_eficiencia,
                "recomendaciones_mejora": eficiencia.recomendaciones_mejora,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener métricas de eficiencia: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
