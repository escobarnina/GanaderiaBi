# business_intelligence/views/dashboard_views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg, Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
import calendar

from ..models import MarcaGanadoBovino, LogoMarcaBovina, KPIGanadoBovino
from ..serializers import (
    DashboardKPIBovinoSerializer,
    EstadisticasMensualesBovinoSerializer,
)
from ..services import AnalyticsService


class DashboardBovinoViewSet(viewsets.ViewSet):
    """
    ViewSet para dashboard principal de ganado bovino

    Proporciona:
    - KPIs principales en tiempo real
    - Tendencias mensuales
    - Métricas de tiempo real
    - Resumen ejecutivo
    - Alertas del sistema
    """

    @action(detail=False, methods=["get"])
    def kpis_principales(self, request):
        """KPIs principales para el dashboard de ganado bovino"""
        ahora = timezone.now()
        inicio_mes = ahora.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        # Marcas registradas este mes
        marcas_mes = MarcaGanadoBovino.objects.filter(
            fecha_registro__gte=inicio_mes
        ).count()

        # Total de cabezas bovinas registradas este mes
        cabezas_mes = (
            MarcaGanadoBovino.objects.filter(fecha_registro__gte=inicio_mes).aggregate(
                Sum("cantidad_cabezas")
            )["cantidad_cabezas__sum"]
            or 0
        )

        # Promedio de cabezas por marca
        promedio_cabezas = round(cabezas_mes / marcas_mes, 2) if marcas_mes > 0 else 0

        # Tiempo promedio de procesamiento
        tiempo_promedio = (
            MarcaGanadoBovino.objects.filter(
                tiempo_procesamiento_horas__isnull=False
            ).aggregate(Avg("tiempo_procesamiento_horas"))[
                "tiempo_procesamiento_horas__avg"
            ]
            or 0
        )

        # Porcentajes de aprobación y rechazo
        total_procesadas = MarcaGanadoBovino.objects.filter(
            estado__in=["APROBADO", "RECHAZADO"]
        ).count()

        aprobadas = MarcaGanadoBovino.objects.filter(estado="APROBADO").count()
        rechazadas = MarcaGanadoBovino.objects.filter(estado="RECHAZADO").count()

        porcentaje_aprobacion = (
            (aprobadas / total_procesadas * 100) if total_procesadas > 0 else 0
        )
        porcentaje_rechazo = (
            (rechazadas / total_procesadas * 100) if total_procesadas > 0 else 0
        )

        # Ingresos del mes actual
        ingresos_mes = (
            MarcaGanadoBovino.objects.filter(
                fecha_registro__gte=inicio_mes, estado="APROBADO"
            ).aggregate(Sum("monto_certificacion"))["monto_certificacion__sum"]
            or 0
        )

        # Distribución por propósito (porcentajes)
        total_marcas_sistema = MarcaGanadoBovino.objects.count()

        if total_marcas_sistema > 0:
            carne_count = MarcaGanadoBovino.objects.filter(
                proposito_ganado="CARNE"
            ).count()
            leche_count = MarcaGanadoBovino.objects.filter(
                proposito_ganado="LECHE"
            ).count()
            doble_count = MarcaGanadoBovino.objects.filter(
                proposito_ganado="DOBLE_PROPOSITO"
            ).count()
            repro_count = MarcaGanadoBovino.objects.filter(
                proposito_ganado="REPRODUCCION"
            ).count()

            porcentaje_carne = round((carne_count / total_marcas_sistema) * 100, 2)
            porcentaje_leche = round((leche_count / total_marcas_sistema) * 100, 2)
            porcentaje_doble_proposito = round(
                (doble_count / total_marcas_sistema) * 100, 2
            )
            porcentaje_reproduccion = round(
                (repro_count / total_marcas_sistema) * 100, 2
            )
        else:
            porcentaje_carne = porcentaje_leche = porcentaje_doble_proposito = (
                porcentaje_reproduccion
            ) = 0

        # Raza más común
        raza_principal = (
            MarcaGanadoBovino.objects.values("raza_bovino")
            .annotate(total=Count("id"))
            .order_by("-total")
            .first()
        )

        raza_mas_comun = raza_principal["raza_bovino"] if raza_principal else "N/A"
        porcentaje_raza_principal = round(
            (
                (raza_principal["total"] / total_marcas_sistema * 100)
                if raza_principal and total_marcas_sistema > 0
                else 0
            ),
            2,
        )

        # Tasa de éxito en generación de logos
        total_logos = LogoMarcaBovina.objects.count()
        logos_exitosos = LogoMarcaBovina.objects.filter(exito=True).count()
        tasa_exito_logos = (
            (logos_exitosos / total_logos * 100) if total_logos > 0 else 0
        )

        # Marcas pendientes
        marcas_pendientes = MarcaGanadoBovino.objects.filter(
            estado__in=["PENDIENTE", "EN_PROCESO"]
        ).count()

        # Generar alertas
        alertas = self._generar_alertas(
            marcas_pendientes, tiempo_promedio, porcentaje_aprobacion
        )

        data = {
            "marcas_registradas_mes_actual": marcas_mes,
            "tiempo_promedio_procesamiento": round(tiempo_promedio, 2),
            "porcentaje_aprobacion": round(porcentaje_aprobacion, 2),
            "porcentaje_rechazo": round(porcentaje_rechazo, 2),
            "ingresos_mes_actual": ingresos_mes,
            "total_cabezas_bovinas": cabezas_mes,
            "promedio_cabezas_por_marca": promedio_cabezas,
            "porcentaje_carne": porcentaje_carne,
            "porcentaje_leche": porcentaje_leche,
            "porcentaje_doble_proposito": porcentaje_doble_proposito,
            "porcentaje_reproduccion": porcentaje_reproduccion,
            "raza_mas_comun": raza_mas_comun,
            "porcentaje_raza_principal": porcentaje_raza_principal,
            "tasa_exito_logos": round(tasa_exito_logos, 2),
            "total_marcas_sistema": total_marcas_sistema,
            "marcas_pendientes": marcas_pendientes,
            "alertas": alertas,
        }

        serializer = DashboardKPIBovinoSerializer(data)
        return Response(serializer.data)

    def _generar_alertas(
        self, marcas_pendientes, tiempo_promedio, porcentaje_aprobacion
    ):
        """Genera alertas para el dashboard"""
        alertas = []

        # Alerta por marcas pendientes
        if marcas_pendientes > 50:
            alertas.append(
                {
                    "tipo": "warning",
                    "titulo": "Alto volumen de marcas pendientes",
                    "mensaje": f"{marcas_pendientes} marcas pendientes de procesamiento",
                    "accion": "Revisar cola de procesamiento",
                }
            )

        # Alerta por tiempo de procesamiento
        if tiempo_promedio > 72:  # Más de 3 días
            alertas.append(
                {
                    "tipo": "warning",
                    "titulo": "Tiempo de procesamiento elevado",
                    "mensaje": f"Promedio: {tiempo_promedio:.1f} horas",
                    "accion": "Optimizar proceso de evaluación",
                }
            )

        # Alerta por tasa de aprobación baja
        if porcentaje_aprobacion < 70:
            alertas.append(
                {
                    "tipo": "danger",
                    "titulo": "Tasa de aprobación baja",
                    "mensaje": f"Solo {porcentaje_aprobacion:.1f}% de marcas aprobadas",
                    "accion": "Revisar criterios de evaluación",
                }
            )

        return alertas

    @action(detail=False, methods=["get"])
    def tendencias_mensuales(self, request):
        """Tendencias de los últimos 12 meses para ganado bovino"""
        ahora = timezone.now()
        hace_12_meses = ahora - timedelta(days=365)

        # Obtener datos por mes
        marcas_por_mes = (
            MarcaGanadoBovino.objects.filter(fecha_registro__gte=hace_12_meses)
            .extra(
                select={"año": "YEAR(fecha_registro)", "mes": "MONTH(fecha_registro)"}
            )
            .values("año", "mes")
            .annotate(
                marcas_registradas=Count("id"),
                cabezas_registradas=Sum("cantidad_cabezas"),
                ingresos=Sum("monto_certificacion", filter=Q(estado="APROBADO")),
                tiempo_promedio=Avg("tiempo_procesamiento_horas"),
                marcas_carne=Count("id", filter=Q(proposito_ganado="CARNE")),
                marcas_leche=Count("id", filter=Q(proposito_ganado="LECHE")),
                marcas_doble_proposito=Count(
                    "id", filter=Q(proposito_ganado="DOBLE_PROPOSITO")
                ),
                marcas_reproduccion=Count(
                    "id", filter=Q(proposito_ganado="REPRODUCCION")
                ),
            )
            .order_by("año", "mes")
        )

        # Formatear datos para el frontend
        datos_formateados = []
        for dato in marcas_por_mes:
            # Determinar departamento principal del mes
            dept_principal = (
                MarcaGanadoBovino.objects.filter(
                    fecha_registro__year=dato["año"], fecha_registro__month=dato["mes"]
                )
                .values("departamento")
                .annotate(total=Count("id"))
                .order_by("-total")
                .first()
            )

            datos_formateados.append(
                {
                    "mes": calendar.month_name[dato["mes"]],
                    "año": dato["año"],
                    "marcas_registradas": dato["marcas_registradas"],
                    "cabezas_registradas": dato["cabezas_registradas"] or 0,
                    "ingresos": dato["ingresos"] or 0,
                    "tiempo_promedio": round(dato["tiempo_promedio"] or 0, 2),
                    "marcas_carne": dato["marcas_carne"],
                    "marcas_leche": dato["marcas_leche"],
                    "marcas_doble_proposito": dato["marcas_doble_proposito"],
                    "marcas_reproduccion": dato["marcas_reproduccion"],
                    "departamento_principal": (
                        dept_principal["departamento"] if dept_principal else "N/A"
                    ),
                    "marcas_departamento_principal": (
                        dept_principal["total"] if dept_principal else 0
                    ),
                }
            )

        serializer = EstadisticasMensualesBovinoSerializer(datos_formateados, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def metricas_tiempo_real(self, request):
        """Métricas en tiempo real para actualizar el dashboard"""
        ahora = timezone.now()
        hoy = ahora.date()

        # Registros de hoy
        registros_hoy = MarcaGanadoBovino.objects.filter(
            fecha_registro__date=hoy
        ).count()

        # Cabezas registradas hoy
        cabezas_hoy = (
            MarcaGanadoBovino.objects.filter(fecha_registro__date=hoy).aggregate(
                Sum("cantidad_cabezas")
            )["cantidad_cabezas__sum"]
            or 0
        )

        # Certificaciones procesadas hoy
        procesadas_hoy = MarcaGanadoBovino.objects.filter(
            fecha_procesamiento__date=hoy
        ).count()

        # Logos generados hoy
        logos_hoy = LogoMarcaBovina.objects.filter(fecha_generacion__date=hoy).count()

        # Ingresos de hoy
        ingresos_hoy = (
            MarcaGanadoBovino.objects.filter(
                fecha_procesamiento__date=hoy, estado="APROBADO"
            ).aggregate(Sum("monto_certificacion"))["monto_certificacion__sum"]
            or 0
        )

        # Distribución por propósito hoy
        propositos_hoy = (
            MarcaGanadoBovino.objects.filter(fecha_registro__date=hoy)
            .values("proposito_ganado")
            .annotate(total=Count("id"))
        )

        # Estado del sistema
        marcas_cola = MarcaGanadoBovino.objects.filter(
            estado__in=["PENDIENTE", "EN_PROCESO"]
        ).count()

        estado_sistema = "normal"
        if marcas_cola > 100:
            estado_sistema = "sobrecargado"
        elif marcas_cola > 50:
            estado_sistema = "ocupado"

        return Response(
            {
                "fecha": hoy,
                "timestamp": ahora.isoformat(),
                "registros_hoy": registros_hoy,
                "cabezas_registradas_hoy": cabezas_hoy,
                "procesadas_hoy": procesadas_hoy,
                "logos_generados_hoy": logos_hoy,
                "ingresos_hoy": ingresos_hoy,
                "distribucion_propositos_hoy": list(propositos_hoy),
                "estado_sistema": estado_sistema,
                "marcas_en_cola": marcas_cola,
                "velocidad_procesamiento": (
                    round(procesadas_hoy / 24, 2) if procesadas_hoy > 0 else 0
                ),  # marcas por hora
            }
        )

    @action(detail=False, methods=["get"])
    def resumen_ejecutivo(self, request):
        """Resumen ejecutivo para la alta dirección"""
        # Período de análisis (últimos 30 días)
        ahora = timezone.now()
        hace_30_dias = ahora - timedelta(days=30)

        # Métricas principales del mes
        marcas_ultimo_mes = MarcaGanadoBovino.objects.filter(
            fecha_registro__gte=hace_30_dias
        )

        total_marcas_mes = marcas_ultimo_mes.count()
        total_cabezas_mes = (
            marcas_ultimo_mes.aggregate(Sum("cantidad_cabezas"))[
                "cantidad_cabezas__sum"
            ]
            or 0
        )

        # Comparación con mes anterior
        hace_60_dias = ahora - timedelta(days=60)
        marcas_mes_anterior = MarcaGanadoBovino.objects.filter(
            fecha_registro__gte=hace_60_dias, fecha_registro__lt=hace_30_dias
        ).count()

        crecimiento_marcas = (
            ((total_marcas_mes - marcas_mes_anterior) / marcas_mes_anterior * 100)
            if marcas_mes_anterior > 0
            else 0
        )

        # Análisis de eficiencia
        eficiencia_regional = AnalyticsService.analizar_eficiencia_regional()
        mejor_region = eficiencia_regional[0] if eficiencia_regional else None

        # Predicciones
        predicciones = AnalyticsService.predecir_demanda_mensual()

        # Top 3 departamentos ganaderos
        top_departamentos = (
            MarcaGanadoBovino.objects.values("departamento")
            .annotate(total_marcas=Count("id"), total_cabezas=Sum("cantidad_cabezas"))
            .order_by("-total_cabezas")[:3]
        )

        # Rendimiento de logos
        total_logos = LogoMarcaBovina.objects.count()
        logos_exitosos = LogoMarcaBovina.objects.filter(exito=True).count()

        return Response(
            {
                "periodo_analisis": "30 días",
                "fecha_generacion": ahora.date(),
                "metricas_clave": {
                    "marcas_registradas": total_marcas_mes,
                    "cabezas_bovinas": total_cabezas_mes,
                    "crecimiento_vs_mes_anterior": round(crecimiento_marcas, 2),
                    "eficiencia_promedio_sistema": (
                        round(
                            sum(r["eficiencia_score"] for r in eficiencia_regional)
                            / len(eficiencia_regional),
                            2,
                        )
                        if eficiencia_regional
                        else 0
                    ),
                },
                "region_mas_eficiente": {
                    "departamento": (
                        mejor_region["departamento_display"] if mejor_region else "N/A"
                    ),
                    "score_eficiencia": (
                        mejor_region["eficiencia_score"] if mejor_region else 0
                    ),
                    "tasa_aprobacion": (
                        mejor_region["tasa_aprobacion"] if mejor_region else 0
                    ),
                },
                "predicciones_proximo_mes": {
                    "marcas_estimadas": predicciones.get("prediccion_marcas", 0),
                    "cabezas_estimadas": predicciones.get("prediccion_cabezas", 0),
                    "ingresos_estimados": predicciones.get("prediccion_ingresos", 0),
                    "confianza_prediccion": predicciones.get("confianza", "Baja"),
                },
                "top_departamentos_ganaderos": [
                    {
                        "departamento": dept["departamento"],
                        "marcas": dept["total_marcas"],
                        "cabezas": dept["total_cabezas"],
                    }
                    for dept in top_departamentos
                ],
                "rendimiento_tecnologia": {
                    "logos_generados": total_logos,
                    "tasa_exito_ia": round(
                        (logos_exitosos / total_logos * 100) if total_logos > 0 else 0,
                        2,
                    ),
                    "estado": (
                        "óptimo"
                        if (logos_exitosos / total_logos) > 0.85
                        else "necesita_optimización" if total_logos > 0 else "sin_datos"
                    ),
                },
                "recomendaciones": self._generar_recomendaciones_ejecutivas(
                    crecimiento_marcas, eficiencia_regional, predicciones
                ),
            }
        )

    def _generar_recomendaciones_ejecutivas(
        self, crecimiento, eficiencia_regional, predicciones
    ):
        """Genera recomendaciones para la alta dirección"""
        recomendaciones = []

        # Recomendación por crecimiento
        if crecimiento > 20:
            recomendaciones.append(
                {
                    "categoria": "Capacidad",
                    "prioridad": "alta",
                    "recomendacion": f"Alto crecimiento ({crecimiento:.1f}%). Considerar aumentar capacidad de procesamiento.",
                    "impacto": "Prevenir cuellos de botella en el procesamiento",
                }
            )
        elif crecimiento < -10:
            recomendaciones.append(
                {
                    "categoria": "Mercadeo",
                    "prioridad": "media",
                    "recomendacion": f"Decrecimiento del {abs(crecimiento):.1f}%. Implementar estrategias de promoción.",
                    "impacto": "Recuperar volumen de registros",
                }
            )

        # Recomendación por eficiencia regional
        if eficiencia_regional:
            regiones_baja_eficiencia = [
                r for r in eficiencia_regional if r["eficiencia_score"] < 50
            ]
            if regiones_baja_eficiencia:
                recomendaciones.append(
                    {
                        "categoria": "Operaciones",
                        "prioridad": "alta",
                        "recomendacion": f"{len(regiones_baja_eficiencia)} regiones con baja eficiencia. Implementar mejores prácticas.",
                        "impacto": "Mejorar tiempo de procesamiento y satisfacción del usuario",
                    }
                )

        # Recomendación por predicciones
        if predicciones.get("confianza") == "Baja":
            recomendaciones.append(
                {
                    "categoria": "Análisis",
                    "prioridad": "baja",
                    "recomendacion": "Mejorar recolección de datos históricos para predicciones más precisas.",
                    "impacto": "Mejor planificación de recursos",
                }
            )

        return recomendaciones
