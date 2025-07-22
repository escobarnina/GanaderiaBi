from typing import Dict, Any
from datetime import date
from decimal import Decimal

from apps.analytics.domain.entities.kpi_ganado_bovino import KPIGanadoBovino
from apps.analytics.domain.repositories.kpi_repository import KPIGanadoBovinoRepository
from apps.analytics.domain.repositories.marca_repository import (
    MarcaGanadoBovinoRepository,
)
from apps.analytics.domain.repositories.logo_repository import LogoMarcaBovinaRepository
from apps.analytics.domain.enums import PropositoGanado, Departamento


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
        return 24.0  # 24 horas promedio

    def _calcular_ingresos_mes(self) -> Decimal:
        """Calcula los ingresos del mes"""
        return Decimal("50000.00")  # 50,000 Bs promedio

    def _calcular_total_cabezas(self) -> int:
        """Calcula el total de cabezas registradas"""
        return 1500  # 1,500 cabezas promedio

    def _calcular_promedio_cabezas(self) -> float:
        """Calcula el promedio de cabezas por marca"""
        return 25.0  # 25 cabezas por marca promedio
