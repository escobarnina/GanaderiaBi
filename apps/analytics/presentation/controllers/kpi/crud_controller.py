"""
Controller para operaciones CRUD de KPIs
Responsabilidad única: Operaciones básicas de KPIs (solo lectura)
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, Any

from apps.analytics.presentation.serializers.kpi_serializers import (
    KPIGanadoBovinoSerializer,
    KPIGanadoBovinoListSerializer,
)
from apps.analytics.infrastructure.container.main_container import Container


class KpiCRUDController:
    """Controller para operaciones CRUD de KPIs"""

    def __init__(self):
        """Inicializa el controller con inyección de dependencias"""
        self.container = Container()

        # Use cases de CRUD
        self.obtener_kpis_use_case = self.container.get_obtener_kpis_use_case()
        self.calcular_kpis_use_case = self.container.get_calcular_kpis_use_case()

    def _build_filters(self, request) -> Dict[str, Any]:
        """Construye filtros a partir de los parámetros de query"""
        filters = {}

        # Filtros de fecha
        if request.query_params.get("fecha_desde"):
            filters["fecha_desde"] = request.query_params.get("fecha_desde")

        if request.query_params.get("fecha_hasta"):
            filters["fecha_hasta"] = request.query_params.get("fecha_hasta")

        # Filtros de tipo KPI
        if request.query_params.get("tipo_kpi"):
            filters["tipo_kpi"] = request.query_params.get("tipo_kpi")

        # Filtros de departamento
        if request.query_params.get("departamento"):
            filters["departamento"] = request.query_params.get("departamento")

        # Ordenamiento
        filters["ordering"] = request.query_params.get("ordering", "-fecha")

        return filters


# ============================================================================
# ENDPOINTS CRUD BÁSICOS
# ============================================================================


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def listar_kpis(request):
    """Lista todos los KPIs con filtros opcionales"""
    try:
        controller = KpiCRUDController()
        filters = controller._build_filters(request)

        # Ejecutar use case
        kpis = controller.obtener_kpis_use_case.execute(filters)

        # Serializar respuesta
        serializer = KPIGanadoBovinoListSerializer()
        data = [serializer.to_representation(kpi) for kpi in kpis]

        return Response(
            {"count": len(data), "results": data, "filters_applied": filters}
        )

    except Exception as e:
        return Response(
            {"error": f"Error al listar KPIs: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def obtener_kpi(request, kpi_id: int):
    """Obtiene un KPI específico por ID"""
    try:
        controller = KpiCRUDController()

        # Ejecutar use case
        kpi = controller.obtener_kpis_use_case.execute({"kpi_id": kpi_id})

        if not kpi:
            return Response(
                {"error": "KPI no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

        # Serializar respuesta
        serializer = KPIGanadoBovinoSerializer()
        data = serializer.to_representation(kpi)

        return Response(data)

    except Exception as e:
        return Response(
            {"error": f"Error al obtener KPI: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def calcular_kpis(request):
    """Calcula KPIs para un período específico"""
    try:
        controller = KpiCRUDController()

        # Validar datos de entrada
        fecha_inicio = request.data.get("fecha_inicio")
        fecha_fin = request.data.get("fecha_fin")

        if not fecha_inicio or not fecha_fin:
            return Response(
                {"error": "fecha_inicio y fecha_fin son requeridos"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Preparar datos para el use case
        data = {
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "tipo_calculo": request.data.get("tipo_calculo", "mensual"),
            "incluir_detalles": request.data.get("incluir_detalles", True),
        }

        # Ejecutar use case
        kpis_calculados = controller.calcular_kpis_use_case.execute(data)

        # Serializar respuesta
        serializer = KPIGanadoBovinoSerializer()
        data = [serializer.to_representation(kpi) for kpi in kpis_calculados]

        return Response(
            {
                "mensaje": f"KPIs calculados para el período {fecha_inicio} a {fecha_fin}",
                "kpis_calculados": data,
                "total_kpis": len(data),
            },
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        return Response(
            {"error": f"Error al calcular KPIs: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
