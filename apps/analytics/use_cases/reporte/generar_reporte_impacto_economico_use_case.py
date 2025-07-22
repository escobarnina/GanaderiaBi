from datetime import datetime

from apps.analytics.domain.entities.reporte_data import ReporteData
from apps.analytics.domain.repositories.reporte_repository import ReporteRepository
from apps.analytics.domain.repositories.marca_repository import (
    MarcaGanadoBovinoRepository,
)
from apps.analytics.domain.repositories.kpi_repository import KPIGanadoBovinoRepository


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
