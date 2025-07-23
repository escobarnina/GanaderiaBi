"""
Controller para generación y regeneración de logos
Responsabilidad única: Generación masiva y regeneración individual
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, Any

from apps.analytics.presentation.serializers.logo_serializers import (
    LogoMarcaBovinaSerializer,
)
from apps.analytics.infrastructure.container.main_container import Container


class LogoGeneracionController:
    """Controller para generación y regeneración de logos"""

    def __init__(self):
        """Inicializa el controller con inyección de dependencias"""
        self.container = Container()

        # Use cases de generación
        self.generar_logo_use_case = self.container.get_generar_logo_use_case()
        self.obtener_logo_use_case = self.container.get_obtener_logo_use_case()


# ============================================================================
# ENDPOINTS DE GENERACIÓN Y REGENERACIÓN
# ============================================================================


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def regenerar_logo(request, logo_id: int):
    """Regenerar un logo específico"""
    try:
        controller = LogoGeneracionController()

        # Obtener logo original
        logo_original = controller.obtener_logo_use_case.execute(logo_id)

        if not logo_original:
            return Response(
                {"error": "Logo no encontrado"}, status=status.HTTP_404_NOT_FOUND
            )

        # Verificar que el logo anterior haya fallado
        if logo_original.exito:
            return Response(
                {"error": "Solo se pueden regenerar logos que fallaron"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Parámetros para regeneración
        nuevo_modelo = request.data.get("modelo_ia", logo_original.modelo_ia_usado)
        nuevo_prompt = request.data.get("prompt_personalizado")

        # Preparar datos para regeneración
        data = {
            "marca_id": logo_original.marca.id,
            "modelo_ia": nuevo_modelo,
            "prompt_personalizado": nuevo_prompt,
            "es_regeneracion": True,
            "logo_original_id": logo_id,
        }

        # Ejecutar use case
        nuevo_logo = controller.generar_logo_use_case.execute(data)

        # Serializar respuesta
        serializer = LogoMarcaBovinaSerializer()
        data = serializer.to_representation(nuevo_logo)

        return Response(
            {
                "mensaje": (
                    "Logo regenerado exitosamente"
                    if nuevo_logo.exito
                    else "Regeneración falló, pero se creó registro"
                ),
                "logo_original": logo_id,
                "logo_nuevo": data,
                "mejora": nuevo_logo.exito and not logo_original.exito,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error regenerando logo: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generar_logos_masivo(request):
    """Generación masiva de logos para marcas sin logos"""
    try:
        controller = LogoGeneracionController()

        modelo_preferido = request.data.get("modelo_ia", "DALL-E-3")
        limite_marcas = request.data.get("limite", 10)

        # Preparar datos para generación masiva
        data = {
            "modelo_ia": modelo_preferido,
            "limite_marcas": limite_marcas,
            "es_generacion_masiva": True,
        }

        # Ejecutar use case
        resultados = controller.generar_logo_use_case.execute(data)

        return Response(
            {
                "mensaje": f"Generación masiva completada: {len(resultados)} logos procesados",
                "resultados": resultados,
                "estadisticas": {
                    "total_procesadas": len(resultados),
                    "exitosos": len([r for r in resultados if r["exito"]]),
                    "fallidos": len([r for r in resultados if not r["exito"]]),
                    "tiempo_promedio": (
                        round(
                            sum(r["tiempo_generacion"] for r in resultados)
                            / len(resultados),
                            2,
                        )
                        if resultados
                        else 0
                    ),
                },
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error en generación masiva: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
