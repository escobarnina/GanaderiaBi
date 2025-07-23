"""
Controller para análisis de estadísticas por categorías
Responsabilidad única: Análisis estadístico por raza, departamento y propósito
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, Any

from apps.analytics.infrastructure.container.main_container import Container


class EstadisticasAnalisisController:
    """Controller para análisis de estadísticas"""

    def __init__(self):
        """Inicializa el controller con inyección de dependencias"""
        self.container = Container()

        # Use cases de análisis de estadísticas
        self.obtener_estadisticas_marcas_use_case = (
            self.container.get_obtener_estadisticas_marcas_use_case()
        )
        self.obtener_estadisticas_logos_use_case = (
            self.container.get_obtener_estadisticas_logos_use_case()
        )


# ============================================================================
# ENDPOINTS DE ANÁLISIS DE ESTADÍSTICAS
# ============================================================================


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def estadisticas_por_raza(request):
    """Estadísticas detalladas por raza bovina"""
    try:
        controller = EstadisticasAnalisisController()

        # Obtener parámetros
        año = int(request.query_params.get("año", 0))

        # Ejecutar use case para obtener estadísticas por raza
        estadisticas = controller.obtener_estadisticas_marcas_use_case.execute(
            {"tipo": "por_raza", "año": año, "incluir_insights": True}
        )

        return Response(
            {
                "año": año,
                "estadisticas_razas": estadisticas.estadisticas_razas,
                "insights_razas": estadisticas.insights_razas,
                "eficiencia_razas": estadisticas.eficiencia_razas,
                "analisis_regiones": estadisticas.analisis_regiones,
                "mapa_ganadero": estadisticas.mapa_ganadero,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener estadísticas por raza: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def estadisticas_por_departamento(request):
    """Estadísticas detalladas por departamento"""
    try:
        controller = EstadisticasAnalisisController()

        # Obtener parámetros
        año = int(request.query_params.get("año", 0))

        # Ejecutar use case para obtener estadísticas por departamento
        estadisticas = controller.obtener_estadisticas_marcas_use_case.execute(
            {"tipo": "por_departamento", "año": año, "incluir_analisis": True}
        )

        return Response(
            {
                "año": año,
                "estadisticas_departamentos": estadisticas.estadisticas_departamentos,
                "mapa_ganadero": estadisticas.mapa_ganadero,
                "corredores_ganaderos": estadisticas.corredores_ganaderos,
                "concentracion_mercado": estadisticas.concentracion_mercado,
                "diversificacion_geografica": estadisticas.diversificacion_geografica,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener estadísticas por departamento: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def estadisticas_por_proposito(request):
    """Estadísticas detalladas por propósito ganadero"""
    try:
        controller = EstadisticasAnalisisController()

        # Obtener parámetros
        año = int(request.query_params.get("año", 0))

        # Ejecutar use case para obtener estadísticas por propósito
        estadisticas = controller.obtener_estadisticas_marcas_use_case.execute(
            {"tipo": "por_proposito", "año": año, "incluir_analisis": True}
        )

        return Response(
            {
                "año": año,
                "estadisticas_propositos": estadisticas.estadisticas_propositos,
                "economia_por_proposito": estadisticas.economia_por_proposito,
                "insights_proposito": estadisticas.insights_proposito,
                "matriz_proposito_departamento": estadisticas.matriz_proposito_departamento,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener estadísticas por propósito: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
