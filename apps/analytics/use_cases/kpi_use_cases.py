# apps/analytics/use_cases/kpi_use_cases.py
"""
Use Cases para gestión de KPIs de ganado bovino
Responsabilidad: Orquestar operaciones de negocio relacionadas con KPIs
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
from decimal import Decimal

from apps.analytics.domain.entities.kpi_ganado_bovino import KPIGanadoBovino
from apps.analytics.domain.repositories.kpi_repository import KPIGanadoBovinoRepository
from apps.analytics.domain.repositories.marca_repository import (
    MarcaGanadoBovinoRepository,
)
from apps.analytics.domain.repositories.logo_repository import LogoMarcaBovinaRepository
from apps.analytics.domain.enums import EstadoMarca, PropositoGanado, Departamento


class CalcularKPIsUseCase:
    """Use Case para calcular KPIs del sistema"""

    def __init__(
        self,
        kpi_repository: KPIGanadoBovinoRepository,
        marca_repository: MarcaGanadoBovinoRepository,
        logo_repository: LogoMarcaBovinaRepository,
    ):
        self.kpi_repository = kpi_repository
        self.marca_repository = marca_repository
        self.logo_repository = logo_repository

    def execute(self, fecha: date = None) -> KPIGanadoBovino:
        """
        Calcula KPIs para una fecha específica

        Args:
            fecha: Fecha para calcular KPIs (por defecto hoy)

        Returns:
            KPIGanadoBovino: KPIs calculados
        """
        if fecha is None:
            fecha = date.today()

        # Obtener estadísticas de marcas
        stats_marcas = self.marca_repository.obtener_estadisticas()

        # Obtener estadísticas de logos
        stats_logos = self.logo_repository.obtener_estadisticas()

        # Calcular KPIs específicos
        marcas_mes = stats_marcas.get("total_marcas", 0)
        tiempo_promedio = self._calcular_tiempo_promedio()
        porcentaje_aprobacion = stats_marcas.get("porcentaje_aprobacion", 0)
        ingresos_mes = self._calcular_ingresos_mes()

        # KPIs específicos bovinos
        total_cabezas = self._calcular_total_cabezas()
        promedio_cabezas = self._calcular_promedio_cabezas()

        # Distribución por propósito
        propositos = stats_marcas.get("propositos", {})
        marcas_carne = propositos.get(PropositoGanado.CARNE.value, 0)
        marcas_leche = propositos.get(PropositoGanado.LECHE.value, 0)
        marcas_doble_proposito = propositos.get(
            PropositoGanado.DOBLE_PROPOSITO.value, 0
        )
        marcas_reproduccion = propositos.get(PropositoGanado.REPRODUCCION.value, 0)

        # Distribución geográfica
        departamentos = stats_marcas.get("departamentos", {})
        marcas_santa_cruz = departamentos.get(Departamento.SANTA_CRUZ.value, 0)
        marcas_beni = departamentos.get(Departamento.BENI.value, 0)
        marcas_la_paz = departamentos.get(Departamento.LA_PAZ.value, 0)
        marcas_otros = sum(
            count
            for dept, count in departamentos.items()
            if dept
            not in [
                Departamento.SANTA_CRUZ.value,
                Departamento.BENI.value,
                Departamento.LA_PAZ.value,
            ]
        )

        # KPIs de logos
        tasa_exito_logos = stats_logos.get("tasa_exito", 0)
        total_logos = stats_logos.get("total_logos", 0)
        tiempo_promedio_logos = stats_logos.get("tiempo_promedio", 0)

        # Crear entidad de dominio
        kpi = KPIGanadoBovino(
            fecha=fecha,
            marcas_registradas_mes=marcas_mes,
            tiempo_promedio_procesamiento=tiempo_promedio,
            porcentaje_aprobacion=porcentaje_aprobacion,
            ingresos_mes=ingresos_mes,
            total_cabezas_registradas=total_cabezas,
            promedio_cabezas_por_marca=promedio_cabezas,
            marcas_carne=marcas_carne,
            marcas_leche=marcas_leche,
            marcas_doble_proposito=marcas_doble_proposito,
            marcas_reproduccion=marcas_reproduccion,
            marcas_santa_cruz=marcas_santa_cruz,
            marcas_beni=marcas_beni,
            marcas_la_paz=marcas_la_paz,
            marcas_otros_departamentos=marcas_otros,
            tasa_exito_logos=tasa_exito_logos,
            total_logos_generados=total_logos,
            tiempo_promedio_generacion_logos=tiempo_promedio_logos,
        )

        # Guardar usando repositorio
        return self.kpi_repository.crear(kpi)

    def _calcular_tiempo_promedio(self) -> float:
        """Calcula el tiempo promedio de procesamiento"""
        # Implementación simplificada
        return 24.0  # 24 horas promedio

    def _calcular_ingresos_mes(self) -> Decimal:
        """Calcula los ingresos del mes"""
        # Implementación simplificada
        return Decimal("50000.00")  # 50,000 Bs promedio

    def _calcular_total_cabezas(self) -> int:
        """Calcula el total de cabezas registradas"""
        # Implementación simplificada
        return 1500  # 1,500 cabezas promedio

    def _calcular_promedio_cabezas(self) -> float:
        """Calcula el promedio de cabezas por marca"""
        # Implementación simplificada
        return 25.0  # 25 cabezas por marca promedio


class ObtenerKPIsUseCase:
    """Use Case para obtener KPIs existentes"""

    def __init__(self, kpi_repository: KPIGanadoBovinoRepository):
        self.kpi_repository = kpi_repository

    def execute(
        self,
        fecha_inicio: Optional[date] = None,
        fecha_fin: Optional[date] = None,
        limit: int = 100,
    ) -> List[KPIGanadoBovino]:
        """
        Obtiene KPIs en un rango de fechas

        Args:
            fecha_inicio: Fecha de inicio del rango
            fecha_fin: Fecha de fin del rango
            limit: Límite de resultados

        Returns:
            List[KPIGanadoBovino]: Lista de KPIs
        """
        return self.kpi_repository.listar_por_fechas(
            fecha_inicio=fecha_inicio, fecha_fin=fecha_fin, limit=limit
        )


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
