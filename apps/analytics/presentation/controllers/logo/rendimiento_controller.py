"""
Controller para análisis de rendimiento de modelos IA
Responsabilidad única: Análisis de rendimiento y prompts
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, Any

from apps.analytics.presentation.serializers.logo_serializers import (
    RendimientoModelosIASerializer,
)
from apps.analytics.infrastructure.container.main_container import Container


class LogoRendimientoController:
    """Controller para análisis de rendimiento de modelos IA"""

    def __init__(self):
        """Inicializa el controller con inyección de dependencias"""
        self.container = Container()

        # Use cases de rendimiento
        self.obtener_estadisticas_logos_use_case = (
            self.container.get_obtener_estadisticas_logos_use_case()
        )


# ============================================================================
# ENDPOINTS DE ANÁLISIS DE RENDIMIENTO
# ============================================================================


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def rendimiento_modelos_ia(request):
    """Análisis completo del rendimiento de modelos IA"""
    try:
        controller = LogoRendimientoController()

        # Ejecutar use case para obtener estadísticas de modelos
        modelos_stats = controller.obtener_estadisticas_logos_use_case.execute(
            {"tipo": "rendimiento_modelos"}
        )

        # Calcular métricas adicionales
        for modelo in modelos_stats:
            modelo["tasa_exito"] = round(
                (
                    (modelo["exitosos"] / modelo["total_generados"] * 100)
                    if modelo["total_generados"] > 0
                    else 0
                ),
                2,
            )
            modelo["porcentaje_alta_calidad"] = round(
                (
                    (modelo["logos_alta_calidad"] / modelo["total_generados"] * 100)
                    if modelo["total_generados"] > 0
                    else 0
                ),
                2,
            )
            modelo["tiempo_promedio_formateado"] = (
                f"{modelo['tiempo_promedio_generacion']:.1f}s"
            )
            modelo["modelo_display"] = modelo["modelo_ia_usado"]

        # Serializar respuesta
        serializer = RendimientoModelosIASerializer()
        data = [serializer.to_representation(modelo) for modelo in modelos_stats]

        # Ranking de modelos
        ranking = sorted(
            modelos_stats,
            key=lambda x: (x["tasa_exito"], x["porcentaje_alta_calidad"]),
            reverse=True,
        )

        return Response(
            {
                "modelos_rendimiento": data,
                "ranking_modelos": [
                    {
                        "posicion": idx + 1,
                        "modelo": modelo["modelo_ia_usado"],
                        "score_general": round(
                            (modelo["tasa_exito"] + modelo["porcentaje_alta_calidad"])
                            / 2,
                            2,
                        ),
                    }
                    for idx, modelo in enumerate(ranking)
                ],
                "recomendacion_modelo": (
                    ranking[0]["modelo_ia_usado"] if ranking else None
                ),
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener rendimiento de modelos: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def analisis_prompts(request):
    """Análisis de efectividad de prompts"""
    try:
        controller = LogoRendimientoController()

        # Ejecutar use case para obtener análisis de prompts
        analisis = controller.obtener_estadisticas_logos_use_case.execute(
            {"tipo": "analisis_prompts"}
        )

        return Response(analisis)

    except Exception as e:
        return Response(
            {"error": f"Error al obtener análisis de prompts: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
