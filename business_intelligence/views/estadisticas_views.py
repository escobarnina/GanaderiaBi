# business_intelligence/views/estadisticas_views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, Sum, Q, Max, Min, Case, When, FloatField
from django.utils import timezone
from datetime import datetime, timedelta
import calendar

from ..models import MarcaGanadoBovino, LogoMarcaBovina
from ..serializers import (
    EstadisticasPorRazaSerializer,
    EstadisticasPorDepartamentoSerializer,
    RendimientoModelosIASerializer,
)
from ..services import AnalyticsService


class EstadisticasBovinoViewSet(viewsets.ViewSet):
    """
    ViewSet para estadísticas y análisis avanzado de ganado bovino

    Proporciona análisis detallados por:
    - Raza bovina
    - Departamento/región
    - Propósito ganadero
    - Rendimiento de IA
    - Comparativas temporales
    - Predicciones de demanda
    - Análisis de eficiencia
    - Tendencias geográficas
    """

    @action(detail=False, methods=["get"])
    def estadisticas_por_raza(self, request):
        """Análisis completo por raza bovina"""
        # Filtros opcionales
        departamento = request.query_params.get("departamento")
        fecha_desde = request.query_params.get("fecha_desde")
        fecha_hasta = request.query_params.get("fecha_hasta")

        queryset = MarcaGanadoBovino.objects.all()

        if departamento:
            queryset = queryset.filter(departamento=departamento)
        if fecha_desde:
            queryset = queryset.filter(fecha_registro__date__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(fecha_registro__date__lte=fecha_hasta)

        stats = (
            queryset.values("raza_bovino")
            .annotate(
                total_marcas=Count("id"),
                total_cabezas=Sum("cantidad_cabezas"),
                promedio_cabezas=Avg("cantidad_cabezas"),
                monto_promedio=Avg("monto_certificacion"),
                tiempo_promedio_procesamiento=Avg("tiempo_procesamiento_horas"),
                aprobadas=Count("id", filter=Q(estado="APROBADO")),
                rechazadas=Count("id", filter=Q(estado="RECHAZADO")),
                pendientes=Count(
                    "id", filter=Q(estado__in=["PENDIENTE", "EN_PROCESO"])
                ),
                cabezas_maximas=Max("cantidad_cabezas"),
                cabezas_minimas=Min("cantidad_cabezas"),
                ingresos_total=Sum("monto_certificacion", filter=Q(estado="APROBADO")),
            )
            .order_by("-total_cabezas")
        )

        # Enriquecer datos
        for stat in stats:
            total_procesadas = stat["aprobadas"] + stat["rechazadas"]
            stat["porcentaje_aprobacion"] = round(
                (
                    (stat["aprobadas"] / total_procesadas * 100)
                    if total_procesadas > 0
                    else 0
                ),
                2,
            )
            stat["raza_display"] = dict(
                MarcaGanadoBovino._meta.get_field("raza_bovino").choices
            ).get(stat["raza_bovino"], stat["raza_bovino"])

            # Propósito más común para esta raza
            proposito_comun = (
                queryset.filter(raza_bovino=stat["raza_bovino"])
                .values("proposito_ganado")
                .annotate(total=Count("id"))
                .order_by("-total")
                .first()
            )

            stat["proposito_principal"] = (
                proposito_comun["proposito_ganado"] if proposito_comun else None
            )

            # Departamento más común para esta raza
            dept_comun = (
                queryset.filter(raza_bovino=stat["raza_bovino"])
                .values("departamento")
                .annotate(total=Count("id"))
                .order_by("-total")
                .first()
            )

            stat["departamento_principal"] = (
                dept_comun["departamento"] if dept_comun else None
            )

            # Rentabilidad por cabeza
            stat["rentabilidad_por_cabeza"] = round(
                (float(stat["ingresos_total"] or 0) / (stat["total_cabezas"] or 1)), 2
            )

        serializer = EstadisticasPorRazaSerializer(stats, many=True)

        # Análisis adicional
        total_general = queryset.count()
        raza_dominante = stats[0] if stats else None

        return Response(
            {
                "estadisticas_por_raza": serializer.data,
                "resumen_general": {
                    "total_marcas_analizadas": total_general,
                    "total_razas": len(stats),
                    "raza_dominante": (
                        raza_dominante["raza_bovino"] if raza_dominante else None
                    ),
                    "porcentaje_raza_dominante": round(
                        (
                            (raza_dominante["total_marcas"] / total_general * 100)
                            if raza_dominante and total_general > 0
                            else 0
                        ),
                        2,
                    ),
                    "diversidad_genetica": {
                        "indice_diversidad": (
                            round(len(stats) / total_general * 100, 2)
                            if total_general > 0
                            else 0
                        ),
                        "concentracion_top3": (
                            round(
                                sum(s["total_marcas"] for s in stats[:3])
                                / total_general
                                * 100,
                                2,
                            )
                            if total_general > 0 and len(stats) >= 3
                            else 0
                        ),
                    },
                },
                "insights": self._generar_insights_razas(stats, total_general),
                "comparativa_eficiencia": self._comparar_eficiencia_razas(stats),
            }
        )

    @action(detail=False, methods=["get"])
    def estadisticas_por_departamento(self, request):
        """Análisis completo por departamento"""
        # Filtros opcionales
        raza_bovino = request.query_params.get("raza_bovino")
        proposito = request.query_params.get("proposito_ganado")

        queryset = MarcaGanadoBovino.objects.all()

        if raza_bovino:
            queryset = queryset.filter(raza_bovino=raza_bovino)
        if proposito:
            queryset = queryset.filter(proposito_ganado=proposito)

        stats = (
            queryset.values("departamento")
            .annotate(
                total_marcas=Count("id"),
                total_cabezas=Sum("cantidad_cabezas"),
                promedio_cabezas=Avg("cantidad_cabezas"),
                aprobadas=Count("id", filter=Q(estado="APROBADO")),
                rechazadas=Count("id", filter=Q(estado="RECHAZADO")),
                pendientes=Count(
                    "id", filter=Q(estado__in=["PENDIENTE", "EN_PROCESO"])
                ),
                ingresos_total=Sum("monto_certificacion", filter=Q(estado="APROBADO")),
                tiempo_promedio_procesamiento=Avg("tiempo_procesamiento_horas"),
                monto_promedio=Avg("monto_certificacion"),
                productores_unicos=Count("ci_productor", distinct=True),
            )
            .order_by("-total_cabezas")
        )

        # Enriquecer con datos adicionales
        for stat in stats:
            # Display name
            stat["departamento_display"] = dict(
                MarcaGanadoBovino._meta.get_field("departamento").choices
            ).get(stat["departamento"], stat["departamento"])

            # Propósito principal del departamento
            proposito_principal = (
                queryset.filter(departamento=stat["departamento"])
                .values("proposito_ganado")
                .annotate(total=Count("id"))
                .order_by("-total")
                .first()
            )

            stat["proposito_principal"] = (
                proposito_principal["proposito_ganado"] if proposito_principal else None
            )

            # Raza principal del departamento
            raza_principal = (
                queryset.filter(departamento=stat["departamento"])
                .values("raza_bovino")
                .annotate(total=Count("id"))
                .order_by("-total")
                .first()
            )

            stat["raza_principal"] = (
                raza_principal["raza_bovino"] if raza_principal else None
            )

            # Eficiencia del departamento
            total_procesadas = stat["aprobadas"] + stat["rechazadas"]
            tasa_aprobacion = (
                (stat["aprobadas"] / total_procesadas * 100)
                if total_procesadas > 0
                else 0
            )
            tiempo_proc = stat["tiempo_promedio_procesamiento"] or 1

            stat["eficiencia_score"] = round(
                (tasa_aprobacion / max(tiempo_proc, 1)) * 100, 2
            )
            stat["tasa_aprobacion"] = round(tasa_aprobacion, 2)

            # Densidad ganadera (cabezas por marca)
            stat["densidad_ganadera"] = round(
                (
                    (stat["total_cabezas"] / stat["total_marcas"])
                    if stat["total_marcas"] > 0
                    else 0
                ),
                2,
            )

            # Promedio de marcas por productor
            stat["marcas_por_productor"] = round(
                (
                    (stat["total_marcas"] / stat["productores_unicos"])
                    if stat["productores_unicos"] > 0
                    else 0
                ),
                2,
            )

        serializer = EstadisticasPorDepartamentoSerializer(stats, many=True)

        # Ranking de departamentos
        ranking_cabezas = sorted(stats, key=lambda x: x["total_cabezas"], reverse=True)
        ranking_eficiencia = sorted(
            stats, key=lambda x: x["eficiencia_score"], reverse=True
        )
        ranking_productividad = sorted(
            stats, key=lambda x: x["densidad_ganadera"], reverse=True
        )

        return Response(
            {
                "estadisticas_por_departamento": serializer.data,
                "rankings": {
                    "por_cabezas_bovinas": [
                        {
                            "posicion": idx + 1,
                            "departamento": dept["departamento_display"],
                            "cabezas": dept["total_cabezas"],
                            "porcentaje_nacional": round(
                                (
                                    (
                                        dept["total_cabezas"]
                                        / sum(d["total_cabezas"] for d in stats)
                                        * 100
                                    )
                                    if sum(d["total_cabezas"] for d in stats) > 0
                                    else 0
                                ),
                                2,
                            ),
                        }
                        for idx, dept in enumerate(ranking_cabezas[:5])
                    ],
                    "por_eficiencia": [
                        {
                            "posicion": idx + 1,
                            "departamento": dept["departamento_display"],
                            "score": dept["eficiencia_score"],
                            "tasa_aprobacion": dept["tasa_aprobacion"],
                        }
                        for idx, dept in enumerate(ranking_eficiencia[:5])
                    ],
                    "por_productividad": [
                        {
                            "posicion": idx + 1,
                            "departamento": dept["departamento_display"],
                            "cabezas_por_marca": dept["densidad_ganadera"],
                        }
                        for idx, dept in enumerate(ranking_productividad[:5])
                    ],
                },
                "analisis_regional": self._analizar_regiones(stats),
                "mapa_ganadero": self._generar_mapa_ganadero(stats),
            }
        )

    @action(detail=False, methods=["get"])
    def estadisticas_por_proposito(self, request):
        """Análisis por propósito ganadero (carne, leche, doble propósito, reproducción)"""
        stats = (
            MarcaGanadoBovino.objects.values("proposito_ganado")
            .annotate(
                total_marcas=Count("id"),
                total_cabezas=Sum("cantidad_cabezas"),
                promedio_cabezas=Avg("cantidad_cabezas"),
                monto_promedio=Avg("monto_certificacion"),
                ingresos_total=Sum("monto_certificacion", filter=Q(estado="APROBADO")),
                tiempo_promedio=Avg("tiempo_procesamiento_horas"),
                aprobadas=Count("id", filter=Q(estado="APROBADO")),
                rechazadas=Count("id", filter=Q(estado="RECHAZADO")),
                productores_unicos=Count("ci_productor", distinct=True),
            )
            .order_by("-total_cabezas")
        )

        # Calcular tasa de aprobación para cada propósito
        for stat in stats:
            total_procesadas = stat["aprobadas"] + stat["rechazadas"]
            stat["tasa_aprobacion"] = round(
                (
                    (stat["aprobadas"] / total_procesadas * 100)
                    if total_procesadas > 0
                    else 0
                ),
                2,
            )

        # Análisis por departamento para cada propósito
        proposito_por_departamento = {}
        for stat in stats:
            proposito = stat["proposito_ganado"]

            # Top 3 departamentos para este propósito
            top_depts = (
                MarcaGanadoBovino.objects.filter(proposito_ganado=proposito)
                .values("departamento")
                .annotate(total=Count("id"), cabezas=Sum("cantidad_cabezas"))
                .order_by("-cabezas")[:3]
            )

            proposito_por_departamento[proposito] = list(top_depts)

            # Agregar display name
            stat["proposito_display"] = dict(
                MarcaGanadoBovino._meta.get_field("proposito_ganado").choices
            ).get(proposito, proposito)

        # Cálculos adicionales
        total_nacional = sum(stat["total_marcas"] for stat in stats)

        for stat in stats:
            stat["porcentaje_nacional"] = round(
                (
                    (stat["total_marcas"] / total_nacional * 100)
                    if total_nacional > 0
                    else 0
                ),
                2,
            )
            stat["eficiencia_economica"] = round(
                (float(stat["ingresos_total"] or 0) / (stat["total_cabezas"] or 1)), 2
            )

        return Response(
            {
                "estadisticas_por_proposito": list(stats),
                "distribucion_geografica": proposito_por_departamento,
                "analisis_economico": self._analizar_economia_por_proposito(stats),
                "insights_proposito": self._generar_insights_proposito(stats),
                "matriz_proposito_departamento": self._crear_matriz_proposito_departamento(),
            }
        )

    @action(detail=False, methods=["get"])
    def rendimiento_modelos_ia(self, request):
        """Análisis detallado del rendimiento de modelos IA"""
        # Parámetros de filtro
        fecha_desde = request.query_params.get("fecha_desde")
        fecha_hasta = request.query_params.get("fecha_hasta")
        modelo_especifico = request.query_params.get("modelo")

        queryset = LogoMarcaBovina.objects.select_related("marca")

        if fecha_desde:
            queryset = queryset.filter(fecha_generacion__date__gte=fecha_desde)
        if fecha_hasta:
            queryset = queryset.filter(fecha_generacion__date__lte=fecha_hasta)
        if modelo_especifico:
            queryset = queryset.filter(modelo_ia_usado=modelo_especifico)

        stats = (
            queryset.values("modelo_ia_usado")
            .annotate(
                total_generados=Count("id"),
                exitosos=Count("id", filter=Q(exito=True)),
                fallidos=Count("id", filter=Q(exito=False)),
                tiempo_promedio_generacion=Avg("tiempo_generacion_segundos"),
                tiempo_minimo=Min("tiempo_generacion_segundos"),
                tiempo_maximo=Max("tiempo_generacion_segundos"),
                logos_alta_calidad=Count("id", filter=Q(calidad_logo="ALTA")),
                logos_media_calidad=Count("id", filter=Q(calidad_logo="MEDIA")),
                logos_baja_calidad=Count("id", filter=Q(calidad_logo="BAJA")),
            )
            .order_by("-total_generados")
        )

        # Enriquecer datos
        for stat in stats:
            total = stat["total_generados"]
            stat["tasa_exito"] = round(
                (stat["exitosos"] / total * 100) if total > 0 else 0, 2
            )
            stat["porcentaje_alta_calidad"] = round(
                (stat["logos_alta_calidad"] / total * 100) if total > 0 else 0, 2
            )
            stat["tiempo_promedio_formateado"] = (
                f"{stat['tiempo_promedio_generacion']:.1f}s"
            )
            stat["modelo_display"] = dict(
                LogoMarcaBovina._meta.get_field("modelo_ia_usado").choices
            ).get(stat["modelo_ia_usado"], stat["modelo_ia_usado"])

            # Score de rendimiento general (combinación de éxito y calidad)
            stat["score_rendimiento"] = round(
                (stat["tasa_exito"] * 0.6) + (stat["porcentaje_alta_calidad"] * 0.4), 2
            )

            # Eficiencia (calidad/tiempo)
            stat["eficiencia_temporal"] = round(
                (
                    stat["porcentaje_alta_calidad"]
                    / max(stat["tiempo_promedio_generacion"], 1)
                )
                * 100,
                2,
            )

            # Análisis por raza de ganado para este modelo
            razas_modelo = (
                queryset.filter(modelo_ia_usado=stat["modelo_ia_usado"])
                .values("marca__raza_bovino")
                .annotate(
                    total=Count("id"), exitosos_raza=Count("id", filter=Q(exito=True))
                )
                .order_by("-total")[:3]
            )

            stat["mejores_razas"] = [
                {
                    "raza": raza["marca__raza_bovino"],
                    "total": raza["total"],
                    "tasa_exito": round(
                        (
                            (raza["exitosos_raza"] / raza["total"] * 100)
                            if raza["total"] > 0
                            else 0
                        ),
                        2,
                    ),
                }
                for raza in razas_modelo
            ]

        serializer = RendimientoModelosIASerializer(stats, many=True)

        # Análisis de tendencias temporales
        tendencias = self._analizar_tendencias_ia(queryset)

        # Recomendaciones
        recomendaciones = self._generar_recomendaciones_ia(stats)

        # Análisis de correlación con características de marca
        correlaciones = self._analizar_correlaciones_marca_logo(queryset)

        return Response(
            {
                "rendimiento_modelos": serializer.data,
                "ranking_general": sorted(
                    stats, key=lambda x: x["score_rendimiento"], reverse=True
                ),
                "tendencias_temporales": tendencias,
                "recomendaciones": recomendaciones,
                "correlaciones_marca": correlaciones,
                "resumen_general": {
                    "total_logos_analizados": queryset.count(),
                    "tasa_exito_promedio": (
                        round(sum(s["tasa_exito"] for s in stats) / len(stats), 2)
                        if stats
                        else 0
                    ),
                    "tiempo_promedio_general": (
                        round(
                            sum(s["tiempo_promedio_generacion"] for s in stats)
                            / len(stats),
                            2,
                        )
                        if stats
                        else 0
                    ),
                    "modelo_recomendado": (
                        stats[0]["modelo_ia_usado"] if stats else None
                    ),
                },
            }
        )

    @action(detail=False, methods=["get"])
    def comparativa_temporal(self, request):
        """Comparativa entre diferentes períodos temporales"""
        # Parámetros
        periodo = request.query_params.get(
            "periodo", "mensual"
        )  # mensual, trimestral, anual

        if periodo == "mensual":
            return self._comparativa_mensual()
        elif periodo == "trimestral":
            return self._comparativa_trimestral()
        elif periodo == "anual":
            return self._comparativa_anual()
        else:
            return Response(
                {"error": "Período no válido. Use: mensual, trimestral, anual"}
            )

    @action(detail=False, methods=["get"])
    def predicciones_demanda(self, request):
        """Predicciones de demanda basadas en ML y tendencias históricas"""
        # Usar el servicio de analytics para predicciones
        predicciones_base = AnalyticsService.predecir_demanda_mensual()

        # Análisis adicional específico para bovinos
        ahora = timezone.now()

        # Tendencias estacionales
        tendencias_estacionales = []
        for mes in range(1, 13):
            marcas_mes = MarcaGanadoBovino.objects.filter(
                fecha_registro__month=mes
            ).count()

            tendencias_estacionales.append(
                {
                    "mes": calendar.month_name[mes],
                    "mes_numero": mes,
                    "promedio_historico": marcas_mes,
                }
            )

        # Predicciones por departamento
        predicciones_departamento = []
        for dept_code, dept_name in MarcaGanadoBovino._meta.get_field(
            "departamento"
        ).choices:
            marcas_dept_6_meses = MarcaGanadoBovino.objects.filter(
                departamento=dept_code, fecha_registro__gte=ahora - timedelta(days=180)
            ).count()

            # Predicción simple basada en tendencia
            prediccion_dept = int(marcas_dept_6_meses / 6 * 1.1)  # Crecimiento del 10%

            predicciones_departamento.append(
                {
                    "departamento": dept_code,
                    "departamento_display": dept_name,
                    "marcas_ultimos_6_meses": marcas_dept_6_meses,
                    "prediccion_proximo_mes": prediccion_dept,
                }
            )

        # Predicciones por propósito
        predicciones_proposito = []
        for prop_code, prop_name in MarcaGanadoBovino._meta.get_field(
            "proposito_ganado"
        ).choices:
            marcas_prop = MarcaGanadoBovino.objects.filter(
                proposito_ganado=prop_code,
                fecha_registro__gte=ahora - timedelta(days=90),
            ).count()

            predicciones_proposito.append(
                {
                    "proposito": prop_code,
                    "proposito_display": prop_name,
                    "tendencia_3_meses": marcas_prop,
                    "prediccion_crecimiento": round(
                        marcas_prop * 0.08, 0
                    ),  # 8% crecimiento
                }
            )

        return Response(
            {
                "predicciones_generales": predicciones_base,
                "tendencias_estacionales": tendencias_estacionales,
                "predicciones_por_departamento": sorted(
                    predicciones_departamento,
                    key=lambda x: x["prediccion_proximo_mes"],
                    reverse=True,
                ),
                "predicciones_por_proposito": predicciones_proposito,
                "factores_influencia": {
                    "estacionalidad": "Media - Picos en octubre-diciembre",
                    "economia": "Alta - Correlación con precios de ganado",
                    "regulaciones": "Baja - Proceso estable",
                    "tecnologia": "Media - Adopción gradual de IA",
                },
                "recomendaciones_planificacion": self._generar_recomendaciones_planificacion(
                    predicciones_base
                ),
            }
        )

    @action(detail=False, methods=["get"])
    def analisis_eficiencia(self, request):
        """Análisis detallado de eficiencia del sistema por múltiples dimensiones"""
        return Response(AnalyticsService.analizar_eficiencia_regional())

    @action(detail=False, methods=["get"])
    def tendencias_geograficas(self, request):
        """Análisis de tendencias geográficas y migración de patrones ganaderos"""
        # Análisis de crecimiento por departamento en últimos 12 meses
        ahora = timezone.now()
        hace_12_meses = ahora - timedelta(days=365)
        hace_6_meses = ahora - timedelta(days=183)

        tendencias_dept = []

        for dept_code, dept_name in MarcaGanadoBovino._meta.get_field(
            "departamento"
        ).choices:
            # Marcas últimos 6 meses vs anteriores 6 meses
            recientes = MarcaGanadoBovino.objects.filter(
                departamento=dept_code, fecha_registro__gte=hace_6_meses
            ).count()

            anteriores = MarcaGanadoBovino.objects.filter(
                departamento=dept_code,
                fecha_registro__gte=hace_12_meses,
                fecha_registro__lt=hace_6_meses,
            ).count()

            # Calcular crecimiento
            if anteriores > 0:
                crecimiento = round(((recientes - anteriores) / anteriores) * 100, 2)
            else:
                crecimiento = 100 if recientes > 0 else 0

            # Concentración de productores
            productores_unicos = (
                MarcaGanadoBovino.objects.filter(departamento=dept_code)
                .values("ci_productor")
                .distinct()
                .count()
            )

            total_marcas_dept = MarcaGanadoBovino.objects.filter(
                departamento=dept_code
            ).count()

            concentracion = round(
                (
                    (total_marcas_dept / productores_unicos)
                    if productores_unicos > 0
                    else 0
                ),
                2,
            )

            tendencias_dept.append(
                {
                    "departamento": dept_code,
                    "departamento_display": dept_name,
                    "marcas_recientes": recientes,
                    "marcas_anteriores": anteriores,
                    "crecimiento_porcentual": crecimiento,
                    "concentracion_productores": concentracion,
                    "dinamismo": (
                        "alto"
                        if crecimiento > 15
                        else "medio" if crecimiento > 0 else "bajo"
                    ),
                }
            )

        # Análisis de corredores ganaderos (departamentos vecinos con alta actividad)
        corredores = self._identificar_corredores_ganaderos(tendencias_dept)

        # Migración de razas por región
        migracion_razas = self._analizar_migracion_razas()

        return Response(
            {
                "tendencias_departamentales": sorted(
                    tendencias_dept,
                    key=lambda x: x["crecimiento_porcentual"],
                    reverse=True,
                ),
                "corredores_ganaderos": corredores,
                "migracion_razas": migracion_razas,
                "hotspots_crecimiento": [
                    dept
                    for dept in tendencias_dept
                    if dept["crecimiento_porcentual"] > 20
                    and dept["marcas_recientes"] > 10
                ],
                "analisis_concentracion": {
                    "departamentos_alta_concentracion": [
                        dept
                        for dept in tendencias_dept
                        if dept["concentracion_productores"] > 3
                    ],
                    "promedio_concentracion_nacional": round(
                        sum(d["concentracion_productores"] for d in tendencias_dept)
                        / len(tendencias_dept),
                        2,
                    ),
                },
            }
        )

    @action(detail=False, methods=["get"])
    def distribucion_razas(self, request):
        """Análisis detallado de distribución de razas bovinas"""
        # Obtener todas las razas con sus estadísticas
        distribucion = (
            MarcaGanadoBovino.objects.values("raza_bovino")
            .annotate(
                total_marcas=Count("id"),
                total_cabezas=Sum("cantidad_cabezas"),
                departamentos_presencia=Count("departamento", distinct=True),
                propositos_diversos=Count("proposito_ganado", distinct=True),
                promedio_cabezas=Avg("cantidad_cabezas"),
                tasa_aprobacion=Avg(
                    Case(
                        When(estado="APROBADO", then=100),
                        When(estado="RECHAZADO", then=0),
                        default=None,
                        output_field=FloatField(),
                    ),
                    filter=Q(estado__in=["APROBADO", "RECHAZADO"]),
                ),
            )
            .order_by("-total_cabezas")
        )

        # Análisis de diversidad genética
        total_marcas_sistema = MarcaGanadoBovino.objects.count()

        for raza in distribucion:
            raza["porcentaje_mercado"] = round(
                (
                    (raza["total_marcas"] / total_marcas_sistema * 100)
                    if total_marcas_sistema > 0
                    else 0
                ),
                2,
            )
            raza["raza_display"] = dict(
                MarcaGanadoBovino._meta.get_field("raza_bovino").choices
            ).get(raza["raza_bovino"])

            # Adaptabilidad (presencia en múltiples departamentos)
            raza["adaptabilidad_score"] = round(
                (raza["departamentos_presencia"] / 9) * 100,
                2,  # 9 departamentos en Bolivia
            )

            # Versatilidad (múltiples propósitos)
            raza["versatilidad_score"] = round(
                (raza["propositos_diversos"] / 4) * 100, 2  # 4 propósitos disponibles
            )

        # Análisis de concentración
        concentracion_mercado = self._calcular_concentracion_mercado(distribucion)

        # Mapeo geográfico de razas
        mapa_razas = self._crear_mapa_razas_departamentos()

        return Response(
            {
                "distribucion_razas": list(distribucion),
                "analisis_concentracion": concentracion_mercado,
                "mapa_geografico_razas": mapa_razas,
                "recomendaciones_diversificacion": self._generar_recomendaciones_diversificacion(
                    distribucion
                ),
                "insights_geneticos": {
                    "raza_mas_adaptable": (
                        max(distribucion, key=lambda x: x["adaptabilidad_score"])[
                            "raza_bovino"
                        ]
                        if distribucion
                        else None
                    ),
                    "raza_mas_versatil": (
                        max(distribucion, key=lambda x: x["versatilidad_score"])[
                            "raza_bovino"
                        ]
                        if distribucion
                        else None
                    ),
                    "indice_diversidad_nacional": (
                        round(len(distribucion) / total_marcas_sistema * 1000, 2)
                        if total_marcas_sistema > 0
                        else 0
                    ),
                },
            }
        )

    # ==================== MÉTODOS AUXILIARES ====================

    def _generar_insights_razas(self, stats, total_general):
        """Genera insights sobre las razas bovinas"""
        if not stats:
            return []

        insights = []

        # Raza más productiva (más cabezas en promedio)
        raza_productiva = max(stats, key=lambda x: x["promedio_cabezas"] or 0)
        insights.append(
            {
                "tipo": "productividad",
                "prioridad": "alta",
                "mensaje": f"Raza {raza_productiva['raza_display']} es la más productiva con {raza_productiva['promedio_cabezas']:.1f} cabezas promedio por marca.",
                "impacto": "Fomentar esta raza puede aumentar la productividad sectorial",
            }
        )

        # Raza más eficiente (mayor tasa de aprobación)
        raza_eficiente = max(stats, key=lambda x: x["porcentaje_aprobacion"])
        if raza_eficiente["porcentaje_aprobacion"] > 0:
            insights.append(
                {
                    "tipo": "eficiencia",
                    "prioridad": "media",
                    "mensaje": f"Raza {raza_eficiente['raza_display']} tiene la mayor tasa de aprobación ({raza_eficiente['porcentaje_aprobacion']:.1f}%).",
                    "impacto": "Procesos más eficientes para esta raza",
                }
            )

        # Análisis de diversidad
        if len(stats) > 5:
            insights.append(
                {
                    "tipo": "diversidad",
                    "prioridad": "baja",
                    "mensaje": f"Alta diversidad genética detectada: {len(stats)} razas diferentes registradas.",
                    "impacto": "Fortaleza del sector ganadero boliviano",
                }
            )

        # Raza más rentable por cabeza
        raza_rentable = max(stats, key=lambda x: x["rentabilidad_por_cabeza"])
        insights.append(
            {
                "tipo": "rentabilidad",
                "prioridad": "alta",
                "mensaje": f"Raza {raza_rentable['raza_display']} genera Bs. {raza_rentable['rentabilidad_por_cabeza']:.2f} por cabeza.",
                "impacto": "Mayor rentabilidad económica",
            }
        )

        return insights

    def _comparar_eficiencia_razas(self, stats):
        """Compara eficiencia entre razas"""
        if len(stats) < 2:
            return {}

        # Ordenar por eficiencia (tasa aprobación / tiempo procesamiento)
        razas_eficientes = []
        for raza in stats:
            if (
                raza["tiempo_promedio_procesamiento"]
                and raza["tiempo_promedio_procesamiento"] > 0
            ):
                eficiencia = (
                    raza["porcentaje_aprobacion"]
                    / raza["tiempo_promedio_procesamiento"]
                )
                razas_eficientes.append(
                    {
                        "raza": raza["raza_display"],
                        "eficiencia_score": round(
                            eficiencia * 10, 2
                        ),  # Multiplicar por 10 para legibilidad
                        "tasa_aprobacion": raza["porcentaje_aprobacion"],
                        "tiempo_promedio": raza["tiempo_promedio_procesamiento"],
                    }
                )

        razas_eficientes.sort(key=lambda x: x["eficiencia_score"], reverse=True)

        return {
            "ranking_eficiencia": razas_eficientes[:5],
            "mejor_raza": razas_eficientes[0] if razas_eficientes else None,
            "gap_eficiencia": (
                round(
                    razas_eficientes[0]["eficiencia_score"]
                    - razas_eficientes[-1]["eficiencia_score"],
                    2,
                )
                if len(razas_eficientes) > 1
                else 0
            ),
        }

    def _analizar_regiones(self, stats):
        """Análisis regional de la ganadería bovina"""
        if not stats:
            return {}

        total_cabezas_nacional = sum(dept["total_cabezas"] for dept in stats)
        total_marcas_nacional = sum(dept["total_marcas"] for dept in stats)

        # Concentración geográfica
        top_3_departamentos = sorted(
            stats, key=lambda x: x["total_cabezas"], reverse=True
        )[:3]
        concentracion_top3 = sum(dept["total_cabezas"] for dept in top_3_departamentos)
        porcentaje_concentracion = round(
            (
                (concentracion_top3 / total_cabezas_nacional * 100)
                if total_cabezas_nacional > 0
                else 0
            ),
            2,
        )

        # Departamento líder
        lider = top_3_departamentos[0] if top_3_departamentos else None

        # Análisis de equilibrio regional
        coeficiente_gini = self._calcular_gini_departamental(stats)

        return {
            "total_cabezas_nacional": total_cabezas_nacional,
            "total_marcas_nacional": total_marcas_nacional,
            "promedio_cabezas_nacional": (
                round(total_cabezas_nacional / total_marcas_nacional, 2)
                if total_marcas_nacional > 0
                else 0
            ),
            "concentracion_geografica": {
                "porcentaje_top3": porcentaje_concentracion,
                "departamentos_top3": [
                    dept["departamento_display"] for dept in top_3_departamentos
                ],
                "nivel_concentracion": (
                    "alta"
                    if porcentaje_concentracion > 70
                    else "media" if porcentaje_concentracion > 50 else "baja"
                ),
            },
            "departamento_lider": {
                "nombre": lider["departamento_display"] if lider else None,
                "cabezas": lider["total_cabezas"] if lider else 0,
                "porcentaje_nacional": round(
                    (
                        (lider["total_cabezas"] / total_cabezas_nacional * 100)
                        if lider and total_cabezas_nacional > 0
                        else 0
                    ),
                    2,
                ),
                "ventaja_competitiva": lider["proposito_principal"] if lider else None,
            },
            "equilibrio_regional": {
                "coeficiente_gini": coeficiente_gini,
                "interpretacion": (
                    "desigual"
                    if coeficiente_gini > 0.5
                    else "equilibrado" if coeficiente_gini < 0.3 else "moderado"
                ),
            },
        }

    def _generar_mapa_ganadero(self, stats):
        """Genera un mapa conceptual de la ganadería por departamento"""
        mapa = {}

        for dept in stats:
            mapa[dept["departamento"]] = {
                "nombre": dept["departamento_display"],
                "intensidad_ganadera": (
                    "alta"
                    if dept["total_cabezas"] > 10000
                    else "media" if dept["total_cabezas"] > 5000 else "baja"
                ),
                "especializacion": dept["proposito_principal"],
                "raza_predominante": dept["raza_principal"],
                "eficiencia": (
                    "alta"
                    if dept["eficiencia_score"] > 5
                    else "media" if dept["eficiencia_score"] > 2 else "baja"
                ),
                "densidad": dept["densidad_ganadera"],
                "productores": dept["productores_unicos"],
            }

        return mapa

    def _analizar_economia_por_proposito(self, stats):
        """Análisis económico por propósito ganadero"""
        if not stats:
            return {}

        # Propósito más rentable por marca
        mas_rentable = max(stats, key=lambda x: x["monto_promedio"] or 0)

        # Propósito con mayor volumen económico
        mayor_volumen = max(stats, key=lambda x: x["ingresos_total"] or 0)

        # Propósito más eficiente económicamente
        mas_eficiente = max(stats, key=lambda x: x["eficiencia_economica"])

        total_ingresos = sum(float(s["ingresos_total"] or 0) for s in stats)

        return {
            "proposito_mas_rentable_por_marca": {
                "proposito": mas_rentable["proposito_ganado"],
                "monto_promedio": round(float(mas_rentable["monto_promedio"] or 0), 2),
            },
            "proposito_mayor_volumen_total": {
                "proposito": mayor_volumen["proposito_ganado"],
                "ingresos_total": round(float(mayor_volumen["ingresos_total"] or 0), 2),
                "participacion_mercado": round(
                    (
                        (
                            float(mayor_volumen["ingresos_total"] or 0)
                            / total_ingresos
                            * 100
                        )
                        if total_ingresos > 0
                        else 0
                    ),
                    2,
                ),
            },
            "proposito_mas_eficiente": {
                "proposito": mas_eficiente["proposito_ganado"],
                "eficiencia": mas_eficiente["eficiencia_economica"],
            },
            "distribucion_ingresos": [
                {
                    "proposito": stat["proposito_ganado"],
                    "porcentaje_ingresos": round(
                        (
                            (float(stat["ingresos_total"] or 0) / total_ingresos * 100)
                            if total_ingresos > 0
                            else 0
                        ),
                        2,
                    ),
                    "ingresos_absolutos": round(float(stat["ingresos_total"] or 0), 2),
                }
                for stat in stats
            ],
        }

    def _generar_insights_proposito(self, stats):
        """Genera insights sobre propósitos ganaderos"""
        insights = []

        if not stats:
            return insights

        # Propósito dominante
        dominante = max(stats, key=lambda x: x["total_marcas"])
        insights.append(
            {
                "tipo": "dominancia",
                "mensaje": f"El propósito {dominante['proposito_display'].lower()} domina con {dominante['porcentaje_nacional']:.1f}% de las marcas.",
                "recomendacion": "Fortalecer cadenas de valor para este segmento",
            }
        )

        # Propósito más eficiente
        mas_eficiente = max(stats, key=lambda x: x["tasa_aprobacion"] or 0)
        if mas_eficiente["tasa_aprobacion"]:
            insights.append(
                {
                    "tipo": "eficiencia",
                    "mensaje": f"Marcas de {mas_eficiente['proposito_display'].lower()} tienen la mayor tasa de aprobación ({mas_eficiente['tasa_aprobacion']:.1f}%).",
                    "recomendacion": "Aplicar mejores prácticas de este segmento a otros",
                }
            )

        # Análisis de escala
        mayor_escala = max(stats, key=lambda x: x["promedio_cabezas"] or 0)
        insights.append(
            {
                "tipo": "escala",
                "mensaje": f"Operaciones de {mayor_escala['proposito_display'].lower()} son las de mayor escala promedio ({mayor_escala['promedio_cabezas']:.1f} cabezas).",
                "recomendacion": "Promover economías de escala en otros segmentos",
            }
        )

        # Análisis de diversificación
        if len(stats) == 4:  # Todos los propósitos están representados
            insights.append(
                {
                    "tipo": "diversificacion",
                    "mensaje": "Sector ganadero boliviano muestra alta diversificación en propósitos productivos.",
                    "recomendacion": "Mantener y fortalecer esta diversificación",
                }
            )

        return insights

    def _crear_matriz_proposito_departamento(self):
        """Crea matriz de propósitos por departamento"""
        matriz = {}

        for dept_code, dept_name in MarcaGanadoBovino._meta.get_field(
            "departamento"
        ).choices:
            matriz[dept_code] = {"departamento_display": dept_name, "propositos": {}}

            for prop_code, prop_name in MarcaGanadoBovino._meta.get_field(
                "proposito_ganado"
            ).choices:
                count = MarcaGanadoBovino.objects.filter(
                    departamento=dept_code, proposito_ganado=prop_code
                ).count()

                cabezas = (
                    MarcaGanadoBovino.objects.filter(
                        departamento=dept_code, proposito_ganado=prop_code
                    ).aggregate(Sum("cantidad_cabezas"))["cantidad_cabezas__sum"]
                    or 0
                )

                matriz[dept_code]["propositos"][prop_code] = {
                    "proposito_display": prop_name,
                    "marcas": count,
                    "cabezas": cabezas,
                    "relevancia": (
                        "alta" if count > 10 else "media" if count > 5 else "baja"
                    ),
                }

        return matriz

    def _analizar_tendencias_ia(self, queryset):
        """Analiza tendencias temporales de los modelos IA"""
        ahora = timezone.now()
        hace_30_dias = ahora - timedelta(days=30)

        tendencias_semanales = []
        for i in range(4):  # 4 semanas
            inicio_semana = hace_30_dias + timedelta(weeks=i)
            fin_semana = inicio_semana + timedelta(weeks=1)

            logos_semana = queryset.filter(
                fecha_generacion__gte=inicio_semana, fecha_generacion__lt=fin_semana
            )

            total_semana = logos_semana.count()
            exitosos_semana = logos_semana.filter(exito=True).count()
            tiempo_promedio = (
                logos_semana.aggregate(Avg("tiempo_generacion_segundos"))[
                    "tiempo_generacion_segundos__avg"
                ]
                or 0
            )

            tendencias_semanales.append(
                {
                    "semana": f"Semana {i+1}",
                    "total_logos": total_semana,
                    "tasa_exito": round(
                        (
                            (exitosos_semana / total_semana * 100)
                            if total_semana > 0
                            else 0
                        ),
                        2,
                    ),
                    "tiempo_promedio": round(tiempo_promedio, 2),
                    "periodo": f"{inicio_semana.strftime('%d/%m')} - {fin_semana.strftime('%d/%m')}",
                    "mejora_vs_anterior": 0,  # Se calculará después
                }
            )

        # Calcular mejoras semana a semana
        for i in range(1, len(tendencias_semanales)):
            actual = tendencias_semanales[i]["tasa_exito"]
            anterior = tendencias_semanales[i - 1]["tasa_exito"]
            mejora = round(actual - anterior, 2) if anterior > 0 else 0
            tendencias_semanales[i]["mejora_vs_anterior"] = mejora

        return tendencias_semanales

    def _generar_recomendaciones_ia(self, stats):
        """Genera recomendaciones para optimizar el uso de IA"""
        recomendaciones = []

        if not stats:
            return recomendaciones

        # Modelo más eficiente
        mejor_modelo = max(stats, key=lambda x: x["score_rendimiento"])
        recomendaciones.append(
            {
                "tipo": "optimizacion",
                "prioridad": "alta",
                "mensaje": f"Priorizar uso de {mejor_modelo['modelo_display']} (score: {mejor_modelo['score_rendimiento']:.1f})",
                "impacto_estimado": "Mejora del 15-25% en calidad de logos",
            }
        )

        # Modelos con bajo rendimiento
        modelos_mejora = [m for m in stats if m["tasa_exito"] < 70]
        if modelos_mejora:
            recomendaciones.append(
                {
                    "tipo": "mejora",
                    "prioridad": "media",
                    "mensaje": f"{len(modelos_mejora)} modelos requieren optimización de prompts o configuración",
                    "acciones": [
                        "Revisar prompts",
                        "Ajustar parámetros",
                        "Entrenar con datos específicos de bovinos",
                    ],
                }
            )

        # Análisis de tiempos
        modelo_rapido = min(stats, key=lambda x: x["tiempo_promedio_generacion"])
        modelo_lento = max(stats, key=lambda x: x["tiempo_promedio_generacion"])

        if (
            modelo_lento["tiempo_promedio_generacion"]
            > modelo_rapido["tiempo_promedio_generacion"] * 2
        ):
            recomendaciones.append(
                {
                    "tipo": "rendimiento",
                    "prioridad": "baja",
                    "mensaje": f"Considerar reemplazar {modelo_lento['modelo_display']} por alternativas más rápidas en casos no críticos",
                    "ahorro_tiempo": f"{modelo_lento['tiempo_promedio_generacion'] - modelo_rapido['tiempo_promedio_generacion']:.1f}s por logo",
                }
            )

        # Recomendaciones por especialización
        if len(stats) > 2:
            modelo_calidad = max(stats, key=lambda x: x["porcentaje_alta_calidad"])
            recomendaciones.append(
                {
                    "tipo": "especializacion",
                    "prioridad": "media",
                    "mensaje": f"Usar {modelo_calidad['modelo_display']} para casos que requieren máxima calidad visual",
                    "casos_uso": ["Marcas premium", "Exportación", "Eventos oficiales"],
                }
            )

        return recomendaciones

    def _analizar_correlaciones_marca_logo(self, queryset):
        """Analiza correlaciones entre características de marca y éxito de logos"""
        correlaciones = {}

        # Correlación con raza bovina
        por_raza = (
            queryset.values("marca__raza_bovino")
            .annotate(
                total=Count("id"),
                exitosos=Count("id", filter=Q(exito=True)),
                tiempo_promedio=Avg("tiempo_generacion_segundos"),
            )
            .order_by("-exitosos")
        )

        correlaciones["por_raza"] = [
            {
                "raza": item["marca__raza_bovino"],
                "tasa_exito": round(
                    (
                        (item["exitosos"] / item["total"] * 100)
                        if item["total"] > 0
                        else 0
                    ),
                    2,
                ),
                "total_logos": item["total"],
                "tiempo_promedio": round(item["tiempo_promedio"] or 0, 2),
            }
            for item in por_raza
            if item["total"] >= 5  # Solo razas con suficientes datos
        ]

        # Correlación con propósito
        por_proposito = queryset.values("marca__proposito_ganado").annotate(
            total=Count("id"), exitosos=Count("id", filter=Q(exito=True))
        )

        correlaciones["por_proposito"] = [
            {
                "proposito": item["marca__proposito_ganado"],
                "tasa_exito": round(
                    (
                        (item["exitosos"] / item["total"] * 100)
                        if item["total"] > 0
                        else 0
                    ),
                    2,
                ),
                "total_logos": item["total"],
            }
            for item in por_proposito
        ]

        # Correlación con tamaño de operación
        correlaciones["por_tamaño_operacion"] = self._analizar_por_tamaño_operacion(
            queryset
        )

        return correlaciones

    def _analizar_por_tamaño_operacion(self, queryset):
        """Analiza éxito de logos por tamaño de operación ganadera"""
        # Definir rangos de tamaño
        rangos = [
            ("pequeña", 1, 50),
            ("mediana", 51, 200),
            ("grande", 201, 1000),
            ("muy_grande", 1001, 10000),
        ]

        resultados = []

        for nombre, min_cabezas, max_cabezas in rangos:
            logos_rango = queryset.filter(
                marca__cantidad_cabezas__gte=min_cabezas,
                marca__cantidad_cabezas__lte=max_cabezas,
            )

            total = logos_rango.count()
            exitosos = logos_rango.filter(exito=True).count()

            if total > 0:
                resultados.append(
                    {
                        "tamaño_operacion": nombre,
                        "rango_cabezas": f"{min_cabezas}-{max_cabezas}",
                        "total_logos": total,
                        "tasa_exito": round((exitosos / total * 100), 2),
                        "tiempo_promedio": round(
                            logos_rango.aggregate(Avg("tiempo_generacion_segundos"))[
                                "tiempo_generacion_segundos__avg"
                            ]
                            or 0,
                            2,
                        ),
                    }
                )

        return resultados

    def _comparativa_mensual(self):
        """Comparativa de los últimos 6 meses"""
        ahora = timezone.now()
        meses_data = []

        for i in range(6):
            # Calcular primer día del mes
            if ahora.month - i > 0:
                mes_inicio = ahora.replace(
                    month=ahora.month - i,
                    day=1,
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0,
                )
            else:
                año_anterior = ahora.year - 1
                mes_anterior = 12 + (ahora.month - i)
                mes_inicio = ahora.replace(
                    year=año_anterior,
                    month=mes_anterior,
                    day=1,
                    hour=0,
                    minute=0,
                    second=0,
                    microsecond=0,
                )

            # Calcular primer día del siguiente mes
            if mes_inicio.month == 12:
                mes_fin = mes_inicio.replace(year=mes_inicio.year + 1, month=1)
            else:
                mes_fin = mes_inicio.replace(month=mes_inicio.month + 1)

            marcas_mes = MarcaGanadoBovino.objects.filter(
                fecha_registro__gte=mes_inicio, fecha_registro__lt=mes_fin
            )

            # Estadísticas del mes
            ingresos_mes = (
                marcas_mes.filter(estado="APROBADO").aggregate(
                    Sum("monto_certificacion")
                )["monto_certificacion__sum"]
                or 0
            )

            tiempo_prom = (
                marcas_mes.filter(tiempo_procesamiento_horas__isnull=False).aggregate(
                    Avg("tiempo_procesamiento_horas")
                )["tiempo_procesamiento_horas__avg"]
                or 0
            )

            # Distribución por propósito
            distribucion_proposito = (
                marcas_mes.values("proposito_ganado")
                .annotate(total=Count("id"))
                .order_by("-total")
            )

            proposito_principal = (
                distribucion_proposito.first()["proposito_ganado"]
                if distribucion_proposito
                else None
            )

            meses_data.append(
                {
                    "periodo": f"{calendar.month_name[mes_inicio.month]} {mes_inicio.year}",
                    "año": mes_inicio.year,
                    "mes": mes_inicio.month,
                    "marcas_registradas": marcas_mes.count(),
                    "cabezas_registradas": marcas_mes.aggregate(
                        Sum("cantidad_cabezas")
                    )["cantidad_cabezas__sum"]
                    or 0,
                    "ingresos": round(float(ingresos_mes), 2),
                    "tiempo_promedio_procesamiento": round(tiempo_prom, 2),
                    "proposito_principal": proposito_principal,
                    "eficiencia_mensual": (
                        round((marcas_mes.count() / max(tiempo_prom, 1)) * 10, 2)
                        if tiempo_prom > 0
                        else 0
                    ),
                }
            )

        # Ordenar cronológicamente (más antiguo primero)
        meses_data.reverse()

        return Response(
            {
                "tipo_comparativa": "mensual",
                "periodos": meses_data,
                "tendencias": self._calcular_tendencias(meses_data),
                "analisis_estacional": self._analizar_estacionalidad(meses_data),
                "metricas_promedio": {
                    "marcas_promedio_mensual": round(
                        sum(m["marcas_registradas"] for m in meses_data)
                        / len(meses_data),
                        2,
                    ),
                    "cabezas_promedio_mensual": round(
                        sum(m["cabezas_registradas"] for m in meses_data)
                        / len(meses_data),
                        2,
                    ),
                    "ingresos_promedio_mensual": round(
                        sum(m["ingresos"] for m in meses_data) / len(meses_data), 2
                    ),
                },
            }
        )

    def _comparativa_trimestral(self):
        """Comparativa de los últimos 4 trimestres"""
        ahora = timezone.now()
        trimestres_data = []

        for i in range(4):
            # Calcular trimestre y año
            trimestre_actual = ((ahora.month - 1) // 3) + 1
            año_actual = ahora.year

            trimestre = trimestre_actual - i
            año = año_actual

            if trimestre <= 0:
                trimestre += 4
                año -= 1

            # Fechas del trimestre
            mes_inicio = (trimestre - 1) * 3 + 1
            mes_fin = trimestre * 3

            inicio_periodo = datetime(año, mes_inicio, 1)

            if mes_fin == 12:
                fin_periodo = datetime(año + 1, 1, 1)
            else:
                fin_periodo = datetime(año, mes_fin + 1, 1)

            marcas_trimestre = MarcaGanadoBovino.objects.filter(
                fecha_registro__gte=inicio_periodo, fecha_registro__lt=fin_periodo
            )

            # Análisis departamental del trimestre
            top_departamento = (
                marcas_trimestre.values("departamento")
                .annotate(total=Count("id"))
                .order_by("-total")
                .first()
            )

            # Análisis de eficiencia trimestral
            aprobadas = marcas_trimestre.filter(estado="APROBADO").count()
            rechazadas = marcas_trimestre.filter(estado="RECHAZADO").count()
            total_procesadas = aprobadas + rechazadas

            trimestres_data.append(
                {
                    "periodo": f"Q{trimestre} {año}",
                    "trimestre": trimestre,
                    "año": año,
                    "marcas_registradas": marcas_trimestre.count(),
                    "cabezas_registradas": marcas_trimestre.aggregate(
                        Sum("cantidad_cabezas")
                    )["cantidad_cabezas__sum"]
                    or 0,
                    "ingresos": round(
                        float(
                            marcas_trimestre.filter(estado="APROBADO").aggregate(
                                Sum("monto_certificacion")
                            )["monto_certificacion__sum"]
                            or 0
                        ),
                        2,
                    ),
                    "tasa_aprobacion": round(
                        (
                            (aprobadas / total_procesadas * 100)
                            if total_procesadas > 0
                            else 0
                        ),
                        2,
                    ),
                    "departamento_lider": (
                        top_departamento["departamento"] if top_departamento else None
                    ),
                    "marcas_departamento_lider": (
                        top_departamento["total"] if top_departamento else 0
                    ),
                }
            )

        # Ordenar cronológicamente
        trimestres_data.reverse()

        return Response(
            {
                "tipo_comparativa": "trimestral",
                "periodos": trimestres_data,
                "tendencias": self._calcular_tendencias(trimestres_data),
                "analisis_crecimiento": {
                    "mejor_trimestre": max(
                        trimestres_data, key=lambda x: x["marcas_registradas"]
                    ),
                    "trimestre_mas_eficiente": max(
                        trimestres_data, key=lambda x: x["tasa_aprobacion"]
                    ),
                    "crecimiento_anual": self._calcular_crecimiento_anual_trimestral(
                        trimestres_data
                    ),
                },
            }
        )

    def _comparativa_anual(self):
        """Comparativa de los últimos 3 años"""
        ahora = timezone.now()
        años_data = []

        for i in range(3):
            año = ahora.year - i
            inicio_año = datetime(año, 1, 1)
            fin_año = datetime(año + 1, 1, 1)

            marcas_año = MarcaGanadoBovino.objects.filter(
                fecha_registro__gte=inicio_año, fecha_registro__lt=fin_año
            )

            # Análisis detallado del año
            total_marcas = marcas_año.count()
            total_cabezas = (
                marcas_año.aggregate(Sum("cantidad_cabezas"))["cantidad_cabezas__sum"]
                or 0
            )
            ingresos_año = (
                marcas_año.filter(estado="APROBADO").aggregate(
                    Sum("monto_certificacion")
                )["monto_certificacion__sum"]
                or 0
            )

            # Diversidad del año
            departamentos_activos = marcas_año.values("departamento").distinct().count()
            razas_registradas = marcas_año.values("raza_bovino").distinct().count()
            productores_unicos = marcas_año.values("ci_productor").distinct().count()

            # Eficiencia anual
            aprobadas = marcas_año.filter(estado="APROBADO").count()
            rechazadas = marcas_año.filter(estado="RECHAZADO").count()
            total_procesadas = aprobadas + rechazadas

            años_data.append(
                {
                    "periodo": str(año),
                    "año": año,
                    "marcas_registradas": total_marcas,
                    "cabezas_registradas": total_cabezas,
                    "ingresos": round(float(ingresos_año), 2),
                    "departamentos_activos": departamentos_activos,
                    "razas_registradas": razas_registradas,
                    "productores_unicos": productores_unicos,
                    "tasa_aprobacion": round(
                        (
                            (aprobadas / total_procesadas * 100)
                            if total_procesadas > 0
                            else 0
                        ),
                        2,
                    ),
                    "promedio_cabezas": round(
                        (total_cabezas / total_marcas) if total_marcas > 0 else 0, 2
                    ),
                    "ingreso_promedio_marca": round(
                        (float(ingresos_año) / aprobadas) if aprobadas > 0 else 0, 2
                    ),
                }
            )

        # Ordenar cronológicamente
        años_data.reverse()

        return Response(
            {
                "tipo_comparativa": "anual",
                "periodos": años_data,
                "tendencias": self._calcular_tendencias(años_data),
                "analisis_crecimiento": self._analizar_crecimiento_anual(años_data),
                "evolucion_sector": {
                    "diversificacion_geografica": self._analizar_diversificacion_geografica(
                        años_data
                    ),
                    "evolucion_tecnologica": self._analizar_evolucion_tecnologica(
                        años_data
                    ),
                    "profesionalizacion": self._analizar_profesionalizacion(años_data),
                },
            }
        )

    def _calcular_tendencias(self, datos):
        """Calcula tendencias básicas de los datos"""
        if len(datos) < 2:
            return {"tendencia_marcas": "insuficiente_datos"}

        # Tendencia de marcas (comparar último vs anterior)
        ultimo = datos[-1]
        anterior = datos[-2]

        cambio_marcas = ultimo["marcas_registradas"] - anterior["marcas_registradas"]
        cambio_porcentual = (
            (cambio_marcas / anterior["marcas_registradas"] * 100)
            if anterior["marcas_registradas"] > 0
            else 0
        )

        # Clasificar tendencia
        if cambio_porcentual > 10:
            tendencia_marcas = "crecimiento_fuerte"
        elif cambio_porcentual > 5:
            tendencia_marcas = "crecimiento_moderado"
        elif cambio_porcentual > -5:
            tendencia_marcas = "estable"
        elif cambio_porcentual > -10:
            tendencia_marcas = "decrecimiento_moderado"
        else:
            tendencia_marcas = "decrecimiento_fuerte"

        # Tendencia de cabezas si está disponible
        tendencia_cabezas = "no_disponible"
        if "cabezas_registradas" in ultimo and "cabezas_registradas" in anterior:
            cambio_cabezas = (
                ultimo["cabezas_registradas"] - anterior["cabezas_registradas"]
            )
            cambio_cabezas_pct = (
                (cambio_cabezas / anterior["cabezas_registradas"] * 100)
                if anterior["cabezas_registradas"] > 0
                else 0
            )

            if cambio_cabezas_pct > 5:
                tendencia_cabezas = "crecimiento"
            elif cambio_cabezas_pct < -5:
                tendencia_cabezas = "decrecimiento"
            else:
                tendencia_cabezas = "estable"

        return {
            "tendencia_marcas": tendencia_marcas,
            "cambio_porcentual": round(cambio_porcentual, 2),
            "cambio_absoluto": cambio_marcas,
            "tendencia_cabezas": tendencia_cabezas,
            "direccion_general": (
                "positiva"
                if cambio_porcentual > 0
                else "negativa" if cambio_porcentual < 0 else "neutral"
            ),
            "volatilidad": self._calcular_volatilidad(datos),
        }

    def _analizar_crecimiento_anual(self, años_data):
        """Análisis específico de crecimiento anual"""
        if len(años_data) < 2:
            return {}

        # Calcular CAGR (Compound Annual Growth Rate)
        primer_año = años_data[0]
        ultimo_año = años_data[-1]
        años_transcurridos = len(años_data) - 1

        if primer_año["marcas_registradas"] > 0:
            cagr = (
                (ultimo_año["marcas_registradas"] / primer_año["marcas_registradas"])
                ** (1 / años_transcurridos)
                - 1
            ) * 100
        else:
            cagr = 0

        # CAGR para cabezas
        cagr_cabezas = 0
        if primer_año["cabezas_registradas"] > 0:
            cagr_cabezas = (
                (ultimo_año["cabezas_registradas"] / primer_año["cabezas_registradas"])
                ** (1 / años_transcurridos)
                - 1
            ) * 100

        # Análisis de aceleración/desaceleración
        if len(años_data) >= 3:
            primera_mitad = años_data[: len(años_data) // 2]
            segunda_mitad = años_data[len(años_data) // 2 :]

            crecimiento_primera = sum(
                año["marcas_registradas"] for año in primera_mitad
            )
            crecimiento_segunda = sum(
                año["marcas_registradas"] for año in segunda_mitad
            )

            aceleracion = (
                "acelerando"
                if crecimiento_segunda > crecimiento_primera
                else "desacelerando"
            )
        else:
            aceleracion = "insuficientes_datos"

        return {
            "cagr_marcas": round(cagr, 2),
            "cagr_cabezas": round(cagr_cabezas, 2),
            "crecimiento_total_marcas": ultimo_año["marcas_registradas"]
            - primer_año["marcas_registradas"],
            "crecimiento_total_cabezas": ultimo_año["cabezas_registradas"]
            - primer_año["cabezas_registradas"],
            "mejor_año": max(años_data, key=lambda x: x["marcas_registradas"])[
                "periodo"
            ],
            "año_mas_eficiente": max(
                años_data, key=lambda x: x.get("tasa_aprobacion", 0)
            )["periodo"],
            "tendencia_general": (
                "positiva" if cagr > 2 else "negativa" if cagr < -2 else "estable"
            ),
            "aceleracion": aceleracion,
            "proyeccion_siguiente_año": (
                int(ultimo_año["marcas_registradas"] * (1 + cagr / 100))
                if cagr != 0
                else ultimo_año["marcas_registradas"]
            ),
        }

    def _analizar_estacionalidad(self, meses_data):
        """Analiza patrones estacionales en los datos mensuales"""
        if len(meses_data) < 6:
            return {"disponible": False}

        # Agrupar por trimestre
        por_trimestre = {}
        for mes in meses_data:
            trimestre = f"Q{((mes['mes'] - 1) // 3) + 1}"
            if trimestre not in por_trimestre:
                por_trimestre[trimestre] = []
            por_trimestre[trimestre].append(mes["marcas_registradas"])

        # Calcular promedios por trimestre
        promedios_trimestre = {}
        for trimestre, valores in por_trimestre.items():
            promedios_trimestre[trimestre] = round(sum(valores) / len(valores), 2)

        # Identificar estación pico y valle
        if promedios_trimestre:
            trimestre_pico = max(promedios_trimestre, key=promedios_trimestre.get)
            trimestre_valle = min(promedios_trimestre, key=promedios_trimestre.get)

            variacion_estacional = (
                round(
                    (
                        (
                            promedios_trimestre[trimestre_pico]
                            - promedios_trimestre[trimestre_valle]
                        )
                        / promedios_trimestre[trimestre_valle]
                        * 100
                    ),
                    2,
                )
                if promedios_trimestre[trimestre_valle] > 0
                else 0
            )
        else:
            trimestre_pico = trimestre_valle = None
            variacion_estacional = 0

        return {
            "disponible": True,
            "promedios_por_trimestre": promedios_trimestre,
            "trimestre_pico": trimestre_pico,
            "trimestre_valle": trimestre_valle,
            "variacion_estacional_porcentaje": variacion_estacional,
            "estacionalidad": (
                "alta"
                if variacion_estacional > 30
                else "media" if variacion_estacional > 15 else "baja"
            ),
        }

    def _calcular_volatilidad(self, datos):
        """Calcula la volatilidad de los datos"""
        if len(datos) < 3:
            return "insuficientes_datos"

        valores = [periodo["marcas_registradas"] for periodo in datos]
        promedio = sum(valores) / len(valores)

        # Calcular desviación estándar
        varianza = sum((x - promedio) ** 2 for x in valores) / len(valores)
        desviacion = varianza**0.5

        # Coeficiente de variación
        coef_variacion = (desviacion / promedio * 100) if promedio > 0 else 0

        if coef_variacion < 10:
            return "baja"
        elif coef_variacion < 25:
            return "media"
        else:
            return "alta"

    def _calcular_crecimiento_anual_trimestral(self, trimestres_data):
        """Calcula crecimiento anual comparando trimestres del mismo año"""
        if len(trimestres_data) < 4:
            return "insuficientes_datos"

        # Buscar trimestres del mismo número en años diferentes
        q1_actual = next((t for t in trimestres_data if t["trimestre"] == 1), None)
        q1_anterior = next(
            (
                t
                for t in trimestres_data
                if t["trimestre"] == 1 and t["año"] == q1_actual["año"] - 1
            ),
            None,
        )

        if q1_actual and q1_anterior:
            crecimiento = (
                round(
                    (
                        (
                            q1_actual["marcas_registradas"]
                            - q1_anterior["marcas_registradas"]
                        )
                        / q1_anterior["marcas_registradas"]
                        * 100
                    ),
                    2,
                )
                if q1_anterior["marcas_registradas"] > 0
                else 0
            )

            return {
                "crecimiento_q1": crecimiento,
                "interpretacion": (
                    "positivo"
                    if crecimiento > 0
                    else "negativo" if crecimiento < 0 else "estable"
                ),
            }

        return "datos_incompletos"

    def _generar_recomendaciones_planificacion(self, predicciones_base):
        """Genera recomendaciones para planificación basadas en predicciones"""
        recomendaciones = []

        confianza = predicciones_base.get("confianza", "Baja")
        prediccion_marcas = predicciones_base.get("prediccion_marcas", 0)

        if confianza == "Alta" and prediccion_marcas > 100:
            recomendaciones.append(
                {
                    "categoria": "capacidad",
                    "prioridad": "alta",
                    "recomendacion": f"Preparar capacidad para procesar {prediccion_marcas} marcas el próximo mes",
                    "acciones": [
                        "Asignar más evaluadores",
                        "Optimizar procesos",
                        "Preparar infraestructura",
                    ],
                }
            )

        if prediccion_marcas < 50:
            recomendaciones.append(
                {
                    "categoria": "promocion",
                    "prioridad": "media",
                    "recomendacion": "Implementar campaña promocional para incrementar registros",
                    "acciones": [
                        "Marketing dirigido",
                        "Incentivos especiales",
                        "Visitas a productores",
                    ],
                }
            )

        if confianza == "Baja":
            recomendaciones.append(
                {
                    "categoria": "datos",
                    "prioridad": "baja",
                    "recomendacion": "Mejorar recolección de datos para predicciones más precisas",
                    "acciones": [
                        "Ampliar histórico",
                        "Mejorar calidad datos",
                        "Implementar más variables",
                    ],
                }
            )

        return recomendaciones

    def _identificar_corredores_ganaderos(self, tendencias_dept):
        """Identifica corredores ganaderos entre departamentos"""
        # Simplificado: departamentos vecinos con alta actividad
        corredores = [
            {
                "nombre": "Corredor Oriental",
                "departamentos": ["SANTA_CRUZ", "BENI"],
                "caracteristicas": "Alta actividad en ganado de carne",
                "intensidad": "alta",
            },
            {
                "nombre": "Corredor Andino",
                "departamentos": ["LA_PAZ", "COCHABAMBA"],
                "caracteristicas": "Enfoque en ganado lechero y doble propósito",
                "intensidad": "media",
            },
            {
                "nombre": "Corredor Sur",
                "departamentos": ["TARIJA", "CHUQUISACA"],
                "caracteristicas": "Ganadería diversificada",
                "intensidad": "media",
            },
        ]

        # Calcular intensidad real basada en datos
        for corredor in corredores:
            actividad_total = sum(
                next(
                    (
                        d["marcas_recientes"]
                        for d in tendencias_dept
                        if d["departamento"] == dept
                    ),
                    0,
                )
                for dept in corredor["departamentos"]
            )

            if actividad_total > 200:
                corredor["intensidad_real"] = "alta"
            elif actividad_total > 100:
                corredor["intensidad_real"] = "media"
            else:
                corredor["intensidad_real"] = "baja"

            corredor["actividad_total"] = actividad_total

        return corredores

    def _analizar_migracion_razas(self):
        """Analiza migración de razas entre departamentos"""
        # Comparar últimos 6 meses vs anteriores 6 meses
        ahora = timezone.now()
        hace_6_meses = ahora - timedelta(days=183)
        hace_12_meses = ahora - timedelta(days=365)

        migracion = {}

        for raza_code, raza_name in MarcaGanadoBovino._meta.get_field(
            "raza_bovino"
        ).choices:
            # Distribución reciente
            reciente = (
                MarcaGanadoBovino.objects.filter(
                    raza_bovino=raza_code, fecha_registro__gte=hace_6_meses
                )
                .values("departamento")
                .annotate(total=Count("id"))
                .order_by("-total")
            )

            # Distribución anterior
            anterior = (
                MarcaGanadoBovino.objects.filter(
                    raza_bovino=raza_code,
                    fecha_registro__gte=hace_12_meses,
                    fecha_registro__lt=hace_6_meses,
                )
                .values("departamento")
                .annotate(total=Count("id"))
                .order_by("-total")
            )

            # Detectar cambios significativos
            cambios = []
            for dept_reciente in reciente:
                dept_code = dept_reciente["departamento"]
                total_reciente = dept_reciente["total"]

                dept_anterior_data = next(
                    (d for d in anterior if d["departamento"] == dept_code),
                    {"total": 0},
                )
                total_anterior = dept_anterior_data["total"]

                if total_anterior > 0:
                    cambio_pct = (
                        (total_reciente - total_anterior) / total_anterior
                    ) * 100
                    if (
                        abs(cambio_pct) > 50 and total_reciente >= 5
                    ):  # Cambio significativo
                        cambios.append(
                            {
                                "departamento": dept_code,
                                "cambio_porcentual": round(cambio_pct, 2),
                                "total_reciente": total_reciente,
                                "total_anterior": total_anterior,
                            }
                        )

            if cambios:
                migracion[raza_code] = {
                    "raza_display": raza_name,
                    "cambios_significativos": cambios,
                }

        return migracion

    def _calcular_concentracion_mercado(self, distribucion):
        """Calcula índices de concentración del mercado por razas"""
        total_marcas = sum(raza["total_marcas"] for raza in distribucion)

        if total_marcas == 0:
            return {}

        # Índice Herfindahl-Hirschman (HHI)
        hhi = (
            sum((raza["total_marcas"] / total_marcas) ** 2 for raza in distribucion)
            * 10000
        )

        # Concentración Top 3
        top_3 = sorted(distribucion, key=lambda x: x["total_marcas"], reverse=True)[:3]
        concentracion_top3 = (
            sum(raza["total_marcas"] for raza in top_3) / total_marcas * 100
        )

        # Interpretación
        if hhi < 1500:
            competencia = "alta_competencia"
        elif hhi < 2500:
            competencia = "competencia_moderada"
        else:
            competencia = "alta_concentracion"

        return {
            "indice_hhi": round(hhi, 2),
            "concentracion_top3_porcentaje": round(concentracion_top3, 2),
            "nivel_competencia": competencia,
            "razas_dominantes": [raza["raza_bovino"] for raza in top_3],
            "diversidad_efectiva": round(
                1
                / sum(
                    (raza["total_marcas"] / total_marcas) ** 2 for raza in distribucion
                ),
                2,
            ),
        }

    def _crear_mapa_razas_departamentos(self):
        """Crea mapa de distribución de razas por departamento"""
        mapa = {}

        for dept_code, dept_name in MarcaGanadoBovino._meta.get_field(
            "departamento"
        ).choices:
            razas_dept = (
                MarcaGanadoBovino.objects.filter(departamento=dept_code)
                .values("raza_bovino")
                .annotate(total=Count("id"), cabezas=Sum("cantidad_cabezas"))
                .order_by("-total")
            )

            if razas_dept:
                mapa[dept_code] = {
                    "departamento_display": dept_name,
                    "raza_principal": razas_dept[0]["raza_bovino"],
                    "marcas_raza_principal": razas_dept[0]["total"],
                    "diversidad_razas": len(razas_dept),
                    "top_3_razas": [
                        {
                            "raza": raza["raza_bovino"],
                            "total": raza["total"],
                            "cabezas": raza["cabezas"],
                        }
                        for raza in razas_dept[:3]
                    ],
                }

        return mapa

    def _generar_recomendaciones_diversificacion(self, distribucion):
        """Genera recomendaciones para diversificación de razas"""
        recomendaciones = []

        total_razas = len(distribucion)
        total_marcas = sum(raza["total_marcas"] for raza in distribucion)

        # Analizar concentración
        raza_dominante = max(distribucion, key=lambda x: x["total_marcas"])
        porcentaje_dominante = (
            (raza_dominante["total_marcas"] / total_marcas * 100)
            if total_marcas > 0
            else 0
        )

        if porcentaje_dominante > 60:
            recomendaciones.append(
                {
                    "tipo": "diversificacion",
                    "prioridad": "alta",
                    "mensaje": f"Alta concentración en raza {raza_dominante['raza_display']} ({porcentaje_dominante:.1f}%)",
                    "accion": "Promover diversificación genética para reducir riesgos",
                }
            )

        # Razas con potencial
        razas_potencial = [
            raza
            for raza in distribucion
            if raza["adaptabilidad_score"] > 70 and raza["total_marcas"] < 50
        ]
        if razas_potencial:
            recomendaciones.append(
                {
                    "tipo": "oportunidad",
                    "prioridad": "media",
                    "mensaje": f"{len(razas_potencial)} razas con alto potencial de adaptación sub-utilizadas",
                    "razas_recomendadas": [
                        raza["raza_bovino"] for raza in razas_potencial
                    ],
                }
            )

        # Diversidad geográfica
        if total_razas > 8:
            recomendaciones.append(
                {
                    "tipo": "fortaleza",
                    "prioridad": "baja",
                    "mensaje": f"Excelente diversidad genética con {total_razas} razas registradas",
                    "accion": "Mantener y fortalecer esta diversidad",
                }
            )

        return recomendaciones

    def _calcular_gini_departamental(self, stats):
        """Calcula coeficiente de Gini para distribución departamental"""
        if not stats:
            return 0

        cabezas = [dept["total_cabezas"] for dept in stats]
        cabezas.sort()

        n = len(cabezas)
        suma_total = sum(cabezas)

        if suma_total == 0:
            return 0

        # Fórmula del coeficiente de Gini
        suma_ponderada = sum((2 * i - n - 1) * x for i, x in enumerate(cabezas, 1))
        gini = suma_ponderada / (n * suma_total)

        return round(gini, 3)

    def _analizar_diversificacion_geografica(self, años_data):
        """Analiza evolución de diversificación geográfica"""
        if len(años_data) < 2:
            return {}

        primer_año = años_data[0]
        ultimo_año = años_data[-1]

        return {
            "departamentos_activos_inicial": primer_año["departamentos_activos"],
            "departamentos_activos_actual": ultimo_año["departamentos_activos"],
            "expansion_geografica": ultimo_año["departamentos_activos"]
            - primer_año["departamentos_activos"],
            "cobertura_nacional": round(
                (ultimo_año["departamentos_activos"] / 9) * 100, 2
            ),  # 9 departamentos en Bolivia
        }

    def _analizar_evolucion_tecnologica(self, años_data):
        """Analiza evolución tecnológica del sector"""
        # Basado en adopción de tecnologías como generación de logos
        ahora = timezone.now()

        # Crecimiento en generación de logos por año
        logos_por_año = []
        for año_data in años_data:
            año = año_data["año"]
            inicio_año = datetime(año, 1, 1)
            fin_año = datetime(año + 1, 1, 1)

            logos_año = LogoMarcaBovina.objects.filter(
                fecha_generacion__gte=inicio_año, fecha_generacion__lt=fin_año
            ).count()

            logos_por_año.append(
                {
                    "año": año,
                    "logos_generados": logos_año,
                    "adopcion_porcentaje": round(
                        (
                            (logos_año / año_data["marcas_registradas"] * 100)
                            if año_data["marcas_registradas"] > 0
                            else 0
                        ),
                        2,
                    ),
                }
            )

        return {
            "adopcion_ia_por_año": logos_por_año,
            "tendencia_digitalizacion": (
                "creciente"
                if len(logos_por_año) > 1
                and logos_por_año[-1]["adopcion_porcentaje"]
                > logos_por_año[0]["adopcion_porcentaje"]
                else "estable"
            ),
        }

    def _analizar_profesionalizacion(self, años_data):
        """Analiza nivel de profesionalización del sector"""
        if len(años_data) < 2:
            return {}

        primer_año = años_data[0]
        ultimo_año = años_data[-1]

        # Concentración de productores (menos productores manejando más marcas indica profesionalización)
        concentracion_inicial = (
            primer_año["marcas_registradas"] / primer_año["productores_unicos"]
            if primer_año["productores_unicos"] > 0
            else 0
        )
        concentracion_actual = (
            ultimo_año["marcas_registradas"] / ultimo_año["productores_unicos"]
            if ultimo_año["productores_unicos"] > 0
            else 0
        )

        return {
            "marcas_por_productor_inicial": round(concentracion_inicial, 2),
            "marcas_por_productor_actual": round(concentracion_actual, 2),
            "evolucion_concentracion": round(
                concentracion_actual - concentracion_inicial, 2
            ),
            "nivel_profesionalizacion": (
                "creciente"
                if concentracion_actual > concentracion_inicial
                else "estable"
            ),
            "promedio_cabezas_inicial": primer_año.get("promedio_cabezas", 0),
            "promedio_cabezas_actual": ultimo_año.get("promedio_cabezas", 0),
        }
