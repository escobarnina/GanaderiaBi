"""
Controller para tendencias mensuales del dashboard
Responsabilidad única: Análisis de tendencias temporales
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, Any

from apps.analytics.presentation.serializers.dashboard_serializers import (
    EstadisticasMensualesBovinoSerializer,
)
from apps.analytics.infrastructure.container.main_container import Container


class DashboardTendenciasController:
    """Controller para tendencias mensuales del dashboard"""

    def __init__(self):
        """Inicializa el controller con inyección de dependencias"""
        self.container = Container()

        # Use cases de tendencias
        self.obtener_dashboard_data_use_case = (
            self.container.get_obtener_dashboard_data_use_case()
        )


# ============================================================================
# ENDPOINTS DE TENDENCIAS
# ============================================================================


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def tendencias_mensuales(request):
    """Tendencias de los últimos 12 meses para ganado bovino"""
    try:
        controller = DashboardTendenciasController()

        # Ejecutar use case para obtener tendencias mensuales
        tendencias = controller.obtener_dashboard_data_use_case.execute(
            {
                "tipo": "tendencias_mensuales",
                "periodo_meses": 12,
                "incluir_departamentos": True,
            }
        )

        # Serializar respuesta
        serializer = EstadisticasMensualesBovinoSerializer()
        data = [serializer.to_representation(tendencia) for tendencia in tendencias]

        return Response(data)

    except Exception as e:
        return Response(
            {"error": f"Error al obtener tendencias mensuales: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def analisis_tendencias(request):
    """Análisis profundo de tendencias con insights"""
    try:
        controller = DashboardTendenciasController()

        # Ejecutar use case para análisis de tendencias
        analisis = controller.obtener_dashboard_data_use_case.execute(
            {
                "tipo": "analisis_tendencias",
                "periodo_meses": 12,
                "incluir_insights": True,
            }
        )

        return Response(
            {
                "periodo_analisis": analisis.periodo_analisis,
                "tendencias_principales": analisis.tendencias_principales,
                "puntos_inflexion": analisis.puntos_inflexion,
                "predicciones": analisis.predicciones,
                "recomendaciones": analisis.recomendaciones,
                "departamentos_crecimiento": analisis.departamentos_crecimiento,
                "departamentos_decrecimiento": analisis.departamentos_decrecimiento,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener análisis de tendencias: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
