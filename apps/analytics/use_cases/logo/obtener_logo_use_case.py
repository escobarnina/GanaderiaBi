from typing import Optional

from apps.analytics.domain.entities.logo_marca_bovina import LogoMarcaBovina
from apps.analytics.domain.repositories.logo_repository import LogoMarcaBovinaRepository


class ObtenerLogoUseCase:
    """Use Case para obtener un logo por ID"""

    def __init__(self, logo_repository: LogoMarcaBovinaRepository):
        self.logo_repository = logo_repository

    def execute(self, logo_id: int) -> Optional[LogoMarcaBovina]:
        """
        Obtiene un logo por su ID

        Args:
            logo_id: ID del logo

        Returns:
            LogoMarcaBovina: El logo encontrado o None
        """
        return self.logo_repository.obtener_por_id(logo_id)
