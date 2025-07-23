"""
Controller para análisis estacional de KPIs
Responsabilidad única: Análisis de patrones estacionales
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, Any
import calendar

from apps.analytics.presentation.serializers.kpi_serializers import (
    KPIGanadoBovinoSerializer,
)
from apps.analytics.infrastructure.container.main_container import Container


class KpiEstacionalController:
    """Controller para análisis estacional de KPIs"""

    def __init__(self):
        """Inicializa el controller con inyección de dependencias"""
        self.container = Container()

        # Use cases de análisis estacional
        self.obtener_kpis_use_case = self.container.get_obtener_kpis_use_case()


# ============================================================================
# ENDPOINTS DE ANÁLISIS ESTACIONAL
# ============================================================================


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def analisis_estacional(request):
    """Análisis de patrones estacionales en los KPIs"""
    try:
        controller = KpiEstacionalController()

        # Ejecutar use case para obtener análisis estacional
        patrones = controller.obtener_kpis_use_case.execute(
            {"tipo": "analisis_estacional", "periodo_años": 2}
        )

        # Procesar datos para respuesta
        patrones_mensuales = {}
        for mes in range(1, 13):
            kpis_mes = [kpi for kpi in patrones if kpi.fecha.month == mes]

            if kpis_mes:
                promedio_marcas = sum(
                    kpi.marcas_registradas_mes for kpi in kpis_mes
                ) / len(kpis_mes)
                promedio_cabezas = sum(
                    kpi.total_cabezas_registradas for kpi in kpis_mes
                ) / len(kpis_mes)
                promedio_ingresos = sum(
                    float(kpi.ingresos_mes) for kpi in kpis_mes
                ) / len(kpis_mes)

                patrones_mensuales[mes] = {
                    "mes_nombre": calendar.month_name[mes],
                    "mes_numero": mes,
                    "promedio_marcas": round(promedio_marcas, 2),
                    "promedio_cabezas": round(promedio_cabezas, 2),
                    "promedio_ingresos": round(promedio_ingresos, 2),
                    "años_con_datos": len(kpis_mes),
                }

        # Identificar picos y valles
        if patrones_mensuales:
            mes_pico = max(
                patrones_mensuales.items(), key=lambda x: x[1]["promedio_marcas"]
            )
            mes_valle = min(
                patrones_mensuales.items(), key=lambda x: x[1]["promedio_marcas"]
            )

            # Análisis de tendencias por estación
            estaciones = controller._analizar_por_estaciones(patrones_mensuales)

            return Response(
                {
                    "patrones_estacionales": patrones_mensuales,
                    "analisis_picos_valles": {
                        "mes_pico_actividad": {
                            "mes": mes_pico[1]["mes_nombre"],
                            "promedio_marcas": mes_pico[1]["promedio_marcas"],
                            "mes_numero": mes_pico[0],
                        },
                        "mes_menor_actividad": {
                            "mes": mes_valle[1]["mes_nombre"],
                            "promedio_marcas": mes_valle[1]["promedio_marcas"],
                            "mes_numero": mes_valle[0],
                        },
                        "variabilidad_estacional": round(
                            mes_pico[1]["promedio_marcas"]
                            - mes_valle[1]["promedio_marcas"],
                            2,
                        ),
                    },
                    "analisis_estaciones": estaciones,
                    "recomendaciones": controller._generar_recomendaciones_estacionales(
                        mes_pico[0], mes_valle[0], estaciones
                    ),
                }
            )

        return Response({"mensaje": "Datos insuficientes para análisis estacional"})

    except Exception as e:
        return Response(
            {"error": f"Error al obtener análisis estacional: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    def _analizar_por_estaciones(self, patrones_mensuales):
        """Analiza patrones por estaciones del año"""
        # Definir estaciones (Hemisferio Sur - Bolivia)
        estaciones = {
            "verano": [12, 1, 2],  # Diciembre, Enero, Febrero
            "otoño": [3, 4, 5],  # Marzo, Abril, Mayo
            "invierno": [6, 7, 8],  # Junio, Julio, Agosto
            "primavera": [9, 10, 11],  # Septiembre, Octubre, Noviembre
        }

        analisis_estaciones = {}

        for estacion, meses in estaciones.items():
            marcas_estacion = []
            cabezas_estacion = []

            for mes in meses:
                if mes in patrones_mensuales:
                    marcas_estacion.append(patrones_mensuales[mes]["promedio_marcas"])
                    cabezas_estacion.append(patrones_mensuales[mes]["promedio_cabezas"])

            if marcas_estacion:
                analisis_estaciones[estacion] = {
                    "promedio_marcas": round(
                        sum(marcas_estacion) / len(marcas_estacion), 2
                    ),
                    "promedio_cabezas": round(
                        sum(cabezas_estacion) / len(cabezas_estacion), 2
                    ),
                    "meses": [
                        calendar.month_name[m] for m in meses if m in patrones_mensuales
                    ],
                }

        # Identificar mejor estación
        if analisis_estaciones:
            mejor_estacion = max(
                analisis_estaciones,
                key=lambda x: analisis_estaciones[x]["promedio_marcas"],
            )
            analisis_estaciones["mejor_estacion"] = mejor_estacion

        return analisis_estaciones

    def _generar_recomendaciones_estacionales(self, mes_pico, mes_valle, estaciones):
        """Genera recomendaciones basadas en patrones estacionales"""
        recomendaciones = []

        # Recomendación para mes pico
        recomendaciones.append(
            {
                "periodo": calendar.month_name[mes_pico],
                "tipo": "preparacion_capacidad",
                "prioridad": "alta",
                "recomendacion": f"Aumentar capacidad de procesamiento en {calendar.month_name[mes_pico]} debido a alta demanda histórica",
                "impacto": "Evitar cuellos de botella en período de mayor actividad",
                "acciones": [
                    "Asignar más evaluadores",
                    "Preparar infraestructura tecnológica",
                    "Optimizar procesos de certificación",
                ],
            }
        )

        # Recomendación para mes valle
        recomendaciones.append(
            {
                "periodo": calendar.month_name[mes_valle],
                "tipo": "promocion_actividad",
                "prioridad": "media",
                "recomendacion": f"Implementar campañas promocionales en {calendar.month_name[mes_valle]} para incrementar registros",
                "impacto": "Nivelar la demanda a lo largo del año",
                "acciones": [
                    "Descuentos en certificaciones",
                    "Campañas de marketing dirigido",
                    "Visitas a zonas ganaderas",
                ],
            }
        )

        # Recomendaciones por estaciones
        if estaciones and "mejor_estacion" in estaciones:
            mejor_estacion = estaciones["mejor_estacion"]
            recomendaciones.append(
                {
                    "periodo": f"Estación de {mejor_estacion}",
                    "tipo": "aprovechamiento_estacional",
                    "prioridad": "media",
                    "recomendacion": f"Aprovechar la alta actividad natural en {mejor_estacion} para lanzar nuevos servicios",
                    "impacto": "Maximizar ingresos en período favorable",
                    "acciones": [
                        "Lanzar servicios premium",
                        "Capacitaciones masivas",
                        "Eventos del sector",
                    ],
                }
            )

        return recomendaciones
