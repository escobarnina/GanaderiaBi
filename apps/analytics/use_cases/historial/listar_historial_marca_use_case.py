from typing import List

from apps.analytics.domain.entities.historial_estado_marca import HistorialEstadoMarca
from apps.analytics.domain.repositories.historial_repository import (
    HistorialEstadoMarcaRepository,
)


class ListarHistorialMarcaUseCase:
    """Use Case para listar historial de una marca"""

    def __init__(self, historial_repository: HistorialEstadoMarcaRepository):
        self.historial_repository = historial_repository

    def execute(self, marca_id: int) -> List[HistorialEstadoMarca]:
        """
        Lista el historial de cambios de una marca

        Args:
            marca_id: ID de la marca

        Returns:
            List[HistorialEstadoMarca]: Lista de registros de historial
        """
        return self.historial_repository.obtener_por_marca(marca_id)
