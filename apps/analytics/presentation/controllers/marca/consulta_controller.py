"""
Controller para consultas especializadas de marcas
Responsabilidad única: Consultas específicas (pendientes, por procesar, etc.)
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, Any

from apps.analytics.presentation.serializers.marca_serializers import (
    MarcaGanadoBovinoListSerializer,
)
from apps.analytics.infrastructure.container.main_container import Container


class MarcaConsultaController:
    """Controller para consultas especializadas de marcas"""

    def __init__(self):
        """Inicializa el controller con inyección de dependencias"""
        self.container = Container()

        # Use cases de consulta
        self.listar_marcas_use_case = self.container.get_listar_marcas_use_case()

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
# ENDPOINTS DE CONSULTA ESPECIALIZADA
# ============================================================================


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def marcas_pendientes(request):
    """Obtiene marcas pendientes de procesamiento"""
    try:
        controller = MarcaConsultaController()

        # Filtros específicos para marcas pendientes
        filters = controller._build_filters(request)
        filters["estado"] = "PENDIENTE"

        # Ejecutar use case
        marcas = controller.listar_marcas_use_case.execute(filters)

        # Serializar respuesta
        serializer = MarcaGanadoBovinoListSerializer()
        data = [serializer.to_representation(marca) for marca in marcas]

        # Calcular estadísticas
        total_cabezas = sum(marca.cantidad_cabezas for marca in marcas)
        promedio_dias = (
            sum(marca.dias_desde_registro for marca in marcas) / len(marcas)
            if marcas
            else 0
        )

        return Response(
            {
                "count": len(data),
                "results": data,
                "resumen": {
                    "total_cabezas": total_cabezas,
                    "promedio_dias_pendiente": round(promedio_dias, 2),
                },
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener marcas pendientes: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def marcas_por_procesar(request):
    """Marcas que requieren atención prioritaria"""
    try:
        controller = MarcaConsultaController()

        # Filtros para marcas por procesar (pendientes por más de 72 horas)
        filters = controller._build_filters(request)
        filters["estado"] = ["PENDIENTE", "EN_PROCESO"]
        filters["tiempo_limite_horas"] = 72

        # Ejecutar use case
        marcas = controller.listar_marcas_use_case.execute(filters)

        # Serializar respuesta
        serializer = MarcaGanadoBovinoListSerializer()
        data = [serializer.to_representation(marca) for marca in marcas]

        return Response(
            {
                "count": len(data),
                "results": data,
                "mensaje": f"{len(data)} marcas requieren atención prioritaria",
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener marcas por procesar: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def marcas_procesadas_hoy(request):
    """Marcas procesadas el día de hoy"""
    try:
        controller = MarcaConsultaController()

        # Filtros para marcas procesadas hoy
        filters = controller._build_filters(request)
        filters["fecha_procesamiento"] = "hoy"

        # Ejecutar use case
        marcas = controller.listar_marcas_use_case.execute(filters)

        # Serializar respuesta
        serializer = MarcaGanadoBovinoListSerializer()
        data = [serializer.to_representation(marca) for marca in marcas]

        # Calcular estadísticas del día
        aprobadas_hoy = len([m for m in marcas if m.estado.value == "APROBADO"])
        rechazadas_hoy = len([m for m in marcas if m.estado.value == "RECHAZADO"])
        tasa_aprobacion = round((aprobadas_hoy / len(marcas) * 100) if marcas else 0, 2)

        return Response(
            {
                "fecha": "hoy",
                "count": len(data),
                "results": data,
                "estadisticas_dia": {
                    "aprobadas": aprobadas_hoy,
                    "rechazadas": rechazadas_hoy,
                    "tasa_aprobacion": tasa_aprobacion,
                },
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener marcas procesadas hoy: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
