"""
Controller para análisis temporal de KPIs
Responsabilidad única: Análisis de KPIs por períodos temporales
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from typing import Dict, Any

from apps.analytics.presentation.serializers.kpi_serializers import (
    KpiGanadoBovinoSerializer,
)
from apps.analytics.infrastructure.container.main_container import Container


class KpiTemporalController:
    """Controller para análisis temporal de KPIs"""

    def __init__(self):
        """Inicializa el controller con inyección de dependencias"""
        self.container = Container()

        # Use cases de análisis temporal
        self.obtener_kpis_use_case = self.container.get_obtener_kpis_use_case()
        self.calcular_kpis_use_case = self.container.get_calcular_kpis_use_case()


# ============================================================================
# ENDPOINTS DE ANÁLISIS TEMPORAL
# ============================================================================


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def ultimos_12_meses(request):
    """KPIs de los últimos 12 meses"""
    try:
        controller = KpiTemporalController()

        # Ejecutar use case para obtener KPIs de últimos 12 meses
        kpis = controller.obtener_kpis_use_case.execute(
            {"periodo": "ultimos_12_meses", "incluir_tendencias": True}
        )

        # Serializar respuesta
        serializer = KpiGanadoBovinoSerializer()
        data = [serializer.to_representation(kpi) for kpi in kpis]

        # Calcular métricas de tendencia
        if len(kpis) >= 2:
            primer_kpi = kpis[0]
            ultimo_kpi = kpis[-1]

            tendencias = {
                "marcas_registradas": {
                    "cambio": ultimo_kpi.marcas_registradas_mes
                    - primer_kpi.marcas_registradas_mes,
                    "porcentaje": round(
                        (
                            (
                                (
                                    ultimo_kpi.marcas_registradas_mes
                                    - primer_kpi.marcas_registradas_mes
                                )
                                / primer_kpi.marcas_registradas_mes
                                * 100
                            )
                            if primer_kpi.marcas_registradas_mes > 0
                            else 0
                        ),
                        2,
                    ),
                },
                "cabezas_bovinas": {
                    "cambio": ultimo_kpi.total_cabezas_registradas
                    - primer_kpi.total_cabezas_registradas,
                    "porcentaje": round(
                        (
                            (
                                (
                                    ultimo_kpi.total_cabezas_registradas
                                    - primer_kpi.total_cabezas_registradas
                                )
                                / primer_kpi.total_cabezas_registradas
                                * 100
                            )
                            if primer_kpi.total_cabezas_registradas > 0
                            else 0
                        ),
                        2,
                    ),
                },
                "ingresos": {
                    "cambio": float(ultimo_kpi.ingresos_mes - primer_kpi.ingresos_mes),
                    "porcentaje": round(
                        (
                            (
                                float(ultimo_kpi.ingresos_mes - primer_kpi.ingresos_mes)
                                / float(primer_kpi.ingresos_mes)
                                * 100
                            )
                            if primer_kpi.ingresos_mes > 0
                            else 0
                        ),
                        2,
                    ),
                },
            }
        else:
            tendencias = {"mensaje": "Datos insuficientes para calcular tendencias"}

        # Calcular resumen estadístico
        resumen_estadistico = controller._calcular_resumen_estadistico(kpis)

        return Response(
            {
                "kpis_12_meses": data,
                "tendencias_anuales": tendencias,
                "periodo": "últimos 12 meses",
                "resumen_estadistico": resumen_estadistico,
                "meses_completos": len(kpis),
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener KPIs de últimos 12 meses: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def kpis_actuales(request):
    """KPIs del mes actual y comparación con el anterior"""
    try:
        controller = KpiTemporalController()

        # Ejecutar use case para obtener KPIs actuales
        kpis_actuales = controller.obtener_kpis_use_case.execute(
            {"periodo": "actual", "incluir_comparacion": True}
        )

        if not kpis_actuales:
            return Response({"mensaje": "No hay KPIs disponibles para el mes actual"})

        kpi_actual = kpis_actuales[0]

        # Serializar KPI actual
        serializer = KpiGanadoBovinoSerializer()
        data_actual = serializer.to_representation(kpi_actual)

        # Comparación con mes anterior (si existe)
        if len(kpis_actuales) > 1:
            kpi_anterior = kpis_actuales[1]

            comparacion = {
                "marcas_registradas": {
                    "actual": kpi_actual.marcas_registradas_mes,
                    "anterior": kpi_anterior.marcas_registradas_mes,
                    "cambio": kpi_actual.marcas_registradas_mes
                    - kpi_anterior.marcas_registradas_mes,
                    "cambio_porcentual": round(
                        (
                            (
                                (
                                    kpi_actual.marcas_registradas_mes
                                    - kpi_anterior.marcas_registradas_mes
                                )
                                / kpi_anterior.marcas_registradas_mes
                                * 100
                            )
                            if kpi_anterior.marcas_registradas_mes > 0
                            else 0
                        ),
                        2,
                    ),
                    "tendencia": controller._determinar_tendencia_cambio(
                        kpi_actual.marcas_registradas_mes
                        - kpi_anterior.marcas_registradas_mes
                    ),
                },
                "cabezas_bovinas": {
                    "actual": kpi_actual.total_cabezas_registradas,
                    "anterior": kpi_anterior.total_cabezas_registradas,
                    "cambio": kpi_actual.total_cabezas_registradas
                    - kpi_anterior.total_cabezas_registradas,
                    "cambio_porcentual": round(
                        (
                            (
                                (
                                    kpi_actual.total_cabezas_registradas
                                    - kpi_anterior.total_cabezas_registradas
                                )
                                / kpi_anterior.total_cabezas_registradas
                                * 100
                            )
                            if kpi_anterior.total_cabezas_registradas > 0
                            else 0
                        ),
                        2,
                    ),
                },
                "tiempo_procesamiento": {
                    "actual": round(kpi_actual.tiempo_promedio_procesamiento, 2),
                    "anterior": round(kpi_anterior.tiempo_promedio_procesamiento, 2),
                    "mejoro": kpi_actual.tiempo_promedio_procesamiento
                    < kpi_anterior.tiempo_promedio_procesamiento,
                    "cambio_horas": round(
                        kpi_actual.tiempo_promedio_procesamiento
                        - kpi_anterior.tiempo_promedio_procesamiento,
                        2,
                    ),
                },
                "tasa_aprobacion": {
                    "actual": round(kpi_actual.porcentaje_aprobacion, 2),
                    "anterior": round(kpi_anterior.porcentaje_aprobacion, 2),
                    "mejoro": kpi_actual.porcentaje_aprobacion
                    > kpi_anterior.porcentaje_aprobacion,
                    "cambio_puntos": round(
                        kpi_actual.porcentaje_aprobacion
                        - kpi_anterior.porcentaje_aprobacion,
                        2,
                    ),
                },
                "ingresos": {
                    "actual": float(kpi_actual.ingresos_mes),
                    "anterior": float(kpi_anterior.ingresos_mes),
                    "cambio": float(
                        kpi_actual.ingresos_mes - kpi_anterior.ingresos_mes
                    ),
                    "cambio_porcentual": round(
                        (
                            (
                                float(
                                    kpi_actual.ingresos_mes - kpi_anterior.ingresos_mes
                                )
                                / float(kpi_anterior.ingresos_mes)
                                * 100
                            )
                            if kpi_anterior.ingresos_mes > 0
                            else 0
                        ),
                        2,
                    ),
                },
                "logos_ia": {
                    "actual": round(kpi_actual.tasa_exito_logos, 2),
                    "anterior": round(kpi_anterior.tasa_exito_logos, 2),
                    "mejoro": kpi_actual.tasa_exito_logos
                    > kpi_anterior.tasa_exito_logos,
                },
            }

            # Análisis general del mes
            analisis_general = controller._generar_analisis_mensual(comparacion)

        else:
            comparacion = {"mensaje": "No hay datos del mes anterior para comparar"}
            analisis_general = {"mensaje": "Análisis limitado sin datos de referencia"}

        return Response(
            {
                "kpi_mes_actual": data_actual,
                "comparacion_mes_anterior": comparacion,
                "analisis_general": analisis_general,
                "fecha_actualizacion": kpi_actual.fecha,
                "alertas": controller._generar_alertas_kpi(
                    kpi_actual, kpi_anterior if len(kpis_actuales) > 1 else None
                ),
            }
        )

    except Exception as e:
        return Response(
            {"error": f"Error al obtener KPIs actuales: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    def _calcular_resumen_estadistico(self, kpis):
        """Calcula resumen estadístico de los KPIs"""
        if not kpis:
            return {}

        marcas_por_mes = [kpi.marcas_registradas_mes for kpi in kpis]
        cabezas_por_mes = [kpi.total_cabezas_registradas for kpi in kpis]

        return {
            "marcas_promedio_mensual": round(
                sum(marcas_por_mes) / len(marcas_por_mes), 2
            ),
            "marcas_maximo_mes": max(marcas_por_mes),
            "marcas_minimo_mes": min(marcas_por_mes),
            "cabezas_promedio_mensual": round(
                sum(cabezas_por_mes) / len(cabezas_por_mes), 2
            ),
            "variabilidad": (
                "alta" if (max(marcas_por_mes) - min(marcas_por_mes)) > 50 else "baja"
            ),
            "tendencia_general": self._determinar_tendencia_general(marcas_por_mes),
        }

    def _determinar_tendencia_general(self, datos):
        """Determina la tendencia general de una serie de datos"""
        if len(datos) < 3:
            return "insuficientes_datos"

        # Comparar primera mitad vs segunda mitad
        mitad = len(datos) // 2
        primera_mitad = sum(datos[:mitad]) / mitad
        segunda_mitad = sum(datos[mitad:]) / (len(datos) - mitad)

        if segunda_mitad > primera_mitad * 1.1:
            return "crecimiento"
        elif segunda_mitad < primera_mitad * 0.9:
            return "decrecimiento"
        else:
            return "estable"

    def _determinar_tendencia_cambio(self, cambio):
        """Determina la tendencia basada en el cambio"""
        if cambio > 10:
            return "crecimiento_fuerte"
        elif cambio > 0:
            return "crecimiento"
        elif cambio == 0:
            return "estable"
        elif cambio > -10:
            return "decrecimiento"
        else:
            return "decrecimiento_fuerte"

    def _generar_analisis_mensual(self, comparacion):
        """Genera análisis general del desempeño mensual"""
        analisis = {
            "tendencia_general": "positiva",
            "areas_mejora": [],
            "fortalezas": [],
            "score_general": 0,
        }

        # Analizar cada métrica
        if comparacion["marcas_registradas"]["cambio"] > 0:
            analisis["fortalezas"].append("Crecimiento en registros de marcas")
            analisis["score_general"] += 20
        else:
            analisis["areas_mejora"].append("Declining in marca registrations")

        if comparacion["tiempo_procesamiento"]["mejoro"]:
            analisis["fortalezas"].append("Mejora en tiempo de procesamiento")
            analisis["score_general"] += 20
        else:
            analisis["areas_mejora"].append("Tiempo de procesamiento se incrementó")

        if comparacion["tasa_aprobacion"]["mejoro"]:
            analisis["fortalezas"].append("Mayor tasa de aprobación")
            analisis["score_general"] += 15
        else:
            analisis["areas_mejora"].append("Tasa de aprobación disminuyó")

        if comparacion["ingresos"]["cambio"] > 0:
            analisis["fortalezas"].append("Incremento en ingresos")
            analisis["score_general"] += 25
        else:
            analisis["areas_mejora"].append("Disminución en ingresos")

        if comparacion["logos_ia"]["mejoro"]:
            analisis["fortalezas"].append("Mejora en generación de logos IA")
            analisis["score_general"] += 20

        # Determinar tendencia general
        if analisis["score_general"] > 70:
            analisis["tendencia_general"] = "muy_positiva"
        elif analisis["score_general"] > 40:
            analisis["tendencia_general"] = "positiva"
        elif analisis["score_general"] > 20:
            analisis["tendencia_general"] = "neutral"
        else:
            analisis["tendencia_general"] = "negativa"

        return analisis

    def _generar_alertas_kpi(self, kpi_actual, kpi_anterior):
        """Genera alertas basadas en los KPIs actuales"""
        alertas = []

        # Alerta por baja tasa de aprobación
        if kpi_actual.porcentaje_aprobacion < 70:
            alertas.append(
                {
                    "tipo": "warning",
                    "categoria": "calidad",
                    "mensaje": f"Tasa de aprobación baja: {kpi_actual.porcentaje_aprobacion:.1f}%",
                    "accion_recomendada": "Revisar criterios de evaluación y capacitar evaluadores",
                }
            )

        # Alerta por tiempo de procesamiento alto
        if kpi_actual.tiempo_promedio_procesamiento > 72:  # Más de 3 días
            alertas.append(
                {
                    "tipo": "danger",
                    "categoria": "eficiencia",
                    "mensaje": f"Tiempo de procesamiento elevado: {kpi_actual.tiempo_promedio_procesamiento:.1f} horas",
                    "accion_recomendada": "Optimizar procesos y aumentar capacidad de evaluación",
                }
            )

        # Alerta por decrecimiento en marcas (comparado con mes anterior)
        if (
            kpi_anterior
            and kpi_actual.marcas_registradas_mes
            < kpi_anterior.marcas_registradas_mes * 0.8
        ):
            alertas.append(
                {
                    "tipo": "warning",
                    "categoria": "demanda",
                    "mensaje": f"Decrecimiento significativo en registros: -{((kpi_anterior.marcas_registradas_mes - kpi_actual.marcas_registradas_mes) / kpi_anterior.marcas_registradas_mes * 100):.1f}%",
                    "accion_recomendada": "Implementar estrategias de marketing y promoción",
                }
            )

        # Alerta por baja tasa de éxito en logos IA
        if kpi_actual.tasa_exito_logos < 80:
            alertas.append(
                {
                    "tipo": "info",
                    "categoria": "tecnologia",
                    "mensaje": f"Tasa de éxito de logos IA por debajo del óptimo: {kpi_actual.tasa_exito_logos:.1f}%",
                    "accion_recomendada": "Revisar y optimizar modelos de IA y prompts",
                }
            )

        return alertas
