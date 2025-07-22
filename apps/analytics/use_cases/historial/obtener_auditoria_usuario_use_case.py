from typing import List

from apps.analytics.domain.entities.historial_estado_marca import HistorialEstadoMarca
from apps.analytics.domain.repositories.historial_repository import (
    HistorialEstadoMarcaRepository,
)


class ObtenerAuditoriaUsuarioUseCase:
    """Use Case para obtener auditoría de un usuario"""

    def __init__(self, historial_repository: HistorialEstadoMarcaRepository):
        self.historial_repository = historial_repository

    def execute(self, usuario: str, dias: int = 30) -> List[HistorialEstadoMarca]:
        """
        Obtiene la auditoría de cambios de un usuario

        Args:
            usuario: Nombre del usuario
            dias: Número de días hacia atrás para buscar

        Returns:
            List[HistorialEstadoMarca]: Lista de cambios del usuario
        """
        return self.historial_repository.listar_por_usuario(usuario)
