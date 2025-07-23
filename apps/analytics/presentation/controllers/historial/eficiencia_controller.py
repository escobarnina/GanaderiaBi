"""
Controller para análisis de eficiencia de evaluadores
Responsabilidad única: Análisis de rendimiento de evaluadores
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, Any

from apps.analytics.infrastructure.container.main_container import Container


class HistorialEficienciaController:
    """Controller para análisis de eficiencia de evaluadores"""

    def __init__(self):
        """Inicializa el controller con inyección de dependencias"""
        self.container = Container()

        # Use cases de eficiencia
        self.obtener_eficiencia_evaluadores_use_case = (
            self.container.get_obtener_eficiencia_evaluadores_use_case()
        )


# ============================================================================
# ENDPOINTS DE ANÁLISIS DE EFICIENCIA
# ============================================================================


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def eficiencia_evaluadores(request):
    """Análisis de eficiencia de evaluadores"""
    try:
        controller = HistorialEficienciaController()

        # Obtener parámetros
        dias = int(request.query_params.get("dias", 30))

        # Ejecutar use case para obtener eficiencia
        eficiencia = controller.obtener_eficiencia_evaluadores_use_case.execute(
            {
                "periodo_dias": dias,
                "incluir_ranking": True,
                "incluir_recomendaciones": True,
            }
        )

        return Response(
            {
                "periodo_analisis": f"{dias} días",
                "estadisticas_evaluadores": eficiencia.estadisticas_evaluadores,
                "ranking_eficiencia": eficiencia.ranking_eficiencia,
                "metricas_sistema": eficiencia.metricas_sistema,
                "analisis_comparativo": eficiencia.analisis_comparativo,
                "recomendaciones": eficiencia.recomendaciones,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener eficiencia de evaluadores: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def evaluador_detalle(request, evaluador_id: str):
    """Análisis detallado de un evaluador específico"""
    try:
        controller = HistorialEficienciaController()

        # Obtener parámetros
        dias = int(request.query_params.get("dias", 30))

        # Ejecutar use case para obtener detalle del evaluador
        detalle = controller.obtener_eficiencia_evaluadores_use_case.execute(
            {
                "tipo": "evaluador_detalle",
                "evaluador_id": evaluador_id,
                "periodo_dias": dias,
                "incluir_analisis": True,
            }
        )

        return Response(
            {
                "evaluador": evaluador_id,
                "periodo_analisis": f"{dias} días",
                "metricas_personales": detalle.metricas_personales,
                "tendencia_rendimiento": detalle.tendencia_rendimiento,
                "patrones_trabajo": detalle.patrones_trabajo,
                "casos_destacados": detalle.casos_destacados,
                "areas_mejora": detalle.areas_mejora,
                "recomendaciones_personalizadas": detalle.recomendaciones_personalizadas,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener detalle del evaluador: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def comparativa_evaluadores(request):
    """Comparativa entre evaluadores"""
    try:
        controller = HistorialEficienciaController()

        # Obtener parámetros
        dias = int(request.query_params.get("dias", 30))
        evaluadores = request.query_params.getlist("evaluadores", [])

        # Ejecutar use case para comparativa
        comparativa = controller.obtener_eficiencia_evaluadores_use_case.execute(
            {
                "tipo": "comparativa",
                "periodo_dias": dias,
                "evaluadores": evaluadores,
                "incluir_analisis": True,
            }
        )

        return Response(
            {
                "periodo_analisis": f"{dias} días",
                "evaluadores_comparados": comparativa.evaluadores_comparados,
                "metricas_comparativas": comparativa.metricas_comparativas,
                "diferencias_clave": comparativa.diferencias_clave,
                "mejores_practicas": comparativa.mejores_practicas,
                "oportunidades_mejora": comparativa.oportunidades_mejora,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener comparativa de evaluadores: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
