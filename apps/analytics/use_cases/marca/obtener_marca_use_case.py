from typing import Optional

from apps.analytics.domain.entities.marca_ganado_bovino import MarcaGanadoBovino
from apps.analytics.domain.repositories.marca_repository import (
    MarcaGanadoBovinoRepository,
)


class ObtenerMarcaUseCase:
    """Use Case para obtener una marca por ID"""

    def __init__(self, marca_repository: MarcaGanadoBovinoRepository):
        self.marca_repository = marca_repository

    def execute(self, marca_id: int) -> Optional[MarcaGanadoBovino]:
        """
        Obtiene una marca por su ID

        Args:
            marca_id: ID de la marca a obtener

        Returns:
            MarcaGanadoBovino: La marca encontrada o None si no existe
        """
        return self.marca_repository.obtener_por_id(marca_id)
