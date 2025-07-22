from typing import Dict, Any

from apps.analytics.domain.repositories.reporte_repository import ReporteRepository
from apps.analytics.domain.repositories.marca_repository import (
    MarcaGanadoBovinoRepository,
)


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
