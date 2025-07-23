"""
Controller para procesamiento masivo de marcas
Responsabilidad única: Operaciones masivas (aprobar/rechazar múltiples)
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, Any

from apps.analytics.presentation.serializers.marca_serializers import (
    MarcaGanadoBovinoSerializer,
)
from apps.analytics.infrastructure.container.main_container import Container


class MarcaProcesamientoController:
    """Controller para procesamiento masivo de marcas"""

    def __init__(self):
        """Inicializa el controller con inyección de dependencias"""
        self.container = Container()

        # Use cases de procesamiento
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
# ENDPOINTS DE PROCESAMIENTO MASIVO
# ============================================================================


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def procesamiento_masivo(request):
    """Procesamiento masivo de marcas (aprobar/rechazar múltiples)"""
    try:
        controller = MarcaProcesamientoController()
        user_info = controller._get_user_info(request)

        accion = request.data.get("accion")  # 'aprobar' o 'rechazar'
        marca_ids = request.data.get("marca_ids", [])
        observaciones = request.data.get("observaciones", "")

        if accion not in ["aprobar", "rechazar"]:
            return Response(
                {"error": 'Acción debe ser "aprobar" o "rechazar"'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not marca_ids:
            return Response(
                {"error": "Debe proporcionar al menos una marca"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        procesadas = []
        errores = []

        for marca_id in marca_ids:
            try:
                # Preparar datos para el use case
                data = {
                    "marca_id": marca_id,
                    "nuevo_estado": "APROBADO" if accion == "aprobar" else "RECHAZADO",
                    "usuario_responsable": user_info["username"],
                    "observaciones": f"Procesamiento masivo: {accion}. {observaciones}",
                }

                # Ejecutar use case
                resultado = controller.cambiar_estado_marca_use_case.execute(data)

                if resultado:
                    procesadas.append(
                        {
                            "id": resultado.id,
                            "numero_marca": resultado.numero_marca,
                            "nuevo_estado": resultado.estado.value,
                        }
                    )
                else:
                    errores.append(
                        {"id": marca_id, "error": "No se pudo procesar la marca"}
                    )

            except Exception as e:
                errores.append({"id": marca_id, "error": str(e)})

        return Response(
            {
                "mensaje": f"{len(procesadas)} marcas procesadas exitosamente",
                "procesadas": procesadas,
                "errores": errores,
                "total_procesadas": len(procesadas),
                "total_errores": len(errores),
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error en procesamiento masivo: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
