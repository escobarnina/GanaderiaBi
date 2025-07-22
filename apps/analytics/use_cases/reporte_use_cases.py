# apps/analytics/use_cases/reporte_use_cases.py
"""
Use Cases para gestión de reportes ejecutivos
Responsabilidad: Orquestar operaciones de negocio relacionadas con reportes
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
from decimal import Decimal

from apps.analytics.domain.entities.reporte_data import ReporteData
from apps.analytics.domain.repositories.reporte_repository import ReporteRepository
from apps.analytics.domain.repositories.marca_repository import (
    MarcaGanadoBovinoRepository,
)
from apps.analytics.domain.repositories.kpi_repository import KPIGanadoBovinoRepository
from apps.analytics.domain.repositories.logo_repository import LogoMarcaBovinaRepository
from apps.analytics.domain.enums import EstadoMarca, PropositoGanado, Departamento


class GenerarReporteMensualUseCase:
    """Use Case para generar reporte ejecutivo mensual"""

    def __init__(
        self,
        reporte_repository: ReporteRepository,
        marca_repository: MarcaGanadoBovinoRepository,
        kpi_repository: KPIGanadoBovinoRepository,
        logo_repository: LogoMarcaBovinaRepository,
    ):
        self.reporte_repository = reporte_repository
        self.marca_repository = marca_repository
        self.kpi_repository = kpi_repository
        self.logo_repository = logo_repository

    def execute(self, año: int, mes: int) -> ReporteData:
        """
        Genera un reporte ejecutivo mensual

        Args:
            año: Año del reporte
            mes: Mes del reporte

        Returns:
            ReporteData: Reporte generado
        """
        fecha_inicio = datetime(año, mes, 1)
        if mes == 12:
            fecha_fin = datetime(año + 1, 1, 1)
        else:
            fecha_fin = datetime(año, mes + 1, 1)

        return self.reporte_repository.generar_reporte_marcas(
            fecha_inicio=fecha_inicio, fecha_fin=fecha_fin
        )


class GenerarReporteAnualUseCase:
    """Use Case para generar reporte ejecutivo anual"""

    def __init__(
        self,
        reporte_repository: ReporteRepository,
        marca_repository: MarcaGanadoBovinoRepository,
        kpi_repository: KPIGanadoBovinoRepository,
    ):
        self.reporte_repository = reporte_repository
        self.marca_repository = marca_repository
        self.kpi_repository = kpi_repository

    def execute(self, año: int) -> ReporteData:
        """
        Genera un reporte ejecutivo anual

        Args:
            año: Año del reporte

        Returns:
            ReporteData: Reporte generado
        """
        fecha_inicio = datetime(año, 1, 1)
        fecha_fin = datetime(año + 1, 1, 1)

        return self.reporte_repository.generar_reporte_anual(
            fecha_inicio=fecha_inicio, fecha_fin=fecha_fin
        )


class GenerarReporteComparativoDepartamentosUseCase:
    """Use Case para generar reporte comparativo por departamentos"""

    def __init__(
        self,
        reporte_repository: ReporteRepository,
        marca_repository: MarcaGanadoBovinoRepository,
    ):
        self.reporte_repository = reporte_repository
        self.marca_repository = marca_repository

    def execute(self, fecha_inicio: datetime, fecha_fin: datetime) -> ReporteData:
        """
        Genera un reporte comparativo por departamentos

        Args:
            fecha_inicio: Fecha de inicio del reporte
            fecha_fin: Fecha de fin del reporte

        Returns:
            ReporteData: Reporte generado
        """
        return self.reporte_repository.generar_reporte_comparativo_departamentos(
            fecha_inicio=fecha_inicio, fecha_fin=fecha_fin
        )


class GenerarReportePersonalizadoUseCase:
    """Use Case para generar reporte personalizado"""

    def __init__(
        self,
        reporte_repository: ReporteRepository,
        marca_repository: MarcaGanadoBovinoRepository,
        logo_repository: LogoMarcaBovinaRepository,
    ):
        self.reporte_repository = reporte_repository
        self.marca_repository = marca_repository
        self.logo_repository = logo_repository

    def execute(
        self,
        fecha_inicio: datetime,
        fecha_fin: datetime,
        tipo_reporte: str,
        filtros: Optional[Dict[str, Any]] = None,
    ) -> ReporteData:
        """
        Genera un reporte personalizado

        Args:
            fecha_inicio: Fecha de inicio del reporte
            fecha_fin: Fecha de fin del reporte
            tipo_reporte: Tipo de reporte a generar
            filtros: Filtros adicionales

        Returns:
            ReporteData: Reporte generado
        """
        if tipo_reporte == "logos":
            return self.reporte_repository.generar_reporte_logos(
                fecha_inicio=fecha_inicio, fecha_fin=fecha_fin
            )
        elif tipo_reporte == "kpis":
            return self.reporte_repository.generar_reporte_kpis(
                fecha_inicio=fecha_inicio, fecha_fin=fecha_fin
            )
        else:
            return self.reporte_repository.generar_reporte_consolidado(
                fecha_inicio=fecha_inicio, fecha_fin=fecha_fin
            )


class ExportarReporteExcelUseCase:
    """Use Case para exportar reporte a Excel"""

    def __init__(
        self,
        reporte_repository: ReporteRepository,
        marca_repository: MarcaGanadoBovinoRepository,
    ):
        self.reporte_repository = reporte_repository
        self.marca_repository = marca_repository

    def execute(
        self,
        fecha_inicio: datetime,
        fecha_fin: datetime,
        filtros: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Exporta un reporte a formato Excel

        Args:
            fecha_inicio: Fecha de inicio del reporte
            fecha_fin: Fecha de fin del reporte
            filtros: Filtros adicionales

        Returns:
            Dict[str, Any]: Datos para exportación
        """
        return self.reporte_repository.exportar_datos_excel(filtros=filtros)


