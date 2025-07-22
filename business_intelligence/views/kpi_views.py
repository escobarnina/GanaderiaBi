# business_intelligence/views/kpi_views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
import calendar

from ..models import KPIGanadoBovino
from ..serializers import KPIGanadoBovinoSerializer


class KPIGanadoBovinoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para KPIs de ganado bovino (solo lectura)

    Los KPIs se generan automáticamente, este ViewSet
    proporciona acceso de consulta y análisis histórico
    """

    queryset = KPIGanadoBovino.objects.all()
    serializer_class = KPIGanadoBovinoSerializer

    def get_queryset(self):
        """Queryset con filtros por fecha"""
        queryset = KPIGanadoBovino.objects.all()

        # Filtro por rango de fechas
        fecha_desde = self.request.query_params.get("fecha_desde")
        if fecha_desde:
            queryset = queryset.filter(fecha__gte=fecha_desde)

        fecha_hasta = self.request.query_params.get("fecha_hasta")
        if fecha_hasta:
            queryset = queryset.filter(fecha__lte=fecha_hasta)

        return queryset.order_by("-fecha")

    @action(detail=False, methods=["get"])
    def ultimos_12_meses(self, request):
        """KPIs de los últimos 12 meses"""
        ahora = timezone.now()
        hace_12_meses = ahora - timedelta(days=365)

        kpis = (
            self.get_queryset()
            .filter(fecha__gte=hace_12_meses.date())
            .order_by("fecha")
        )

        serializer = self.get_serializer(kpis, many=True)

        # Calcular métricas de tendencia
        if len(kpis) >= 2:
            primer_kpi = kpis[0]
            ultimo_kpi = kpis[len(kpis) - 1]

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

        return Response(
            {
                "kpis_12_meses": serializer.data,
                "tendencias_anuales": tendencias,
                "periodo": f'{hace_12_meses.strftime("%Y-%m")} a {ahora.strftime("%Y-%m")}',
                "resumen_estadistico": self._calcular_resumen_estadistico(kpis),
                "meses_completos": len(kpis),
            }
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

    @action(detail=False, methods=["get"])
    def comparativa_trimestral(self, request):
        """Comparativa de KPIs por trimestre"""
        ahora = timezone.now()

        # Calcular últimos 4 trimestres
        trimestres = []
        for i in range(4):
            # Calcular trimestre
            trimestre_actual = ((ahora.month - 1) // 3) + 1
            año_actual = ahora.year

            trimestre = trimestre_actual - i
            año = año_actual

            if trimestre <= 0:
                trimestre += 4
                año -= 1

            # Meses del trimestre
            meses_trimestre = [(trimestre - 1) * 3 + j + 1 for j in range(3)]

            # Obtener KPIs del trimestre
            kpis_trimestre = self.get_queryset().filter(
                fecha__year=año, fecha__month__in=meses_trimestre
            )

            if kpis_trimestre.exists():
                # Agregar métricas del trimestre
                total_marcas = sum(kpi.marcas_registradas_mes for kpi in kpis_trimestre)
                total_cabezas = sum(
                    kpi.total_cabezas_registradas for kpi in kpis_trimestre
                )
                total_ingresos = sum(kpi.ingresos_mes for kpi in kpis_trimestre)
                tiempo_promedio = sum(
                    kpi.tiempo_promedio_procesamiento for kpi in kpis_trimestre
                ) / len(kpis_trimestre)

                # Promedio de tasa de éxito de logos del trimestre
                tasa_logos_promedio = sum(
                    kpi.tasa_exito_logos for kpi in kpis_trimestre
                ) / len(kpis_trimestre)

                trimestres.append(
                    {
                        "trimestre": f"Q{trimestre} {año}",
                        "numero_trimestre": trimestre,
                        "año": año,
                        "total_marcas": total_marcas,
                        "total_cabezas": total_cabezas,
                        "total_ingresos": float(total_ingresos),
                        "tiempo_promedio_procesamiento": round(tiempo_promedio, 2),
                        "tasa_exito_logos_promedio": round(tasa_logos_promedio, 2),
                        "meses_con_datos": len(kpis_trimestre),
                        "eficiencia_trimestral": round(
                            (total_marcas / max(tiempo_promedio, 1)) * 10, 2
                        ),
                    }
                )

        return Response(
            {
                "comparativa_trimestral": list(reversed(trimestres)),
                "mejor_trimestre": {
                    "por_marcas": (
                        max(trimestres, key=lambda x: x["total_marcas"])
                        if trimestres
                        else None
                    ),
                    "por_eficiencia": (
                        max(trimestres, key=lambda x: x["eficiencia_trimestral"])
                        if trimestres
                        else None
                    ),
                    "por_logos": (
                        max(trimestres, key=lambda x: x["tasa_exito_logos_promedio"])
                        if trimestres
                        else None
                    ),
                },
                "crecimiento_interanual": self._calcular_crecimiento_interanual(
                    trimestres
                ),
                "analisis_estacionalidad": self._analizar_estacionalidad_trimestral(
                    trimestres
                ),
            }
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

    @action(detail=False, methods=["get"])
    def analisis_estacional(self, request):
        """Análisis de patrones estacionales en los KPIs"""
        # Obtener datos de los últimos 2 años para identificar patrones
        hace_2_años = timezone.now() - timedelta(days=730)

        kpis = self.get_queryset().filter(fecha__gte=hace_2_años.date())

        # Agrupar por mes del año
        patrones_mensuales = {}
        for mes in range(1, 13):
            kpis_mes = [kpi for kpi in kpis if kpi.fecha.month == mes]

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
            estaciones = self._analizar_por_estaciones(patrones_mensuales)

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
                    "recomendaciones": self._generar_recomendaciones_estacionales(
                        mes_pico[0], mes_valle[0], estaciones
                    ),
                }
            )

        return Response({"mensaje": "Datos insuficientes para análisis estacional"})

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

    @action(detail=False, methods=["get"])
    def kpis_actuales(self, request):
        """KPIs del mes actual y comparación con el anterior"""
        ahora = timezone.now()
        mes_actual = ahora.replace(day=1)
        mes_anterior = (mes_actual - timedelta(days=1)).replace(day=1)

        # KPI del mes actual
        kpi_actual = self.get_queryset().filter(fecha__gte=mes_actual.date()).first()

        # KPI del mes anterior
        kpi_anterior = (
            self.get_queryset()
            .filter(fecha__gte=mes_anterior.date(), fecha__lt=mes_actual.date())
            .first()
        )

        if kpi_actual:
            data_actual = self.get_serializer(kpi_actual).data

            # Comparación con mes anterior
            if kpi_anterior:
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
                        "tendencia": self._determinar_tendencia_cambio(
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
                        "anterior": round(
                            kpi_anterior.tiempo_promedio_procesamiento, 2
                        ),
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
                                        kpi_actual.ingresos_mes
                                        - kpi_anterior.ingresos_mes
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
                analisis_general = self._generar_analisis_mensual(comparacion)

            else:
                comparacion = {"mensaje": "No hay datos del mes anterior para comparar"}
                analisis_general = {
                    "mensaje": "Análisis limitado sin datos de referencia"
                }

            return Response(
                {
                    "kpi_mes_actual": data_actual,
                    "comparacion_mes_anterior": comparacion,
                    "analisis_general": analisis_general,
                    "fecha_actualizacion": kpi_actual.fecha,
                    "alertas": self._generar_alertas_kpi(kpi_actual, kpi_anterior),
                }
            )

        return Response({"mensaje": "No hay KPIs disponibles para el mes actual"})

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
