from typing import Dict, Any

from apps.analytics.domain.repositories.historial_repository import (
    HistorialEstadoMarcaRepository,
)


class ObtenerPatronesCambioUseCase:
    """Use Case para obtener patrones de cambio de estado"""

    def __init__(self, historial_repository: HistorialEstadoMarcaRepository):
        self.historial_repository = historial_repository

    def execute(self) -> Dict[str, Any]:
        """
        Obtiene patrones de cambio de estado

        Returns:
            Dict[str, Any]: Patrones de cambio identificados
        """
        return self.historial_repository.obtener_estadisticas()
