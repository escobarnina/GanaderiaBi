from datetime import datetime

from apps.analytics.domain.entities.reporte_data import ReporteData
from apps.analytics.domain.repositories.reporte_repository import ReporteRepository
from apps.analytics.domain.repositories.logo_repository import LogoMarcaBovinaRepository


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
