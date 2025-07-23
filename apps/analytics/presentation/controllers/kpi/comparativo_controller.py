"""
Controller para análisis comparativo de KPIs
Responsabilidad única: Comparativas trimestrales y análisis de crecimiento
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, Any

from apps.analytics.presentation.serializers.kpi_serializers import (
    KPIGanadoBovinoSerializer,
)
from apps.analytics.infrastructure.container.main_container import Container


class KpiComparativoController:
    """Controller para análisis comparativo de KPIs"""

    def __init__(self):
        """Inicializa el controller con inyección de dependencias"""
        self.container = Container()

        # Use cases de análisis comparativo
        self.obtener_kpis_use_case = self.container.get_obtener_kpis_use_case()


# ============================================================================
# ENDPOINTS DE ANÁLISIS COMPARATIVO
# ============================================================================


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def comparativa_trimestral(request):
    """Comparativa de KPIs por trimestre"""
    try:
        controller = KpiComparativoController()

        # Ejecutar use case para obtener comparativa trimestral
        trimestres = controller.obtener_kpis_use_case.execute(
            {"tipo": "comparativa_trimestral", "num_trimestres": 4}
        )

        # Procesar datos para respuesta
        comparativa_data = []
        for trimestre in trimestres:
            comparativa_data.append(
                {
                    "trimestre": trimestre.periodo,
                    "numero_trimestre": trimestre.numero_trimestre,
                    "año": trimestre.año,
                    "total_marcas": trimestre.total_marcas,
                    "total_cabezas": trimestre.total_cabezas,
                    "total_ingresos": float(trimestre.total_ingresos),
                    "tiempo_promedio_procesamiento": round(
                        trimestre.tiempo_promedio_procesamiento, 2
                    ),
                    "tasa_exito_logos_promedio": round(
                        trimestre.tasa_exito_logos_promedio, 2
                    ),
                    "meses_con_datos": trimestre.meses_con_datos,
                    "eficiencia_trimestral": round(trimestre.eficiencia_trimestral, 2),
                }
            )

        # Identificar mejores trimestres
        mejor_trimestre_por_marcas = (
            max(comparativa_data, key=lambda x: x["total_marcas"])
            if comparativa_data
            else None
        )
        mejor_trimestre_por_eficiencia = (
            max(comparativa_data, key=lambda x: x["eficiencia_trimestral"])
            if comparativa_data
            else None
        )
        mejor_trimestre_por_logos = (
            max(comparativa_data, key=lambda x: x["tasa_exito_logos_promedio"])
            if comparativa_data
            else None
        )

        # Calcular crecimiento interanual
        crecimiento_interanual = controller._calcular_crecimiento_interanual(
            comparativa_data
        )

        # Analizar estacionalidad
        analisis_estacionalidad = controller._analizar_estacionalidad_trimestral(
            comparativa_data
        )

        return Response(
            {
                "comparativa_trimestral": comparativa_data,
                "mejor_trimestre": {
                    "por_marcas": mejor_trimestre_por_marcas,
                    "por_eficiencia": mejor_trimestre_por_eficiencia,
                    "por_logos": mejor_trimestre_por_logos,
                },
                "crecimiento_interanual": crecimiento_interanual,
                "analisis_estacionalidad": analisis_estacionalidad,
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener comparativa trimestral: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    def _calcular_crecimiento_interanual(self, trimestres):
        """Calcula crecimiento comparando con el mismo trimestre del año anterior"""
        if len(trimestres) < 4:
            return {"mensaje": "Datos insuficientes para comparación interanual"}

        # Comparar último trimestre con el de hace un año
        ultimo_trimestre = trimestres[-1]
        mismo_trimestre_año_anterior = trimestres[0]  # Hace 4 trimestres

        cambio_marcas = (
            ultimo_trimestre["total_marcas"]
            - mismo_trimestre_año_anterior["total_marcas"]
        )
        cambio_porcentual = (
            (cambio_marcas / mismo_trimestre_año_anterior["total_marcas"] * 100)
            if mismo_trimestre_año_anterior["total_marcas"] > 0
            else 0
        )

        # Análisis de cabezas bovinas
        cambio_cabezas = (
            ultimo_trimestre["total_cabezas"]
            - mismo_trimestre_año_anterior["total_cabezas"]
        )
        cambio_cabezas_pct = (
            (cambio_cabezas / mismo_trimestre_año_anterior["total_cabezas"] * 100)
            if mismo_trimestre_año_anterior["total_cabezas"] > 0
            else 0
        )

        return {
            "marcas": {
                "cambio_absoluto": cambio_marcas,
                "cambio_porcentual": round(cambio_porcentual, 2),
            },
            "cabezas_bovinas": {
                "cambio_absoluto": cambio_cabezas,
                "cambio_porcentual": round(cambio_cabezas_pct, 2),
            },
            "tendencia": (
                "crecimiento_fuerte"
                if cambio_porcentual > 15
                else (
                    "crecimiento_moderado"
                    if cambio_porcentual > 5
                    else "decrecimiento" if cambio_porcentual < -5 else "estable"
                )
            ),
            "interpretacion": self._interpretar_crecimiento(cambio_porcentual),
        }

    def _interpretar_crecimiento(self, cambio_porcentual):
        """Interpreta el crecimiento interanual"""
        if cambio_porcentual > 20:
            return "Crecimiento excepcional del sector ganadero"
        elif cambio_porcentual > 10:
            return "Crecimiento sólido y sostenible"
        elif cambio_porcentual > 0:
            return "Crecimiento moderado del sector"
        elif cambio_porcentual > -10:
            return "Contracción leve, revisar factores"
        else:
            return "Contracción significativa, requiere atención"

    def _analizar_estacionalidad_trimestral(self, trimestres):
        """Analiza patrones estacionales en datos trimestrales"""
        if len(trimestres) < 4:
            return {"disponible": False}

        # Agrupar por número de trimestre
        por_trimestre = {}
        for trimestre in trimestres:
            num_trim = trimestre["numero_trimestre"]
            if num_trim not in por_trimestre:
                por_trimestre[num_trim] = []
            por_trimestre[num_trim].append(trimestre["total_marcas"])

        # Calcular promedios
        promedios = {}
        for num_trim, valores in por_trimestre.items():
            promedios[f"Q{num_trim}"] = round(sum(valores) / len(valores), 2)

        # Identificar trimestre pico y valle
        if promedios:
            trimestre_pico = max(promedios, key=promedios.get)
            trimestre_valle = min(promedios, key=promedios.get)

            return {
                "disponible": True,
                "promedios_por_trimestre": promedios,
                "trimestre_pico": trimestre_pico,
                "trimestre_valle": trimestre_valle,
                "variacion_estacional": round(
                    promedios[trimestre_pico] - promedios[trimestre_valle], 2
                ),
            }

        return {"disponible": False}
