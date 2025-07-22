from typing import Optional

from apps.analytics.domain.entities.historial_estado_marca import HistorialEstadoMarca
from apps.analytics.domain.repositories.historial_repository import (
    HistorialEstadoMarcaRepository,
)


class ObtenerHistorialUseCase:
    """Use Case para obtener historial por ID"""

    def __init__(self, historial_repository: HistorialEstadoMarcaRepository):
        self.historial_repository = historial_repository

    def execute(self, historial_id: int) -> Optional[HistorialEstadoMarca]:
        """
        Obtiene un registro de historial por su ID

        Args:
            historial_id: ID del registro de historial

        Returns:
            HistorialEstadoMarca: El registro encontrado o None
        """
        return self.historial_repository.obtener_por_id(historial_id)
