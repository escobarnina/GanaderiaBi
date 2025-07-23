"""
Controller para análisis de tendencias y predicciones
Responsabilidad única: Análisis temporal y predicciones
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, Any

from apps.analytics.infrastructure.container.main_container import Container


class EstadisticasTendenciasController:
    """Controller para análisis de tendencias"""

    def __init__(self):
        """Inicializa el controller con inyección de dependencias"""
        self.container = Container()

        # Use cases de tendencias
        self.calcular_tendencias_departamento_use_case = (
            self.container.get_calcular_tendencias_departamento_use_case()
        )


# ============================================================================
# ENDPOINTS DE ANÁLISIS DE TENDENCIAS
# ============================================================================


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def comparativa_temporal(request):
    """Comparativa temporal de estadísticas"""
    try:
        controller = EstadisticasTendenciasController()

        # Obtener parámetros
        meses_atras = int(request.query_params.get("meses_atras", 6))

        # Ejecutar use case para obtener comparativa temporal
        tendencias = controller.calcular_tendencias_departamento_use_case.execute(
            {"meses_atras": meses_atras, "incluir_analisis": True}
        )

        return Response(
            {
                "periodo_analisis": f"{meses_atras} meses",
                "comparativa_mensual": tendencias.comparativa_mensual,
                "comparativa_trimestral": tendencias.comparativa_trimestral,
                "comparativa_anual": tendencias.comparativa_anual,
                "tendencias": tendencias.tendencias,
                "crecimiento_anual": tendencias.crecimiento_anual,
                "estacionalidad": tendencias.estacionalidad,
                "volatilidad": tendencias.volatilidad,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener comparativa temporal: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def predicciones_demanda(request):
    """Predicciones de demanda del sector ganadero"""
    try:
        controller = EstadisticasTendenciasController()

        # Obtener parámetros
        meses_futuro = int(request.query_params.get("meses_futuro", 12))

        # Ejecutar use case para obtener predicciones
        predicciones = controller.calcular_tendencias_departamento_use_case.execute(
            {
                "tipo": "predicciones",
                "meses_futuro": meses_futuro,
                "incluir_planificacion": True,
            }
        )

        return Response(
            {
                "periodo_prediccion": f"{meses_futuro} meses",
                "predicciones_base": predicciones.predicciones_base,
                "recomendaciones_planificacion": predicciones.recomendaciones_planificacion,
                "corredores_ganaderos": predicciones.corredores_ganaderos,
                "migracion_razas": predicciones.migracion_razas,
                "concentracion_mercado": predicciones.concentracion_mercado,
                "mapa_razas_departamentos": predicciones.mapa_razas_departamentos,
                "recomendaciones_diversificacion": predicciones.recomendaciones_diversificacion,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener predicciones de demanda: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def tendencias_geograficas(request):
    """Análisis de tendencias geográficas"""
    try:
        controller = EstadisticasTendenciasController()

        # Obtener parámetros
        años_analisis = int(request.query_params.get("años_analisis", 3))

        # Ejecutar use case para obtener tendencias geográficas
        tendencias = controller.calcular_tendencias_departamento_use_case.execute(
            {
                "tipo": "tendencias_geograficas",
                "años_analisis": años_analisis,
                "incluir_analisis": True,
            }
        )

        return Response(
            {
                "periodo_analisis": f"{años_analisis} años",
                "diversificacion_geografica": tendencias.diversificacion_geografica,
                "evolucion_tecnologica": tendencias.evolucion_tecnologica,
                "profesionalizacion": tendencias.profesionalizacion,
                "gini_departamental": tendencias.gini_departamental,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener tendencias geográficas: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
