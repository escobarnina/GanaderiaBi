"""
Controller para operaciones CRUD de historial
Responsabilidad única: Operaciones básicas de consulta de historial
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, Any

from apps.analytics.presentation.serializers.historial_serializers import (
    HistorialEstadoMarcaSerializer,
    HistorialEstadoMarcaListSerializer,
)
from apps.analytics.infrastructure.container.main_container import Container


class HistorialCRUDController:
    """Controller para operaciones CRUD de historial"""

    def __init__(self):
        """Inicializa el controller con inyección de dependencias"""
        self.container = Container()

        # Use cases de CRUD
        self.obtener_historial_use_case = (
            self.container.get_obtener_historial_use_case()
        )
        self.listar_historial_marca_use_case = (
            self.container.get_listar_historial_marca_use_case()
        )

    def _build_filters(self, request) -> Dict[str, Any]:
        """Construye filtros a partir de los parámetros de query"""
        filters = {}

        # Filtros de marca
        if request.query_params.get("marca_id"):
            filters["marca_id"] = request.query_params.get("marca_id")

        if request.query_params.get("numero_marca"):
            filters["numero_marca"] = request.query_params.get("numero_marca")

        # Filtros de usuario
        if request.query_params.get("usuario_responsable"):
            filters["usuario_responsable"] = request.query_params.get(
                "usuario_responsable"
            )

        # Filtros de estado
        if request.query_params.get("estado_nuevo"):
            filters["estado_nuevo"] = request.query_params.get("estado_nuevo")

        if request.query_params.get("estado_anterior"):
            filters["estado_anterior"] = request.query_params.get("estado_anterior")

        # Filtros de fecha
        if request.query_params.get("fecha_desde"):
            filters["fecha_desde"] = request.query_params.get("fecha_desde")

        if request.query_params.get("fecha_hasta"):
            filters["fecha_hasta"] = request.query_params.get("fecha_hasta")

        # Ordenamiento
        filters["ordering"] = request.query_params.get("ordering", "-fecha_cambio")

        return filters


# ============================================================================
# ENDPOINTS CRUD BÁSICOS
# ============================================================================


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def listar_historial(request):
    """Lista todo el historial con filtros opcionales"""
    try:
        controller = HistorialCRUDController()
        filters = controller._build_filters(request)

        # Ejecutar use case
        historial = controller.obtener_historial_use_case.execute(filters)

        # Serializar respuesta
        serializer = HistorialEstadoMarcaListSerializer()
        data = [serializer.to_representation(registro) for registro in historial]

        return Response(
            {"count": len(data), "results": data, "filters_applied": filters}
        )

    except Exception as e:
        return Response(
            {"error": f"Error al listar historial: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def obtener_historial(request, historial_id: int):
    """Obtiene un registro específico del historial por ID"""
    try:
        controller = HistorialCRUDController()

        # Ejecutar use case
        historial = controller.obtener_historial_use_case.execute(
            {"historial_id": historial_id}
        )

        if not historial:
            return Response(
                {"error": "Registro de historial no encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Serializar respuesta
        serializer = HistorialEstadoMarcaSerializer()
        data = serializer.to_representation(historial)

        return Response(data)

    except Exception as e:
        return Response(
            {"error": f"Error al obtener historial: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def historial_por_marca(request, marca_id: int):
    """Obtiene el historial completo de una marca específica"""
    try:
        controller = HistorialCRUDController()

        # Ejecutar use case
        historial_marca = controller.listar_historial_marca_use_case.execute(
            {"marca_id": marca_id, "incluir_detalles": True}
        )

        # Serializar respuesta
        serializer = HistorialEstadoMarcaSerializer()
        data = [serializer.to_representation(registro) for registro in historial_marca]

        return Response(
            {
                "marca_id": marca_id,
                "total_registros": len(data),
                "historial": data,
                "resumen": {
                    "primer_cambio": data[0]["fecha_cambio"] if data else None,
                    "ultimo_cambio": data[-1]["fecha_cambio"] if data else None,
                    "estados_recorridos": list(
                        set(registro["estado_nuevo"] for registro in data)
                    ),
                    "usuarios_involucrados": list(
                        set(registro["usuario_responsable"] for registro in data)
                    ),
                },
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener historial de marca: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
