from datetime import datetime

from apps.analytics.domain.entities.reporte_data import ReporteData
from apps.analytics.domain.repositories.reporte_repository import ReporteRepository
from apps.analytics.domain.repositories.marca_repository import (
    MarcaGanadoBovinoRepository,
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
