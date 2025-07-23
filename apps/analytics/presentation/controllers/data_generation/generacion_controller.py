"""
Controller para generación de datos
Responsabilidad única: Generación de datos y prompts
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, Any

from apps.analytics.infrastructure.container.main_container import Container


class DataGenerationController:
    """Controller para generación de datos"""

    def __init__(self):
        """Inicializa el controller con inyección de dependencias"""
        self.container = Container()

        # Use cases de generación de datos
        self.generar_datos_mockaroo_use_case = (
            self.container.get_generar_datos_mockaroo_use_case()
        )
        self.generar_descripcion_marca_use_case = (
            self.container.get_generar_descripcion_marca_use_case()
        )
        self.generar_prompt_logo_use_case = (
            self.container.get_generar_prompt_logo_use_case()
        )


# ============================================================================
# ENDPOINTS DE GENERACIÓN DE DATOS
# ============================================================================


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generar_datos_mockaroo(request):
    """Genera datos de prueba usando Mockaroo"""
    try:
        controller = DataGenerationController()

        # Obtener parámetros
        cantidad = int(request.data.get("cantidad", 50))

        # Ejecutar use case para generar datos
        datos = controller.generar_datos_mockaroo_use_case.execute(
            {"cantidad": cantidad, "incluir_creacion": True}
        )

        return Response(
            {
                "mensaje": f"Se generaron {cantidad} registros de datos",
                "datos_generados": len(datos),
                "esquema_utilizado": datos[0].keys() if datos else [],
                "ejemplo_datos": datos[:3] if datos else [],
            },
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        return Response(
            {"error": f"Error al generar datos Mockaroo: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generar_descripcion_marca(request):
    """Genera descripción para una marca específica"""
    try:
        controller = DataGenerationController()

        # Obtener parámetros
        marca_id = int(request.data.get("marca_id", 0))

        if not marca_id:
            return Response(
                {"error": "Parámetro marca_id es requerido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ejecutar use case para generar descripción
        descripcion = controller.generar_descripcion_marca_use_case.execute(
            {"marca_id": marca_id, "incluir_llm": True}
        )

        return Response(
            {
                "marca_id": marca_id,
                "descripcion_generada": descripcion,
                "longitud_descripcion": len(descripcion),
                "tipo_generacion": "llm_simulado",
            },
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        return Response(
            {"error": f"Error al generar descripción de marca: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generar_prompts_logo(request):
    """Genera prompts para logos de una marca específica"""
    try:
        controller = DataGenerationController()

        # Obtener parámetros
        marca_id = int(request.data.get("marca_id", 0))

        if not marca_id:
            return Response(
                {"error": "Parámetro marca_id es requerido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ejecutar use case para generar prompts
        prompts = controller.generar_prompt_logo_use_case.execute(
            {"marca_id": marca_id, "incluir_variaciones": True}
        )

        return Response(
            {
                "marca_id": marca_id,
                "prompts_generados": len(prompts),
                "tipos_prompt": ["corporativo", "rural", "profesional", "tradicional"],
                "prompts": prompts,
            },
            status=status.HTTP_201_CREATED,
        )

    except Exception as e:
        return Response(
            {"error": f"Error al generar prompts de logo: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
