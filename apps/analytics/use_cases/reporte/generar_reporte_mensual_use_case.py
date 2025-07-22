from datetime import datetime

from apps.analytics.domain.entities.reporte_data import ReporteData
from apps.analytics.domain.repositories.reporte_repository import ReporteRepository
from apps.analytics.domain.repositories.marca_repository import (
    MarcaGanadoBovinoRepository,
)
from apps.analytics.domain.repositories.kpi_repository import KPIGanadoBovinoRepository
from apps.analytics.domain.repositories.logo_repository import LogoMarcaBovinaRepository


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
