from typing import Dict, Any
from datetime import datetime, date

from apps.analytics.domain.repositories.dashboard_repository import DashboardRepository


class GenerarReporteDashboardUseCase:
    """Use Case para generar reportes del dashboard"""

    def __init__(self, dashboard_repository: DashboardRepository):
        self.dashboard_repository = dashboard_repository

    def execute(
        self, fecha_inicio: date, fecha_fin: date, formato: str = "json"
    ) -> Dict[str, Any]:
        """
        Genera un reporte del dashboard

        Args:
            fecha_inicio: Fecha de inicio del reporte
            fecha_fin: Fecha de fin del reporte
            formato: Formato del reporte (json, csv, pdf)

        Returns:
            Dict[str, Any]: Reporte generado
        """
        # Obtener datos del dashboard del período
        datos_dashboard = self.dashboard_repository.obtener_por_fechas(
            fecha_inicio=fecha_inicio, fecha_fin=fecha_fin
        )

        if not datos_dashboard:
            return {
                "error": "No hay datos de dashboard para el período especificado",
                "fecha_inicio": fecha_inicio.isoformat(),
                "fecha_fin": fecha_fin.isoformat(),
            }

        # Calcular métricas del reporte
        total_marcas = sum(d.marcas_registradas_mes_actual for d in datos_dashboard)
        promedio_aprobacion = sum(
            d.porcentaje_aprobacion for d in datos_dashboard
        ) / len(datos_dashboard)
        promedio_tiempo = sum(
            d.tiempo_promedio_procesamiento for d in datos_dashboard
        ) / len(datos_dashboard)
        total_ingresos = sum(d.ingresos_mes_actual for d in datos_dashboard)

        # Generar reporte
        reporte = {
            "periodo": {
                "fecha_inicio": fecha_inicio.isoformat(),
                "fecha_fin": fecha_fin.isoformat(),
                "dias": (fecha_fin - fecha_inicio).days,
            },
            "resumen": {
                "total_marcas": total_marcas,
                "promedio_aprobacion": round(promedio_aprobacion, 2),
                "promedio_tiempo_procesamiento": round(promedio_tiempo, 2),
                "total_ingresos": float(total_ingresos),
                "total_datos_generados": len(datos_dashboard),
            },
            "datos_detallados": [
                {
                    "fecha": d.fecha_actualizacion.isoformat(),
                    "marcas_registradas": d.marcas_registradas_mes_actual,
                    "porcentaje_aprobacion": d.porcentaje_aprobacion,
                    "tiempo_promedio": d.tiempo_promedio_procesamiento,
                    "ingresos": float(d.ingresos_mes_actual),
                    "total_cabezas": d.total_cabezas_bovinas,
                    "promedio_cabezas": d.promedio_cabezas_por_marca,
                    "tasa_exito_logos": d.tasa_exito_logos,
                    "alertas": len(d.alertas),
                }
                for d in datos_dashboard
            ],
            "formato": formato,
            "generado_en": datetime.now().isoformat(),
        }

        return reporte
