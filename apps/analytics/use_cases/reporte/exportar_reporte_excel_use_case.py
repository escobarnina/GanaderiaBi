from typing import Optional, Dict, Any
from datetime import datetime

from apps.analytics.domain.repositories.reporte_repository import ReporteRepository
from apps.analytics.domain.repositories.marca_repository import (
    MarcaGanadoBovinoRepository,
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
