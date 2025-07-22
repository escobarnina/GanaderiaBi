from typing import Dict, Any
from datetime import datetime, date

from apps.analytics.domain.repositories.kpi_repository import KPIGanadoBovinoRepository


class GenerarReporteKPIsUseCase:
    """Use Case para generar reportes de KPIs"""

    def __init__(self, kpi_repository: KPIGanadoBovinoRepository):
        self.kpi_repository = kpi_repository

    def execute(
        self, fecha_inicio: date, fecha_fin: date, formato: str = "json"
    ) -> Dict[str, Any]:
        """
        Genera un reporte de KPIs

        Args:
            fecha_inicio: Fecha de inicio del reporte
            fecha_fin: Fecha de fin del reporte
            formato: Formato del reporte (json, csv, pdf)

        Returns:
            Dict[str, Any]: Reporte generado
        """
        # Obtener KPIs del período
        kpis = self.kpi_repository.listar_por_fechas(
            fecha_inicio=fecha_inicio, fecha_fin=fecha_fin
        )

        if not kpis:
            return {
                "error": "No hay datos para el período especificado",
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin,
            }

        # Calcular métricas del reporte
        total_marcas = sum(kpi.marcas_registradas_mes for kpi in kpis)
        promedio_tiempo = sum(kpi.tiempo_promedio_procesamiento for kpi in kpis) / len(
            kpis
        )
        promedio_aprobacion = sum(kpi.porcentaje_aprobacion for kpi in kpis) / len(kpis)
        total_ingresos = sum(kpi.ingresos_mes for kpi in kpis)

        # Generar reporte
        reporte = {
            "periodo": {
                "fecha_inicio": fecha_inicio.isoformat(),
                "fecha_fin": fecha_fin.isoformat(),
                "dias": (fecha_fin - fecha_inicio).days,
            },
            "resumen": {
                "total_marcas": total_marcas,
                "promedio_tiempo_procesamiento": round(promedio_tiempo, 2),
                "promedio_porcentaje_aprobacion": round(promedio_aprobacion, 2),
                "total_ingresos": float(total_ingresos),
                "total_kpis_generados": len(kpis),
            },
            "kpis_detallados": [
                {
                    "fecha": kpi.fecha.isoformat(),
                    "marcas_registradas": kpi.marcas_registradas_mes,
                    "tiempo_promedio": kpi.tiempo_promedio_procesamiento,
                    "porcentaje_aprobacion": kpi.porcentaje_aprobacion,
                    "ingresos": float(kpi.ingresos_mes),
                    "total_cabezas": kpi.total_cabezas_registradas,
                    "promedio_cabezas": kpi.promedio_cabezas_por_marca,
                }
                for kpi in kpis
            ],
            "formato": formato,
            "generado_en": datetime.now().isoformat(),
        }

        return reporte
