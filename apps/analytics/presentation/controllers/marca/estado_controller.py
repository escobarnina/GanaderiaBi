"""
Controller para operaciones de estado de marcas
Responsabilidad única: Cambios de estado (aprobar/rechazar)
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, Any

from apps.analytics.presentation.serializers.marca_serializers import (
    MarcaGanadoBovinoSerializer,
)
from apps.analytics.infrastructure.container.main_container import (
    MainContainer as Container,
)


class MarcaEstadoController:
    """Controller para operaciones de estado de marcas"""

    def __init__(self):
        """Inicializa el controller con inyección de dependencias"""
        self.container = Container()

        # Use cases de estado
        self.cambiar_estado_marca_use_case = (
            self.container.get_cambiar_estado_marca_use_case()
        )

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


# ============================================================================
# ENDPOINTS DE ESTADO
# ============================================================================


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def aprobar_marca(request, marca_id: int):
    """Aprueba una marca específica"""
    try:
        controller = MarcaEstadoController()
        user_info = controller._get_user_info(request)

        # Preparar datos para el use case
        data = {
            "marca_id": marca_id,
            "nuevo_estado": "APROBADO",
            "usuario_responsable": user_info["username"],
            "observaciones": request.data.get(
                "observaciones", "Marca aprobada manualmente"
            ),
        }

        # Ejecutar use case
        resultado = controller.cambiar_estado_marca_use_case.execute(data)

        if not resultado:
            return Response(
                {"error": "No se pudo aprobar la marca"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "mensaje": f"Marca {resultado.numero_marca} aprobada exitosamente",
                "marca": MarcaGanadoBovinoSerializer().to_representation(resultado),
                "tiempo_procesamiento": f"{resultado.tiempo_procesamiento_horas} horas",
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al aprobar marca: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def rechazar_marca(request, marca_id: int):
    """Rechaza una marca específica"""
    try:
        controller = MarcaEstadoController()
        user_info = controller._get_user_info(request)

        motivo_rechazo = request.data.get("motivo", "No especificado")

        # Preparar datos para el use case
        data = {
            "marca_id": marca_id,
            "nuevo_estado": "RECHAZADO",
            "usuario_responsable": user_info["username"],
            "observaciones": f"Marca rechazada. Motivo: {motivo_rechazo}",
        }

        # Ejecutar use case
        resultado = controller.cambiar_estado_marca_use_case.execute(data)

        if not resultado:
            return Response(
                {"error": "No se pudo rechazar la marca"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                "mensaje": f"Marca {resultado.numero_marca} rechazada",
                "marca": MarcaGanadoBovinoSerializer().to_representation(resultado),
                "motivo": motivo_rechazo,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al rechazar marca: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
