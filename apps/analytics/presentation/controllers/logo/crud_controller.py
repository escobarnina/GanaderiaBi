"""
Controller para operaciones CRUD de logos
Responsabilidad única: Operaciones básicas de logos
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, Any

from apps.analytics.presentation.serializers.logo_serializers import (
    LogoMarcaBovinaSerializer,
    LogoMarcaBovinaListSerializer,
)
from apps.analytics.infrastructure.container.main_container import Container


class LogoCRUDController:
    """Controller para operaciones CRUD de logos"""

    def __init__(self):
        """Inicializa el controller con inyección de dependencias"""
        self.container = Container()

        # Use cases de CRUD
        self.generar_logo_use_case = self.container.get_generar_logo_use_case()
        self.obtener_logo_use_case = self.container.get_obtener_logo_use_case()
        self.listar_logos_use_case = self.container.get_listar_logos_use_case()

    def _build_filters(self, request) -> Dict[str, Any]:
        """Construye filtros a partir de los parámetros de query"""
        filters = {}

        # Filtros básicos
        if request.query_params.get("modelo_ia"):
            filters["modelo_ia"] = request.query_params.get("modelo_ia")

        if request.query_params.get("exito"):
            filters["exito"] = request.query_params.get("exito").lower() == "true"

        if request.query_params.get("calidad"):
            filters["calidad"] = request.query_params.get("calidad")

        # Filtros por marca
        if request.query_params.get("marca_numero"):
            filters["marca_numero"] = request.query_params.get("marca_numero")

        if request.query_params.get("raza_bovino"):
            filters["raza_bovino"] = request.query_params.get("raza_bovino")

        if request.query_params.get("departamento"):
            filters["departamento"] = request.query_params.get("departamento")

        # Ordenamiento
        filters["ordering"] = request.query_params.get("ordering", "-fecha_generacion")

        return filters


# ============================================================================
# ENDPOINTS CRUD BÁSICOS
# ============================================================================


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def listar_logos(request):
    """Lista todos los logos con filtros opcionales"""
    try:
        controller = LogoCRUDController()
        filters = controller._build_filters(request)

        # Ejecutar use case
        logos = controller.listar_logos_use_case.execute(filters)

        # Serializar respuesta
        serializer = LogoMarcaBovinaListSerializer()
        data = [serializer.to_representation(logo) for logo in logos]

        return Response(
            {"count": len(data), "results": data, "filters_applied": filters}
        )

    except Exception as e:
        return Response(
            {"error": f"Error al listar logos: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def obtener_logo(request, logo_id: int):
    """Obtiene un logo específico por ID"""
    try:
        controller = LogoCRUDController()

        # Ejecutar use case
        logo = controller.obtener_logo_use_case.execute(logo_id)

        if not logo:
            return Response(
                {"error": "Logo no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

        # Serializar respuesta
        serializer = LogoMarcaBovinaSerializer()
        data = serializer.to_representation(logo)

        return Response(data)

    except Exception as e:
        return Response(
            {"error": f"Error al obtener logo: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generar_logo(request):
    """Genera un nuevo logo para una marca"""
    try:
        controller = LogoCRUDController()

        # Validar datos de entrada
        serializer = LogoMarcaBovinaSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Ejecutar use case
        logo = controller.generar_logo_use_case.execute(serializer.validated_data)

        # Serializar respuesta
        response_serializer = LogoMarcaBovinaSerializer()
        data = response_serializer.to_representation(logo)

        return Response(data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {"error": f"Error al generar logo: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
