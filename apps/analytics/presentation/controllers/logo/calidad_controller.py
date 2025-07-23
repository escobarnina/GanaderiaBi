"""
Controller para análisis de calidad de logos
Responsabilidad única: Análisis de calidad y evaluación masiva
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, Any

from apps.analytics.presentation.serializers.logo_serializers import (
    LogoMarcaBovinaListSerializer,
)
from apps.analytics.infrastructure.container.main_container import Container


class LogoCalidadController:
    """Controller para análisis de calidad de logos"""

    def __init__(self):
        """Inicializa el controller con inyección de dependencias"""
        self.container = Container()

        # Use cases de calidad
        self.listar_logos_use_case = self.container.get_listar_logos_use_case()
        self.obtener_estadisticas_logos_use_case = (
            self.container.get_obtener_estadisticas_logos_use_case()
        )


# ============================================================================
# ENDPOINTS DE ANÁLISIS DE CALIDAD
# ============================================================================


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def logos_por_calidad(request):
    """Distribución de logos por calidad"""
    try:
        controller = LogoCalidadController()

        # Ejecutar use case para obtener estadísticas
        estadisticas = controller.obtener_estadisticas_logos_use_case.execute(
            {"tipo": "distribucion_calidad"}
        )

        # Procesar datos para respuesta
        distribucion = []
        total_logos = 0

        for calidad, stats in estadisticas.items():
            total_logos += stats["total"]
            distribucion.append(
                {
                    "calidad_logo": calidad,
                    "total": stats["total"],
                    "tiempo_promedio": stats["tiempo_promedio"],
                    "porcentaje": round(
                        (
                            (
                                stats["total"]
                                / sum(s["total"] for s in estadisticas.values())
                                * 100
                            )
                            if estadisticas
                            else 0
                        ),
                        2,
                    ),
                    "calidad_display": calidad.title(),
                }
            )

        # Ordenar por total descendente
        distribucion.sort(key=lambda x: x["total"], reverse=True)

        # Calcular métricas adicionales
        alta_calidad_porcentaje = next(
            (
                item["porcentaje"]
                for item in distribucion
                if item["calidad_logo"] == "ALTA"
            ),
            0,
        )

        return Response(
            {
                "total_logos": total_logos,
                "distribucion_calidad": distribucion,
                "metricas_calidad": {
                    "alta_calidad_porcentaje": alta_calidad_porcentaje,
                    "necesita_mejora": total_logos
                    - next(
                        (
                            item["total"]
                            for item in distribucion
                            if item["calidad_logo"] == "ALTA"
                        ),
                        0,
                    ),
                },
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener distribución por calidad: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def evaluar_calidad_masiva(request):
    """Evaluación masiva de calidad de logos"""
    try:
        controller = LogoCalidadController()

        logo_ids = request.data.get("logo_ids", [])
        nueva_calidad = request.data.get("calidad", "MEDIA")

        if nueva_calidad not in ["ALTA", "MEDIA", "BAJA"]:
            return Response(
                {"error": "Calidad debe ser ALTA, MEDIA o BAJA"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not logo_ids:
            return Response(
                {"error": "Debe proporcionar al menos un logo"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ejecutar use case para actualizar calidad
        actualizados = controller.obtener_estadisticas_logos_use_case.execute(
            {
                "tipo": "actualizar_calidad",
                "logo_ids": logo_ids,
                "nueva_calidad": nueva_calidad,
            }
        )

        return Response(
            {
                "mensaje": f"{len(actualizados)} logos actualizados",
                "actualizados": actualizados,
                "nueva_distribucion": controller._obtener_distribucion_calidad(),
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error en evaluación masiva: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def _obtener_distribucion_calidad(self):
    """Obtiene la distribución actual de calidad de logos"""
    try:
        controller = LogoCalidadController()

        estadisticas = controller.obtener_estadisticas_logos_use_case.execute(
            {"tipo": "distribucion_calidad"}
        )

        total = sum(stats["total"] for stats in estadisticas.values())
        if total == 0:
            return {"alta": 0, "media": 0, "baja": 0}

        resultado = {"alta": 0, "media": 0, "baja": 0}
        for calidad, stats in estadisticas.items():
            if calidad == "ALTA":
                resultado["alta"] = round((stats["total"] / total) * 100, 2)
            elif calidad == "MEDIA":
                resultado["media"] = round((stats["total"] / total) * 100, 2)
            elif calidad == "BAJA":
                resultado["baja"] = round((stats["total"] / total) * 100, 2)

        return resultado

    except Exception:
        return {"alta": 0, "media": 0, "baja": 0}
