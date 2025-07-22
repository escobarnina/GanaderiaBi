"""
Implementación de repositorio de dashboard usando Django ORM
Responsabilidad única: Gestionar datos del dashboard
"""

from typing import Dict, Any, List
from datetime import timedelta
from django.db import models
from django.utils import timezone

from apps.analytics.domain.entities.dashboard_data import DashboardData
from apps.analytics.domain.repositories.dashboard_repository import DashboardRepository
from apps.analytics.domain.enums import EstadoMarca

# Importar modelo Django de la nueva arquitectura
from apps.analytics.infrastructure.models import MarcaGanadoBovinoModel


class DjangoDashboardRepository(DashboardRepository):
    """Implementación de repositorio de dashboard usando Django ORM
    Responsabilidad única: Gestionar datos del dashboard"""

    def get_kpis_principales(self) -> DashboardData:
        """Obtiene KPIs principales del dashboard"""
        from django.db.models import Count, Avg, Sum

        hoy = timezone.now().date()
        inicio_mes = hoy.replace(day=1)

        # Estadísticas del mes actual
        marcas_mes = MarcaGanadoBovinoModel.objects.filter(
            fecha_registro__gte=inicio_mes
        )

        total_marcas_mes = marcas_mes.count()
        ingresos_mes = (
            marcas_mes.aggregate(total=Sum("monto_certificacion"))["total"] or 0
        )
        total_cabezas = (
            marcas_mes.aggregate(total=Sum("cantidad_cabezas"))["total"] or 0
        )
        promedio_cabezas = (
            marcas_mes.aggregate(promedio=Avg("cantidad_cabezas"))["promedio"] or 0
        )

        # Tiempo promedio de procesamiento
        tiempo_promedio = (
            marcas_mes.aggregate(promedio=Avg("tiempo_procesamiento_horas"))["promedio"]
            or 0
        )

        # Porcentaje de aprobación
        marcas_aprobadas = MarcaGanadoBovinoModel.objects.filter(
            estado=EstadoMarca.APROBADO.value
        ).count()
        marcas_rechazadas = MarcaGanadoBovinoModel.objects.filter(
            estado=EstadoMarca.RECHAZADO.value
        ).count()
        total_procesadas = marcas_aprobadas + marcas_rechazadas
        porcentaje_aprobacion = (
            (marcas_aprobadas / total_procesadas * 100) if total_procesadas > 0 else 0
        )

        return DashboardData(
            tipo_dashboard="kpis_principales",
            fecha_actualizacion=timezone.now(),
            datos={
                "marcas_registradas_mes": total_marcas_mes,
                "tiempo_promedio_procesamiento": tiempo_promedio,
                "porcentaje_aprobacion": porcentaje_aprobacion,
                "ingresos_mes": float(ingresos_mes),
                "total_cabezas_registradas": total_cabezas,
                "promedio_cabezas_por_marca": promedio_cabezas,
            },
        )

    def get_tendencias_mensuales(self, meses: int = 12) -> List[DashboardData]:
        """Obtiene tendencias mensuales"""
        from django.db.models import Count, Sum, Avg

        tendencias = []
        hoy = timezone.now().date()

        for i in range(meses):
            fecha = hoy.replace(day=1) - timedelta(days=i * 30)
            inicio_mes = fecha.replace(day=1)
            fin_mes = (inicio_mes + timedelta(days=32)).replace(day=1) - timedelta(
                days=1
            )

            marcas_mes = MarcaGanadoBovinoModel.objects.filter(
                fecha_registro__gte=inicio_mes, fecha_registro__lte=fin_mes
            )

            total_marcas = marcas_mes.count()
            ingresos = (
                marcas_mes.aggregate(total=Sum("monto_certificacion"))["total"] or 0
            )
            tiempo_promedio = (
                marcas_mes.aggregate(promedio=Avg("tiempo_procesamiento_horas"))[
                    "promedio"
                ]
                or 0
            )

            tendencias.append(
                DashboardData(
                    tipo_dashboard="tendencia_mensual",
                    fecha_actualizacion=timezone.now(),
                    datos={
                        "mes": fecha.strftime("%Y-%m"),
                        "marcas_registradas": total_marcas,
                        "ingresos": float(ingresos),
                        "tiempo_promedio": tiempo_promedio,
                    },
                )
            )

        return tendencias

    def get_metricas_tiempo_real(self) -> DashboardData:
        """Obtiene métricas en tiempo real"""
        from django.db.models import Count, Avg

        marcas_pendientes = MarcaGanadoBovinoModel.objects.filter(
            estado=EstadoMarca.PENDIENTE.value
        ).count()
        marcas_procesando = MarcaGanadoBovinoModel.objects.filter(
            estado=EstadoMarca.EN_PROCESO.value
        ).count()
        marcas_aprobadas_hoy = MarcaGanadoBovinoModel.objects.filter(
            fecha_procesamiento__date=timezone.now().date(),
            estado=EstadoMarca.APROBADO.value,
        ).count()

        # Tiempo promedio actual
        marcas_procesadas_hoy = MarcaGanadoBovinoModel.objects.filter(
            fecha_procesamiento__date=timezone.now().date()
        )
        tiempo_promedio_actual = (
            marcas_procesadas_hoy.aggregate(promedio=Avg("tiempo_procesamiento_horas"))[
                "promedio"
            ]
            or 0
        )

        return DashboardData(
            tipo_dashboard="metricas_tiempo_real",
            fecha_actualizacion=timezone.now(),
            datos={
                "marcas_pendientes": marcas_pendientes,
                "marcas_procesando": marcas_procesando,
                "marcas_aprobadas_hoy": marcas_aprobadas_hoy,
                "tiempo_promedio_actual": tiempo_promedio_actual,
            },
        )

    def get_resumen_ejecutivo(self) -> DashboardData:
        """Obtiene resumen ejecutivo"""
        kpis = self.get_kpis_principales()
        metricas = self.get_metricas_tiempo_real()

        return DashboardData(
            tipo_dashboard="resumen_ejecutivo",
            fecha_actualizacion=timezone.now(),
            datos={
                "kpis_principales": kpis.datos,
                "metricas_tiempo_real": metricas.datos,
                "fecha_actualizacion": timezone.now().isoformat(),
            },
        )
