"""
Controller para estadísticas de marcas
Responsabilidad única: Estadísticas y reportes de marcas
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, Any

from apps.analytics.presentation.serializers.dashboard_serializers import (
    EstadisticasPorRazaSerializer,
    EstadisticasPorDepartamentoSerializer,
)
from apps.analytics.infrastructure.container.main_container import Container


class MarcaEstadisticasController:
    """Controller para estadísticas de marcas"""

    def __init__(self):
        """Inicializa el controller con inyección de dependencias"""
        self.container = Container()

        # Use cases de estadísticas
        self.obtener_estadisticas_marcas_use_case = (
            self.container.get_obtener_estadisticas_marcas_use_case()
        )

    def _build_filters(self, request) -> Dict[str, Any]:
        """Construye filtros a partir de los parámetros de query"""
        filters = {}

        # Filtros básicos
        if request.query_params.get("raza_bovino"):
            filters["raza_bovino"] = request.query_params.get("raza_bovino")

        if request.query_params.get("proposito_ganado"):
            filters["proposito_ganado"] = request.query_params.get("proposito_ganado")

        if request.query_params.get("departamento"):
            filters["departamento"] = request.query_params.get("departamento")

        if request.query_params.get("estado"):
            filters["estado"] = request.query_params.get("estado")

        # Filtros de rango
        if request.query_params.get("cabezas_min"):
            filters["cabezas_min"] = int(request.query_params.get("cabezas_min"))

        if request.query_params.get("cabezas_max"):
            filters["cabezas_max"] = int(request.query_params.get("cabezas_max"))

        if request.query_params.get("fecha_desde"):
            filters["fecha_desde"] = request.query_params.get("fecha_desde")

        if request.query_params.get("fecha_hasta"):
            filters["fecha_hasta"] = request.query_params.get("fecha_hasta")

        if request.query_params.get("productor"):
            filters["productor"] = request.query_params.get("productor")

        # Ordenamiento
        filters["ordering"] = request.query_params.get("ordering", "-fecha_registro")

        return filters


# ============================================================================
# ENDPOINTS DE ESTADÍSTICAS
# ============================================================================


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def estadisticas_por_raza(request):
    """Estadísticas agrupadas por raza bovina"""
    try:
        controller = MarcaEstadisticasController()

        # Ejecutar use case
        estadisticas = controller.obtener_estadisticas_marcas_use_case.execute(
            {"tipo": "por_raza", "filters": controller._build_filters(request)}
        )

        # Serializar respuesta
        serializer = EstadisticasPorRazaSerializer()
        data = [serializer.to_representation(stat) for stat in estadisticas]

        return Response(data)

    except Exception as e:
        return Response(
            {"error": f"Error al obtener estadísticas por raza: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def estadisticas_por_departamento(request):
    """Estadísticas agrupadas por departamento"""
    try:
        controller = MarcaEstadisticasController()

        # Ejecutar use case
        estadisticas = controller.obtener_estadisticas_marcas_use_case.execute(
            {"tipo": "por_departamento", "filters": controller._build_filters(request)}
        )

        # Serializar respuesta
        serializer = EstadisticasPorDepartamentoSerializer()
        data = [serializer.to_representation(stat) for stat in estadisticas]

        return Response(data)

    except Exception as e:
        return Response(
            {"error": f"Error al obtener estadísticas por departamento: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
