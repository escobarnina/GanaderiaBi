"""
Controller para reportes comparativos
Responsabilidad única: Análisis comparativo entre departamentos
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, Any

from apps.analytics.infrastructure.container.main_container import Container


class ReporteComparativoController:
    """Controller para reportes comparativos"""

    def __init__(self):
        """Inicializa el controller con inyección de dependencias"""
        self.container = Container()

        # Use cases de reportes comparativos
        self.generar_reporte_comparativo_departamentos_use_case = (
            self.container.get_generar_reporte_comparativo_departamentos_use_case()
        )


# ============================================================================
# ENDPOINTS DE REPORTES COMPARATIVOS
# ============================================================================


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def reporte_comparativo_departamentos(request):
    """Reporte comparativo entre departamentos"""
    try:
        controller = ReporteComparativoController()

        # Obtener parámetros
        año = int(request.query_params.get("año", 0))
        mes = int(request.query_params.get("mes", 0))

        if not año:
            return Response(
                {"error": "Parámetro año es requerido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ejecutar use case para generar reporte comparativo
        reporte = controller.generar_reporte_comparativo_departamentos_use_case.execute(
            {
                "año": año,
                "mes": mes,
                "incluir_analisis": True,
                "incluir_recomendaciones": True,
            }
        )

        return Response(
            {
                "periodo": f"{mes}/{año}" if mes else f"{año}",
                "fecha_generacion": reporte.fecha_generacion,
                "analisis_departamental": {
                    "departamentos_analizados": reporte.departamentos_analizados,
                    "ranking_competitividad": reporte.ranking_competitividad,
                    "brechas_departamentales": reporte.brechas_departamentales,
                    "oportunidades_nivelacion": reporte.oportunidades_nivelacion,
                },
                "analisis_razas": {
                    "distribucion_razas": reporte.distribucion_razas,
                    "especializacion_departamental": reporte.especializacion_departamental,
                    "diversidad_genetica": reporte.diversidad_genetica,
                },
                "analisis_propositos": {
                    "distribucion_propositos": reporte.distribucion_propositos,
                    "especializacion_geografica": reporte.especializacion_geografica,
                },
                "metricas_competitividad": reporte.metricas_competitividad,
                "recomendaciones_politicas": reporte.recomendaciones_politicas,
                "insights_estrategicos": reporte.insights_estrategicos,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al generar reporte comparativo: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def analisis_competitividad_departamental(request):
    """Análisis detallado de competitividad por departamento"""
    try:
        controller = ReporteComparativoController()

        # Obtener parámetros
        departamento = request.query_params.get("departamento", "")
        año = int(request.query_params.get("año", 0))

        if not departamento or not año:
            return Response(
                {"error": "Parámetros departamento y año son requeridos"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ejecutar use case para análisis de competitividad
        analisis = (
            controller.generar_reporte_comparativo_departamentos_use_case.execute(
                {
                    "tipo": "analisis_competitividad",
                    "departamento": departamento,
                    "año": año,
                    "incluir_analisis": True,
                }
            )
        )

        return Response(
            {
                "departamento": departamento,
                "año": año,
                "score_competitividad": analisis.score_competitividad,
                "clasificacion": analisis.clasificacion,
                "fortalezas": analisis.fortalezas,
                "areas_mejora": analisis.areas_mejora,
                "posicion_ranking": analisis.posicion_ranking,
                "comparacion_nacional": analisis.comparacion_nacional,
                "recomendaciones_especificas": analisis.recomendaciones_especificas,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener análisis de competitividad: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
