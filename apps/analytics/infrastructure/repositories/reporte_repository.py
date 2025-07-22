"""
Implementación de repositorio de reportes usando Django ORM
Responsabilidad única: Gestionar reportes de datos
"""

from datetime import datetime
from django.db.models import Count, Sum, Avg, Q
from django.utils import timezone

from apps.analytics.domain.entities.reporte_data import ReporteData
from apps.analytics.domain.repositories.reporte_repository import ReporteRepository

# Importar modelo Django de la nueva arquitectura
from apps.analytics.infrastructure.models import (
    MarcaGanadoBovinoModel,
    LogoMarcaBovinaModel,
    KPIGanadoBovinoModel,
)


class DjangoReporteRepository(ReporteRepository):
    """Implementación de repositorio de reportes usando Django ORM
    Responsabilidad única: Gestionar reportes de datos"""

    def generar_reporte_marcas(
        self, fecha_inicio: datetime, fecha_fin: datetime
    ) -> ReporteData:
        """Implementa ReporteRepository.generar_reporte_ejecutivo_mensual"""
        from apps.analytics.domain.enums import EstadoMarca

        marcas_periodo = MarcaGanadoBovinoModel.objects.filter(
            fecha_registro__gte=fecha_inicio, fecha_registro__lte=fecha_fin
        )

        # Estadísticas generales
        total_marcas = marcas_periodo.count()
        marcas_aprobadas = marcas_periodo.filter(
            estado=EstadoMarca.APROBADO.value
        ).count()
        marcas_rechazadas = marcas_periodo.filter(
            estado=EstadoMarca.RECHAZADO.value
        ).count()
        marcas_pendientes = marcas_periodo.filter(
            estado=EstadoMarca.PENDIENTE.value
        ).count()

        # Ingresos y cabezas
        ingresos_totales = (
            marcas_periodo.aggregate(total=Sum("monto_certificacion"))["total"] or 0
        )
        total_cabezas = (
            marcas_periodo.aggregate(total=Sum("cantidad_cabezas"))["total"] or 0
        )
        tiempo_promedio = (
            marcas_periodo.aggregate(promedio=Avg("tiempo_procesamiento_horas"))[
                "promedio"
            ]
            or 0
        )

        # Distribución por propósito
        propositos = marcas_periodo.values("proposito_ganado").annotate(
            total=Count("id"), cabezas=Sum("cantidad_cabezas")
        )

        # Distribución por departamento
        departamentos = marcas_periodo.values("departamento").annotate(
            total=Count("id"), ingresos=Sum("monto_certificacion")
        )

        # Distribución por raza
        razas = marcas_periodo.values("raza_bovino").annotate(
            total=Count("id"), promedio_cabezas=Avg("cantidad_cabezas")
        )

        return ReporteData(
            tipo_reporte="marcas_periodo",
            fecha_generacion=timezone.now(),
            periodo_inicio=fecha_inicio,
            periodo_fin=fecha_fin,
            datos={
                "total_marcas": total_marcas,
                "marcas_aprobadas": marcas_aprobadas,
                "marcas_rechazadas": marcas_rechazadas,
                "marcas_pendientes": marcas_pendientes,
                "porcentaje_aprobacion": (
                    (marcas_aprobadas / total_marcas * 100) if total_marcas > 0 else 0
                ),
                "ingresos_totales": float(ingresos_totales),
                "total_cabezas": total_cabezas,
                "tiempo_promedio_procesamiento": tiempo_promedio,
                "propositos": {
                    p["proposito_ganado"]: {
                        "total": p["total"],
                        "cabezas": p["cabezas"] or 0,
                    }
                    for p in propositos
                },
                "departamentos": {
                    d["departamento"]: {
                        "total": d["total"],
                        "ingresos": float(d["ingresos"] or 0),
                    }
                    for d in departamentos
                },
                "razas": {
                    r["raza_bovino"]: {
                        "total": r["total"],
                        "promedio_cabezas": float(r["promedio_cabezas"] or 0),
                    }
                    for r in razas
                },
            },
        )

    def generar_reporte_logos(
        self, fecha_inicio: datetime, fecha_fin: datetime
    ) -> ReporteData:
        """Implementa ReporteRepository.generar_reporte_personalizado (logos)"""
        logos_periodo = LogoMarcaBovinaModel.objects.filter(
            fecha_generacion__gte=fecha_inicio, fecha_generacion__lte=fecha_fin
        )

        # Estadísticas generales
        total_logos = logos_periodo.count()
        logos_exitosos = logos_periodo.filter(exito=True).count()
        logos_fallidos = logos_periodo.filter(exito=False).count()
        tasa_exito = (logos_exitosos / total_logos * 100) if total_logos > 0 else 0

        # Tiempo promedio de generación
        tiempo_promedio = (
            logos_periodo.aggregate(promedio=Avg("tiempo_generacion_segundos"))[
                "promedio"
            ]
            or 0
        )

        # Distribución por modelo de IA
        modelos = logos_periodo.values("modelo_ia_usado").annotate(
            total=Count("id"), exitosos=Count("id", filter=Q(exito=True))
        )

        # Distribución por calidad
        calidades = logos_periodo.values("calidad_logo").annotate(total=Count("id"))

        return ReporteData(
            tipo_reporte="logos_periodo",
            fecha_generacion=timezone.now(),
            periodo_inicio=fecha_inicio,
            periodo_fin=fecha_fin,
            datos={
                "total_logos": total_logos,
                "logos_exitosos": logos_exitosos,
                "logos_fallidos": logos_fallidos,
                "tasa_exito": tasa_exito,
                "tiempo_promedio_generacion": tiempo_promedio,
                "modelos": {
                    m["modelo_ia_usado"]: {
                        "total": m["total"],
                        "exitosos": m["exitosos"],
                        "tasa_exito": (
                            (m["exitosos"] / m["total"] * 100) if m["total"] > 0 else 0
                        ),
                    }
                    for m in modelos
                },
                "calidades": {c["calidad_logo"]: c["total"] for c in calidades},
            },
        )

    def generar_reporte_kpis(
        self, fecha_inicio: datetime, fecha_fin: datetime
    ) -> ReporteData:
        """Implementa ReporteRepository.generar_reporte_anual (KPIs)"""
        kpis_periodo = KPIGanadoBovinoModel.objects.filter(
            fecha__gte=fecha_inicio.date(), fecha__lte=fecha_fin.date()
        ).order_by("fecha")

        # Calcular promedios y tendencias
        total_kpis = kpis_periodo.count()
        if total_kpis > 0:
            promedio_marcas = (
                kpis_periodo.aggregate(promedio=Avg("marcas_registradas_mes"))[
                    "promedio"
                ]
                or 0
            )
            promedio_aprobacion = (
                kpis_periodo.aggregate(promedio=Avg("porcentaje_aprobacion"))[
                    "promedio"
                ]
                or 0
            )
            promedio_tiempo = (
                kpis_periodo.aggregate(promedio=Avg("tiempo_promedio_procesamiento"))[
                    "promedio"
                ]
                or 0
            )
            total_ingresos = (
                kpis_periodo.aggregate(total=Sum("ingresos_mes"))["total"] or 0
            )
        else:
            promedio_marcas = promedio_aprobacion = promedio_tiempo = total_ingresos = 0

        # Tendencia (comparar primer y último KPI)
        tendencia = "estable"
        if total_kpis >= 2:
            primer_kpi = kpis_periodo.first()
            ultimo_kpi = kpis_periodo.last()
            if primer_kpi and ultimo_kpi:
                if (
                    ultimo_kpi.marcas_registradas_mes
                    > primer_kpi.marcas_registradas_mes
                ):
                    tendencia = "creciente"
                elif (
                    ultimo_kpi.marcas_registradas_mes
                    < primer_kpi.marcas_registradas_mes
                ):
                    tendencia = "decreciente"

        return ReporteData(
            tipo_reporte="kpis_periodo",
            fecha_generacion=timezone.now(),
            periodo_inicio=fecha_inicio,
            periodo_fin=fecha_fin,
            datos={
                "total_kpis_analizados": total_kpis,
                "promedio_marcas_mes": promedio_marcas,
                "promedio_porcentaje_aprobacion": promedio_aprobacion,
                "promedio_tiempo_procesamiento": promedio_tiempo,
                "total_ingresos_periodo": float(total_ingresos),
                "tendencia": tendencia,
                "kpis_detallados": [
                    {
                        "fecha": kpi.fecha.isoformat(),
                        "marcas_registradas": kpi.marcas_registradas_mes,
                        "porcentaje_aprobacion": kpi.porcentaje_aprobacion,
                        "ingresos": float(kpi.ingresos_mes),
                    }
                    for kpi in kpis_periodo
                ],
            },
        )

    def generar_reporte_consolidado(
        self, fecha_inicio: datetime, fecha_fin: datetime
    ) -> ReporteData:
        """Implementa ReporteRepository.generar_reporte_comparativo_departamentos"""
        # Obtener reportes individuales
        reporte_marcas = self.generar_reporte_marcas(fecha_inicio, fecha_fin)
        reporte_logos = self.generar_reporte_logos(fecha_inicio, fecha_fin)
        reporte_kpis = self.generar_reporte_kpis(fecha_inicio, fecha_fin)

        # Consolidar datos
        datos_consolidados = {
            "resumen_general": {
                "periodo_analizado": f"{fecha_inicio.date()} a {fecha_fin.date()}",
                "total_marcas": reporte_marcas.datos["total_marcas"],
                "total_logos": reporte_logos.datos["total_logos"],
                "tasa_aprobacion_marcas": reporte_marcas.datos["porcentaje_aprobacion"],
                "tasa_exito_logos": reporte_logos.datos["tasa_exito"],
            },
            "marcas": reporte_marcas.datos,
            "logos": reporte_logos.datos,
            "kpis": reporte_kpis.datos,
        }

        return ReporteData(
            tipo_reporte="consolidado",
            fecha_generacion=timezone.now(),
            periodo_inicio=fecha_inicio,
            periodo_fin=fecha_fin,
            datos=datos_consolidados,
        )
