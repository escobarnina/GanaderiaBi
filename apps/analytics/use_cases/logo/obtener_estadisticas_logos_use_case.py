from typing import Dict, Any

from apps.analytics.domain.repositories.logo_repository import LogoMarcaBovinaRepository


class ObtenerEstadisticasLogosUseCase:
    """Use Case para obtener estadísticas de logos"""

    def __init__(self, logo_repository: LogoMarcaBovinaRepository):
        self.logo_repository = logo_repository

    def execute(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de logos generados

        Returns:
            Dict[str, Any]: Estadísticas de logos
        """
        return self.logo_repository.obtener_estadisticas()
