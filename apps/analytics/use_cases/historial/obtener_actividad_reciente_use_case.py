from typing import List
from datetime import datetime, timedelta

from apps.analytics.domain.entities.historial_estado_marca import HistorialEstadoMarca
from apps.analytics.domain.repositories.historial_repository import (
    HistorialEstadoMarcaRepository,
)


class ObtenerActividadRecienteUseCase:
    """Use Case para obtener actividad reciente del sistema"""

    def __init__(self, historial_repository: HistorialEstadoMarcaRepository):
        self.historial_repository = historial_repository

    def execute(self, dias: int = 7) -> List[HistorialEstadoMarca]:
        """
        Obtiene la actividad reciente del sistema

        Args:
            dias: Número de días hacia atrás para buscar

        Returns:
            List[HistorialEstadoMarca]: Lista de actividad reciente
        """
        return self.historial_repository.listar_por_fecha(
            fecha_inicio=datetime.now() - timedelta(days=dias),
            fecha_fin=datetime.now(),
        )
