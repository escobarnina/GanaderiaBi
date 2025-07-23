"""
Controller para análisis de tecnología e IA
Responsabilidad única: Análisis de rendimiento tecnológico
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, Any

from apps.analytics.infrastructure.container.main_container import Container


class EstadisticasTecnologiaController:
    """Controller para análisis de tecnología"""

    def __init__(self):
        """Inicializa el controller con inyección de dependencias"""
        self.container = Container()

        # Use cases de tecnología
        self.obtener_estadisticas_logos_use_case = (
            self.container.get_obtener_estadisticas_logos_use_case()
        )


# ============================================================================
# ENDPOINTS DE ANÁLISIS DE TECNOLOGÍA
# ============================================================================


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def rendimiento_modelos_ia(request):
    """Análisis de rendimiento de modelos de IA"""
    try:
        controller = EstadisticasTecnologiaController()

        # Obtener parámetros
        año = int(request.query_params.get("año", 0))

        # Ejecutar use case para obtener rendimiento de IA
        rendimiento = controller.obtener_estadisticas_logos_use_case.execute(
            {"tipo": "rendimiento_ia", "año": año, "incluir_analisis": True}
        )

        return Response(
            {
                "año": año,
                "tendencias_ia": rendimiento.tendencias_ia,
                "recomendaciones_ia": rendimiento.recomendaciones_ia,
                "correlaciones_marca_logo": rendimiento.correlaciones_marca_logo,
                "analisis_tamaño_operacion": rendimiento.analisis_tamaño_operacion,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener rendimiento de modelos IA: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def analisis_eficiencia(request):
    """Análisis de eficiencia del sistema"""
    try:
        controller = EstadisticasTecnologiaController()

        # Obtener parámetros
        periodo_dias = int(request.query_params.get("periodo_dias", 30))

        # Ejecutar use case para obtener análisis de eficiencia
        eficiencia = controller.obtener_estadisticas_logos_use_case.execute(
            {
                "tipo": "analisis_eficiencia",
                "periodo_dias": periodo_dias,
                "incluir_analisis": True,
            }
        )

        return Response(
            {
                "periodo_analisis": f"{periodo_dias} días",
                "metricas_eficiencia": eficiencia.metricas_eficiencia,
                "tendencias_rendimiento": eficiencia.tendencias_rendimiento,
                "optimizaciones_recomendadas": eficiencia.optimizaciones_recomendadas,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener análisis de eficiencia: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def distribucion_razas(request):
    """Distribución detallada de razas bovinas"""
    try:
        controller = EstadisticasTecnologiaController()

        # Obtener parámetros
        año = int(request.query_params.get("año", 0))

        # Ejecutar use case para obtener distribución de razas
        distribucion = controller.obtener_estadisticas_logos_use_case.execute(
            {"tipo": "distribucion_razas", "año": año, "incluir_analisis": True}
        )

        return Response(
            {
                "año": año,
                "distribucion_razas": distribucion.distribucion_razas,
                "mapa_razas_departamentos": distribucion.mapa_razas_departamentos,
                "recomendaciones_diversificacion": distribucion.recomendaciones_diversificacion,
                "tendencias_razas": distribucion.tendencias_razas,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener distribución de razas: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
