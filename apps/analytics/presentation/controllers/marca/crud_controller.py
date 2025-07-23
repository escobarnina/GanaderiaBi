"""
Controller para operaciones CRUD de marcas
Responsabilidad única: Operaciones básicas de marcas
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, Any

from apps.analytics.presentation.serializers.marca_serializers import (
    MarcaGanadoBovinoSerializer,
    MarcaGanadoBovinoListSerializer,
)
from apps.analytics.infrastructure.container.main_container import Container


class MarcaCRUDController:
    """Controller para operaciones CRUD de marcas"""

    def __init__(self):
        """Inicializa el controller con inyección de dependencias"""
        self.container = Container()

        # Use cases de CRUD
        self.crear_marca_use_case = self.container.get_crear_marca_use_case()
        self.obtener_marca_use_case = self.container.get_obtener_marca_use_case()
        self.actualizar_marca_use_case = self.container.get_actualizar_marca_use_case()
        self.eliminar_marca_use_case = self.container.get_eliminar_marca_use_case()
        self.listar_marcas_use_case = self.container.get_listar_marcas_use_case()

    def _get_user_info(self, request) -> Dict[str, str]:
        """Obtiene información del usuario autenticado"""
        if request.user.is_authenticated:
            return {
                "username": request.user.username,
                "user_id": request.user.id,
            }
        return {
            "username": "anonimo",
            "user_id": None,
        }

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
# ENDPOINTS CRUD BÁSICOS
# ============================================================================


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def listar_marcas(request):
    """Lista todas las marcas con filtros opcionales"""
    try:
        controller = MarcaCRUDController()
        filters = controller._build_filters(request)

        # Ejecutar use case
        marcas = controller.listar_marcas_use_case.execute(filters)

        # Serializar respuesta
        serializer = MarcaGanadoBovinoListSerializer()
        data = [serializer.to_representation(marca) for marca in marcas]

        return Response(
            {"count": len(data), "results": data, "filters_applied": filters}
        )

    except Exception as e:
        return Response(
            {"error": f"Error al listar marcas: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def obtener_marca(request, marca_id: int):
    """Obtiene una marca específica por ID"""
    try:
        controller = MarcaCRUDController()

        # Ejecutar use case
        marca = controller.obtener_marca_use_case.execute(marca_id)

        if not marca:
            return Response(
                {"error": "Marca no encontrada"}, status=status.HTTP_404_NOT_FOUND
            )

        # Serializar respuesta
        serializer = MarcaGanadoBovinoSerializer()
        data = serializer.to_representation(marca)

        return Response(data)

    except Exception as e:
        return Response(
            {"error": f"Error al obtener marca: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def crear_marca(request):
    """Crea una nueva marca"""
    try:
        controller = MarcaCRUDController()
        user_info = controller._get_user_info(request)

        # Validar datos de entrada
        serializer = MarcaGanadoBovinoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Agregar información del usuario
        data = serializer.validated_data
        data["creado_por"] = user_info["username"]

        # Ejecutar use case
        marca = controller.crear_marca_use_case.execute(data)

        # Serializar respuesta
        response_serializer = MarcaGanadoBovinoSerializer()
        data = response_serializer.to_representation(marca)

        return Response(data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {"error": f"Error al crear marca: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def actualizar_marca(request, marca_id: int):
    """Actualiza una marca existente"""
    try:
        controller = MarcaCRUDController()
        user_info = controller._get_user_info(request)

        # Validar datos de entrada
        serializer = MarcaGanadoBovinoSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Agregar información del usuario
        data = serializer.validated_data
        data["actualizado_por"] = user_info["username"]

        # Ejecutar use case
        marca = controller.actualizar_marca_use_case.execute(marca_id, data)

        if not marca:
            return Response(
                {"error": "Marca no encontrada"}, status=status.HTTP_404_NOT_FOUND
            )

        # Serializar respuesta
        response_serializer = MarcaGanadoBovinoSerializer()
        data = response_serializer.to_representation(marca)

        return Response(data)

    except Exception as e:
        return Response(
            {"error": f"Error al actualizar marca: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def eliminar_marca(request, marca_id: int):
    """Elimina una marca"""
    try:
        controller = MarcaCRUDController()

        # Ejecutar use case
        success = controller.eliminar_marca_use_case.execute(marca_id)

        if not success:
            return Response(
                {"error": "Marca no encontrada"}, status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {"mensaje": "Marca eliminada exitosamente"},
            status=status.HTTP_204_NO_CONTENT,
        )

    except Exception as e:
        return Response(
            {"error": f"Error al eliminar marca: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
