from typing import Dict, Any

from apps.analytics.domain.repositories.historial_repository import (
    HistorialEstadoMarcaRepository,
)


class ObtenerEficienciaEvaluadoresUseCase:
    """Use Case para obtener eficiencia de evaluadores"""

    def __init__(self, historial_repository: HistorialEstadoMarcaRepository):
        self.historial_repository = historial_repository

    def execute(self) -> Dict[str, Any]:
        """
        Obtiene métricas de eficiencia de evaluadores

        Returns:
            Dict[str, Any]: Métricas de eficiencia
        """
        return self.historial_repository.obtener_tendencias_cambios()
