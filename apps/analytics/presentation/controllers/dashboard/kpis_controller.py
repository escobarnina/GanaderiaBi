"""
Controller para KPIs principales del dashboard
Responsabilidad única: Métricas clave del dashboard principal
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, Any

from apps.analytics.presentation.serializers.dashboard_serializers import (
    DashboardKPIBovinoSerializer,
)
from apps.analytics.infrastructure.container.main_container import Container


class DashboardKPIsController:
    """Controller para KPIs principales del dashboard"""

    def __init__(self):
        """Inicializa el controller con inyección de dependencias"""
        self.container = Container()

        # Use cases de dashboard
        self.obtener_dashboard_data_use_case = (
            self.container.get_obtener_dashboard_data_use_case()
        )


# ============================================================================
# ENDPOINTS DE KPIs PRINCIPALES
# ============================================================================


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def kpis_principales(request):
    """KPIs principales para el dashboard de ganado bovino"""
    try:
        controller = DashboardKPIsController()

        # Ejecutar use case para obtener KPIs principales
        dashboard_data = controller.obtener_dashboard_data_use_case.execute(
            {"tipo": "kpis_principales", "incluir_alertas": True}
        )

        # Serializar respuesta
        serializer = DashboardKPIBovinoSerializer()
        data = serializer.to_representation(dashboard_data)

        return Response(data)

    except Exception as e:
        return Response(
            {"error": f"Error al obtener KPIs principales: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def metricas_tiempo_real(request):
    """Métricas en tiempo real para actualizar el dashboard"""
    try:
        controller = DashboardKPIsController()

        # Ejecutar use case para obtener métricas en tiempo real
        metricas_realtime = controller.obtener_dashboard_data_use_case.execute(
            {"tipo": "metricas_tiempo_real", "incluir_estado_sistema": True}
        )

        return Response(
            {
                "fecha": metricas_realtime.fecha,
                "timestamp": metricas_realtime.timestamp,
                "registros_hoy": metricas_realtime.registros_hoy,
                "cabezas_registradas_hoy": metricas_realtime.cabezas_registradas_hoy,
                "procesadas_hoy": metricas_realtime.procesadas_hoy,
                "logos_generados_hoy": metricas_realtime.logos_generados_hoy,
                "ingresos_hoy": metricas_realtime.ingresos_hoy,
                "distribucion_propositos_hoy": metricas_realtime.distribucion_propositos_hoy,
                "estado_sistema": metricas_realtime.estado_sistema,
                "marcas_en_cola": metricas_realtime.marcas_en_cola,
                "velocidad_procesamiento": metricas_realtime.velocidad_procesamiento,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener métricas en tiempo real: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
