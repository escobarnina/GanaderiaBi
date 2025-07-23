"""
Controller para análisis de patrones de cambio de estado
Responsabilidad única: Análisis de patrones y flujos
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, Any

from apps.analytics.infrastructure.container.main_container import Container


class HistorialPatronesController:
    """Controller para análisis de patrones de cambio"""

    def __init__(self):
        """Inicializa el controller con inyección de dependencias"""
        self.container = Container()

        # Use cases de patrones
        self.obtener_patrones_cambio_use_case = (
            self.container.get_obtener_patrones_cambio_use_case()
        )


# ============================================================================
# ENDPOINTS DE ANÁLISIS DE PATRONES
# ============================================================================


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def patrones_cambio_estado(request):
    """Análisis de patrones en cambios de estado"""
    try:
        controller = HistorialPatronesController()

        # Obtener parámetros
        dias = int(request.query_params.get("dias", 90))

        # Ejecutar use case para obtener patrones
        patrones = controller.obtener_patrones_cambio_use_case.execute(
            {"periodo_dias": dias, "incluir_analisis": True}
        )

        return Response(
            {
                "periodo_analisis": f"{dias} días",
                "flujos_mas_comunes": patrones.flujos_mas_comunes,
                "patrones_temporales": {
                    "actividad_por_hora": patrones.actividad_por_hora,
                    "actividad_por_dia_semana": patrones.actividad_por_dia_semana,
                    "hora_mas_activa": patrones.hora_mas_activa,
                    "dia_mas_activo": patrones.dia_mas_activo,
                },
                "reversiones_detectadas": patrones.reversiones_detectadas,
                "tiempos_entre_cambios": patrones.tiempos_entre_cambios,
                "productividad_temporal": patrones.productividad_temporal,
                "insights": patrones.insights,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener patrones de cambio: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def analisis_flujos_estado(request):
    """Análisis detallado de flujos de estado"""
    try:
        controller = HistorialPatronesController()

        # Obtener parámetros
        dias = int(request.query_params.get("dias", 30))
        estado_inicial = request.query_params.get("estado_inicial")

        # Ejecutar use case para análisis de flujos
        flujos = controller.obtener_patrones_cambio_use_case.execute(
            {
                "tipo": "analisis_flujos",
                "periodo_dias": dias,
                "estado_inicial": estado_inicial,
                "incluir_estadisticas": True,
            }
        )

        return Response(
            {
                "periodo_analisis": f"{dias} días",
                "estado_inicial": estado_inicial,
                "flujos_posibles": flujos.flujos_posibles,
                "tiempos_promedio": flujos.tiempos_promedio,
                "probabilidades_transicion": flujos.probabilidades_transicion,
                "flujos_anomalos": flujos.flujos_anomalos,
                "recomendaciones_optimizacion": flujos.recomendaciones_optimizacion,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener análisis de flujos: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