class GenerarReporteProductorUseCase:
    """Use Case para generar reporte de un productor específico"""

    def __init__(
        self,
        reporte_repository: ReporteRepository,
        marca_repository: MarcaGanadoBovinoRepository,
    ):
        self.reporte_repository = reporte_repository
        self.marca_repository = marca_repository

    def execute(self, marca_id: int) -> Dict[str, Any]:
        """
        Genera un reporte específico para un productor

        Args:
            marca_id: ID de la marca del productor

        Returns:
            Dict[str, Any]: Reporte del productor
        """
        return self.reporte_repository.generar_reporte_productor(marca_id)


class GenerarReporteImpactoEconomicoUseCase:
    """Use Case para generar reporte de impacto económico"""

    def __init__(
        self,
        reporte_repository: ReporteRepository,
        marca_repository: MarcaGanadoBovinoRepository,
        kpi_repository: KPIGanadoBovinoRepository,
    ):
        self.reporte_repository = reporte_repository
        self.marca_repository = marca_repository
        self.kpi_repository = kpi_repository

    def execute(self, año: int) -> ReporteData:
        """
        Genera un reporte de impacto económico

        Args:
            año: Año del reporte

        Returns:
            ReporteData: Reporte de impacto económico
        """
        fecha_inicio = datetime(año, 1, 1)
        fecha_fin = datetime(año + 1, 1, 1)

        return self.reporte_repository.generar_reporte_consolidado(
            fecha_inicio=fecha_inicio, fecha_fin=fecha_fin
        )


class GenerarReporteInnovacionTecnologicaUseCase:
    """Use Case para generar reporte de innovación tecnológica"""

    def __init__(
        self,
        reporte_repository: ReporteRepository,
        logo_repository: LogoMarcaBovinaRepository,
    ):
        self.reporte_repository = reporte_repository
        self.logo_repository = logo_repository

    def execute(self, año: int) -> ReporteData:
        """
        Genera un reporte de innovación tecnológica

        Args:
            año: Año del reporte

        Returns:
            ReporteData: Reporte de innovación tecnológica
        """
        fecha_inicio = datetime(año, 1, 1)
        fecha_fin = datetime(año + 1, 1, 1)

        return self.reporte_repository.generar_reporte_logos(
            fecha_inicio=fecha_inicio, fecha_fin=fecha_fin
        )


class GenerarReporteSostenibilidadUseCase:
    """Use Case para generar reporte de sostenibilidad sectorial"""

    def __init__(
        self,
        reporte_repository: ReporteRepository,
        marca_repository: MarcaGanadoBovinoRepository,
    ):
        self.reporte_repository = reporte_repository
        self.marca_repository = marca_repository

    def execute(self, año: int) -> ReporteData:
        """
        Genera un reporte de sostenibilidad sectorial

        Args:
            año: Año del reporte

        Returns:
            ReporteData: Reporte de sostenibilidad
        """
        fecha_inicio = datetime(año, 1, 1)
        fecha_fin = datetime(año + 1, 1, 1)

        return self.reporte_repository.generar_reporte_consolidado(
            fecha_inicio=fecha_inicio, fecha_fin=fecha_fin
        )
