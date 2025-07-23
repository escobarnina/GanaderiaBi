"""
Controller para análisis de actividad reciente del historial
Responsabilidad única: Análisis de actividad temporal
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, Any

from apps.analytics.presentation.serializers.historial_serializers import (
    HistorialEstadoMarcaSerializer,
)
from apps.analytics.infrastructure.container.main_container import Container


class HistorialActividadController:
    """Controller para análisis de actividad reciente"""

    def __init__(self):
        """Inicializa el controller con inyección de dependencias"""
        self.container = Container()

        # Use cases de actividad
        self.obtener_actividad_reciente_use_case = (
            self.container.get_obtener_actividad_reciente_use_case()
        )


# ============================================================================
# ENDPOINTS DE ANÁLISIS DE ACTIVIDAD
# ============================================================================


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def actividad_reciente(request):
    """Actividad reciente en el sistema (últimas 24 horas)"""
    try:
        controller = HistorialActividadController()

        # Ejecutar use case para obtener actividad reciente
        actividad = controller.obtener_actividad_reciente_use_case.execute(
            {"periodo_horas": 24, "incluir_analisis": True}
        )

        # Serializar respuesta
        serializer = HistorialEstadoMarcaSerializer()
        data = [
            serializer.to_representation(registro) for registro in actividad.registros
        ]

        return Response(
            {
                "actividad_ultimas_24h": data,
                "resumen_actividad": {
                    "total_cambios": actividad.total_cambios,
                    "por_estado": actividad.por_estado,
                    "usuarios_mas_activos": actividad.usuarios_mas_activos,
                    "hora_mas_activa": actividad.hora_mas_activa,
                    "marcas_con_mas_cambios": actividad.marcas_con_mas_cambios,
                },
                "periodo": "24 horas",
                "tendencia_actividad": actividad.tendencia_actividad,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener actividad reciente: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def auditoria_usuario(request):
    """Auditoría de actividad por usuario"""
    try:
        controller = HistorialActividadController()

        # Validar parámetros
        usuario = request.query_params.get("usuario", "")
        dias = int(request.query_params.get("dias", 30))

        if not usuario:
            return Response(
                {"error": "Parámetro usuario requerido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ejecutar use case para auditoría de usuario
        auditoria = controller.obtener_actividad_reciente_use_case.execute(
            {
                "tipo": "auditoria_usuario",
                "usuario": usuario,
                "periodo_dias": dias,
                "incluir_analisis": True,
            }
        )

        # Serializar respuesta
        serializer = HistorialEstadoMarcaSerializer()
        historial_detallado = [
            serializer.to_representation(registro)
            for registro in auditoria.historial_detallado
        ]

        return Response(
            {
                "usuario": usuario,
                "periodo_dias": dias,
                "estadisticas": {
                    "total_cambios": auditoria.total_cambios,
                    "promedio_cambios_por_dia": auditoria.promedio_cambios_por_dia,
                    "cambios_por_estado": auditoria.cambios_por_estado,
                    "dias_activos": auditoria.dias_activos,
                },
                "eficiencia": auditoria.eficiencia,
                "patrones_trabajo": auditoria.patrones_trabajo,
                "actividad_diaria": auditoria.actividad_diaria,
                "marcas_mas_trabajadas": auditoria.marcas_mas_trabajadas,
                "historial_detallado": historial_detallado,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener auditoría de usuario: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
